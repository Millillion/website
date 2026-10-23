"""Vertical Short (1080x1920) from an episode moment, with word-by-word captions.

  python3 episodes-src/make_short.py NNN <slug> <raw_start_s> <raw_end_s> "<first words>" "<last words>" "<Hook title>"

Times are in the raw recording (Whisper raw.json). The clip is cut from the mastered episode
(voice starts at +11 s), re-transcribed with word timestamps, and trimmed exactly to the
first/last phrase. Writes episodes-src/NNN/shorts/<slug>.mp4 (+ .srt).
"""
import json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
NNN, SLUG, A, B, FIRST, LAST, HOOK = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), sys.argv[5], sys.argv[6], sys.argv[7]
OFFSET = 11.0
D = os.path.join(HERE, NNN); OUT = os.path.join(D, "shorts"); os.makedirs(OUT, exist_ok=True)
FONTS = os.path.expanduser("~/.cache/millillion/fonts")
W, H, FPS = 1080, 1920, 30
vocab = []
for line in open(os.path.join(HERE, "vocab.tsv")):
    if line.strip() and not line.startswith("#"):
        p, _, r = line.rstrip("\n").partition("\t"); vocab.append((re.compile(p), r))
norm = lambda w: re.sub(r"[^a-z0-9']", "", w.lower())

# 1. wide clip from the mastered episode, transcribed with word timestamps
pad = 2.0
s0 = A + OFFSET - pad
wide = f"{OUT}/{SLUG}-wide.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(s0), "-t", str(B - A + 2 * pad), "-i", f"{D}/episode.mp3", "-ac", "1", "-ar", "16000", wide], check=True)
hq = f"{OUT}/{SLUG}-wide-hq.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(s0), "-t", str(B - A + 2 * pad), "-i", f"{D}/episode.mp3", "-ar", "44100", hq], check=True)
subprocess.run(["whisper", wide, "--model", "small.en", "--language", "en", "--word_timestamps", "True", "--output_format", "json",
                "--output_dir", OUT, "--fp16", "False"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
raw_words = [w for s in json.load(open(f"{OUT}/{SLUG}-wide.json"))["segments"] for w in s.get("words", [])]
# Whisper splits tokens like "GPT" "5" ".2": glue pieces without a leading space onto the previous word
words = []
for w in raw_words:
    if words and not w["word"].startswith(" "):
        words[-1] = {**words[-1], "word": words[-1]["word"] + w["word"], "end": w["end"]}
    else:
        words.append(dict(w))
# join a model name and its version ("GPT" "5.2" -> "GPT-5.2"), and drop false starts like "or 3, 5.3" -> "or 5.3"
merged = []
for w in words:
    t = w["word"].strip()
    if merged and re.fullmatch(r"\d+(\.\d+)?[,.]?", t) and re.fullmatch(r"(GPT|gpt|GBT|Opus|opus)", merged[-1]["word"].strip()):
        merged[-1] = {**merged[-1], "word": merged[-1]["word"] + "-" + t, "end": w["end"]}
    else:
        merged.append(w)
words = [w for i, w in enumerate(merged)
         if not (re.fullmatch(r"\d,", w["word"].strip()) and i + 1 < len(merged) and re.fullmatch(r"\d+\.\d+[,.]?", merged[i + 1]["word"].strip()))]

def locate(phrase, last=False):
    toks = [norm(t) for t in phrase.split()]
    ws = [norm(w["word"]) for w in words]
    idx = [i for i in range(len(ws) - len(toks) + 1) if ws[i:i + len(toks)] == toks]
    if not idx:
        sys.exit(f"phrase not found: {phrase!r}")
    i = idx[-1] if last else idx[0]
    return i, i + len(toks) - 1
i0, _ = locate(FIRST); _, i1 = locate(LAST, last=True)
sel = words[i0:i1 + 1]
t_in, t_out = sel[0]["start"] - 0.15, sel[-1]["end"] + 0.35
dur = t_out - t_in

# 2. captions: groups of <= 4 words, karaoke fill as each word is spoken
def fix(t):
    for p, r in vocab:
        t = p.sub(r, t)
    return t
fmt = lambda t: f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"
ass = [f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: K,Shippori Mincho SemiBold,96,&H00121416,&H00909CA3,&H00EAF2F6,&H00EAF2F6,0,0,0,0,100,100,1,0,1,0,0,5,90,90,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"""]
srt, groups, cur = [], [], []
for w in sel:
    cur.append(w)
    if len(cur) == 4 or re.search(r"[.!?,]$", w["word"].strip()):
        groups.append(cur); cur = []
if cur:
    groups.append(cur)
sentence_start = True
for n, g in enumerate(groups, 1):
    if sentence_start:
        w0 = g[0]["word"].lstrip(); g[0]["word"] = w0[:1].upper() + w0[1:]
    sentence_start = bool(re.search(r"[.!?]$", g[-1]["word"].strip()))
    gs, ge = g[0]["start"] - t_in, g[-1]["end"] - t_in
    if n < len(groups):
        ge = max(ge, groups[n][0]["start"] - t_in - 0.02)
    parts, t = [], g[0]["start"]
    for w in g:
        txt = fix(w["word"].strip()).strip(",")
        if not txt:
            continue
        parts.append(f"{{\\kf{max(1, int((w['end'] - w['start']) * 100))}}}{txt} ")
    ass.append(f"Dialogue: 0,{fmt(gs)},{fmt(ge)},K,,0,0,0,,{{\\fad(60,40)}}{''.join(parts).strip()}")
    srt.append(f"{n}\n{fmt(gs).replace('.', ',')}0 --> {fmt(ge).replace('.', ',')}0\n{fix(' '.join(w['word'].strip() for w in g))}\n")
open(f"{OUT}/{SLUG}.ass", "w").write("\n".join(ass) + "\n")
open(f"{OUT}/{SLUG}.srt", "w").write("\n".join(srt))

# 3. background: logo, hook, footer
html = f"""<html><head><style>@font-face{{font-family:M;src:url(file://{FONTS}/ShipporiMincho-SemiBold.ttf)}}
@font-face{{font-family:Mm;src:url(file://{FONTS}/ShipporiMincho-Medium.ttf)}}
body{{margin:0;width:{W}px;height:{H}px;background:#f6f2ea;color:#161412;font-family:M,serif;position:relative;overflow:hidden}}</style></head><body>
<img src="file://{REPO}/public/millillion-black.svg" style="position:absolute;left:50%;transform:translateX(-50%);top:150px;width:360px">
<div style="position:absolute;top:420px;left:80px;right:80px;text-align:center;font-size:74px;line-height:1.15">{HOOK}</div>
<img src="file://{REPO}/public/brush-rule.svg" style="position:absolute;left:50%;transform:translateX(-50%);top:640px;width:300px;height:10px;opacity:.8">
<div style="position:absolute;bottom:230px;left:0;right:0;text-align:center;font-family:Mm;font-size:34px;letter-spacing:6px;color:#57524b">MILLILLION PODCAST · EP {int(NNN)}</div>
<div style="position:absolute;bottom:165px;left:0;right:0;text-align:center;font-family:Mm;font-size:34px;letter-spacing:6px;color:#57524b">MILLILLION.ORG</div>
<div style="position:absolute;bottom:110px;left:50%;margin-left:-9px;width:18px;height:18px;background:#b3341f;transform:rotate(45deg)"></div>
</body></html>"""
with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as fh:
    fh.write(html)
subprocess.run(["google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars", "--allow-file-access-from-files",
                "--virtual-time-budget=4000", f"--window-size={W},{H}", f"--screenshot={OUT}/{SLUG}-bg.png", f"file://{fh.name}"],
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)

# 4. render
fc = (f"[1:a]atrim={t_in}:{t_out},asetpts=PTS-STARTPTS,afade=t=in:d=0.12,afade=t=out:st={dur - 0.3}:d=0.3,asplit[a][aw];"
      f"[aw]showwaves=s=760x90:mode=cline:rate={FPS}:colors=0x161412@0.35:scale=sqrt,format=rgba[wave];"
      f"[0:v]format=rgba[bg];[bg][wave]overlay=(W-w)/2:1460[b];[b]ass={OUT}/{SLUG}.ass:fontsdir={FONTS},format=yuv420p[v]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-i", f"{OUT}/{SLUG}-bg.png", "-i", hq,
                "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", f"{dur:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                "-r", str(FPS), "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-movflags", "+faststart", f"{OUT}/{SLUG}.mp4"], check=True)
os.unlink(fh.name)
print(f"wrote {OUT}/{SLUG}.mp4 ({dur:.1f}s)")
