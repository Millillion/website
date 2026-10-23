"""Prototype "visual essay" chapter: motion graphics synced to Jordan's words (episode 1, Jagged intelligence).

Frames are drawn with PIL in the ink-on-washi style and piped to ffmpeg; timing comes from Whisper
word timestamps, so visuals land on the words that trigger them.

  python3 episodes-src/make_visual_chapter.py 001 <raw_start_s> <raw_end_s>
Writes episodes-src/001/visual/jagged-intelligence.mp4
"""
import json, math, os, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
NNN, A, B = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
D = os.path.join(HERE, NNN); OUT = os.path.join(D, "visual"); os.makedirs(OUT, exist_ok=True)
FONTS = os.path.expanduser("~/.cache/millillion/fonts")
W, H, FPS, OFFSET = 1920, 1080, 24, 11.0
PAPER, INK, SOFT, SHU, FAINT = (246, 242, 234), (22, 20, 18), (87, 82, 75), (179, 52, 31), (217, 210, 197)
F = lambda size, w="SemiBold": ImageFont.truetype(f"{FONTS}/ShipporiMincho-{w}.ttf", size)
norm = lambda w: re.sub(r"[^a-z0-9']", "", w.lower())

# audio + word timestamps
clip = f"{OUT}/clip.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(A + OFFSET), "-t", str(B - A), "-i", f"{D}/episode.mp3", "-ar", "44100", clip], check=True)
if not os.path.exists(f"{OUT}/clip.json"):
    subprocess.run(["whisper", clip, "--model", "small.en", "--language", "en", "--word_timestamps", "True", "--output_format", "json",
                    "--output_dir", OUT, "--fp16", "False"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
words = []
for w in (w for s in json.load(open(f"{OUT}/clip.json"))["segments"] for w in s.get("words", [])):
    if words and not w["word"].startswith(" "):  # glue split tokens ("y" "-axis")
        words[-1] = {**words[-1], "word": words[-1]["word"] + w["word"], "end": w["end"]}
    else:
        words.append(dict(w))
WS = [norm(w["word"]) for w in words]
DUR = B - A

def at(phrase, default=None, nth=0):
    toks = [norm(t) for t in phrase.split()]
    hits = [i for i in range(len(WS) - len(toks) + 1) if WS[i:i + len(toks)] == toks]
    return words[hits[nth]]["start"] if len(hits) > nth else default

AREAS = [("Software\nengineering", 0.88, "software engineering"), ("Mathematics", 0.72, "mathematics"), ("Accounting", 0.52, "accounting"),
         ("Art", 0.78, "art"), ("Video", 0.40, "video generation"), ("Audio", 0.62, "audio"), ("Teaching", 0.46, "teaching"), ("Writing", 0.82, "writing")]
T = {
    "title_out": 3.2,
    "axes": (at("graph of intelligence") or 6.0),
    "yaxis": at("y-axis") or at("y axis"),
    "xaxis": at("x-axis") or at("x axis"),
    "bars": [at(p, None) for _, _, p in AREAS],
    "jagged": at("jagged graph") or at("there's gaps") or DUR * 0.55,
    "fill": at("fill in") or DUR * 0.65,
    "quote1": at("I don't believe being useful") or at("being useful economically") or DUR * 0.75,
    "quote2": at("outrageous amounts") or DUR * 0.88,
}
# bars without a spoken cue appear right after the previous one
prev = T["axes"] + 0.6
for i, t in enumerate(T["bars"]):
    T["bars"][i] = t if t else prev + 0.5
    prev = T["bars"][i]
print("cues:", {k: (round(v, 1) if isinstance(v, float) else [round(x, 1) for x in v]) for k, v in T.items()})

ease = lambda x: 0 if x <= 0 else 1 if x >= 1 else 1 - (1 - x) ** 3
def fade(t, start, dur=0.5): return ease((t - start) / dur)

# chart geometry
CX0, CX1, CY0, CY1 = 260, 1660, 210, 760  # plot box: x0..x1, top..baseline
bw = (CX1 - CX0) / len(AREAS)
HUMAN = 0.80  # the level humans help fill up to

def brush_line(d, pts, width, color):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        d.line([(x0, y0), (x1, y1)], fill=color, width=width)
    for x, y in pts:
        d.ellipse([x - width / 2, y - width / 2, x + width / 2, y + width / 2], fill=color)

def caption(t):
    cur = [w for w in words if w["start"] <= t + 0.05][-9:]
    if not cur or t > cur[-1]["end"] + 1.2:
        return ""
    return " ".join(w["word"].strip() for w in cur)

def frame(t):
    im = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(im, "RGBA")
    # title card
    if t < T["title_out"] + 0.6:
        a = 1 - fade(t, T["title_out"], 0.6)
        d.text((W / 2, H / 2 - 40), "Jagged intelligence", font=F(110), fill=INK + (int(255 * a),), anchor="mm")
        d.text((W / 2, H / 2 + 70), "CHAPTER · EPISODE 1", font=F(30, "Medium"), fill=SOFT + (int(255 * a),), anchor="mm")
    in_quotes = t >= T["quote1"] - 0.2
    chart_a = 1 - fade(t, T["quote1"] - 0.6, 0.6)
    if t >= T["axes"] and chart_a > 0:
        ax = fade(t, T["axes"], 0.8)
        ca = int(255 * chart_a)
        # y axis label + baseline drawn like a brush stroke
        brush_line(d, [(CX0 - 30, CY1), (CX0 - 30 + (CX1 - CX0 + 60) * ax, CY1)], 5, INK + (ca,))
        if T["yaxis"] and t >= T["yaxis"]:
            ya = fade(t, T["yaxis"], 0.8)
            brush_line(d, [(CX0 - 30, CY1), (CX0 - 30, CY1 - (CY1 - CY0 + 40) * ya)], 5, INK + (ca,))
            d.text((CX0 - 10, CY0 - 50), "level of intelligence", font=F(30, "Medium"), fill=SOFT + (int(ca * ya),), anchor="ls")
        if T["xaxis"] and t >= T["xaxis"] and t < T["bars"][0] + 0.7:
            xa = fade(t, T["xaxis"], 0.8) * (1 - fade(t, T["bars"][0], 0.7))
            d.text((W / 2, CY1 + 60), "areas of intelligence", font=F(30, "Medium"), fill=SOFT + (int(ca * xa),), anchor="mm")
            for i in range(len(AREAS)):
                x0 = CX0 + i * bw + bw * 0.2; x1 = CX0 + (i + 1) * bw - bw * 0.2
                d.rectangle([x0, CY0 + 120, x1, CY1 - 4], outline=FAINT + (int(ca * xa),), width=3)
        for i, (label, hgt, _) in enumerate(AREAS):
            g = fade(t, T["bars"][i], 0.7)
            if g <= 0:
                continue
            x0 = CX0 + i * bw + bw * 0.2; x1 = CX0 + (i + 1) * bw - bw * 0.2
            top = CY1 - (CY1 - CY0) * hgt * g
            d.rectangle([x0, top, x1, CY1 - 4], fill=INK + (int(ca * 0.92),))
            for k, line in enumerate(label.split("\n")):
                d.text(((x0 + x1) / 2, CY1 + 40 + k * 34), line, font=F(28, "Medium"), fill=SOFT + (int(ca * g),), anchor="mm")
            # humans fill the gap up to the human level
            fg = fade(t, T["fill"] + i * 0.12, 0.7)
            if fg > 0 and hgt < HUMAN:
                htop = CY1 - (CY1 - CY0) * HUMAN
                d.rectangle([x0, top - (top - htop) * fg, x1, top], fill=SHU + (int(ca * 0.75),))
        # the jagged line across the bar tops
        jg = fade(t, T["jagged"], 1.4)
        if jg > 0:
            pts = [(CX0 + (i + 0.5) * bw, CY1 - (CY1 - CY0) * h) for i, (_, h, _) in enumerate(AREAS)]
            n = 1 + jg * (len(pts) - 1); k = int(n)
            seg = pts[:k] + ([(pts[k - 1][0] + (pts[min(k, len(pts) - 1)][0] - pts[k - 1][0]) * (n - k),
                               pts[k - 1][1] + (pts[min(k, len(pts) - 1)][1] - pts[k - 1][1]) * (n - k))] if k < len(pts) else [])
            brush_line(d, seg, 7, SHU + (ca,))
        if t >= T["fill"]:
            fa = int(ca * fade(t, T["fill"] + 0.8, 0.6))
            d.text((CX1, CY0 - 40), "where humans fill the gaps", font=F(30, "Medium"), fill=SHU + (fa,), anchor="rs")
    # quotes
    for key, text, nxt in (("quote1", "“I don't believe being useful\neconomically is the purpose\nof humanity.”", "quote2"),
                           ("quote2", "“…outrageous amounts\nof abundance.”", None)):
        s = T[key]; e = T[nxt] - 0.4 if nxt else DUR
        if s - 0.1 <= t <= e + 0.5:
            a = fade(t, s, 0.6) * (1 - fade(t, e, 0.5))
            d.multiline_text((W / 2, H / 2 - 40), text, font=F(86), fill=INK + (int(255 * a),), anchor="mm", align="center", spacing=22)
    # captions (bottom, soft)
    quoting = any(T[k] - 0.2 <= t for k in ("quote1",))
    if t > T["title_out"] and not quoting:
        c = caption(t)
        if c:
            d.text((W / 2, 975), c, font=F(38, "Medium"), fill=SOFT, anchor="mm")
    # corner mark
    d.text((80, 80), "MILLILLION", font=F(26, "Medium"), fill=SOFT, anchor="ls")
    return im

out = f"{OUT}/jagged-intelligence.mp4"
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                      "-i", clip, "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                      "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
for n in range(int(DUR * FPS)):
    p.stdin.write(frame(n / FPS).tobytes())
p.stdin.close(); p.wait()
print("wrote", out)
