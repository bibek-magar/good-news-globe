#!/usr/bin/env python3
"""Share a post to the Instagram Story: the reel.mp4 (with music) if present, else the cover image 01.jpg.

Env: IG_USER_ID, IG_ACCESS_TOKEN, GITHUB_REPOSITORY, GITHUB_SHA.
Usage: python post_story.py posts/2026-10-01-morning   (writes STORY_POSTED on success)
"""
import os, sys, time, pathlib, requests

VER = os.environ.get("IG_API_VERSION", "v21.0")
API = f"https://graph.facebook.com/{VER}"
UID = os.environ["IG_USER_ID"]
TOKEN = os.environ["IG_ACCESS_TOKEN"]

class ApiError(Exception):
    pass

def call(method, path, **params):
    params["access_token"] = TOKEN
    r = requests.request(method, f"{API}/{path}", params=params, timeout=120)
    if r.status_code >= 400:
        raise ApiError(f"{path}: {r.status_code} {r.text}")
    return r.json()

def wait(cid, tries=60):
    for _ in range(tries):
        st = call("GET", cid, fields="status_code,status")
        if st.get("status_code") == "FINISHED":
            return
        if st.get("status_code") == "ERROR":
            raise ApiError(f"processing failed: {st}")
        time.sleep(10)
    raise ApiError("not processed in time")

def video_story(video):
    cid = call("POST", f"{UID}/media", media_type="STORIES", upload_type="resumable")["id"]
    data = video.read_bytes()
    up = requests.post(f"https://rupload.facebook.com/ig-api-upload/{VER}/{cid}",
                       headers={"Authorization": f"OAuth {TOKEN}", "offset": "0", "file_size": str(len(data))},
                       data=data, timeout=300)
    if up.status_code >= 400:
        raise ApiError(f"upload: {up.status_code} {up.text}")
    wait(cid)
    return cid

def image_story(img):
    url = f"https://raw.githubusercontent.com/{os.environ['GITHUB_REPOSITORY']}/{os.environ.get('GITHUB_SHA','main')}/{img.as_posix()}"
    cid = call("POST", f"{UID}/media", media_type="STORIES", image_url=url)["id"]
    wait(cid, 30)
    return cid

def main(folder):
    folder = pathlib.Path(folder)
    if (folder / "STORY_POSTED").exists():
        print("Story already posted, skipping"); return
    cid = None
    if (folder / "reel.mp4").exists():
        try:
            cid = video_story(folder / "reel.mp4"); print("Video story ready")
        except ApiError as e:
            print("Video story failed, falling back to cover image:", e)
    if cid is None:
        cid = image_story(folder / "01.jpg"); print("Image story ready")
    print("Story published:", call("POST", f"{UID}/media_publish", creation_id=cid))
    (folder / "STORY_POSTED").write_text(time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()))

if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except ApiError as e:
        sys.exit(f"Story failed: {e}")
