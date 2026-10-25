# SPEC: Pay the Tax Now (Economics 1144 Short)

GOAL:    The viewer leaves knowing a Roth IRA is taxed going in, so it pays out with $0 tax,
         and that $583 a month maxes it.
OUTPUT:  HyperFrames, 1080 x 1920, 30 fps, vertical (YouTube Shorts).
TIME:    32.9 s x 30 = 987 frames. No music bed (no music source here); effects only.

LOOK:    Split ground at y=835: slate #4A5868 on top (Traditional), deep teal #0B7A78 below (Roth).
         Ink #FFFFFF. Accent gold #F2C14E for "$0", "$583" and the end-card rule only.
         Tax colour coral #FFB4A2, used for the tax band and "- Taxes" only.
         Display: Oswald 600, 110-130 px headers, 80 px labels, -1% tracking. Body: Inter 400/700, 38-48 px.
         Medium: a glass coin jar with a metal lid and a coin slot, filled with stacked gold coins
         (#E2B23E rows, #A97C1C seams every 18 px); glass is 10% white with a 6 px 90% white edge
         and one 16 px highlight stripe; contact shadow 25% black.
OBJECTS: Two identical coin jars (savings), a coral band inside the Traditional jar (the tax bite),
         falling gold coins with "$" (monthly contributions), an age counter (35 to 59½).
MOTION:  Arrivals expo.out / power4.out over 0.18-0.35 s; the flood and camera moves power2.inOut / power3.inOut
         over 0.7-1.0 s; the tax drop power3.in over 0.4 s. Exits are blur-outs of 0.15-0.2 s. Titles land, then hold still.
SAFE:    All words between y=168 and y=1330, x between 110 and 930 (clear of the action rail).

SHOTS:
  0.0-4.0    Hook. Both jars 30% full, labels on frame 0. "Same savings." then "One gets taxed later."
  4.0-10.0   Grow. "Both grow for decades" + age 35 to 59½; both jars fill 30% to 80% together. Quiet line "Illustrative growth".
  10.0-14.6  Bite. "Time to withdraw". A coral band wipes across the top of the Traditional jar's coins, then
             drops out of the jar (80% to 55%); "- Taxes" lands in coral. Bass impact on the drop.
  14.6-18.4  Payout. "Roth pays out whole". "$0" lands in gold beside the Roth jar, "tax on withdrawals". Ping.
  18.4-20.4  Collapse. Teal floods up over the slate; the Roth jar travels to the centre and grows 1.25x. Whoosh.
  20.4-28.4  Claim. "Pay the tax now." Coins drop into the slot: "Up to $7,000 a year", then "$583 a month maxes it";
             "2025 limit · $8,000 if 50 or older". Pops on each coin. Jar then shrinks into the end-card icon.
  28.4-32.9  End card. ECONOMICS 1144 wipes in on a bass hit, gold rule, "Full video on the channel",
             "Subscribe for more", "Educational only. Not financial advice." Holds 3 s.

FACTS (from script_video4.md / script_video9.md): Traditional = tax break now, taxed on withdrawal.
         Roth = after-tax money in, tax-free growth, $0 tax on withdrawals after 59½.
         2025 limit $7,000 (under 50), $8,000 (50+); $583 a month hits the limit. Jar growth is illustrative.

BANNED:  dark void ground, glow, particles, purple/blue gradients, glass cards, pill chips, centred-everything,
         fade-and-slide-up entrances, drifting titles, corner labels, three cards in a row, docked logo,
         a tax percentage or dollar amount the scripts never state.
QA:      t=0 (both jars, labels and hook line readable), 9.5 (age 59½, jars equal), 12.2 (Traditional jar lower, "- Taxes"),
         16.5 ("$0"), 20.2 (teal full frame, jar centred), 26.5 ("$583 a month maxes it"), 31.5 (end card complete).
