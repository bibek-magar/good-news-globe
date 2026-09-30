#!/usr/bin/env python3
"""Turn posts/<folder>/NN.jpg into posts/<folder>/reel.mp4 (1080x1920, H.264 + AAC) with calm music from audio/.

Usage: python make_reel.py posts/2026-10-01-morning
Each slide is shown for SLIDE_SECONDS with a soft crossfade; the music track is picked from audio/*.m4a
by the folder name (so it rotates), faded in/out and trimmed to the video length.
"""
import hashlib, pathlib, subprocess, sys

SLIDE_SECONDS = 6.0      # time each slide is fully visible (roughly)
FADE = 0.6               # crossfade between slides
BG = "0xFFF8EE"          # brand background used to pad 4:5 slides to 9:16

def main(folder):
    folder = pathlib.Path(folder)
    slides = sorted(p for p in folder.iterdir() if p.suffix.lower() in (".jpg", ".jpeg"))
    if len(slides) < 2:
        sys.exit(f"Need at least 2 JPEGs in {folder}")
    tracks = sorted(pathlib.Path("audio").glob("*.m4a"))
    if not tracks:
        sys.exit("No audio/*.m4a tracks found")
    track = tracks[int(hashlib.md5(folder.name.encode()).hexdigest(), 16) % len(tracks)]
    n = len(slides)
    seg = SLIDE_SECONDS + FADE                      # each input clip length
    total = n * seg - (n - 1) * FADE                # length after crossfades
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for s in slides:
        cmd += ["-loop", "1", "-t", f"{seg:.2f}", "-i", str(s)]
    cmd += ["-i", str(track)]
    f = []
    for i in range(n):
        f.append(f"[{i}:v]scale=1080:1350,pad=1080:1920:0:285:color={BG},setsar=1,fps=30,format=yuv420p[v{i}]")
    prev = "v0"
    for i in range(1, n):
        off = i * seg - i * FADE
        out = f"x{i}"
        f.append(f"[{prev}][v{i}]xfade=transition=fade:duration={FADE}:offset={off:.2f}[{out}]")
        prev = out
    f.append(f"[{n}:a]atrim=0:{total:.2f},afade=t=in:d=1.5,afade=t=out:st={total-2.5:.2f}:d=2.5,asetpts=N/SR/TB[a]")
    cmd += ["-filter_complex", ";".join(f), "-map", f"[{prev}]", "-map", "[a]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-profile:v", "high", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-movflags", "+faststart",
            "-t", f"{total:.2f}", str(folder / "reel.mp4")]
    subprocess.run(cmd, check=True)
    print(f"reel.mp4: {n} slides, {total:.1f}s, music {track.name}")

if __name__ == "__main__":
    main(sys.argv[1])
