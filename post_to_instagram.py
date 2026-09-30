#!/usr/bin/env python3
"""Publish a carousel folder (posts/<name>/01.jpg..NN.jpg + caption.txt) to Instagram.

Uses the Instagram Graph API via Facebook Login (graph.facebook.com) with a Page access token.
Env: IG_USER_ID, IG_ACCESS_TOKEN, GITHUB_REPOSITORY, GITHUB_SHA
Usage: python post_to_instagram.py posts/2026-10-01-morning
"""
import os, sys, time, pathlib, requests

API = os.environ.get("IG_API_BASE", "https://graph.facebook.com/v21.0")
UID = os.environ["IG_USER_ID"]
TOKEN = os.environ["IG_ACCESS_TOKEN"]
REPO = os.environ["GITHUB_REPOSITORY"]
SHA = os.environ.get("GITHUB_SHA", "main")

def call(method, path, **params):
    params["access_token"] = TOKEN
    r = requests.request(method, f"{API}/{path}", params=params, timeout=60)
    if r.status_code >= 400:
        sys.exit(f"Instagram API error on {path}: {r.status_code} {r.text}")
    return r.json()

def wait_ready(cid):
    for _ in range(30):
        s = call("GET", cid, fields="status_code").get("status_code")
        if s == "FINISHED":
            return
        if s == "ERROR":
            sys.exit(f"Container {cid} failed processing")
        time.sleep(5)
    sys.exit(f"Container {cid} not ready in time")

def main(folder):
    folder = pathlib.Path(folder)
    if (folder / "POSTED").exists():
        print("Already posted, skipping"); return
    imgs = sorted(p for p in folder.iterdir() if p.suffix.lower() in (".jpg", ".jpeg"))
    if not 2 <= len(imgs) <= 10:
        sys.exit(f"Need 2-10 JPEGs in {folder}, found {len(imgs)}")
    caption = (folder / "caption.txt").read_text(encoding="utf-8")[:2200]
    children = []
    for p in imgs:
        url = f"https://raw.githubusercontent.com/{REPO}/{SHA}/{p.as_posix()}"
        cid = call("POST", f"{UID}/media", image_url=url, is_carousel_item="true")["id"]
        wait_ready(cid); children.append(cid)
        print("uploaded", p.name)
    carousel = call("POST", f"{UID}/media", media_type="CAROUSEL", children=",".join(children), caption=caption)["id"]
    wait_ready(carousel)
    post = call("POST", f"{UID}/media_publish", creation_id=carousel)
    print("Published:", post)

if __name__ == "__main__":
    main(sys.argv[1])
