#!/usr/bin/env python3
"""Build posts/<folder>/reel.mp4 (1080x1920, H.264 + AAC) with music from audio/.

Usage: python make_reel.py posts/2026-10-01-morning

Two modes:
- Single-story Reel (preferred): if posts/<folder>/reel/r1.jpg..rN.jpg exist (9:16 frames made by the renderer),
  each frame gets a slow push-in zoom and quick crossfades — short and punchy, built for the Reels tab.
- Slideshow fallback: otherwise the carousel slides NN.jpg are padded to 9:16 and shown one after another.

The music track is picked from audio/*.m4a by the folder name (so it rotates), faded in/out and trimmed.
"""
import hashlib, pathlib, subprocess, sys

SLIDE_SECONDS = 6.0      # slideshow: time each slide is fully visible (roughly)
FADE = 0.6               # slideshow: crossfade between slides
BG = "0xFFF8EE"          # brand background used to pad 4:5 slides to 9:16
FPS = 30
STORY_SECONDS = [2.6, 2.6, 5.0, 4.0]   # single-story: hook, number, what happened, why + follow
STORY_FADE = 0.35

def pick_track(folder):
    tracks = sorted(pathlib.Path("audio").glob("*.m4a"))
    if not tracks:
        sys.exit("No audio/*.m4a tracks found")
    return tracks[int(hashlib.md5(folder.name.encode()).hexdigest(), 16) % len(tracks)]

def encode(cmd, filters, last, total, out):
    cmd += ["-filter_complex", ";".join(filters), "-map", f"[{last}]", "-map", "[a]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-profile:v", "high", "-pix_fmt", "yuv420p",
            "-r", str(FPS), "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-movflags", "+faststart",
            "-t", f"{total:.2f}", str(out)]
    subprocess.run(cmd, check=True)

def chain(filters, n, durs, fade, transition="fade"):
    prev, t = "v0", 0.0
    for i in range(1, n):
        t += durs[i - 1] - fade
        filters.append(f"[{prev}][v{i}]xfade=transition={transition}:duration={fade}:offset={t:.2f}[x{i}]")
        prev = f"x{i}"
    return prev

def story_reel(folder, frames, track):
    n = len(frames)
    durs = [STORY_SECONDS[i] if i < len(STORY_SECONDS) else 3.5 for i in range(n)]
    total = sum(durs) - (n - 1) * STORY_FADE
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for fr, d in zip(frames, durs):
        cmd += ["-loop", "1", "-framerate", str(FPS), "-t", f"{d:.2f}", "-i", str(fr)]
    cmd += ["-i", str(track)]
    f = []
    for i, d in enumerate(durs):
        k = int(d * FPS)
        # upscale first so the slow zoom stays smooth, then push in ~6% over the clip
        f.append(f"[{i}:v]scale=2160:3840,zoompan=z='1+0.06*on/{k}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                 f":d=1:s=1080x1920:fps={FPS},setsar=1,format=yuv420p[v{i}]")
    last = chain(f, n, durs, STORY_FADE, "smoothleft")
    f.append(f"[{n}:a]atrim=0:{total:.2f},afade=t=in:d=0.6,afade=t=out:st={total-1.5:.2f}:d=1.5,asetpts=N/SR/TB[a]")
    encode(cmd, f, last, total, folder / "reel.mp4")
    print(f"reel.mp4: single-story, {n} frames, {total:.1f}s, music {track.name}")

def slideshow(folder, slides, track):
    n = len(slides)
    seg = SLIDE_SECONDS + FADE
    total = n * seg - (n - 1) * FADE
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for s in slides:
        cmd += ["-loop", "1", "-t", f"{seg:.2f}", "-i", str(s)]
    cmd += ["-i", str(track)]
    f = [f"[{i}:v]scale=1080:1350,pad=1080:1920:0:285:color={BG},setsar=1,fps={FPS},format=yuv420p[v{i}]" for i in range(n)]
    last = chain(f, n, [seg] * n, FADE)
    f.append(f"[{n}:a]atrim=0:{total:.2f},afade=t=in:d=1.5,afade=t=out:st={total-2.5:.2f}:d=2.5,asetpts=N/SR/TB[a]")
    encode(cmd, f, last, total, folder / "reel.mp4")
    print(f"reel.mp4: slideshow, {n} slides, {total:.1f}s, music {track.name}")

def main(folder):
    folder = pathlib.Path(folder)
    track = pick_track(folder)
    frames = sorted((folder / "reel").glob("r*.jpg")) if (folder / "reel").is_dir() else []
    if len(frames) >= 2:
        return story_reel(folder, frames, track)
    slides = sorted(p for p in folder.iterdir() if p.suffix.lower() in (".jpg", ".jpeg"))
    if len(slides) < 2:
        sys.exit(f"Need at least 2 JPEGs in {folder}")
    slideshow(folder, slides, track)

if __name__ == "__main__":
    main(sys.argv[1])
