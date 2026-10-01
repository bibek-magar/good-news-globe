#!/usr/bin/env python3
"""Publish posts/<folder>/reel.mp4 to Instagram as a Reel (Reels tab only, not the main feed grid).

Uses the Instagram Graph API resumable upload, so the video doesn't need to be hosted anywhere.
Env: IG_USER_ID, IG_ACCESS_TOKEN.  Usage: python post_reel.py posts/2026-10-01-morning
Writes posts/<folder>/REEL_POSTED on success; skips folders that already have it.
"""
import os, sys, time, pathlib, requests

VER = os.environ.get("IG_API_VERSION", "v21.0")
API = f"https://graph.facebook.com/{VER}"
UID = os.environ["IG_USER_ID"]
TOKEN = os.environ["IG_ACCESS_TOKEN"]

def call(method, path, **params):
    params["access_token"] = TOKEN
    r = requests.request(method, f"{API}/{path}", params=params, timeout=120)
    if r.status_code >= 400:
        sys.exit(f"Instagram API error on {path}: {r.status_code} {r.text}")
    return r.json()

def main(folder):
    folder = pathlib.Path(folder)
    if (folder / "REEL_POSTED").exists():
        print("Reel already posted, skipping"); return
    video = folder / "reel.mp4"
    if not video.exists():
        sys.exit(f"No {video}")
    cap = folder / "reel_caption.txt"   # single-story Reel caption from the renderer; carousel caption as fallback
    caption = (cap if cap.exists() else folder / "caption.txt").read_text(encoding="utf-8")[:2200]
    cid = call("POST", f"{UID}/media", media_type="REELS", upload_type="resumable",
               caption=caption, share_to_feed="false")["id"]
    data = video.read_bytes()
    up = requests.post(f"https://rupload.facebook.com/ig-api-upload/{VER}/{cid}",
                       headers={"Authorization": f"OAuth {TOKEN}", "offset": "0", "file_size": str(len(data))},
                       data=data, timeout=300)
    if up.status_code >= 400:
        sys.exit(f"Video upload failed: {up.status_code} {up.text}")
    for _ in range(60):  # up to ~10 min of processing
        st = call("GET", cid, fields="status_code,status")
        if st.get("status_code") == "FINISHED":
            break
        if st.get("status_code") == "ERROR":
            sys.exit(f"Reel processing failed: {st}")
        time.sleep(10)
    else:
        sys.exit("Reel not processed in time")
    post = call("POST", f"{UID}/media_publish", creation_id=cid)
    print("Reel published:", post)
    (folder / "REEL_POSTED").write_text(time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()))

if __name__ == "__main__":
    main(sys.argv[1])
