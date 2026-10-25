"""Build compositions/captions.html from assets/voice/words.json (written by make_narration.py).

Groups break at a sentence end or comma, at 4 words, or before passing 22 characters.
One group shows at a time; each word lights up on its spoken start.
Run from short3/:  python3 scripts/make_captions.py
"""
import json

W = [(w["text"], w["start"], w["end"]) for w in json.load(open("assets/voice/words.json"))]
groups, cur = [], []
for w in W:
    if cur and (len(cur) == 4 or len(" ".join(x[0] for x in cur + [w])) > 22):
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
      top: 196px;
      width: 1080px;
      text-align: center;
      font-family: "Oswald", sans-serif;
      font-weight: 600;
      font-size: 80px;
      line-height: 1.1;
      color: #1f2a44;
      white-space: nowrap;
      overflow: visible;
      opacity: 0;
    }
    .cap span {
      opacity: 0.4;
    }''', '  </style>', '  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">']
js = []
for gi, g in enumerate(groups):
    gid = f"cap-{gi+1}"
    html.append(f'    <div id="{gid}" class="cap">' + " ".join(f'<span id="{gid}-w{wi+1}">{w}</span>' for wi, (w, _, _) in enumerate(g)) + '</div>')
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
