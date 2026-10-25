import json
# word timings written by scripts/make_narration.py
W=[(w["text"], w["start"], w["end"]) for w in json.load(open("assets/voice/words.json"))]
sizes=[2,2,4,3,4,6,3,6,3,2,5,4,3,3,2,2,3,2,5,2,6,3,2,3,4,3,3,3]
assert sum(sizes)==len(W), (sum(sizes),len(W))
groups=[];i=0
for n in sizes: groups.append(W[i:i+n]); i+=n
for g in groups: assert len(" ".join(w for w,_,_ in g))<=26, g
html=['<template>','  <style>','''    #root {
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
      color: #ffffff;
      white-space: nowrap;
      overflow: visible;
      opacity: 0;
    }
    .cap span {
      opacity: 0.4;
    }''','  </style>','  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">']
js=[]
for gi,g in enumerate(groups):
    gid=f"cap-{gi+1}"
    spans=" ".join(f'<span id="{gid}-w{wi+1}">{w}</span>' for wi,(w,_,_) in enumerate(g))
    html.append(f'    <div id="{gid}" class="cap">{spans}</div>')
    start=0.0 if gi==0 else round(g[0][1]-0.05,3)
    nxt=groups[gi+1][0][1]-0.05 if gi+1<len(groups) else 35.1
    end=round(min(g[-1][2]+0.3, nxt),3)
    js.append(f'    tl.set("#{gid}", {{ opacity: 1 }}, {start});')
    for wi,(w,ws,we) in enumerate(g):
        if gi==0:
            # the hook is the thumbnail: fully lit on frame 0
            js.append(f'    tl.set("#{gid}-w{wi+1}", {{ opacity: 1 }}, 0);')
        else:
            js.append(f'    tl.to("#{gid}-w{wi+1}", {{ opacity: 1, duration: 0.08, ease: "power2.out" }}, {round(ws,3)});')
    js.append(f'    tl.to("#{gid}", {{ opacity: 0, duration: 0.1, ease: "power2.in" }}, {round(end-0.1,3)});')
    js.append(f'    tl.set("#{gid}", {{ opacity: 0, visibility: "hidden" }}, {end});')
html.append('  </div>')
html.append('  <script>')
html.append('    // One caption group at a time; each word lights up on its spoken start (word timings from assets/voice/words.json)')
html.append('    const tl = gsap.timeline({ paused: true });')
html+=js
html.append('    window.__timelines["captions"] = tl;')
html.append('  </script>')
html.append('</template>')
open('compositions/captions.html','w').write("\n".join(html)+"\n")
print(len(groups), "groups")
