"""Build assets/voice/narration.wav from the free local Kokoro voice (af_heart).

Each sentence is synthesised on its own and laid end to end with a short pause.
Word timings are spread across each sentence's speech by spoken length and
written to assets/voice/words.json (for scripts/make_captions.py), with each
sentence's start in assets/voice/sentences.json (the scenes are cued to these).

Run from short3/:  python3 scripts/make_narration.py <hyperframes-cli>
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
    ("This ten thousand dollars pays you every year.", "This $10,000 pays you every year."),
    ("Put it in dividend stocks yielding four percent.", "Put it in dividend stocks yielding 4%."),
    ("Year one, it pays you four hundred dollars.", "Year one, it pays you $400."),
    ("Reinvest it, and now ten thousand four hundred is working for you.", "Reinvest it, and now $10,400 is working for you."),
    ("Next year's payout? Four hundred sixteen.", "Next year's payout? $416."),
    ("Keep reinvesting for twenty years, without adding a dollar, and it could grow to over twenty-one thousand.",
     "Keep reinvesting for 20 years, without adding a dollar, and it could grow to over $21,000."),
    ("Want five hundred dollars a month? At a four percent yield, that takes about one hundred fifty thousand invested.",
     "Want $500 a month? At a 4% yield, that takes about $150,000 invested."),
    ("Start small. Reinvest. Let it compound.", "Start small. Reinvest. Let it compound."),
    ("Get the full breakdown on Economics one oh one. And please subscribe to my channel!",
     "Get the full breakdown on Economics 101. And please subscribe to my channel!"),
]
# Spoken length of a caption word, for spreading time (numbers say more than they show).
SPOKEN = {"$10,000": "ten thousand dollars", "4%.": "four percent", "4%": "four percent", "$400.": "four hundred dollars",
          "$10,400": "ten thousand four hundred", "$416.": "four hundred sixteen", "20": "twenty",
          "$21,000.": "twenty-one thousand", "$500": "five hundred dollars", "$150,000": "one hundred fifty thousand",
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
