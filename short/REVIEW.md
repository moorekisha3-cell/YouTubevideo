# Review: Pay the Tax Now

Render: `renders/pay-the-tax-now.mp4` (not committed). 1080x1920, 30 fps, 35.2 s, H.264 + AAC, 2.4 MB.
Built with HyperFrames CLI 0.8.194 (the plugin pins 0.8.195, which isn't on npm yet).

## Creative calls
- Built storyline C from `STORYLINES.md`. A (Your Number) and B (The $10,000 That Pays You) are still there to build.
- Facts come only from `script_video4.md` and `script_video9.md`. The tax bite is a visual with no percentage,
  and the jar growth is labelled "Illustrative growth".
- The limits are the 2026 IRS figures: $7,500 a year, or $8,600 at 50+. $7,500 / 12 = $625 a month.
  The scripts still carry the 2025 numbers ($7,000 / $8,000 / $583). The copy is in the `limitLine`/`limitNote`
  variables and the `$625` span in `compositions/roth.html`.
- Narration: the free local Kokoro voice (af_heart), made by `scripts/make_narration.py`. A HeyGen Joanna take
  was generated, but this session's network blocks its file host, so it was never used.
  Each sentence is synthesised separately and placed at the start time the scenes are cued to.
  "IRA" is spelled out ("I R A") and the channel is read as "Economics eleven forty-four".
- Captions (`compositions/captions.html`, from `scripts/make_captions.py`) replace the header titles. Word times
  inside a sentence are estimated by character count, not measured (no transcriber can download here), so
  a highlighted word may lead or lag its spoken word by up to about 0.2 s.
- Effects sit under the voice (bundled Pixabay-licensed files, no attribution needed). There's no music bed
  (no music source set up here).
- GSAP is loaded from `assets/vendor/gsap.min.js`, because the render browser can't reach the CDN.

## Measured vs. looked at
- `check` passes with no errors or warnings. The only remaining notes are info-level: the Traditional
  labels are covered by the teal flood, which is intentional.
- I looked at snapshots and decoded frames at 0, 3, 9.5, 11.1, 12.3, 16.5, 19, 20.2, 23, 26.5, 28.1 and 31.5 s.
- Audio was measured, not heard: -16.8 LUFS integrated, true peak -1.7 dBTP, no clipping. Nobody has listened
  to the Kokoro pronunciation, especially "I R A" and "eleven forty-four".

## Weakest shot
- 0-4.7 s: the picture is still while the voice and captions carry the hook; a coin dropping into each jar on
  frames 0-1 would give it motion.
- The voice: Kokoro is flatter than a HeyGen voice. Swap in a better take by replacing
  `assets/voice/narration.wav` and regenerating `words.json` and the captions.
- The lower third of the frame (below 1330 px) is plain teal by design, because the Shorts UI covers that area.
