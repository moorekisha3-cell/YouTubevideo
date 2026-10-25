"""Build compositions/captions.html from assets/voice/words.json (written by make_narration.py).

Groups break at a sentence end or comma, at 7 words, or before passing 46 characters.
One group shows at a time; each word lights up on its spoken start.
Run from ladybird/:  python3 scripts/make_captions.py
"""
import json

W = [(w["text"], w["start"], w["end"]) for w in json.load(open("assets/voice/words.json"))]
groups, cur = [], []
for w in W:
    if cur and (len(cur) == 7 or len(" ".join(x[0] for x in cur + [w])) > 46):
        groups.append(cur); cur = []
    cur.append(w)
    if w[0][-1] in ".?!,":
        groups.append(cur); cur = []
if cur:
    groups.append(cur)

html = ['<template>', '  <style>', '''    #root {
      position: absolute;
      inset: 0;
      pointer-events: none;
    }
    .cap {
      position: absolute;
      left: 0;
      top: 930px;
      width: 1920px;
      text-align: center;
      font-family: "Inter", sans-serif;
      font-weight: 700;
      font-size: 50px;
      line-height: 1.2;
      color: #ffffff;
      white-space: nowrap;
      overflow: visible;
      opacity: 0;
    }
    .cap b {
      display: inline-block;
      padding: 10px 28px;
      border-radius: 14px;
      background: rgba(31, 42, 68, 0.88);
      font-weight: 700;
    }
    .cap span {
      opacity: 0.45;
    }''', '  </style>', '  <div id="root" data-composition-id="captions" data-width="1920" data-height="1080">']
js = []
for gi, g in enumerate(groups):
    gid = f"cap-{gi+1}"
    html.append(f'    <div id="{gid}" class="cap"><b>' + " ".join(f'<span id="{gid}-w{wi+1}">{w}</span>' for wi, (w, _, _) in enumerate(g)) + '</b></div>')
    start = 0.0 if gi == 0 else round(g[0][1] - 0.05, 3)
    nxt = groups[gi + 1][0][1] - 0.05 if gi + 1 < len(groups) else g[-1][2] + 0.6
    end = round(min(g[-1][2] + 0.3, nxt), 3)
    js.append(f'    tl.set("#{gid}", {{ opacity: 1 }}, {start});')
    for wi, (w, ws, we) in enumerate(g):
        if gi == 0:
            # the hook is the thumbnail: fully lit on frame 0
            js.append(f'    tl.set("#{gid}-w{wi+1}", {{ opacity: 1 }}, 0);')
        else:
            js.append(f'    tl.to("#{gid}-w{wi+1}", {{ opacity: 1, duration: 0.08, ease: "power2.out" }}, {round(ws, 3)});')
    js.append(f'    tl.to("#{gid}", {{ opacity: 0, duration: 0.1, ease: "power2.in" }}, {round(end - 0.1, 3)});')
    js.append(f'    tl.set("#{gid}", {{ opacity: 0, visibility: "hidden" }}, {end});')
html += ['  </div>', '  <script>',
         '    // One caption group at a time; each word lights up on its spoken start (assets/voice/words.json)',
         '    const tl = gsap.timeline({ paused: true });'] + js + ['    window.__timelines["captions"] = tl;', '  </script>', '</template>']
open("compositions/captions.html", "w").write("\n".join(html) + "\n")
print(len(groups), "groups:", " | ".join(" ".join(w for w, _, _ in g) for g in groups))
