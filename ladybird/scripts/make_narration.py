"""Build assets/voice/narration.wav from the free local Kokoro voice (af_heart).

Each sentence is synthesised on its own and laid end to end with a short pause.
Word timings are spread across each sentence's speech by spoken length and
written to assets/voice/words.json (for scripts/make_captions.py), with each
sentence's start in assets/voice/sentences.json (the scenes are cued to these).

Run from ladybird/:  python3 scripts/make_narration.py <hyperframes-cli>
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
# (scene, spoken text, caption text). Numbers are spelled out for the voice and shown as digits.
SENTENCES = [
    ("hook", "What if you could pass your home to your children without a will, without probate court, and without losing Medicaid benefits?",
             "What if you could pass your home to your children without a will, without probate court, and without losing Medicaid benefits?"),
    ("hook", "It's real. It's called a Ladybird Deed.", "It's real. It's called a Ladybird Deed."),
    ("hook", "In the next two minutes: how it works, who can use it, and what to watch out for.",
             "In the next two minutes: how it works, who can use it, and what to watch out for."),
    ("what", "A Ladybird Deed, officially an enhanced life estate deed, lets you keep full control of your home while you're alive.",
             "A Ladybird Deed, officially an enhanced life estate deed, lets you keep full control of your home while you're alive."),
    ("what", "You can still sell it, mortgage it, or change the deed at any time, without anyone's permission.",
             "You can still sell it, mortgage it, or change the deed at any time, without anyone's permission."),
    ("what", "Then, the moment you pass away, the home transfers automatically to the people you named.",
             "Then, the moment you pass away, the home transfers automatically to the people you named."),
    ("what", "The nickname comes from President Lyndon B. Johnson, who reportedly used a similar deed for his wife, Lady Bird.",
             "The nickname comes from President Lyndon B. Johnson, who reportedly used a similar deed for his wife, Lady Bird."),
    ("how", "Here's how it works. An attorney drafts the deed. You're the life tenant. Your children, or whoever you choose, are the beneficiaries.",
            "Here's how it works. An attorney drafts the deed. You're the life tenant. Your children, or whoever you choose, are the beneficiaries."),
    ("how", "When you die, they record a death certificate with the county, and the home is theirs. No court.",
            "When you die, they record a death certificate with the county, and the home is theirs. No court."),
    ("how", "With a will, your family could wait six months to two years in probate, paying court and attorney fees the whole time.",
            "With a will, your family could wait 6 months to 2 years in probate, paying court and attorney fees the whole time."),
    ("medicaid", "Now the big one: Medicaid.", "Now the big one: Medicaid."),
    ("medicaid", "If Medicaid pays for nursing home care, the state may try to recover that cost from your estate after you die. That can include your home.",
                 "If Medicaid pays for nursing home care, the state may try to recover that cost from your estate after you die. That can include your home."),
    ("medicaid", "But a home passed by a Ladybird Deed skips probate, and in states that allow these deeds, estate recovery usually reaches only probate assets. So your family can keep the house.",
                 "But a home passed by a Ladybird Deed skips probate, and in states that allow these deeds, estate recovery usually reaches only probate assets. So your family can keep the house."),
    ("tax", "There's a tax benefit, too: the stepped-up basis.", "There's a tax benefit, too: the stepped-up basis."),
    ("tax", "Say you bought your home for eighty thousand dollars in nineteen eighty-five, and it's worth three hundred fifty thousand when you pass.",
            "Say you bought your home for $80,000 in 1985, and it's worth $350,000 when you pass."),
    ("tax", "Your child's cost basis resets to three hundred fifty thousand. Sell it for that, and they owe zero capital gains tax.",
            "Your child's cost basis resets to $350,000. Sell it for that, and they owe zero capital gains tax."),
    ("tax", "If you'd added your child to the deed years earlier, they'd keep your eighty thousand dollar basis, and could owe tax on a two hundred seventy thousand dollar gain.",
            "If you'd added your child to the deed years earlier, they'd keep your $80,000 basis, and could owe tax on a $270,000 gain."),
    ("states", "The catch? Only five states recognize Ladybird Deeds: Florida, Michigan, Texas, Vermont, and West Virginia.",
               "The catch? Only 5 states recognize Ladybird Deeds: Florida, Michigan, Texas, Vermont, and West Virginia."),
    ("states", "Everywhere else, ask an attorney about a transfer on death deed or a revocable living trust.",
               "Everywhere else, ask an attorney about a transfer on death deed or a revocable living trust."),
    ("watch", "Four things to watch out for.", "4 things to watch out for."),
    ("watch", "One: use a licensed estate planning attorney. A badly drafted deed can fail.",
              "1: use a licensed estate planning attorney. A badly drafted deed can fail."),
    ("watch", "Two: if you have a mortgage, confirm the deed won't trigger a due-on-sale clause.",
              "2: if you have a mortgage, confirm the deed won't trigger a due-on-sale clause."),
    ("watch", "Three: blended families and family disputes need careful choices about beneficiaries.",
              "3: blended families and family disputes need careful choices about beneficiaries."),
    ("watch", "And four: it only covers your home. You still need a will, a healthcare directive, and a power of attorney.",
              "And 4: it only covers your home. You still need a will, a healthcare directive, and a power of attorney."),
    ("cta", "Protecting your home can take an hour or two with the right attorney. It could be one of the best gifts you leave your family.",
            "Protecting your home can take an hour or two with the right attorney. It could be one of the best gifts you leave your family."),
    ("cta", "This is Economics one oh one. If this helped, give the video a like, please subscribe to my channel, and tap the bell.",
            "This is Economics 101. If this helped, give the video a like, please subscribe to my channel, and tap the bell."),
]
# Spoken length of a caption word, for spreading time (numbers say more than they show).
SPOKEN = {"6": "six", "2": "two", "$80,000": "eighty thousand dollars", "1985,": "nineteen eighty-five",
          "$350,000": "three hundred fifty thousand", "$350,000.": "three hundred fifty thousand", "$270,000": "two hundred seventy thousand dollar",
          "5": "five", "4": "four", "1:": "one", "2:": "two", "3:": "three", "101.": "one oh one"}


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
for n, (scene, spoken, caption) in enumerate(SENTENCES):
    if starts and starts[-1]["scene"] != scene:
        track += [0] * int(0.5 * RATE)  # a breath between chapters
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
    starts.append({"n": n, "scene": scene, "start": round(s0, 3), "end": round(s1, 3), "caption": caption})
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
