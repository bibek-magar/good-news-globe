#!/usr/bin/env python3
"""Download free-licence photo candidates for each story in posts/<folder>/stories.json.

Usage: python fetch_images.py posts/2026-10-02-midday

For every story with an "image_query" (e.g. "Ghana cuckooshrike", "Nazca mummy", "strawberry field"), searches
Wikimedia Commons first, then Openverse (Flickr etc.), keeping only CC0 / public domain / CC BY / CC BY-SA photos
(no NC, no ND). Saves up to 2 candidates per story as img/s<N>a.jpg, img/s<N>b.jpg (max 1600 px wide) and their
attribution in img/credits.json. The scheduled run then looks at the candidates and picks one per story by setting
"image": "img/s1a.jpg" in stories.json (render.py adds the credit line from credits.json).

Stories whose query hasn't changed since the last run are skipped, so re-pushing stories.json is cheap.
Never fails the job: problems are printed and the story just gets no candidates.
"""
import html, io, json, re, sys, pathlib
import requests
from PIL import Image

UA = {"User-Agent": "GoodNewsGlobe/1.0 (https://github.com/bibek-magar/good-news-globe)"}
PER_STORY = 2
MAX_W = 1600

def clean(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()

def free(lic):
    l = (lic or "").lower().replace("-", " ")
    if {"nc", "nd"} & set(l.split()):
        return False
    return "cc0" in l or "public domain" in l or l.startswith("cc by") or l == "pd"

def commons(q):
    r = requests.get("https://commons.wikimedia.org/w/api.php", headers=UA, timeout=30, params={
        "action": "query", "format": "json", "generator": "search", "gsrsearch": f"{q} filetype:bitmap",
        "gsrnamespace": 6, "gsrlimit": 12, "prop": "imageinfo", "iiprop": "url|extmetadata|size|mime",
        "iiurlwidth": MAX_W}).json()
    pages = sorted(r.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
    for p in pages:
        ii = (p.get("imageinfo") or [{}])[0]
        md = ii.get("extmetadata", {})
        lic = clean(md.get("LicenseShortName", {}).get("value"))
        w, h = ii.get("width", 0), ii.get("height", 0)
        if ii.get("mime") not in ("image/jpeg", "image/png") or w < 1000 or not h or not 0.5 < w / h < 2.4 or not free(lic):
            continue
        artist = clean(md.get("Artist", {}).get("value")) or "Unknown"
        yield {"url": ii.get("thumburl") or ii["url"], "page": ii.get("descriptionurl", ""),
               "credit": f"{artist[:60]} / Wikimedia Commons, {lic}", "license": lic}

def openverse(q):
    r = requests.get("https://api.openverse.org/v1/images/", headers=UA, timeout=30, params={
        "q": q, "license": "by,by-sa,cc0,pdm", "page_size": 12, "mature": "false"}).json()
    for x in r.get("results", []):
        w, h = x.get("width") or 0, x.get("height") or 0
        if w and (w < 1000 or not 0.5 < w / max(h, 1) < 2.4):
            continue
        lic = ("CC0" if x["license"] == "cc0" else "Public domain" if x["license"] == "pdm"
               else f"CC {x['license'].upper()} {x.get('license_version') or ''}".strip())
        src = (x.get("source") or x.get("provider") or "Openverse").title()
        yield {"url": x["url"], "page": x.get("foreign_landing_url", ""),
               "credit": f"{clean(x.get('creator'))[:60] or 'Unknown'} / {src}, {lic}", "license": lic}

def save(url, dst):
    r = requests.get(url, headers=UA, timeout=60)
    r.raise_for_status()
    im = Image.open(io.BytesIO(r.content)).convert("RGB")
    if im.width < 900:
        raise ValueError("too small")
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    im.save(dst, "JPEG", quality=85)

def main(folder):
    folder = pathlib.Path(folder)
    d = json.loads((folder / "stories.json").read_text(encoding="utf-8"))
    img = folder / "img"; img.mkdir(exist_ok=True)
    cf = img / "credits.json"
    credits = json.loads(cf.read_text()) if cf.exists() else {}
    for i, s in enumerate(d.get("stories", []), 1):
        q = (s.get("image_query") or "").strip()
        if not q:
            continue
        if credits.get(f"s{i}a", {}).get("query") == q:
            print(f"s{i}: '{q}' already fetched"); continue
        for k in "ab":
            (img / f"s{i}{k}.jpg").unlink(missing_ok=True); credits.pop(f"s{i}{k}", None)
        got, seen = 0, set()
        for finder in (commons, openverse):
            try:
                for c in finder(q):
                    if got >= PER_STORY:
                        break
                    if c["url"] in seen:
                        continue
                    seen.add(c["url"])
                    name = f"s{i}{'ab'[got]}"
                    try:
                        save(c["url"], img / f"{name}.jpg")
                    except Exception as e:
                        print(f"  skip {c['url'][:80]}: {e}"); continue
                    credits[name] = {**c, "query": q}
                    got += 1
            except Exception as e:
                print(f"  {finder.__name__} failed for '{q}': {e}")
            if got >= PER_STORY:
                break
        print(f"s{i}: '{q}' -> {got} candidate(s)")
    cf.write_text(json.dumps(credits, indent=1, ensure_ascii=False))

if __name__ == "__main__":
    main(sys.argv[1])
