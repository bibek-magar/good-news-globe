#!/usr/bin/env python3
"""Pull Instagram Insights for recent posts and write a performance report the scheduled runs learn from.

Env: IG_USER_ID, IG_ACCESS_TOKEN (needs instagram_manage_insights / instagram_basic).
Usage: python insights.py            -> writes analytics/posts.csv, analytics/account.csv, analytics/REPORT.md

Every API call is best effort: anything Instagram refuses is listed under "Problems" in the report
instead of failing the job.
"""
import csv, datetime as dt, json, os, pathlib, statistics, sys
import requests

VER = os.environ.get("IG_API_VERSION", "v21.0")
API = f"https://graph.facebook.com/{VER}"
UID = os.environ["IG_USER_ID"]
TOKEN = os.environ["IG_ACCESS_TOKEN"]
OUT = pathlib.Path("analytics")
DAYS = 30
FEED_METRICS = ["reach", "saved", "shares", "likes", "comments", "total_interactions", "views"]
REEL_METRICS = FEED_METRICS + ["ig_reels_avg_watch_time"]
problems = []

def get(path, **params):
    params["access_token"] = TOKEN
    r = requests.get(f"{API}/{path}", params=params, timeout=60)
    if r.status_code >= 400:
        raise RuntimeError(f"{path}: {r.status_code} {r.text[:300]}")
    return r.json()

def media_insights(mid, metrics):
    """Ask for all metrics at once; if Instagram rejects one, retry them one by one."""
    def parse(js):
        return {m["name"]: (m.get("values") or [{}])[0].get("value", m.get("total_value", {}).get("value")) for m in js.get("data", [])}
    try:
        return parse(get(f"{mid}/insights", metric=",".join(metrics)))
    except RuntimeError:
        out = {}
        for m in metrics:
            try:
                out.update(parse(get(f"{mid}/insights", metric=m)))
            except RuntimeError:
                pass
        return out

def first_line(text):
    return (text or "").strip().splitlines()[0].strip() if (text or "").strip() else ""

def folder_index():
    """caption first line -> post folder, so each IG post can be tied to its stories.json."""
    idx = {}
    for f in sorted(pathlib.Path("posts").glob("*")):
        for name in ("caption.txt", "reel_caption.txt"):
            p = f / name
            if p.exists():
                idx[first_line(p.read_text(encoding="utf-8"))] = f
    return idx

def load_meta(folder):
    p = folder / "stories.json" if folder else None
    if p and p.exists():
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            cats = [s.get("category", "") for s in d.get("stories", [])]
            return d.get("cover_hook", ""), cats, d.get("question", "")
        except ValueError:
            pass
    return "", [], ""

def score(r):
    """Shares and saves are what Instagram rewards most, so they weigh more than likes."""
    reach = r.get("reach") or 0
    if not reach:
        return 0.0
    return round(100 * (3 * (r.get("shares") or 0) + 2 * (r.get("saved") or 0) + (r.get("comments") or 0) + (r.get("likes") or 0)) / reach, 2)

def main():
    OUT.mkdir(exist_ok=True)
    today = dt.datetime.now(dt.timezone.utc).date().isoformat()

    # account snapshot (follower trend)
    acct_rows = []
    acct_file = OUT / "account.csv"
    if acct_file.exists():
        acct_rows = list(csv.DictReader(acct_file.open()))
    try:
        a = get(UID, fields="username,followers_count,media_count")
        acct_rows = [r for r in acct_rows if r["date"] != today] + [
            {"date": today, "followers": a.get("followers_count", ""), "media": a.get("media_count", "")}]
        with acct_file.open("w", newline="") as fh:
            w = csv.DictWriter(fh, ["date", "followers", "media"]); w.writeheader(); w.writerows(acct_rows)
    except RuntimeError as e:
        problems.append(f"account: {e}")

    # recent media + insights
    idx = folder_index()
    since = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=DAYS)
    rows, url_params = [], {"fields": "id,caption,timestamp,media_type,media_product_type,permalink", "limit": 50}
    path = f"{UID}/media"
    try:
        for _ in range(4):
            js = get(path, **url_params)
            stop = False
            for m in js.get("data", []):
                ts = dt.datetime.fromisoformat(m["timestamp"].replace("+0000", "+00:00"))
                if ts < since:
                    stop = True; break
                kind = m.get("media_product_type", "FEED")
                if kind == "STORY":
                    continue
                ins = media_insights(m["id"], REEL_METRICS if kind == "REELS" else FEED_METRICS)
                folder = idx.get(first_line(m.get("caption")))
                hook, cats, question = load_meta(folder)
                npt = ts + dt.timedelta(hours=5, minutes=45)
                slot = "morning" if npt.hour < 10 else "midday" if npt.hour < 15 else "evening"
                r = {"date": npt.date().isoformat(), "time_npt": npt.strftime("%H:%M"), "slot": slot, "type": kind,
                     "folder": folder.name if folder else "", "hook": hook or first_line(m.get("caption"))[:90],
                     "categories": " ".join(cats), "question": question, "permalink": m.get("permalink", ""), **ins}
                r["score"] = score(r)
                rows.append(r)
            nxt = js.get("paging", {}).get("cursors", {}).get("after")
            if stop or not nxt or not js.get("paging", {}).get("next"):
                break
            url_params["after"] = nxt
    except RuntimeError as e:
        problems.append(f"media list: {e}")

    cols = ["date", "time_npt", "slot", "type", "folder", "hook", "categories", "question", "score"] + REEL_METRICS + ["permalink"]
    with (OUT / "posts.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)

    # audience: when followers are online, and where they are
    online, countries = None, None
    try:
        js = get(f"{UID}/insights", metric="online_followers", period="lifetime")
        vals = js["data"][0]["values"]
        online = next((v["value"] for v in reversed(vals) if v.get("value")), None)
    except (RuntimeError, KeyError, IndexError) as e:
        problems.append(f"online_followers: {e}")
    try:
        js = get(f"{UID}/insights", metric="follower_demographics", period="lifetime", metric_type="total_value", breakdown="country")
        res = js["data"][0]["total_value"]["breakdowns"][0]["results"]
        countries = sorted(((x["dimension_values"][0], x["value"]) for x in res), key=lambda t: -t[1])[:8]
    except (RuntimeError, KeyError, IndexError) as e:
        problems.append(f"follower_demographics (needs 100+ followers): {e}")

    write_report(today, acct_rows, rows, online, countries)
    print(f"{len(rows)} posts, {len(problems)} problems -> {OUT}/REPORT.md")

def avg(xs):
    xs = [x for x in xs if isinstance(x, (int, float))]
    return round(statistics.mean(xs), 1) if xs else 0

def write_report(today, acct, rows, online, countries):
    L = [f"# Good News Globe — performance report", f"_Updated {today} (UTC). Last {DAYS} days. "
         "Score = 100 × (3·shares + 2·saves + comments + likes) ÷ reach._", ""]
    if acct:
        last = acct[-8:]
        L += ["## Followers", " → ".join(f"{r['date'][5:]}: {r['followers']}" for r in last), ""]
    feed = [r for r in rows if r["type"] != "REELS"]
    reels = [r for r in rows if r["type"] == "REELS"]
    week = (dt.date.fromisoformat(today) - dt.timedelta(days=7)).isoformat()
    def table(rs, extra=False):
        out = ["| date | slot | hook | reach | shares | saves | comments | score |" + (" avg watch (ms) |" if extra else ""),
               "|---|---|---|---|---|---|---|---|" + ("---|" if extra else "")]
        for r in rs:
            out.append(f"| {r['date']} | {r['slot']} | {r['hook'][:70]} | {r.get('reach', '')} | {r.get('shares', '')} | "
                       f"{r.get('saved', '')} | {r.get('comments', '')} | {r['score']} |" + (f" {r.get('ig_reels_avg_watch_time', '')} |" if extra else ""))
        return out
    if feed:
        best = sorted(feed, key=lambda r: -r["score"])
        L += ["## Best carousels (copy what these hooks did)"] + table(best[:5]) + [""]
        if len(best) >= 6:
            L += ["## Weakest carousels (avoid these patterns)"] + table(best[-3:][::-1]) + [""]
        lw = [r for r in feed if r["date"] >= week]
        L += ["## This week vs before", f"- Last 7 days: {len(lw)} carousels, avg reach {avg([r.get('reach') for r in lw])}, avg score {avg([r['score'] for r in lw])}",
              f"- Earlier: avg reach {avg([r.get('reach') for r in feed if r['date'] < week])}, avg score {avg([r['score'] for r in feed if r['date'] < week])}", ""]
        L += ["## By slot (Nepal time)"]
        for s in ("morning", "midday", "evening"):
            rs = [r for r in feed if r["slot"] == s]
            if rs:
                L.append(f"- {s}: {len(rs)} posts, avg reach {avg([r.get('reach') for r in rs])}, avg score {avg([r['score'] for r in rs])}")
        L.append("")
        cover, anycat = {}, {}
        for r in feed:
            cats = r["categories"].split()
            if cats:
                cover.setdefault(cats[0], []).append(r["score"])
                for c in cats:
                    anycat.setdefault(c, []).append(r["score"])
        if cover:
            L += ["## Categories", "Cover (story #1) category → avg score: " +
                  ", ".join(f"{c} {avg(v)} ({len(v)})" for c, v in sorted(cover.items(), key=lambda kv: -avg(kv[1]))),
                  "Any position → avg score: " +
                  ", ".join(f"{c} {avg(v)}" for c, v in sorted(anycat.items(), key=lambda kv: -avg(kv[1]))), ""]
    if reels:
        L += ["## Best Reels"] + table(sorted(reels, key=lambda r: -(r.get("reach") or 0))[:5], extra=True) + [""]
    if online:
        top = sorted(((int(h), v) for h, v in online.items()), key=lambda t: -t[1])[:5]
        L += ["## When followers are online",
              "Top hours as Instagram reports them (Pacific time; add 12:45 in summer / 13:45 in winter for Nepal time): " +
              ", ".join(f"{h:02d}:00 ({v})" for h, v in top), ""]
    if countries:
        L += ["## Top follower countries", ", ".join(f"{c} {v}" for c, v in countries), ""]
    L += ["## How the scheduled runs should use this",
          "- Lead with the cover patterns and categories that score highest; drop the patterns in the weakest list.",
          "- Shares and saves matter most: favour stories people would send to a specific friend.",
          "- If one slot keeps scoring low, say so in the run's notification so the schedule can be moved.", ""]
    if problems:
        L += ["## Problems"] + [f"- {p}" for p in problems] + [""]
    (OUT / "REPORT.md").write_text("\n".join(L), encoding="utf-8")

if __name__ == "__main__":
    main()
