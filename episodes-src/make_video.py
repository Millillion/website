"""Faceless YouTube video for an episode: title card over the intro, then large captions
synced to the transcript on washi paper, with a thin ink waveform. Also renders a thumbnail.

  python3 episodes-src/make_video.py NNN "Episode title" [voice_offset_seconds]

Writes episodes-src/NNN/video.mp4, thumbnail.jpg, captions.ass (and captions.srt for YouTube upload).
Needs: ffmpeg (libass), google-chrome (headless), Shippori Mincho in ~/.cache/millillion/fonts.
"""
import json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
NNN, TITLE = sys.argv[1], sys.argv[2]
OFFSET = float(sys.argv[3]) if len(sys.argv) > 3 else 11.0
D = os.path.join(HERE, NNN)
FONTS = os.path.expanduser("~/.cache/millillion/fonts")
W, H, FPS = 1920, 1080, 24
PAPER, INK, SOFT = "#f6f2ea", "#161412", "#57524b"

vocab = []
for line in open(os.path.join(HERE, "vocab.tsv")):
    if line.strip() and not line.startswith("#"):
        p, _, r = line.rstrip("\n").partition("\t")
        vocab.append((re.compile(p), r))


def fix(t):
    for p, r in vocab:
        t = p.sub(r, t)
    return re.sub(r"\s+", " ", t).strip()


def chrome(html, out, w, h):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as fh:
        fh.write(html)
    subprocess.run(["google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                    "--allow-file-access-from-files", "--virtual-time-budget=4000", f"--window-size={w},{h}",
                    f"--screenshot={out}", f"file://{fh.name}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    os.unlink(fh.name)


FACE = f"""<style>@font-face{{font-family:M;src:url(file://{FONTS}/ShipporiMincho-SemiBold.ttf)}}
@font-face{{font-family:Mm;src:url(file://{FONTS}/ShipporiMincho-Medium.ttf)}}
body{{margin:0;background:{PAPER};color:{INK};font-family:M,serif;overflow:hidden}}</style>"""
LOGO = f"file://{REPO}/public/millillion-black.svg"
RULE = f"file://{REPO}/public/brush-rule.svg"
ep_no = TITLE.split(".")[0] if TITLE[0].isdigit() else ""
ep_title = TITLE.split(". ", 1)[-1]


def frames():
    title = f"""<html><head>{FACE}</head><body style="width:{W}px;height:{H}px;display:flex;flex-direction:column;align-items:center;justify-content:center">
<img src="{LOGO}" style="width:760px"><div style="font-size:34px;letter-spacing:14px;margin-top:70px;color:{SOFT}">MILLILLION · EPISODE {ep_no}</div>
<div style="font-size:78px;margin-top:26px;letter-spacing:2px">{ep_title}</div>
<img src="{RULE}" style="width:420px;height:12px;margin-top:46px;opacity:.85"></body></html>"""
    bg = f"""<html><head>{FACE}</head><body style="width:{W}px;height:{H}px;position:relative">
<img src="{LOGO}" style="position:absolute;left:80px;top:64px;width:170px">
<div style="position:absolute;right:84px;top:82px;font-family:Mm;font-size:26px;letter-spacing:6px;color:{SOFT}">EPISODE {ep_no} · {ep_title.upper()}</div>
<div style="position:absolute;left:80px;bottom:70px;font-family:Mm;font-size:24px;letter-spacing:5px;color:{SOFT}">MILLILLION.ORG</div>
<div style="position:absolute;right:84px;bottom:66px;width:16px;height:16px;background:#b3341f;transform:rotate(45deg)"></div>
</body></html>"""
    thumb = f"""<html><head>{FACE}</head><body style="width:1280px;height:720px;display:flex;flex-direction:column;align-items:center;justify-content:center">
<img src="{LOGO}" style="width:430px"><div style="font-size:84px;line-height:1.08;text-align:center;margin-top:46px;max-width:1100px">{ep_title}</div>
<div style="font-size:26px;letter-spacing:10px;margin-top:30px;color:{SOFT}">MILLILLION PODCAST · EP {ep_no}</div></body></html>"""
    chrome(title, f"{D}/v-title.png", W, H)
    chrome(bg, f"{D}/v-bg.png", W, H)
    chrome(thumb, f"{D}/thumbnail.png", 1280, 720)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{D}/thumbnail.png", "-q:v", "3", f"{D}/thumbnail.jpg"], check=True)


def ts(t, ass=True):
    h, r = divmod(max(t, 0), 3600); m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}" if ass else f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int((s % 1) * 1000):03d}"


def captions():
    """Segment-level captions, split so each card holds <= ~14 words on <= 2 lines."""
    cards = []
    for s in json.load(open(f"{D}/raw.json"))["segments"]:
        words = fix(s["text"]).split()
        if not words:
            continue
        n = max(1, -(-len(words) // 14))
        per = -(-len(words) // n)
        dur = (s["end"] - s["start"]) / n
        for k in range(n):
            chunk = words[k * per:(k + 1) * per]
            if chunk:
                cards.append((s["start"] + OFFSET + k * dur, s["start"] + OFFSET + (k + 1) * dur, " ".join(chunk)))
    def wrap(t):
        if len(t) <= 34:
            return t
        mid = len(t) // 2
        cut = min((i for i, c in enumerate(t) if c == " "), key=lambda i: abs(i - mid))
        return t[:cut] + r"\N" + t[cut + 1:]
    ass = [f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Shippori Mincho SemiBold,70,&H00121416,&H00121416,&H00EAF2F6,&H00EAF2F6,0,0,0,0,100,100,1,0,1,0,0,5,220,220,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"""]
    srt = []
    for i, (a, b, t) in enumerate(cards, 1):
        ass.append(f"Dialogue: 0,{ts(a)},{ts(b)},Cap,,0,0,0,,{{\\fad(120,120)}}{wrap(t)}")
        srt.append(f"{i}\n{ts(a, False)} --> {ts(b, False)}\n{t}\n")
    open(f"{D}/captions.ass", "w").write("\n".join(ass) + "\n")
    open(f"{D}/captions.srt", "w").write("\n".join(srt))
    return len(cards)


def render():
    fc = (f"[0:v]format=rgba[bg];[1:v]format=rgba,fade=t=out:st={OFFSET - 1.2}:d=1.4:alpha=1[title];"
          f"[2:a]showwaves=s=900x70:mode=cline:rate={FPS}:colors=0x161412@0.35:scale=sqrt,format=rgba[wave];"
          f"[bg][wave]overlay=(W-w)/2:H-200:enable='gte(t,{OFFSET})'[b1];[b1][title]overlay=0:0[b2];"
          f"[b2]ass={D}/captions.ass:fontsdir={FONTS},format=yuv420p[v]")
    subprocess.run(["ffmpeg", "-v", "error", "-stats", "-y",
                    "-loop", "1", "-framerate", str(FPS), "-i", f"{D}/v-bg.png",
                    "-loop", "1", "-framerate", str(FPS), "-i", f"{D}/v-title.png",
                    "-i", f"{D}/episode.mp3", "-filter_complex", fc, "-map", "[v]", "-map", "2:a",
                    "-c:v", "libx264", "-preset", "medium", "-tune", "stillimage", "-crf", "20", "-r", str(FPS),
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", f"{D}/video.mp4"], check=True)


if __name__ == "__main__":
    frames()
    print("captions:", captions())
    if "--frames-only" not in sys.argv:
        render()
        print("wrote", f"{D}/video.mp4")
