# Review: Pay the Tax Now

Render: `renders/pay-the-tax-now.mp4` (not committed). 1080x1920, 30 fps, 32.9 s, H.264 + AAC, 1.3 MB.
Built with HyperFrames CLI 0.8.194 (the plugin pins 0.8.195, which isn't on npm yet).

## Creative calls
- Built storyline C from `STORYLINES.md`. A (Your Number) and B (The $10,000 That Pays You) are still there to build.
- Facts come only from `script_video4.md` and `script_video9.md`. The tax bite is a visual with no percentage,
  and the jar growth is labelled "Illustrative growth".
- The limits are the 2026 IRS figures: $7,500 a year, or $8,600 at 50+. $7,500 / 12 = $625 a month.
  The scripts still carry the 2025 numbers ($7,000 / $8,000 / $583). The copy is in the `limitLine`/`limitNote`
  variables and the `$625` span in `compositions/roth.html`.
- Sound is effects only (bundled Pixabay-licensed files, no attribution needed): pop, bass impact, ping, whoosh.
  There's no music bed, because no music source is set up here (HeyGen CLI not installed).
- GSAP is loaded from `assets/vendor/gsap.min.js`, because the render browser can't reach the CDN.

## Measured vs. looked at
- `check` passes with no errors or warnings. The only remaining notes are info-level: the Traditional
  labels are covered by the teal flood, which is intentional.
- I looked at snapshots and decoded frames at 0, 3, 9.5, 11.1, 12.3, 16.5, 19, 20.2, 23, 26.5, 28.1 and 31.5 s.
- Audio was measured, not heard: true peak -1.3 dBTP, no clipping, and onsets at 9.3, 11.8, 15.3,
  22.8, 25.3, 25.9, 26.9 (mark swell) and 29.4 s, each on its picture cue.

## Weakest shot
- 0-4 s: the jars are now 360x480 px (one-third of the frame width), the most the split panels allow. The hook
  is still static until 1.5 s; a coin dropping into each jar on frames 0-1 would give it motion.
- The lower third of the frame (below 1330 px) is plain teal by design, because the Shorts UI covers that area.
