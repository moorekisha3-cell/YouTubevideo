"""Build assets/voice/narration.wav from the free local Kokoro voice (af_heart).

Each sentence is synthesised on its own and placed at a fixed start time, so the
scenes (timed to these anchors) and the captions stay in sync. Word timings are
spread across each sentence's speech by character count and written to
assets/voice/words.json for scripts/make_captions.py.

Run from short/:  python3 scripts/make_narration.py <hyperframes-cli>
"""
import json, subprocess, sys, wave, struct, os, re

CLI = sys.argv[1] if len(sys.argv) > 1 else "npx hyperframes"
VOICE = "af_heart"
RATE = 24000
OUT = "assets/voice/narration.wav"
TMP = ".hyperframes/tts"

# (start s, spoken text, caption words). Starts match the scene anchors.
SENTENCES = [
    (0.30, "Same savings.", "Same savings."),
    (1.45, "Two accounts.", "Two accounts."),
    (2.60, "But one of them gets taxed later.", "But one of them gets taxed later."),
    (4.78, "With a Traditional I R A, you get the tax break now.", "With a Traditional IRA, you get the tax break now."),
    (7.81, "With a Roth, you pay the tax going in.", "With a Roth, you pay the tax going in."),
    (10.54, "Then both grow for decades.", "Then both grow for decades."),
    (12.47, "At fifty-nine and a half, it's time to withdraw, and every Traditional withdrawal is taxed as income.",
            "At 59 and a half, it's time to withdraw, and every Traditional withdrawal is taxed as income."),
    (18.02, "The Roth?", "The Roth?"),
    (18.70, "Zero tax on qualified withdrawals.", "Zero tax on qualified withdrawals."),
    (21.01, "So pay the tax now.", "So pay the tax now."),
    (22.45, "For twenty twenty-six, you can put in up to seventy-five hundred dollars a year.",
            "For 2026, you can put in up to $7,500 a year."),
    (27.01, "That's about six hundred twenty-five a month.", "That's about $625 a month."),
    (29.40, "Get the full breakdown on Economics one oh one. And please subscribe to my channel!",
            "Get the full breakdown on Economics 101. And please subscribe to my channel!"),
]
# Spoken length of a caption word, for spreading time (numbers say more than they show).
SPOKEN = {"IRA,": "I R A", "59": "fifty-nine", "2026,": "twenty twenty-six", "$7,500": "seventy-five hundred dollars",
          "$625": "six hundred twenty-five", "101.": "one oh one"}


def read(path):
    with wave.open(path) as w:
        assert w.getframerate() == RATE and w.getnchannels() == 1 and w.getsampwidth() == 2
        return list(struct.unpack(f"<{w.getnframes()}h", w.readframes(w.getnframes())))


def speech_span(x, thresh=600):
    idx = [i for i, v in enumerate(x) if abs(v) > thresh]
    return (idx[0], idx[-1]) if idx else (0, len(x))


os.makedirs(TMP, exist_ok=True)
track = []
words = []
# Sentences that must speed up to finish before the next anchor
SPEED = {6: 1.12}
for n, (start, spoken, caption) in enumerate(SENTENCES):
    f = f"{TMP}/s{n:02d}.wav"
    subprocess.run(f'{CLI} tts {json.dumps(spoken)} -v {VOICE} -s {SPEED.get(n, 1.0)} -o {f}', shell=True, check=True, capture_output=True)
    x = read(f)
    a, b = speech_span(x)
    clip = x[a:b + int(0.05 * RATE)]
    at = int(start * RATE)
    if len(track) > at:
        raise SystemExit(f"sentence {n} ({caption!r}) would start at {len(track)/RATE:.2f}s, after its anchor {start}s")
    track += [0] * (at - len(track)) + clip
    s0, s1 = start, start + (b - a) / RATE
    toks = caption.split()
    weights = [len(SPOKEN.get(t, t)) + 1 for t in toks]
    t = s0
    for tok, wgt in zip(toks, weights):
        d = (s1 - s0) * wgt / sum(weights)
        words.append({"text": tok, "start": round(t, 3), "end": round(t + d, 3)})
        t += d
    print(f"{n:2d} {s0:6.2f}-{s1:6.2f}  {caption}")

track += [0] * int(0.3 * RATE)
with wave.open(OUT, "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
    w.writeframes(struct.pack(f"<{len(track)}h", *track))
for i, wd in enumerate(words):
    wd["id"] = f"w{i}"
json.dump(words, open("assets/voice/words.json", "w"), indent=1)
print(f"{OUT}: {len(track)/RATE:.2f}s, {len(words)} words")
