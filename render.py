#!/usr/bin/env python3
"""Good News Globe carousel + reel renderer (v3: hook cover, stat callouts, share/save CTA, single-story Reel frames).

Usage:  python3 render.py stories.json out_dir/     (fonts are read from ./fonts next to this file)
Writes:
  out/01.png..NN.png      1080x1350 carousel (cover, one slide per story, closing)
  out/caption.txt         carousel caption
  out/reel/r1.png..r4.png 1080x1920 frames for a single-story Reel about story #1 (hook, number, story, follow)
  out/reel_caption.txt    Reel caption
  out/first_comment.txt   comment the account posts under the carousel (only if "first_comment" is set)
Exits with code 2 and prints WARNING lines if any text overflows its slide.

stories.json (fields marked * are new in v2 and optional; old files still render):
{
  "edition": "Midday", "date": "2026-10-01", "handle": "@good_newsglobe",
  "cover_hook": "Sea turtles nested in California for the 1st time",   # max ~50 chars, slide 1 title
  "cover_highlight": "1st time",        # * exact substring of cover_hook drawn in the accent colour
  "cover_kicker": "Never recorded before", # * small line above the hook, max ~28 chars
  "caption_hook": "...",                # caption line 1, max ~125 chars (what shows before "more")
  "question": "...",                    # comment prompt, max ~90 chars
  "stories": [
    {"category": "nature", "place": "Orange County, USA", "emoji": "🐢",   # * emoji used in caption only
     "stat": "204", "stat_label": "eggs rescued before a storm",            # * big number callout (stat max ~7 chars, label max ~34)
     "headline": "...", "summary": "...", "why": "...",
     "source_name": "...", "source_url": "https://...",
     "source_ig": "@goodnewsnetwork"}                                         # * outlet/lab Instagram handle, only if verified ("" otherwise)
  ],
  "fun_fact": "...",
  "share_line": "Send this to someone who needs a win today",   # * closing-slide CTA, max ~48 chars
  "reel_hook": "This snake was lost for 154 years",            # * optional first Reel frame text, max ~45 chars (default: cover_hook)
  "first_comment": "Bonus fact: ...",                           # * optional comment posted under the carousel, max ~200 chars
  "cover_tease": "from this week",                              # * optional words after "+ N more wins" on the cover
  "hashtags": "#goodnews #positivenews #goodnewsglobe ..."
}
Photos (v4, optional, per story):
  "image_query": "Ghana cuckooshrike"   # what fetch_images.py searches for (free-licence photos only)
  "image": "img/s1a.jpg"                # chosen photo, relative to stories.json; omit for the no-photo design
  "image_credit": "..."                 # optional; default comes from img/credits.json
  Story #1's photo fills the cover and the Reel; each story slide shows its own photo as a header.
Categories: space, science, archaeology, nature, health, energy, invention, kindness, nepal, quirky
"""
import base64, datetime, html, json, os, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
FONT_DIRS = [HERE / "fonts", HERE / "node_modules/@fontsource/fraunces/files", HERE / "node_modules/@fontsource/inter/files"]

def font_b64(name):
    for d in FONT_DIRS:
        p = d / name
        if p.exists():
            return base64.b64encode(p.read_bytes()).decode()
    return None

def font_css():
    out = []
    for fam, file, w in [("Fraunces", "fraunces-latin-700-normal.woff2", 700),
                         ("Fraunces", "fraunces-latin-900-normal.woff2", 900),
                         ("Inter", "inter-latin-400-normal.woff2", 400),
                         ("Inter", "inter-latin-600-normal.woff2", 600),
                         ("Inter", "inter-latin-700-normal.woff2", 700),
                         ("Inter", "inter-latin-800-normal.woff2", 800)]:
        b = font_b64(file)
        if b:
            out.append(f"@font-face{{font-family:'{fam}';font-weight:{w};src:url(data:font/woff2;base64,{b}) format('woff2');}}")
    return "\n".join(out)

ICONS = {
    "space": '<circle cx="32" cy="32" r="14"/><ellipse cx="32" cy="32" rx="28" ry="9" transform="rotate(-20 32 32)"/>',
    "science": '<path d="M24 8h16M28 8v18L14 52a4 4 0 0 0 4 6h28a4 4 0 0 0 4-6L36 26V8"/><path d="M20 42h24"/>',
    "archaeology": '<path d="M10 54h44M14 54V26M26 54V26M38 54V26M50 54V26M8 26h48L32 10z"/>',
    "nature": '<path d="M12 52C12 26 30 12 54 10c-2 24-16 42-42 42z"/><path d="M12 52L36 28"/>',
    "health": '<path d="M32 54S8 40 8 24a12 12 0 0 1 24-4 12 12 0 0 1 24 4c0 16-24 30-24 30z"/><path d="M22 30h6l3-6 4 12 3-6h6"/>',
    "energy": '<path d="M36 6L14 36h16l-4 22 24-32H34z"/>',
    "invention": '<path d="M24 44a16 16 0 1 1 16 0v6H24z"/><path d="M26 56h12"/>',
    "kindness": '<path d="M32 54S8 40 8 24a12 12 0 0 1 24-4 12 12 0 0 1 24 4c0 16-24 30-24 30z"/>',
    "nepal": '<path d="M4 54L22 22l10 14 8-12 20 30z"/><path d="M18 30l4-8 5 7"/>',
    "quirky": '<path d="M32 6l7 16 17 2-13 11 4 17-15-9-15 9 4-17L8 24l17-2z"/>',
}
# category -> (label, accent, soft background)
CATS = {
    "space":       ("Space",        "#4F46E5", "#E9EAFB"),
    "science":     ("Science",      "#0E7C86", "#DDF3F2"),
    "archaeology": ("History",      "#A1531B", "#F8E8D8"),
    "nature":      ("Nature",       "#2F7D32", "#E3F2DF"),
    "health":      ("Health",       "#C0392B", "#FBE4E0"),
    "energy":      ("Clean energy", "#B7791F", "#FBF0D5"),
    "invention":   ("Invention",    "#6B3FA0", "#EFE6F8"),
    "kindness":    ("Kindness",     "#C2185B", "#FBE3EE"),
    "nepal":       ("Nepal",        "#B71C1C", "#FBE5E5"),
    "quirky":      ("Delightful",   "#D35400", "#FDEBDD"),
}
INK, PAPER, MUTED, GOLD = "#1F1A14", "#FFF8EE", "#7A6E60", "#FFC94D"

def cat(s):
    return CATS.get(s.get("category"), CATS["quirky"])

def icon(c, color, size=64, sw=4):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 64 64" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICONS.get(c, ICONS["quirky"])}</svg>')

GLOBE = ('<svg width="{s}" height="{s}" viewBox="0 0 64 64" fill="none" stroke="{c}" stroke-width="3.5" stroke-linecap="round">'
         '<circle cx="32" cy="32" r="26"/><ellipse cx="32" cy="32" rx="11" ry="26"/><path d="M6 32h52M10 19h44M10 45h44"/>'
         '<path d="M44 8l3-6M52 14l5-3M20 8l-3-6" stroke="#F2A93B"/></svg>')
ARROW = ('<svg width="{s}" height="{s}" viewBox="0 0 64 64" fill="none" stroke="{c}" stroke-width="6" stroke-linecap="round" '
         'stroke-linejoin="round"><path d="M12 32h38M36 16l16 16-16 16"/></svg>')

BASE_CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1080px;height:1350px}}
body{{background:{PAPER};color:{INK};font-family:Inter,'Noto Color Emoji',sans-serif;overflow:hidden}}
.slide{{position:relative;width:1080px;height:1350px;padding:80px 88px;display:flex;flex-direction:column;overflow:hidden}}
.brand{{display:flex;align-items:center;gap:16px;font:700 28px Inter;letter-spacing:.01em;position:relative;z-index:2}}
.brand small{{margin-left:auto;font:700 24px Inter;color:{MUTED}}}
.foot{{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;font:600 24px Inter;color:{MUTED};position:relative;z-index:2}}
.dots{{display:flex;gap:10px;align-items:center}}
.dots i{{display:block;width:12px;height:12px;border-radius:6px;background:#D9CDBB}}
.dots i.on{{width:40px;background:{INK}}}
"""

def page(body, extra_css=""):
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{font_css()}{BASE_CSS}{extra_css}</style>"
            f"</head><body>{body}</body></html>")

def esc(s):
    return html.escape(s or "")

def photo(d, s):
    """(data URI, credit) for a story's chosen photo, or (None, None)."""
    rel = (s.get("image") or "").strip()
    p = (Path(d.get("_base", ".")) / rel) if rel else None
    if not p or not p.is_file():
        return None, None
    credit = (s.get("image_credit") or "").strip()
    if not credit:
        cf = p.parent / "credits.json"
        try:
            credit = json.loads(cf.read_text()).get(p.stem, {}).get("credit", "")
        except (OSError, ValueError):
            credit = ""
    mime = "png" if p.suffix.lower() == ".png" else "jpeg"
    return f"data:image/{mime};base64,{base64.b64encode(p.read_bytes()).decode()}", credit

def credit_html(c, cls="cr"):
    return f'<div class="{cls}">Photo: {esc(c)}</div>' if c else ""

def dots(i, n):
    return '<div class="dots">' + "".join(f'<i class="{"on" if k == i else ""}"></i>' for k in range(1, n + 1)) + "</div>"

def hook_html(hook, hi):
    if hi and hi in hook:
        a, b = hook.split(hi, 1)
        return f'{esc(a)}<span class="hi">{esc(hi)}</span>{esc(b)}'
    return esc(hook)

def cover(d, total):
    s0 = d["stories"][0]
    label, accent, soft = cat(s0)
    n = len(d["stories"])
    hook = (d.get("cover_hook") or "").strip() or f"{n} good things happening right now"
    L = len(hook)
    size = 118 if L <= 26 else 104 if L <= 36 else 92 if L <= 46 else 82
    also = "".join(f'<div><span>{icon(s["category"], CATS.get(s["category"], CATS["quirky"])[2], 34)}</span>'
                   f'{cat(s)[0]}<em>· {esc(s.get("place", "").split(",")[-1].strip())}</em></div>' for s in d["stories"][1:4])
    if n > 4:
        also += f'<div><span>+{n - 4}</span>more inside</div>'
    tease = (d.get("cover_tease") or "").strip() or "you probably missed:"
    kicker = (d.get("cover_kicker") or "").strip() or f"{label} · {s0.get('place', '').split(',')[-1].strip()}".strip(" ·")
    date = datetime.date.fromisoformat(d["date"]).strftime("%d %B %Y").lstrip("0")
    img, cred = photo(d, s0)
    css = f"""
    body{{background:{INK};color:{PAPER}}}
    .glow{{position:absolute;width:900px;height:900px;right:-330px;top:-360px;border-radius:50%;
           background:radial-gradient(circle,{GOLD} 0%,rgba(255,201,77,.35) 38%,rgba(31,26,20,0) 70%)}}
    .glow2{{position:absolute;width:700px;height:700px;left:-320px;bottom:-300px;border-radius:50%;
            background:radial-gradient(circle,{accent} 0%,rgba(31,26,20,0) 68%);opacity:.55}}
    .kick{{display:inline-flex;align-items:center;gap:14px;margin-top:110px;background:{GOLD};color:{INK};
           font:800 28px Inter;letter-spacing:.06em;text-transform:uppercase;padding:14px 26px 14px 18px;border-radius:40px;align-self:flex-start;position:relative}}
    h1{{font:900 {size}px/1.02 Fraunces;margin:44px 0 0;letter-spacing:-.015em;position:relative}}
    h1 .hi{{color:{GOLD}}}
    .tease{{margin-top:44px;font:600 34px/1.35 Inter;color:#E9DFCF;position:relative}}
    .tease b{{color:{PAPER};font-weight:800}}
    .also{{margin-top:34px;display:flex;flex-direction:column;gap:16px;position:relative}}
    .also div{{display:flex;align-items:center;gap:20px;font:700 30px Inter;color:{PAPER}}}
    .also div span{{display:grid;place-items:center;width:62px;height:62px;border-radius:18px;background:#2E2720}}
    .also div em{{font-style:normal;font-weight:600;color:#B8AC9B}}
    .bar{{margin-top:auto;display:flex;justify-content:space-between;align-items:center;position:relative}}
    .meta{{font:600 26px/1.5 Inter;color:#B8AC9B}}
    .swipe{{display:flex;align-items:center;gap:18px;background:{PAPER};color:{INK};padding:22px 26px 22px 36px;border-radius:60px;font:800 30px Inter}}
    .brand{{color:{PAPER}}} .brand small{{color:#B8AC9B}}
    """
    bg = '<div class="glow"></div><div class="glow2"></div>'
    if img:
        css += f"""
    .bgp{{position:absolute;inset:0;background:url({img}) center 30%/cover}}
    .shade{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,16,12,.55) 0%,rgba(20,16,12,0) 22%,
            rgba(20,16,12,.25) 40%,rgba(20,16,12,.88) 60%,rgba(20,16,12,.97) 100%)}}
    .kick{{margin-top:auto}} h1{{text-shadow:0 2px 24px rgba(0,0,0,.45)}} .tease{{margin-top:30px}} .also{{margin-top:26px}}
    .also div span{{background:rgba(255,255,255,.12)}} .bar{{margin-top:48px}}
    .cr{{position:absolute;right:30px;top:50%;transform-origin:right top;transform:rotate(-90deg) translateX(50%);
         font:600 17px Inter;color:rgba(255,255,255,.7);white-space:nowrap;z-index:3}}
    """
        bg = f'<div class="bgp"></div><div class="shade"></div>{credit_html(cred)}'
    body = f"""<div class="slide">{bg}
      <div class="brand">{GLOBE.format(s=54, c=PAPER)}Good News Globe</div>
      <div class="kick">{icon(s0['category'], INK, 34, 6)}{esc(kicker)}</div>
      <h1>{hook_html(hook, (d.get('cover_highlight') or '').strip())}</h1>
      <div class="tease"><b>{f"{n} wins" if d.get("edition") == "Weekly" else f"+ {n - 1} more wins"}</b> {esc(tease)}</div>
      <div class="also">{also}</div>
      <div class="bar"><div class="meta">{esc(d['handle'])}<br>{date}</div>
        <div class="swipe">Swipe {ARROW.format(s=38, c=INK)}</div></div>
    </div>"""
    return page(body, css)

def story(d, s, i, n, total):
    label, accent, soft = cat(s)
    hl = s["headline"]
    has_stat = bool((s.get("stat") or "").strip())
    L = len(hl)
    if has_stat:
        size = 70 if L <= 40 else 62 if L <= 56 else 56
    else:
        size = 80 if L <= 40 else 72 if L <= 56 else 64
    stat = ""
    st = (s.get("stat") or "").strip()
    if has_stat:
        ssize = 150 if len(st) <= 4 else 124 if len(st) <= 6 else 104
        stat = (f'<div class="stat"><div class="num" style="font-size:{ssize}px">{esc(st)}</div>'
                f'<div class="lab">{esc(s.get("stat_label", ""))}</div></div>')
    img, cred = photo(d, s)
    if img:
        size = (58 if L <= 40 else 54 if L <= 56 else 50) if has_stat else (66 if L <= 40 else 60 if L <= 56 else 56)
        if has_stat:
            ssize = 104 if len(st) <= 4 else 88 if len(st) <= 6 else 76
            stat = (f'<div class="stat"><div class="num" style="font-size:{ssize}px">{esc(st)}</div>'
                    f'<div class="lab">{esc(s.get("stat_label", ""))}</div></div>')
    nxt = (f'<span class="next">Next {ARROW.format(s=26, c=accent)}</span>' if i < n
           else f'<span class="next">One more {ARROW.format(s=26, c=accent)}</span>')
    css = f"""
    .band{{position:absolute;left:0;top:0;width:1080px;height:16px;background:{accent}}}
    .chip{{display:inline-flex;align-items:center;gap:14px;background:{soft};color:{accent};font:800 26px Inter;
          letter-spacing:.08em;text-transform:uppercase;padding:14px 26px 14px 18px;border-radius:40px}}
    .place{{font:600 26px Inter;color:{MUTED};margin-left:18px}}
    .stat{{display:flex;align-items:center;gap:28px;margin-top:46px}}
    .num{{font:900 150px/0.9 Fraunces;color:{accent};letter-spacing:-.03em}}
    .lab{{font:700 32px/1.25 Inter;color:{INK};max-width:420px}}
    h2{{font:900 {size}px/1.05 Fraunces;margin:{36 if has_stat else 56}px 0 {30 if has_stat else 40}px;letter-spacing:-.01em}}
    .sum{{font:400 {33 if has_stat else 36}px/1.45 Inter;color:#3A3128}}
    .why{{position:relative;z-index:1;margin-top:{32 if has_stat else 44}px;border-left:8px solid {accent};background:{soft};
          padding:24px 32px;border-radius:0 24px 24px 0;font:600 {30 if has_stat else 32}px/1.4 Inter}}
    .why b{{display:block;font:800 22px Inter;letter-spacing:.14em;text-transform:uppercase;color:{accent};margin-bottom:6px}}
    .src{{font:600 23px/1.4 Inter;color:{MUTED}}} .src b{{color:{INK}}}
    .next{{display:inline-flex;align-items:center;gap:10px;font:800 26px Inter;color:{accent}}}
    .wm{{position:absolute;right:60px;bottom:120px;opacity:.10;z-index:0}}
    """
    if img:
        css += f"""
    .ph{{position:relative;margin:-80px -88px 0;height:530px;padding:56px 88px 30px;display:flex;flex-direction:column;
         background:url({img}) center 35%/cover;flex-shrink:0}}
    .ph:before{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,16,12,.55) 0%,rgba(20,16,12,0) 30%,rgba(20,16,12,0) 62%,rgba(20,16,12,.6) 100%)}}
    .ph .brand{{color:{PAPER}}} .ph .brand small{{color:rgba(255,255,255,.85)}}
    .ph .row{{margin-top:auto;display:flex;align-items:center;position:relative}}
    .ph .place{{color:{PAPER};text-shadow:0 1px 8px rgba(0,0,0,.6)}}
    .ph .cr{{position:absolute;right:20px;bottom:10px;font:600 16px Inter;color:rgba(255,255,255,.75);z-index:2}}
    .stat{{margin-top:34px;gap:24px}} .lab{{font-size:29px}}
    h2{{margin:{24 if has_stat else 40}px 0 {20 if has_stat else 28}px}}
    .sum{{font-size:{29 if has_stat else 32}px;line-height:1.42}}
    .why{{margin-top:{24 if has_stat else 32}px;padding:20px 28px;font-size:{27 if has_stat else 29}px}}
    .slide{{padding-bottom:64px}}
    """
        body = f"""<div class="slide">
      <div class="ph"><div class="brand">{GLOBE.format(s=44, c=PAPER)}Good News Globe<small>{i + 1}/{total}</small></div>
        <div class="row"><span class="chip">{icon(s['category'], accent, 36)}{label}</span><span class="place">{esc(s.get('place', ''))}</span></div>
        {credit_html(cred)}</div>
      {stat}
      <h2>{esc(hl)}</h2>
      <div class="sum">{esc(s['summary'])}</div>
      <div class="why"><b>Why it's cool</b>{esc(s['why'])}</div>
      <div class="foot"><span class="src">Source: <b>{esc(s['source_name'])}</b><br>Link in caption</span>
        <div style="display:flex;flex-direction:column;align-items:flex-end;gap:16px">{nxt}{dots(i, n)}</div></div>
    </div>"""
        return page(body, css)
    body = f"""<div class="slide"><div class="band"></div>
      <div class="wm">{icon(s['category'], accent, 260)}</div>
      <div class="brand">{GLOBE.format(s=44, c=INK)}Good News Globe<small>{i + 1}/{total}</small></div>
      <div style="margin-top:52px;display:flex;align-items:center"><span class="chip">{icon(s['category'], accent, 36)}{label}</span><span class="place">{esc(s.get('place', ''))}</span></div>
      {stat}
      <h2>{esc(hl)}</h2>
      <div class="sum">{esc(s['summary'])}</div>
      <div class="why"><b>Why it's cool</b>{esc(s['why'])}</div>
      <div class="foot"><span class="src">Source: <b>{esc(s['source_name'])}</b><br>Link in caption</span>
        <div style="display:flex;flex-direction:column;align-items:flex-end;gap:16px">{nxt}{dots(i, n)}</div></div>
    </div>"""
    return page(body, css)

def closing(d, total):
    share = (d.get("share_line") or "").strip() or "Send this to someone who needs a win today"
    q = (d.get("question") or "").strip()
    css = f"""
    .k{{font:800 26px Inter;letter-spacing:.14em;text-transform:uppercase;color:#E07A2E;margin-top:70px}}
    .fact{{font:900 56px/1.14 Fraunces;margin:20px 0 0}}
    .q{{margin-top:44px;background:#FFFFFF;border:3px solid #EADFCF;border-radius:28px;padding:28px 34px;font:700 32px/1.35 Inter}}
    .q small{{display:block;font:800 21px Inter;letter-spacing:.14em;text-transform:uppercase;color:{MUTED};margin-bottom:8px}}
    .cta{{margin-top:auto;background:{INK};color:{PAPER};border-radius:36px;padding:40px 44px}}
    .cta p{{font:900 46px/1.12 Fraunces}}
    .acts{{display:flex;gap:16px;margin-top:26px}}
    .acts span{{display:inline-flex;align-items:center;gap:10px;background:#3A3128;border-radius:40px;padding:14px 24px;font:700 25px Inter;color:{GOLD}}}
    .fol{{display:flex;align-items:center;gap:18px;margin-top:28px;font:700 27px Inter;color:#E9DFCF}}
    """
    send = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#FFC94D" stroke-width="2.4" stroke-linejoin="round"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4z"/></svg>'
    save = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#FFC94D" stroke-width="2.4" stroke-linejoin="round"><path d="M6 3h12v18l-6-4-6 4z"/></svg>'
    body = f"""<div class="slide">
      <div class="brand">{GLOBE.format(s=44, c=INK)}Good News Globe<small>{total}/{total}</small></div>
      <div class="k">Wait, one more thing</div>
      <div class="fact">{esc(d['fun_fact'])}</div>
      {f'<div class="q"><small>Tell us in the comments</small>{esc(q)}</div>' if q else ''}
      <div class="cta"><p>{esc(share)}</p>
        <div class="acts"><span>{send}Share</span><span>{save}Save for a bad day</span></div>
        <div class="fol">{GLOBE.format(s=40, c=PAPER)}Follow {esc(d['handle'])} for daily good news</div></div>
    </div>"""
    return page(body, css)

def caption(d):
    n = len(d["stories"])
    first = (d.get("caption_hook") or "").strip() or f"🌍 {n} good things happening in the world right now."
    lines = [first, ""]
    for i, s in enumerate(d["stories"], 1):
        e = (s.get("emoji") or "").strip()
        lines += [f"{i}. {e + ' ' if e else ''}{s['headline']}", s["summary"], f"🔗 {s['source_name']}{' (' + s['source_ig'].strip() + ')' if (s.get('source_ig') or '').strip() else ''}: {s['source_url']}", ""]
    lines += [f"✨ Fun fact: {d['fun_fact']}", ""]
    if (d.get("question") or "").strip():
        lines += [f"💬 {d['question'].strip()}", ""]
    creds = [f"{i}: {c}" for i, s in enumerate(d["stories"], 1) for c in [photo(d, s)[1]] if c]
    if creds:
        lines += ["📷 Photos: " + " · ".join(creds), ""]
    lines += ["📤 Send this to someone who needs good news today.",
              "🔖 Save it for a day you need a reminder that the world is still full of wins.",
              f"➕ Follow {d['handle']} for good news, 3 times a day.", "",
              d.get("hashtags", "#goodnews #positivenews #goodnewsglobe")]
    return "\n".join(lines)[:2200]

REEL_CSS = f"""
html,body{{width:1080px;height:1920px}}
body{{background:{INK};color:{PAPER}}}
.slide{{width:1080px;height:1920px;padding:150px 96px 170px;justify-content:center}}
.glow{{position:absolute;width:1100px;height:1100px;right:-420px;top:-420px;border-radius:50%;
       background:radial-gradient(circle,{GOLD} 0%,rgba(255,201,77,.30) 38%,rgba(31,26,20,0) 70%)}}
.brand{{position:absolute;top:110px;left:96px;color:{PAPER}}}
.tag{{position:absolute;bottom:150px;left:96px;right:96px;text-align:center;font:700 30px Inter;color:#B8AC9B}}
.kick{{display:inline-flex;align-items:center;gap:14px;background:{GOLD};color:{INK};font:800 32px Inter;letter-spacing:.06em;
       text-transform:uppercase;padding:16px 30px 16px 22px;border-radius:44px;align-self:flex-start}}
.hi{{color:{GOLD}}}
.rcr{{position:absolute;right:40px;bottom:60px;font:600 20px Inter;color:rgba(255,255,255,.75);z-index:3}}
"""

def reel_frames(d):
    s = d["stories"][0]
    label, accent, soft = cat(s)
    hook = (d.get("reel_hook") or d.get("cover_hook") or s["headline"]).strip()
    hi = (d.get("cover_highlight") or "").strip()
    hsize = 124 if len(hook) <= 30 else 108 if len(hook) <= 42 else 96
    place = esc(s.get("place", ""))
    brand = f'<div class="brand">{GLOBE.format(s=54, c=PAPER)}Good News Globe</div>'
    img, cred = photo(d, s)
    frames = []
    if img:
        bgp = (f'<div style="position:absolute;inset:0;background:url({img}) center 35%/cover"></div>'
               '<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,16,12,.6) 0%,rgba(20,16,12,0) 18%,'
               'rgba(20,16,12,.15) 42%,rgba(20,16,12,.9) 64%,rgba(20,16,12,.97) 100%)"></div>')
        rc = f'<div class="rcr">Photo: {esc(cred)}</div>' if cred else ""
        frames.append(f"""<div class="slide" style="justify-content:flex-end;padding-bottom:300px">{bgp}{brand}{rc}
          <div class="kick" style="position:relative">{icon(s['category'], INK, 38, 6)}{esc((d.get('cover_kicker') or label).strip())}</div>
          <h1 style="position:relative;font:900 {hsize}px/1.03 Fraunces;margin-top:40px;letter-spacing:-.015em;text-shadow:0 2px 24px rgba(0,0,0,.5)">{hook_html(hook, hi)}</h1>
          <div style="position:relative;margin-top:40px;font:700 40px Inter;color:#E9DFCF">{place}</div>
          <div class="tag">Watch to the end</div></div>""")
        st = (s.get("stat") or "").strip()
        dim = (f'<div style="position:absolute;inset:0;background:url({img}) center/cover;filter:blur(6px) brightness(.32);transform:scale(1.08)"></div>')
        if st:
            ssize = 300 if len(st) <= 4 else 230 if len(st) <= 6 else 190
            frames.append(f"""<div class="slide" style="align-items:center;text-align:center">{dim}{brand}
              <div style="position:relative;font:900 {ssize}px/0.9 Fraunces;color:{GOLD};letter-spacing:-.03em">{esc(st)}</div>
              <div style="position:relative;margin-top:44px;font:800 58px/1.2 Inter;max-width:860px">{esc(s.get('stat_label', ''))}</div></div>""")
        else:
            frames.append(f"""<div class="slide">{dim}{brand}
              <h2 style="position:relative;font:900 96px/1.05 Fraunces;letter-spacing:-.01em">{esc(s['headline'])}</h2></div>""")
        frames.append(f"""<div class="slide" style="background:{PAPER};color:{INK};justify-content:flex-start;padding-top:0">
          <div style="position:relative;margin:0 -96px;height:800px;flex-shrink:0;background:url({img}) center 35%/cover">
            <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,16,12,.55) 0%,rgba(20,16,12,0) 25%)"></div>
            <div class="brand" style="top:110px">{GLOBE.format(s=54, c=PAPER)}Good News Globe</div>
            {f'<div class="rcr" style="bottom:14px">Photo: {esc(cred)}</div>' if cred else ''}</div>
          <span style="align-self:flex-start;margin-top:56px;display:inline-flex;align-items:center;gap:14px;background:{soft};color:{accent};font:800 30px Inter;letter-spacing:.08em;text-transform:uppercase;padding:16px 30px 16px 22px;border-radius:44px">{icon(s['category'], accent, 40)}{label}</span>
          <h2 style="font:900 72px/1.06 Fraunces;margin:36px 0 30px;letter-spacing:-.01em">{esc(s['headline'])}</h2>
          <div style="font:400 38px/1.42 Inter;color:#3A3128">{esc(s['summary'])}</div>
          <div class="tag" style="color:{MUTED};bottom:110px">Source: {esc(s['source_name'])}</div></div>""")
        frames.append(why_frame(d, s, brand))
        return [page(f, REEL_CSS) for f in frames]
    # 1 — hook
    frames.append(f"""<div class="slide"><div class="glow"></div>{brand}
      <div class="kick">{icon(s['category'], INK, 38, 6)}{esc((d.get('cover_kicker') or label).strip())}</div>
      <h1 style="font:900 {hsize}px/1.03 Fraunces;margin-top:48px;letter-spacing:-.015em">{hook_html(hook, hi)}</h1>
      <div style="margin-top:56px;font:700 40px Inter;color:#E9DFCF">{place}</div>
      <div class="tag">Watch to the end</div></div>""")
    # 2 — the number (or the headline when there is no number)
    st = (s.get("stat") or "").strip()
    if st:
        ssize = 300 if len(st) <= 4 else 230 if len(st) <= 6 else 190
        frames.append(f"""<div class="slide" style="align-items:center;text-align:center">{brand}
          <div style="font:900 {ssize}px/0.9 Fraunces;color:{GOLD};letter-spacing:-.03em">{esc(st)}</div>
          <div style="margin-top:44px;font:800 58px/1.2 Inter;max-width:860px">{esc(s.get('stat_label', ''))}</div></div>""")
    else:
        frames.append(f"""<div class="slide">{brand}
          <h2 style="font:900 96px/1.05 Fraunces;letter-spacing:-.01em">{esc(s['headline'])}</h2></div>""")
    # 3 — what happened
    frames.append(f"""<div class="slide" style="background:{PAPER};color:{INK}">
      <div class="brand" style="color:{INK}">{GLOBE.format(s=54, c=INK)}Good News Globe</div>
      <span style="align-self:flex-start;display:inline-flex;align-items:center;gap:14px;background:{soft};color:{accent};font:800 30px Inter;letter-spacing:.08em;text-transform:uppercase;padding:16px 30px 16px 22px;border-radius:44px">{icon(s['category'], accent, 40)}{label}</span>
      <h2 style="font:900 84px/1.06 Fraunces;margin:44px 0 40px;letter-spacing:-.01em">{esc(s['headline'])}</h2>
      <div style="font:400 44px/1.45 Inter;color:#3A3128">{esc(s['summary'])}</div>
      <div class="tag" style="color:{MUTED}">Source: {esc(s['source_name'])}</div></div>""")
    frames.append(why_frame(d, s, brand))
    return [page(f, REEL_CSS) for f in frames]

def why_frame(d, s, brand):
    """Reel frame 4: why it matters + follow."""
    return (f"""<div class="slide"><div class="glow"></div>{brand}
      <div style="font:800 32px Inter;letter-spacing:.14em;text-transform:uppercase;color:{GOLD}">Why it's cool</div>
      <div style="margin-top:28px;font:900 74px/1.12 Fraunces">{esc(s['why'])}</div>
      <div style="margin-top:90px;background:{PAPER};color:{INK};border-radius:40px;padding:44px 48px;display:flex;align-items:center;gap:30px">
        {GLOBE.format(s=110, c=INK)}<div><div style="font:900 54px/1.1 Fraunces">Follow for daily good news</div>
        <div style="margin-top:10px;font:700 34px Inter;color:{MUTED}">{esc(d['handle'])} · 3 more wins in our latest post</div></div></div></div>""")

def reel_caption(d):
    s = d["stories"][0]
    e = (s.get("emoji") or "").strip()
    src = s["source_name"] + (f" ({s['source_ig'].strip()})" if (s.get("source_ig") or "").strip() else "")
    lines = [f"{e + ' ' if e else ''}{s['headline']}", "", s["summary"], "", f"Why it's cool: {s['why']}", "",
             f"🔗 {src}: {s['source_url']}", ""]
    c = photo(d, s)[1]
    if c:
        lines += [f"📷 Photo: {c}", ""]
    lines += [
             "📤 Send this to someone who needs good news today.",
             f"➕ Follow {d['handle']} for more wins like this, 3 times a day.", "",
             d.get("hashtags", "#goodnews #positivenews #goodnewsglobe")]
    return "\n".join(lines)[:2200]

def overflow(pg):
    return pg.evaluate("""() => { const s = document.querySelector('.slide'); const r = s.getBoundingClientRect();
        const limit = r.bottom - parseFloat(getComputedStyle(s).paddingBottom); let m = 0;
        for (const c of s.children) { const cs = getComputedStyle(c); if (cs.position === 'absolute') continue;
          m = Math.max(m, c.getBoundingClientRect().bottom - limit); }
        return Math.round(m); }""")

def main(src, out):
    d = json.loads(Path(src).read_text())
    d["_base"] = str(Path(src).resolve().parent)
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    n = len(d["stories"]); total = n + 2
    pages = [cover(d, total)] + [story(d, s, i, n, total) for i, s in enumerate(d["stories"], 1)] + [closing(d, total)]
    exe = "/opt/pw-browsers/chromium" if os.path.isfile("/opt/pw-browsers/chromium") else None
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        warn = []
        for i, h in enumerate(pages, 1):
            pg.set_content(h); pg.wait_for_timeout(150)
            # overflow check: content taller than the slide means text will be clipped
            over = overflow(pg)
            if over > 2:
                warn.append(f"{i:02d}.png overflows by {over}px — shorten its text")
            pg.screenshot(path=str(out / f"{i:02d}.png"))
        reel = out / "reel"; reel.mkdir(exist_ok=True)
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        for i, h in enumerate(reel_frames(d), 1):
            pg.set_content(h); pg.wait_for_timeout(150)
            over = overflow(pg)
            if over > 2:
                warn.append(f"reel/r{i}.png overflows by {over}px — shorten story #1's text")
            pg.screenshot(path=str(reel / f"r{i}.png"))
        b.close()
    (out / "caption.txt").write_text(caption(d))
    (out / "reel_caption.txt").write_text(reel_caption(d))
    fc = (d.get("first_comment") or "").strip()
    (out / "first_comment.txt").unlink(missing_ok=True)
    if fc:
        (out / "first_comment.txt").write_text(fc[:2200])
    print(f"Rendered {len(pages)} slides + 4 reel frames + captions -> {out}")
    for w in warn:
        print("WARNING:", w)
    if warn:
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
