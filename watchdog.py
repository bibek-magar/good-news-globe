#!/usr/bin/env python3
"""Daily safety checks; each problem becomes a GitHub issue (GitHub emails the repo owner).

Usage: python watchdog.py <check>      check = morning | midday | evening | token
- morning/midday/evening: was today's edition (Nepal date) posted? Sunday evening expects the weekly roundup.
- token: does IG_ACCESS_TOKEN still work, and does it expire within 10 days?
Prints one line per problem to problems.txt (title<TAB>body); the workflow opens an issue for each.
"""
import datetime as dt, os, pathlib, sys
import requests

NPT = dt.timezone(dt.timedelta(hours=5, minutes=45))
API = os.environ.get("IG_API_BASE", "https://graph.facebook.com/v21.0")
out = []

def check_edition(ed):
    today = dt.datetime.now(NPT).date()
    if ed == "evening" and today.weekday() == 6:
        ed = "weekly"
    f = pathlib.Path("posts") / f"{today.isoformat()}-{ed}"
    if (f / "POSTED").exists():
        print(f"{f}: posted"); return
    cool = pathlib.Path(".ig_blocked_until")
    if cool.exists() and dt.datetime.now(dt.timezone.utc).timestamp() < int(cool.read_text().split()[0]):
        until = dt.datetime.fromtimestamp(int(cool.read_text().split()[0]), dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        out.append(("Instagram is blocking automated posts",
                    f"Posting is paused until {until} after Instagram blocked publishing (error 2207051). Open the Instagram app "
                    "as @good_newsglobe, find the 'action blocked' notice and tap 'Tell us'. Delete `.ig_blocked_until` "
                    "in the repo to retry sooner. Editions are still built in `posts/` for posting by hand."))
        return
    if (f / "caption.txt").exists():
        why = "the caption was pushed but the Post workflow didn't finish. Check the Actions tab for the failed run."
    elif f.exists():
        why = "the run started (some files were pushed) but stopped before the caption. Check the autoposter session."
    else:
        why = "nothing was pushed. The scheduled autoposter run didn't happen or failed early. Check the autoposter session and its routine."
    out.append((f"Missed post: {today} {ed}", f"`{f}` has no POSTED marker: {why}"))

def check_token():
    tok = os.environ.get("IG_ACCESS_TOKEN", "")
    if not tok:
        out.append(("Instagram token missing", "The IG_ACCESS_TOKEN secret is empty.")); return
    r = requests.get(f"{API}/debug_token", params={"input_token": tok, "access_token": tok}, timeout=60)
    if r.status_code >= 400:
        r2 = requests.get(f"{API}/me", params={"access_token": tok}, timeout=60)
        if r2.status_code >= 400:
            out.append(("Instagram token is not working",
                        f"Instagram rejected IG_ACCESS_TOKEN ({r2.status_code}). Posts will fail until a new token is saved "
                        "in Settings → Secrets and variables → Actions → IG_ACCESS_TOKEN."))
        return
    data = r.json().get("data", {})
    if not data.get("is_valid", True):
        out.append(("Instagram token is not working", "Instagram says IG_ACCESS_TOKEN is no longer valid. Save a new one in the repo secrets."))
        return
    exp = data.get("expires_at") or 0
    if exp:
        days = (dt.datetime.fromtimestamp(exp, dt.timezone.utc) - dt.datetime.now(dt.timezone.utc)).days
        print(f"token expires in {days} days")
        if days <= 10:
            out.append(("Instagram token expires soon",
                        f"IG_ACCESS_TOKEN expires in {days} days. Make a new long-lived token and save it in "
                        "Settings → Secrets and variables → Actions → IG_ACCESS_TOKEN."))
    else:
        print("token does not expire")

if __name__ == "__main__":
    c = sys.argv[1]
    check_token() if c == "token" else check_edition(c)
    pathlib.Path("problems.txt").write_text("".join(f"{t}\t{b}\n" for t, b in out))
    for t, b in out:
        print("PROBLEM:", t, "-", b)
