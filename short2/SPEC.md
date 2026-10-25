# SPEC: Your Number (Economics 101 Short)

GOAL:    The viewer leaves knowing their retirement number: yearly spending x 25 (the 4% Rule, flipped).
OUTPUT:  HyperFrames, 1080 x 1920, 30 fps, vertical (YouTube Shorts). Storyline A in STORYLINES.md.
TIME:    45 s. Narrated with the free local Kokoro voice af_heart (scripts/make_narration.py, 43.6 s,
         levelled to about -15 LUFS); sentences laid end to end, scenes cued to assets/voice/words.json.
CAPTIONS: scripts/make_captions.py -> compositions/captions.html, same style as the first Short.
LOOK:    Deep green ground #0F4C3A, ink #F4F1E8, gold #F2C14E only for the result row (your number) and end card.
         Oswald 600 140 px numbers, 110 px operator; Inter 700 40 px labels; a 6 px calculator rule.
FORM:    One frame that rebuilds: value row, operator, rule, result. Numbers roll like an odometer (expo.out).
SHOTS:   0-13.6 $40,000 x 25 = ? -> $1,000,000 | 13.6-21 flip: $1,000,000 x 4% = $40,000 a year, ~30 years |
         21-27.8 $30,000 -> $750,000, $60,000 -> $1,500,000 | 27.8-35.5 goal $50,000 - $20,000 Social Security
         -> $30,000 x 25 = $750,000 | 35.5-38.7 "Your spending x 25 = Your number" | 38.7-45 end card (ECONOMICS 101).
FACTS:   From script_video3.md (4% Rule, 25x Rule, $40k->$1M, $30k->$750k, $60k->$1.5M, Social Security example).
