"""Whisper JSON -> cleaned, timestamped Markdown transcript using vocab.tsv.

  python3 episodes-src/make_transcript.py episodes-src/NNN/raw.json episodes-src/NNN/transcript.md [voice_offset_seconds]
"""
import json, os, re, sys

src, dst = sys.argv[1], sys.argv[2]
offset = float(sys.argv[3]) if len(sys.argv) > 3 else 11.0  # where the voice starts in the mastered episode
vocab = []
for line in open(os.path.join(os.path.dirname(__file__), "vocab.tsv")):
    if line.strip() and not line.startswith("#"):
        pat, _, rep = line.rstrip("\n").partition("\t")
        vocab.append((re.compile(pat), rep))

paras, cur, start = [], [], None
for s in json.load(open(src))["segments"]:
    start = s["start"] if start is None else start
    cur.append(s["text"].strip())
    if (s["end"] - start > 45 and re.search(r"[.!?]$|\b(so|and)$", cur[-1])) or s["end"] - start > 70:
        paras.append((start, " ".join(cur))); cur, start = [], None
if cur:
    paras.append((start, " ".join(cur)))

out, prev_end = [], True
for st, txt in paras:
    for pat, rep in vocab:
        txt = pat.sub(rep, txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    if not prev_end:
        txt = "…" + txt[0].lower() + txt[1:]
    prev_end = bool(re.search(r"[.!?]$", txt))
    if not prev_end:
        txt += "…"
    m, sec = divmod(int(st + offset), 60)
    out.append(f"**[{m:02d}:{sec:02d}]** {txt}")
open(dst, "w").write("\n\n".join(out) + "\n")
print(f"wrote {dst}: {len(out)} paragraphs")
