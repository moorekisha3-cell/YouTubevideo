import json
# word timings from the HeyGen narration (assets/voice/narration.wav)
W=[("Same",0.299,0.512),("savings.",0.597,1.216),("Two",1.451,1.621),("accounts.",1.707,2.304),("But",2.603,2.731),("one",2.773,2.987),("of",3.029,3.072),("them",3.115,3.243),("gets",3.285,3.413),("taxed",3.541,3.797),("later.",3.84,4.395),("With",4.779,4.907),("a",4.949,4.992),("Traditional",5.035,5.248),("IRA,",5.461,6.037),("you",6.229,6.315),("get",6.357,6.443),("the",6.485,6.571),("tax",6.613,6.741),("break",6.827,6.997),("now.",7.083,7.531),("With",7.808,7.979),("a",8.021,8.107),("Roth,",8.149,8.491),("you",8.661,8.875),("pay",8.917,9.045),("the",9.088,9.131),("tax",9.173,9.344),("going",9.472,9.6),("in.",9.728,10.197),("Then",10.539,10.709),("both",10.923,11.136),("grow",11.264,11.477),("for",11.563,11.648),("decades.",11.691,12.274),("At",12.474,12.645),("59",12.688,13.072),("and",13.157,13.2),("a",13.242,13.285),("half,",13.328,13.669),("it's",13.84,14.053),("time",14.096,14.266),("to",14.309,14.394),("withdraw,",14.437,14.906),("and",15.077,15.248),("every",15.29,15.546),("Traditional",15.76,16.016),("withdrawal",16.229,16.613),("is",16.741,16.869),("taxed",16.912,17.21),("as",17.296,17.338),("income.",17.381,17.85),("The",18.021,18.149),("Roth?",18.192,18.512),("Zero",18.704,19.045),("tax",19.173,19.386),("on",19.557,19.642),("qualified",19.685,19.941),("withdrawals.",20.197,20.837),("So",21.008,21.136),("pay",21.178,21.349),("the",21.392,21.434),("tax",21.477,21.648),("now.",21.776,22.196),("For",22.445,22.53),("2026,",22.573,23.81),("you",24.023,24.109),("can",24.151,24.279),("put",24.322,24.407),("in",24.493,24.578),("up",24.621,24.706),("to",24.749,24.834),("$7,500",24.877,26.072),("a",26.2,26.285),("year.",26.328,26.754),("That's",27.01,27.224),("about",27.266,27.394),("$625",27.437,28.418),("a",28.503,28.589),("month.",28.631,29.058),("Get",29.399,29.57),("the",29.613,29.698),("full",29.741,29.869),("breakdown",29.954,30.381),("on",30.466,30.552),("Economics",30.637,31.064),("1144.",31.234,32.375)]
sizes=[2,2,4,3,4,6,3,6,3,2,5,4,3,3,2,2,3,2,5,2,6,3,2,3,4,3]
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
html.append('    // One caption group at a time; each word lights up on its spoken start (word timings from the HeyGen narration)')
html.append('    const tl = gsap.timeline({ paused: true });')
html+=js
html.append('    window.__timelines["captions"] = tl;')
html.append('  </script>')
html.append('</template>')
open('compositions/captions.html','w').write("\n".join(html)+"\n")
json.dump([{"id":f"w{i}","text":w,"start":s,"end":e} for i,(w,s,e) in enumerate(W)], open('assets/voice/words.json','w'), indent=1)
print(len(groups), "groups")
