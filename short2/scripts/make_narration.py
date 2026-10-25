"""Build assets/voice/narration.wav from the free local Kokoro voice (af_heart).

Each sentence is synthesised on its own and laid end to end with a short pause.
Word timings are spread across each sentence's speech by spoken length and
written to assets/voice/words.json (for scripts/make_captions.py), with each
sentence's start in assets/voice/sentences.json (the scenes are cued to these).

Run from short2/:  python3 scripts/make_narration.py <hyperframes-cli>
"""
import json, subprocess, sys, wave, struct, os

CLI = sys.argv[1] if len(sys.argv) > 1 else "npx hyperframes"
VOICE = "af_heart"
RATE = 24000
OUT = "assets/voice/narration.wav"
TMP = ".hyperframes/tts"
LEAD = 0.25   # silence before the first sentence
GAP = 0.28    # pause between sentences

# (spoken text, caption text). Numbers are spelled out for the voice and shown as digits.
SENTENCES = [
    ("How much do you need to retire?", "How much do you need to retire?"),
    ("Start with what you'd spend each year. Say, forty thousand dollars.",
     "Start with what you'd spend each year. Say, $40,000."),
    ("Multiply it by twenty-five.", "Multiply it by 25."),
    ("That's one million dollars. That's your number.", "That's $1,000,000. That's your number."),
    ("Why twenty-five? It's the flip side of the four percent rule.", "Why 25? It's the flip side of the 4% Rule."),
    ("Take out four percent of a million in year one, and that's forty thousand, adjusted for inflation, for about thirty years.",
     "Take out 4% of a million in year one, and that's $40,000, adjusted for inflation, for about 30 years."),
    ("Want thirty thousand a year? You need seven hundred fifty thousand.", "Want $30,000 a year? You need $750,000."),
    ("Want sixty thousand? One and a half million.", "Want $60,000? $1.5 million."),
    ("And Social Security counts. If it covers twenty thousand of a fifty thousand dollar goal, you only need seven hundred fifty thousand.",
     "And Social Security counts. If it covers $20,000 of a $50,000 goal, you only need $750,000."),
    ("Your spending, times twenty-five. That's your number.", "Your spending, times 25. That's your number."),
    ("Get the full breakdown on Economics one oh one. And please subscribe to my channel!",
     "Get the full breakdown on Economics 101. And please subscribe to my channel!"),
]
# Spoken length of a caption word, for spreading time (numbers say more than they show).
SPOKEN = {"$40,000.": "forty thousand dollars", "$40,000,": "forty thousand", "25.": "twenty-five", "25?": "twenty-five",
          "25": "twenty-five", "$1,000,000.": "one million dollars", "4%": "four percent", "30": "thirty",
          "$30,000": "thirty thousand", "$750,000.": "seven hundred fifty thousand", "$60,000?": "sixty thousand",
          "$1.5": "one and a half", "$20,000": "twenty thousand", "$50,000": "fifty thousand dollar",
          "101.": "one oh one"}


def read(path):
    with wave.open(path) as w:
        assert w.getframerate() == RATE and w.getnchannels() == 1 and w.getsampwidth() == 2
        return list(struct.unpack(f"<{w.getnframes()}h", w.readframes(w.getnframes())))


def speech_span(x, thresh=600):
    idx = [i for i, v in enumerate(x) if abs(v) > thresh]
    return (idx[0], idx[-1]) if idx else (0, len(x))


os.makedirs(TMP, exist_ok=True)
track = [0] * int(LEAD * RATE)
words, starts = [], []
for n, (spoken, caption) in enumerate(SENTENCES):
    f = f"{TMP}/s{n:02d}.wav"
    subprocess.run(f'{CLI} tts {json.dumps(spoken)} -v {VOICE} -o {f}', shell=True, check=True, capture_output=True)
    x = read(f)
    a, b = speech_span(x)
    s0 = len(track) / RATE
    s1 = s0 + (b - a) / RATE
    track += x[a:b] + [0] * int(GAP * RATE)
    toks = caption.split()
    weights = [len(SPOKEN.get(t, t)) + 1 for t in toks]
    t = s0
    for tok, wgt in zip(toks, weights):
        d = (s1 - s0) * wgt / sum(weights)
        words.append({"text": tok, "start": round(t, 3), "end": round(t + d, 3)})
        t += d
    starts.append({"n": n, "start": round(s0, 3), "end": round(s1, 3), "caption": caption})
    print(f"{n:2d} {s0:6.2f}-{s1:6.2f}  {caption}")

with wave.open(OUT, "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
    w.writeframes(struct.pack(f"<{len(track)}h", *track))
for i, wd in enumerate(words):
    wd["id"] = f"w{i}"
json.dump(words, open("assets/voice/words.json", "w"), indent=1)
json.dump(starts, open("assets/voice/sentences.json", "w"), indent=1)
print(f"{OUT}: {len(track)/RATE:.2f}s, {len(words)} words")

# Level the voice for Shorts: about -15 LUFS with a -2 dBTP ceiling (the effects sit under it).
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", OUT, "-af", "loudnorm=I=-15:TP=-2:LRA=11", "-ar", str(RATE), OUT + ".tmp.wav"], check=True)
os.replace(OUT + ".tmp.wav", OUT)
