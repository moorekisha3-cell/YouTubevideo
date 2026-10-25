"""Write the eight chapter scenes into compositions/ (run from ladybird/).

Each scene is a <template> sub-composition. Times below are global seconds from
assets/voice/words.json; each scene subtracts its own start (SCENES) so the
script reads like the narration.
"""

SCENES = {  # id: (start, end)
    "hook": (0.0, 13.9), "what": (13.9, 38.6), "how": (38.6, 59.3), "medicaid": (59.3, 81.4),
    "tax": (81.4, 108.5), "states": (108.5, 122.3), "watch": (122.3, 145.6), "cta": (145.6, 162.5),
}

INK, RED, GREEN, MUTED, GROUND = "#1f2a44", "#c8372d", "#2e7d5b", "#5b6478", "#eef1f4"

LADYBUG = """<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="26" r="16" fill="#1f2a44"/>
  <ellipse cx="50" cy="58" rx="38" ry="36" fill="#c8372d"/>
  <rect x="48" y="24" width="4" height="70" fill="#1f2a44"/>
  <circle cx="32" cy="50" r="7" fill="#1f2a44"/><circle cx="68" cy="50" r="7" fill="#1f2a44"/>
  <circle cx="34" cy="74" r="6" fill="#1f2a44"/><circle cx="66" cy="74" r="6" fill="#1f2a44"/>
</svg>"""

HOUSE = """<svg viewBox="0 0 520 480" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="260" cy="466" rx="230" ry="12" fill="rgba(31,42,68,0.15)"/>
  <rect x="70" y="200" width="380" height="262" fill="#ffffff" stroke="#1f2a44" stroke-width="10"/>
  <polygon points="40,214 260,40 480,214" fill="#1f2a44"/>
  <rect x="350" y="70" width="44" height="90" fill="#1f2a44"/>
  <rect x="215" y="310" width="90" height="152" fill="#c8372d"/>
  <circle cx="290" cy="392" r="6" fill="#ffffff"/>
  <rect x="110" y="250" width="80" height="80" fill="#cfe0ef" stroke="#1f2a44" stroke-width="8"/>
  <rect x="330" y="250" width="80" height="80" fill="#cfe0ef" stroke="#1f2a44" stroke-width="8"/>
</svg>"""

CHECK = f"""<svg viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"><circle cx="30" cy="30" r="28" fill="{GREEN}"/>
<polyline points="17,31 26,40 44,21" fill="none" stroke="#ffffff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>"""

BASE_CSS = f"""
    #root {{ position: absolute; inset: 0; overflow: hidden; background: {GROUND}; color: {INK}; font-family: "Inter", sans-serif; }}
    .t {{ position: absolute; font-family: "Oswald", sans-serif; font-weight: 600; line-height: 1.05; white-space: nowrap; }}
    .b {{ position: absolute; font-weight: 700; line-height: 1.25; white-space: nowrap; }}
    .m {{ color: {MUTED}; }}
    .red {{ color: {RED}; }}
    .green {{ color: {GREEN}; }}
    .h {{ opacity: 0; }}
    .row {{ position: absolute; display: flex; align-items: center; gap: 28px; white-space: nowrap; }}
    .row svg {{ width: 64px; height: 64px; flex: none; }}
    .chapter {{ left: 140px; top: 84px; font-size: 76px; }}
"""

BASE_JS = """
    const tl = gsap.timeline({ paused: true });
    const S0 = %(start)s;  // scene start (global s); times below are global
    const at = (t) => Math.max(0, t - S0);
    const show = (sel, t, d = 0.22) =>
      tl.fromTo(sel, { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: d, ease: "power4.out" }, at(t));
    const hide = (sel, t) => tl.to(sel, { opacity: 0, filter: "blur(8px)", duration: 0.18, ease: "power2.in" }, at(t));
    const pop = (sel, t) =>
      tl.fromTo(sel, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.6)" }, at(t));
    const ink = (sel, t) => tl.to(sel, { color: "#1f2a44", duration: 0.12 }, at(t));
    const mute = (sel, t) => tl.to(sel, { opacity: 0.45, duration: 0.25, ease: "power2.out" }, at(t));
"""


def scene(sid, markup, js, extra_css=""):
    start = SCENES[sid][0]
    html = f"""<template>
  <style>{BASE_CSS}{extra_css}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1920" data-height="1080">
{markup}
  </div>
  <script>{BASE_JS % {"start": start}}
{js}
    window.__timelines["{sid}"] = tl;
  </script>
</template>
"""
    open(f"compositions/{sid}.html", "w").write(html)


def roll_js(el_id, rolls, start_value):
    """A seek-safe number roll: text is a pure function of scene time."""
    return f"""
    (() => {{
      const el = document.querySelector("#{el_id}");
      const rolls = {rolls};
      const ease = gsap.parseEase("expo.out");
      const val = (t) => {{
        let v = {start_value};
        for (const [s, e, to] of rolls) {{
          if (t < s) break;
          if (t >= e) {{ v = to; continue; }}
          return v + (to - v) * ease((t - s) / (e - s));
        }}
        return v;
      }};
      const d = {{ p: 0 }};
      tl.to(d, {{ p: 1, duration: SCENE_LEN, ease: "none", onUpdate: () => {{
        el.textContent = "$" + (Math.round(val(S0 + d.p * SCENE_LEN) / 1000) * 1000).toLocaleString("en-US");
      }} }}, 0);
    }})();"""


# ── 1. Hook ───────────────────────────────────────────────────────────────────
scene("hook", f"""
    <div id="hook-house" style="position:absolute; left:180px; top:200px; width:560px; height:518px">{HOUSE}</div>
    <div id="hook-q" class="t" style="left:840px; top:200px; font-size:84px">Pass your home to your kids</div>
    <div id="hook-c1" class="row h" style="left:840px; top:350px; font-size:60px"><span>{CHECK}</span><span class="t" style="position:static">No will</span></div>
    <div id="hook-c2" class="row h" style="left:840px; top:450px; font-size:60px"><span>{CHECK}</span><span class="t" style="position:static">No probate court</span></div>
    <div id="hook-c3" class="row h" style="left:840px; top:550px; font-size:60px"><span>{CHECK}</span><span class="t" style="position:static">Keep your Medicaid</span></div>
    <div id="hook-title" class="h" style="position:absolute; left:840px; top:300px; display:flex; align-items:center; gap:30px">
      <div style="width:150px; height:150px">{LADYBUG}</div>
      <div class="t" style="position:static; font-size:120px">THE <span class="red">LADYBIRD</span><br>DEED</div>
    </div>
    <div id="hook-sub" class="b h" style="left:840px; top:620px; font-size:40px">
      <span id="hook-s1" class="m">How it works</span> &nbsp;&middot;&nbsp; <span id="hook-s2" class="m">Who can use it</span><br>
      <span id="hook-s3" class="m">What to watch out for</span></div>""", """
    pop("#hook-c1", 3.25); pop("#hook-c2", 3.95); pop("#hook-c3", 5.6);
    hide(["#hook-q", "#hook-c1", "#hook-c2", "#hook-c3"], 7.0);
    tl.fromTo("#hook-title", { opacity: 0, scale: 1.12, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.35, ease: "expo.out", transformOrigin: "0% 50%" }, at(8.25));
    show("#hook-sub", 9.3);
    ink("#hook-s1", 10.6); ink("#hook-s2", 11.3); ink("#hook-s3", 12.2);""")

# ── 2. What it is ─────────────────────────────────────────────────────────────
DEED = f"""<svg viewBox="0 0 480 620" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="14" width="460" height="600" rx="10" fill="rgba(31,42,68,0.12)"/>
  <rect x="0" y="0" width="460" height="600" rx="10" fill="#ffffff" stroke="#1f2a44" stroke-width="6"/>
  <text x="230" y="78" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="34" fill="#1f2a44">ENHANCED LIFE</text>
  <text x="230" y="120" text-anchor="middle" font-family="Oswald" font-weight="600" font-size="34" fill="#1f2a44">ESTATE DEED</text>
  <rect x="60" y="160" width="340" height="10" rx="5" fill="#c9d1dc"/><rect x="60" y="195" width="300" height="10" rx="5" fill="#c9d1dc"/>
  <rect x="60" y="230" width="330" height="10" rx="5" fill="#c9d1dc"/><rect x="60" y="265" width="260" height="10" rx="5" fill="#c9d1dc"/>
  <rect x="60" y="300" width="320" height="10" rx="5" fill="#c9d1dc"/><rect x="60" y="335" width="280" height="10" rx="5" fill="#c9d1dc"/>
  <text x="60" y="420" font-family="Inter" font-weight="700" font-size="28" fill="#5b6478">LIFE TENANT</text>
  <rect x="60" y="440" width="200" height="6" fill="#1f2a44"/>
  <text x="60" y="510" font-family="Inter" font-weight="700" font-size="28" fill="#5b6478">BENEFICIARIES</text>
  <rect x="60" y="530" width="200" height="6" fill="#1f2a44"/>
  <circle cx="360" cy="490" r="62" fill="#c8372d" opacity="0.12"/>
</svg>"""
scene("what", f"""
    <div id="what-deed" style="position:absolute; left:200px; top:170px; width:480px; height:620px">{DEED}
      <div style="position:absolute; left:308px; top:438px; width:104px; height:104px">{LADYBUG}</div></div>
    <div id="what-control" class="t h" style="left:820px; top:180px; font-size:84px">You keep <span class="green">full control</span></div>
    <div id="what-l1" class="row h" style="left:820px; top:330px"><span>{CHECK}</span><span class="t" style="position:static; font-size:60px">Sell it</span></div>
    <div id="what-l2" class="row h" style="left:820px; top:430px"><span>{CHECK}</span><span class="t" style="position:static; font-size:60px">Mortgage it</span></div>
    <div id="what-l3" class="row h" style="left:820px; top:530px"><span>{CHECK}</span><span class="t" style="position:static; font-size:60px">Change the deed</span></div>
    <div id="what-perm" class="b m h" style="left:820px; top:640px; font-size:42px">Anytime. No one's permission needed.</div>
    <div id="what-xfer" class="h" style="position:absolute; left:820px; top:250px; width:980px; height:420px">
      <div class="t" style="left:0; top:0; font-size:84px">Then it passes <span class="green">automatically</span></div>
      <div class="b" style="left:0; top:200px; font-size:56px">You</div>
      <div id="what-arrow" style="position:absolute; left:150px; top:228px; width:520px; height:12px; background:#1f2a44"></div>
      <div id="what-head" style="position:absolute; left:660px; top:210px; width:0; height:0; border-left:44px solid #1f2a44; border-top:24px solid transparent; border-bottom:24px solid transparent"></div>
      <div class="b" style="left:730px; top:200px; font-size:56px">Your family</div>
      <div class="b m" style="left:0; top:300px; font-size:40px">The people you named on the deed</div>
    </div>
    <div id="what-lbj" class="h" style="position:absolute; left:820px; top:230px; width:980px">
      <div class="t" style="position:static; font-size:84px">Named for <span class="red">Lady Bird</span> Johnson</div>
      <div class="b m" style="position:static; margin-top:30px; font-size:42px; white-space:normal; width:900px">President Lyndon B. Johnson reportedly used a similar deed for his wife.</div>
    </div>""", """
    tl.fromTo("#what-deed", { opacity: 0, scale: 0.85, rotation: -4 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.5, ease: "expo.out" }, at(14.2));
    show("#what-control", 17.9);
    pop("#what-l1", 21.65); pop("#what-l2", 22.1); pop("#what-l3", 23.0);
    show("#what-perm", 24.4);
    hide(["#what-control", "#what-l1", "#what-l2", "#what-l3", "#what-perm"], 26.0);
    show("#what-xfer", 26.25);
    tl.fromTo("#what-arrow", { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "power3.inOut", transformOrigin: "0% 50%" }, at(28.4));
    tl.fromTo("#what-head", { opacity: 0 }, { opacity: 1, duration: 0.1 }, at(28.95));
    hide("#what-xfer", 31.2);
    show("#what-lbj", 31.45);""")

# ── 3. How it works ───────────────────────────────────────────────────────────
NODE = "position:absolute; top:330px; width:120px; height:120px; border-radius:50%; background:#ffffff; border:10px solid #1f2a44;"
scene("how", f"""
    <div class="t chapter">How it works</div>
    <div id="how-flow" style="position:absolute; inset:0">
      <div id="how-line" style="position:absolute; left:260px; top:384px; width:1400px; height:12px; background:#1f2a44"></div>
      <div id="how-n1" class="h" style="{NODE} left:200px"></div>
      <div id="how-n2" class="h" style="{NODE} left:900px; border-color:#2e7d5b"></div>
      <div id="how-n3" class="h" style="{NODE} left:1600px; border-color:#c8372d"></div>
      <div id="how-l1" class="b h" style="left:120px; top:480px; width:280px; text-align:center; font-size:40px; white-space:normal">Attorney drafts the deed</div>
      <div id="how-l2" class="b h" style="left:820px; top:480px; width:280px; text-align:center; font-size:40px; white-space:normal">You: the life tenant</div>
      <div id="how-l3" class="b h" style="left:1500px; top:480px; width:320px; text-align:center; font-size:40px; white-space:normal">Your beneficiaries</div>
      <div id="how-cert" class="b m h" style="left:1000px; top:620px; width:760px; text-align:center; font-size:38px; white-space:normal">They record a death certificate with the county</div>
      <div id="how-nocourt" class="t green h" style="left:1180px; top:200px; font-size:96px">No court.</div>
    </div>
    <div id="how-cmp" class="h" style="position:absolute; inset:0">
      <div class="b" style="left:140px; top:260px; font-size:44px">With a will: probate</div>
      <div id="how-bar" style="position:absolute; left:140px; top:330px; width:1500px; height:90px; background:#c8372d"></div>
      <div id="how-6m" class="t h" style="left:150px; top:440px; font-size:60px">6 months</div>
      <div id="how-2y" class="t red h" style="left:1500px; top:440px; font-size:60px">2 years</div>
      <div id="how-fees" class="b m h" style="left:140px; top:560px; font-size:42px">Court fees and attorney fees the whole time</div>
      <div class="b" style="left:140px; top:690px; font-size:44px">With a Ladybird Deed: <span class="green">no probate</span></div>
    </div>""", """
    pop("#how-n1", 40.2); show("#how-l1", 40.3);
    pop("#how-n2", 42.3); show("#how-l2", 42.4);
    pop("#how-n3", 45.5); show("#how-l3", 45.6);
    tl.fromTo("#how-line", { scaleX: 0 }, { scaleX: 1, duration: 2.0, ease: "power2.inOut", transformOrigin: "0% 50%" }, at(40.2));
    tl.to("#how-n2", { x: 700, opacity: 0, duration: 0.8, ease: "power3.inOut" }, at(47.2));
    show("#how-cert", 48.2);
    pop("#how-nocourt", 51.4);
    hide("#how-flow", 52.05);
    show("#how-cmp", 52.2);
    tl.fromTo("#how-bar", { scaleX: 0 }, { scaleX: 0.1, duration: 0.4, ease: "expo.out", transformOrigin: "0% 50%" }, at(54.2));
    show("#how-6m", 54.2);
    tl.to("#how-bar", { scaleX: 1, duration: 0.9, ease: "power2.inOut" }, at(54.9));
    show("#how-2y", 55.4);
    show("#how-fees", 56.6);""")

# ── 4. Medicaid ───────────────────────────────────────────────────────────────
ARROW = "position:absolute; width:300px; height:16px; background:#c8372d;"
scene("medicaid", f"""
    <div class="t chapter">The Medicaid advantage</div>
    <div id="med-house" style="position:absolute; left:720px; top:250px; width:480px; height:443px">{HOUSE}</div>
    <div id="med-care" class="b h" style="left:140px; top:300px; width:520px; font-size:44px">Medicaid pays for nursing home care</div>
    <div id="med-arrows" class="h" style="position:absolute; inset:0">
      <div class="b red" style="left:1380px; top:250px; font-size:44px">Estate recovery</div>
      <div id="med-a1" style="{ARROW} left:1300px; top:380px"></div>
      <div id="med-a2" style="{ARROW} left:1300px; top:470px"></div>
      <div id="med-a3" style="{ARROW} left:1300px; top:560px"></div>
    </div>
    <div id="med-shield" class="h" style="position:absolute; left:1150px; top:300px; width:180px; height:220px">
      <svg viewBox="0 0 180 220" xmlns="http://www.w3.org/2000/svg"><path d="M90 6 L170 36 L170 106 C170 160 132 196 90 214 C48 196 10 160 10 106 L10 36 Z" fill="#2e7d5b"/>
      <polyline points="52,108 80,138 130,80" fill="none" stroke="#ffffff" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
    <div id="med-skip" class="t green h" style="left:140px; top:430px; font-size:72px">Skips probate</div>
    <div id="med-only" class="b m h" style="left:140px; top:540px; width:540px; font-size:38px; white-space:normal">In Ladybird states, estate recovery usually reaches only probate assets</div>
    <div id="med-keep" class="t h" style="left:720px; top:740px; font-size:64px">Your family keeps the house</div>""", """
    show("#med-care", 62.6);
    show("#med-arrows", 64.9);
    tl.fromTo(["#med-a1", "#med-a2", "#med-a3"], { x: 200 }, { x: 0, duration: 0.7, ease: "power3.out", stagger: 0.12 }, at(64.9));
    tl.to(["#med-a1", "#med-a2", "#med-a3"], { x: -60, duration: 0.5, ease: "power2.in", stagger: 0.1 }, at(68.0));
    hide("#med-care", 69.4);
    pop("#med-shield", 69.9);
    tl.to(["#med-a1", "#med-a2", "#med-a3"], { x: 320, opacity: 0, duration: 0.5, ease: "power2.out", stagger: 0.08 }, at(72.0));
    hide("#med-arrows", 72.6);
    show("#med-skip", 72.0);
    show("#med-only", 75.3);
    show("#med-keep", 78.8);""")

# ── 5. Tax ────────────────────────────────────────────────────────────────────
scene("tax", f"""
    <div class="t chapter">The stepped-up basis</div>
    <div class="b m" style="left:140px; top:230px; font-size:40px">Bought in 1985</div>
    <div id="tax-buy" class="t h" style="left:140px; top:280px; font-size:110px">$80,000</div>
    <div id="tax-worth-l" class="b m h" style="left:140px; top:440px; font-size:40px">Worth when you pass</div>
    <div id="tax-worth" class="t h" style="left:140px; top:490px; font-size:110px">$350,000</div>
    <div id="tax-left" class="h" style="position:absolute; left:760px; top:230px; width:520px">
      <div class="b green" style="position:static; font-size:40px">With a Ladybird Deed</div>
      <div class="b m" style="position:static; margin-top:10px; font-size:36px">Your child's basis</div>
      <div id="tax-basis" class="t green" style="position:static; font-size:110px">$80,000</div>
      <div id="tax-zero-l" class="b h" style="position:static; margin-top:20px; font-size:40px">Capital gains tax</div>
      <div id="tax-zero" class="t green h" style="position:static; font-size:130px">$0</div>
    </div>
    <div id="tax-right" class="h" style="position:absolute; left:1340px; top:230px; width:520px">
      <div class="b red" style="position:static; font-size:40px">Added to the deed early</div>
      <div class="b m" style="position:static; margin-top:10px; font-size:36px">Your child keeps your basis</div>
      <div id="tax-keep" class="t h" style="position:static; font-size:110px">$80,000</div>
      <div id="tax-gain-l" class="b h" style="position:static; margin-top:20px; font-size:40px">Taxable gain up to</div>
      <div id="tax-gain" class="t red h" style="position:static; font-size:130px">$270,000</div>
    </div>""", """
    const SCENE_LEN = 27.1;
    show("#tax-buy", 86.1);
    show(["#tax-worth-l", "#tax-worth"], 89.2);
    show("#tax-left", 91.7);""" + roll_js("tax-basis", "[[93.8, 94.6, 350000]]", 80000) + """
    show(["#tax-zero-l", "#tax-zero"], 97.7);
    show("#tax-right", 99.5);
    show("#tax-keep", 103.1);
    show(["#tax-gain-l", "#tax-gain"], 105.9);""")

# ── 6. States ─────────────────────────────────────────────────────────────────
STATE = "position:absolute; left:220px; display:flex; align-items:center; gap:26px; font-family:Oswald; font-weight:600; font-size:76px;"
BUG = f'<div style="width:62px; height:62px">{LADYBUG}</div>'
scene("states", f"""
    <div class="t" style="left:140px; top:84px; font-size:76px">Only <span id="st-5" class="red" style="display:inline-block">5</span> states allow it</div>
    <div id="st-1" class="h" style="{STATE} top:230px">{BUG}Florida</div>
    <div id="st-2" class="h" style="{STATE} top:340px">{BUG}Michigan</div>
    <div id="st-3" class="h" style="{STATE} top:450px">{BUG}Texas</div>
    <div id="st-4" class="h" style="{STATE} top:560px">{BUG}Vermont</div>
    <div id="st-6" class="h" style="{STATE} top:670px">{BUG}West Virginia</div>
    <div id="st-else" class="h" style="position:absolute; left:1000px; top:250px; width:800px">
      <div class="b m" style="position:static; font-size:44px">Everywhere else, ask an attorney about</div>
      <div id="st-tod" class="t h" style="position:static; margin-top:40px; font-size:72px">A transfer on death deed</div>
      <div id="st-trust" class="t h" style="position:static; margin-top:30px; font-size:72px">A revocable living trust</div>
    </div>""", """
    tl.fromTo("#st-5", { scale: 1.5 }, { scale: 1, duration: 0.4, ease: "expo.out" }, at(109.9));
    show("#st-1", 112.4); show("#st-2", 113.0); show("#st-3", 113.65); show("#st-4", 114.1); show("#st-6", 115.0);
    show("#st-else", 116.3);
    show("#st-tod", 118.7);
    show("#st-trust", 120.4);""")

# ── 7. Watch out ──────────────────────────────────────────────────────────────
def item(n, top, text):
    return (f'<div id="w-{n}" class="h" style="position:absolute; left:140px; top:{top}px; display:flex; align-items:center; gap:34px">'
            f'<div style="width:96px; height:96px; border-radius:50%; background:{RED}; color:#ffffff; font-family:Oswald; font-weight:600; '
            f'font-size:58px; line-height:96px; text-align:center; flex:none">{n}</div>'
            f'<div class="b" style="position:static; font-size:46px; white-space:normal; width:1500px">{text}</div></div>')
scene("watch", f"""
    <div class="t chapter">4 things to watch out for</div>
    {item(1, 230, "Use a licensed estate planning attorney. A badly drafted deed can fail.")}
    {item(2, 380, "Have a mortgage? Confirm the deed won&rsquo;t trigger a due-on-sale clause.")}
    {item(3, 530, "Blended families or disputes? Choose beneficiaries carefully.")}
    {item(4, 680, "It covers your home only. You still need a will, a healthcare directive and a power of attorney.")}""", """
    show("#w-1", 124.2);
    mute("#w-1", 129.2); show("#w-2", 129.3);
    mute("#w-2", 133.9); show("#w-3", 134.0);
    mute("#w-3", 139.3); show("#w-4", 139.4);""")

# ── 8. Like, subscribe, bell ──────────────────────────────────────────────────
THUMB = """<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><path d="M6 20h8v22H6z M16 42V21l9-15c3 0 5 2 4 6l-2 8h13c3 0 5 3 4 6l-4 13c-1 2-2 3-4 3z" fill="currentColor"/></svg>"""
BELL = """<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><path d="M24 4c-7 0-12 5-12 12v10l-5 7v2h34v-2l-5-7V16c0-7-5-12-12-12z M18 39a6 6 0 0 0 12 0z" fill="currentColor"/></svg>"""
CURSOR = """<svg viewBox="0 0 40 56" xmlns="http://www.w3.org/2000/svg"><path d="M2 2 L2 46 L14 35 L22 54 L30 50 L22 32 L38 32 Z" fill="#ffffff" stroke="#1f2a44" stroke-width="3.5" stroke-linejoin="round"/></svg>"""
BTN = "position:absolute; top:520px; height:120px; border-radius:60px; display:flex; align-items:center; justify-content:center; gap:22px; font-family:Oswald; font-weight:600; font-size:56px;"
scene("cta", f"""
    <div id="cta-gift" style="position:absolute; inset:0">
      <div style="position:absolute; left:200px; top:230px; width:520px; height:480px">{HOUSE}</div>
      <div id="cta-gift-t" class="t h" style="left:820px; top:330px; font-size:84px">One of the best gifts</div>
      <div id="cta-gift-t2" class="t h" style="left:820px; top:440px; font-size:84px">you can leave <span class="red">your family</span></div>
    </div>
    <div id="cta-end" class="h" style="position:absolute; inset:0">
      <div id="cta-mark" class="t" style="left:0; top:200px; width:1920px; text-align:center; font-size:130px">ECONOMICS 101</div>
      <div id="cta-rule" style="position:absolute; left:810px; top:370px; width:300px; height:12px; background:#c8372d"></div>
      <div id="cta-like" style="{BTN} left:430px; width:340px; background:#dfe4ea; color:#1f2a44">
        <div id="cta-thumb" style="width:62px; height:62px">{THUMB}</div><span id="cta-like-t">LIKE</span></div>
      <div id="cta-sub" style="{BTN} left:830px; width:480px; background:#cc0000; color:#ffffff"><span id="cta-sub-t">SUBSCRIBE</span><span id="cta-sub-t2" style="position:absolute; opacity:0">SUBSCRIBED</span></div>
      <div id="cta-bell" style="{BTN} left:1370px; width:120px; background:#dfe4ea; color:#1f2a44">
        <div id="cta-bell-i" style="width:62px; height:62px">{BELL}</div></div>
      <div class="b m" style="left:0; top:720px; width:1920px; text-align:center; font-size:32px; font-weight:400">Educational only. Not legal advice. Laws vary by state.</div>
      <div id="cta-cursor" style="position:absolute; left:1500px; top:760px; width:56px; height:78px">{CURSOR}</div>
    </div>""", """
    show("#cta-gift-t", 149.6); show("#cta-gift-t2", 150.6);
    hide("#cta-gift", 152.6);
    tl.fromTo("#cta-end", { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "power2.out" }, at(152.75));
    tl.fromTo("#cta-mark", { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "power4.out" }, at(153.2));
    tl.fromTo("#cta-rule", { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: "expo.out" }, at(153.6));
    pop("#cta-like", 154.6); pop("#cta-sub", 154.75); pop("#cta-bell", 154.9);
    tl.fromTo("#cta-cursor", { opacity: 0 }, { opacity: 1, duration: 0.15 }, at(155.3));
    // cursor clicks: like on "like" (156.4), subscribe on "subscribe" (157.2), bell on "bell" (159.4)
    const click = (x, y, t) => {
      tl.to("#cta-cursor", { x, y, duration: 0.45, ease: "power3.inOut" }, at(t - 0.5));
      tl.to("#cta-cursor", { scale: 0.85, duration: 0.06, ease: "power2.in", transformOrigin: "0% 0%" }, at(t - 0.05));
      tl.to("#cta-cursor", { scale: 1, duration: 0.12, ease: "power2.out" }, at(t + 0.03));
    };
    click(-870, -170, 156.4);
    tl.to("#cta-like", { backgroundColor: "#1f2a44", color: "#ffffff", duration: 0.12 }, at(156.4));
    tl.fromTo("#cta-thumb", { scale: 1 }, { scale: 1.35, duration: 0.14, ease: "power2.out", yoyo: true, repeat: 1, immediateRender: false }, at(156.4));
    click(-440, -170, 157.2);
    tl.to("#cta-sub", { backgroundColor: "#5b6478", duration: 0.12 }, at(157.2));
    tl.to("#cta-sub-t", { opacity: 0, duration: 0.08 }, at(157.2));
    tl.to("#cta-sub-t2", { opacity: 1, duration: 0.08 }, at(157.2));
    click(-70, -170, 159.4);
    tl.to("#cta-bell", { backgroundColor: "#1f2a44", color: "#ffffff", duration: 0.12 }, at(159.4));
    tl.to("#cta-bell-i", { keyframes: { rotation: [0, -22, 18, -12, 8, 0] }, duration: 0.8, ease: "none", transformOrigin: "50% 10%" }, at(159.4));
    tl.to("#cta-cursor", { opacity: 0, duration: 0.3 }, at(160.6));""")

print("wrote", ", ".join(SCENES))
