"""Proofread and fact-check everything written about an episode before (and after) it's published.

  python3 episodes-src/check_text.py NNN [--live DIR] [--no-links]

Checks, against Jordan's actual words (raw.json with vocab.tsv fixes applied):
  spelling   aspell over every title, description, show note, post, hook, tag and caption
  fidelity   numbers, names and quotes must appear in what he said; Short hooks/descriptions
             must use words from that clip; tags must be topics he talked about
  chapters   YouTube rules (00:00 first, >= 3, ascending, >= 10 s apart, inside the video)
             and each title must match what's being said at that time
  format     YouTube limits (title <= 100, description <= 5000, no < >, tags <= 500),
             consistent episode title/number/URLs everywhere, the mark written ɛ∞ɜ
  links      every URL returns 200
  media      video length = audio length, Shorts vertical and <= 3 min, thumbnail size, captions in range
  --live DIR compares what YouTube Studio actually shows (DIR/<slug|full>.title / .description / .tags)
             with the expected text, character for character

Also writes the exact expected YouTube text to episodes-src/NNN/youtube/ (paste from these files).
A finding that is genuinely fine goes in episodes-src/NNN/checked-ok.txt (one per line, with the reason
after a TAB); never add a line just to silence a real problem. Exits 1 if anything is unresolved.
"""
import glob, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
NNN = sys.argv[1]; N = int(NNN); D = os.path.join(HERE, NNN)
LIVE = sys.argv[sys.argv.index("--live") + 1] if "--live" in sys.argv else None
LINKS = "--no-links" not in sys.argv
OFFSET = 11.0
FAILS, NOTES = [], []
OK = {}
if os.path.exists(f"{D}/checked-ok.txt"):
    for line in open(f"{D}/checked-ok.txt"):
        if line.strip() and not line.startswith("#"):
            k, _, why = line.rstrip("\n").partition("\t"); OK[k.strip()] = why

def fail(kind, msg):
    key = f"{kind}: {msg}"
    (NOTES if key in OK else FAILS).append(key + (f"   [ok: {OK[key]}]" if key in OK else ""))

# ---------- Jordan's words ----------
vocab = []
for line in open(f"{HERE}/vocab.tsv"):
    if line.strip() and not line.startswith("#"):
        p, _, r = line.rstrip("\n").partition("\t"); vocab.append((re.compile(p, re.I), r))
def fix(t):
    for p, r in vocab:
        t = p.sub(r, t)
    return t
SEGS = [(s["start"] + OFFSET, s["end"] + OFFSET, fix(s["text"]).strip()) for s in json.load(open(f"{D}/raw.json"))["segments"]]
SAID = " ".join(t for _, _, t in SEGS)
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"\.(?!\d)|[^a-z0-9.%$' ]", " ", s.lower().replace("’", "'").replace("-", " "))).strip()
SAIDN = f" {norm(SAID)} "
said = lambda phrase: f" {norm(phrase)} " in SAIDN
STOP = set("""a an the and or but if of to in on at by for with from as is are was were be been being it its it's this that these
those i i'm i've me my we we're our you your he she they them their there here what which who how why when where so than then too very
just not no do does did done can could would should will now all any some more most much many one two also into out up down over about
like get got go going make made way thing things really still for now every everyone everything each episode millillion podcast""".split())
words = lambda s: [w for w in re.findall(r"[a-z0-9][a-z0-9'.%-]*[a-z0-9%]|[a-z0-9]", s.lower().replace("’", "'"))]
content = lambda s: [w for w in words(s) if w not in STOP and not w.isdigit() and len(w) > 2]
def said_word(w, text=SAIDN):
    w = norm(re.sub(r"'s$", "", w.strip(".,'")))
    if " " in w:  # "gpt-3" -> "gpt 3"
        return f" {w} " in text
    stems = {w, w.rstrip("s"), re.sub(r"(ing|ed|es|ly)$", "", w), re.sub(r"(ies)$", "y", w), re.sub(r"n't$", "", w)}
    return any(re.search(rf"\b{re.escape(x)}", text) for x in stems if len(x) >= 2)

# ---------- what we wrote ----------
def front(path):
    s = open(path).read(); m = re.match(r"---\n(.*?)\n---\n(.*)", s, re.S)
    fm = {k: v.strip().strip('"') for k, v in re.findall(r"^(\w+):\s*(.*)$", m.group(1), re.M)}
    return fm, m.group(2)
ep_path = glob.glob(f"{REPO}/src/content/podcast/{NNN}-*.md")[0]
EP_SLUG = os.path.basename(ep_path)[:-3]
ep, ep_body = front(ep_path)
EP_TITLE = re.sub(r"^\d+\.\s*", "", ep["title"])
notes_md = ep_body.split("## Transcript")[0]
post_path = f"{REPO}/src/content/blog/{ep.get('blog')}.md"
post, post_body = front(post_path) if os.path.exists(post_path) else ({}, "")
EP_URL = f"https://millillion.org/podcast/{EP_SLUG}/"

shorts = []
if os.path.exists(f"{D}/shorts.tsv"):
    for line in open(f"{D}/shorts.tsv"):
        if line.strip() and not line.startswith("#"):
            c = line.rstrip("\n").split("\t") + [""] * 8
            shorts.append(dict(slug=c[0], hook=c[5], desc=c[6], tags=c[7]))
full_desc = open(f"{D}/youtube-description.txt").read().strip()
full_tags = open(f"{D}/youtube-tags.txt").read().strip() if os.path.exists(f"{D}/youtube-tags.txt") else ""

# expected YouTube text (the only source to paste from)
EXPECT = {"full": dict(title=f"{EP_TITLE} | Millillion Podcast Ep. {N}", description=full_desc, tags=full_tags)}
for s in shorts:
    EXPECT[s["slug"]] = dict(title=f"{s['hook']} #shorts", tags=s["tags"], description=
        f"{s['desc']}\n\nFrom episode {N} of the Millillion podcast, \"{EP_TITLE}\".\nFull episode, transcript and blog post: {EP_URL}\n\n"
        f"Millillion: impossibly ambitious AI. https://millillion.org")
os.makedirs(f"{D}/youtube", exist_ok=True)
for k, v in EXPECT.items():
    for f, t in v.items():
        open(f"{D}/youtube/{k}.{f}.txt", "w").write(t + "\n")

def strip_md(s):
    s = re.sub(r"```.*?```", " ", s, flags=re.S); s = re.sub(r"`[^`]*`", " ", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s); s = re.sub(r"https?://\S+", " ", s)
    return re.sub(r"[*#>]|(?<!\w)_|_(?!\w)", "", s)
WRITTEN = {  # name -> prose that must be true to what he said
    "episode title": EP_TITLE, "episode description": ep.get("description", ""), "show notes": strip_md(notes_md),
    "post title": post.get("title", ""), "post description": post.get("description", ""),
    "post": strip_md(re.sub(r"^#+ .*$", "", post_body, flags=re.M)),  # headings are labels, not claims
    "full video description": full_desc.split("\n\n")[0],  # the summary; chapters and links are checked separately
}
SUMMARIES = {"episode description", "show notes", "post description", "full video description", "episode title", "post title"}
for s in shorts:
    WRITTEN[f"short {s['slug']} hook"] = s["hook"]; WRITTEN[f"short {s['slug']} description"] = s["desc"]

# ---------- 1. spelling ----------
WORDLIST = f"{HERE}/wordlist.txt"
def misspelled(text):
    out = subprocess.run(["aspell", "list", "--lang=en_US", "--mode=none", "--ignore-case", f"--personal={WORDLIST}"],
                         input=text, capture_output=True, text=True).stdout.split()
    return sorted(set(out))
SPELL = dict(WRITTEN)
SPELL.update({f"tags {k}": v["tags"] for k, v in EXPECT.items()})
for srt in sorted(glob.glob(f"{D}/shorts/*.srt")) + [f"{D}/captions.srt"]:
    SPELL[f"captions {os.path.relpath(srt, D)}"] = re.sub(r"^\d+\n[\d:, >-]+\n", "", open(srt).read(), flags=re.M)
for name, text in SPELL.items():
    for w in misspelled(text):
        fail("spelling", f"{name}: '{w}'")

# ---------- 2. fidelity ----------
ALLOW_NAMES = set("""Millillion Jordan Last lastmjs Apple Podcasts Spotify YouTube GitHub Patreon Support Full Read Listen Watch
How From Episode Intro Wrap-up AI I I'm I've""".split())
for name, text in WRITTEN.items():
    t = re.sub(r"\b\d{1,2}:\d{2}(:\d{2})?\b", " ", text)          # chapter timestamps
    t = re.sub(r"\b(episode|ep\.?)\s+\d+\b", " ", t, flags=re.I)  # "episode 1"
    for num in set(x.rstrip(".,") for x in re.findall(r"(?<![\w.])\$?\d[\d,]*(?:\.\d+)?%?", t)):
        if not said(num.rstrip(".,")) and not said(num.replace(",", "")):
            fail("fidelity", f"{name}: number '{num}' is not in the transcript")
    for sent in re.split(r"(?<=[.!?:])\s+|\n+", t):
        toks = re.findall(r"[A-Za-z][\w'.-]*", sent)
        for w in toks[1:]:
            w = w.strip(".'")
            if w[:1].isupper() and w not in ALLOW_NAMES and not said_word(w.lower()):
                fail("fidelity", f"{name}: name/term '{w}' is not in the transcript")
    for q in re.findall(r"[“\"]([^”\"]{12,})[”\"]", t):
        if not said(q) and norm(q) != norm(EP_TITLE):
            fail("fidelity", f"{name}: quote not said verbatim: \"{q[:70]}\"")
# Shorts: hook and description must come from that clip
for s in shorts:
    srt = f"{D}/shorts/{s['slug']}.srt"
    if not os.path.exists(srt):
        fail("media", f"missing {srt}"); continue
    clip = f" {norm(open(srt).read())} "
    for part in ("hook", "desc"):
        miss = sorted(set(w for w in content(s[part]) if not said_word(w, clip)))
        never = [w for w in miss if not said_word(w)]
        if never:  # paraphrase: make sure it means what he said in the clip
            fail("fidelity", f"short {s['slug']} {part}: words he never said: {', '.join(never)}")
        if set(miss) - set(never):
            NOTES.append(f"fidelity: short {s['slug']} {part}: said elsewhere in the episode, not in this clip: {', '.join(sorted(set(miss) - set(never)))}")
# tags: topics he actually talked about
for k, v in EXPECT.items():
    for tag in [x.strip() for x in v["tags"].split(",") if x.strip()]:
        if tag.lower() in ("millillion", "podcast"):
            continue
        miss = [w for w in words(tag) if w not in STOP and not said_word(w)]
        if miss or not said(tag):
            fail("fidelity", f"tags {k}: '{tag}' was not said" + (f" (missing: {', '.join(miss)})" if miss else " as a phrase"))

# ---------- 3. chapters ----------
dur = lambda p: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                     capture_output=True, text=True).stdout or 0)
AUDIO = dur(f"{D}/episode.mp3")
chap = [(int(m[0]) * 60 + int(m[1]), m[2]) for m in re.findall(r"^(\d{1,2}):(\d{2}) (.+)$", full_desc, re.M)]
if not chap or chap[0][0] != 0: fail("chapters", "first chapter must be 00:00")
if len(chap) < 3: fail("chapters", "YouTube needs at least 3 chapters")
for (a, ta), (b, tb) in zip(chap, chap[1:]):
    if b - a < 10: fail("chapters", f"'{tb}' starts {b - a}s after '{ta}' (needs >= 10 s)")
if chap and chap[-1][0] > AUDIO - 10: fail("chapters", f"last chapter '{chap[-1][1]}' starts after the end")
print("Chapter check (title -> what's said there):")
for i, (t, title) in enumerate(chap):
    end = chap[i + 1][0] if i + 1 < len(chap) else AUDIO
    window = " ".join(x for a, b, x in SEGS if b > t - 5 and a < min(end, t + 90))
    first = next((x for a, b, x in SEGS if b > t), "")
    print(f"  {t // 60:02d}:{t % 60:02d} {title:<45} | {first[:90]}")
    kw = content(title)
    if t > 0 and title.lower() not in ("wrap-up", "outro") and kw and not any(said_word(w, f" {norm(window)} ") for w in kw):
        fail("chapters", f"'{title}' at {t // 60:02d}:{t % 60:02d}: none of its words are said in that stretch")
    if t > 0 and not any(abs(a - t) < 3 for a, _, _ in SEGS):
        NOTES.append(f"chapters: '{title}' at {t // 60:02d}:{t % 60:02d} isn't at a sentence start (nearest segment starts elsewhere)")

# ---------- 4. format and consistency ----------
for k, v in EXPECT.items():
    if len(v["title"]) > 100: fail("format", f"{k} title is {len(v['title'])} chars (max 100)")
    if len(v["description"]) > 5000: fail("format", f"{k} description is {len(v['description'])} chars (max 5000)")
    for f in ("title", "description", "tags"):
        if re.search(r"[<>]", v[f]): fail("format", f"{k} {f} contains < or > (YouTube rejects them)")
    if len(v["tags"]) > 500: fail("format", f"{k} tags are {len(v['tags'])} chars (max 500)")
    if not v["tags"]: fail("format", f"{k} has no tags")
    if re.search(r"\s{2,}\S|[ \t]$", v["title"]) or v["title"] != v["title"].strip(): fail("format", f"{k} title has stray spaces")
for s in shorts:
    if not s["hook"] or not s["desc"]: fail("format", f"short {s['slug']} is missing its hook or description")
if f"/podcast/{EP_SLUG}/" not in full_desc: fail("format", "full description doesn't link this episode's page")
if ep.get("blog") and f"/blog/{ep['blog']}/" not in full_desc: fail("format", "full description doesn't link the blog post")
if post and norm(post.get("title", "")) != norm(EP_TITLE): NOTES.append(f"format: post title '{post.get('title')}' differs from episode title '{EP_TITLE}'")
ALL = "\n".join([full_desc, notes_md, post_body, ep.get("description", "")] + [v["description"] for v in EXPECT.values()])
if re.search(r"ɛ∞3|ε∞ɜ|ε∞з|e∞ɜ", ALL): fail("format", "the mark must be written ɛ∞ɜ (U+025B U+221E U+025C)")
for name, text in WRITTEN.items():
    if re.search(r"\b(\w+) \1\b", text, re.I) and not re.search(r"\b(very very|had had|that that)\b", text, re.I):
        fail("format", f"{name}: doubled word '{re.search(r'\b(\w+) \1\b', text, re.I).group(0)}'")
    if re.search(r" [,.;:!?]|\.\.(?!\.)|,,|\( | \)", text): fail("format", f"{name}: stray punctuation spacing")

# ---------- 5. links ----------
if LINKS:
    urls = set(re.findall(r"https?://[^\s)\"'<>\]]+", ALL + "\n" + open(ep_path).read()))
    for u in sorted(urls):
        u = u.rstrip(".,;")
        c = subprocess.run(["curl", "-s", "-o", "/dev/null", "-L", "-A", "Mozilla/5.0 (X11; Linux x86_64) Chrome/130", "-w", "%{http_code}", u],
                           capture_output=True, text=True).stdout
        if c != "200" and "github.com/" in u:  # GitHub rate-limits curl; ask the API
            m = re.match(r"https://github.com/([^/]+/[^/]+)(?:/(?:tree|blob)/[^/]+/(.*))?", u)
            if m and subprocess.run(["gh", "api", f"repos/{m[1]}/contents/{m[2] or ''}".rstrip("/")], capture_output=True).returncode == 0:
                c = "200"
        if c != "200": fail("links", f"{c} {u}")
        if "github.com/sponsors/" in u:
            page = subprocess.run(["curl", "-sL", "-A", "Mozilla/5.0 Chrome/130", u], capture_output=True, text=True).stdout
            if "sponsors" not in (re.search(r"<title>([^<]*)", page) or ["", ""])[1].lower():
                fail("links", f"{u} redirects to a profile: GitHub Sponsors isn't live yet")

# ---------- 6. media ----------
probe = lambda p: json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", p],
                                            capture_output=True, text=True).stdout or "{}")
if os.path.exists(f"{D}/video.mp4"):
    if abs(dur(f"{D}/video.mp4") - AUDIO) > 1.5: fail("media", f"video.mp4 is {dur(f'{D}/video.mp4'):.1f}s but episode.mp3 is {AUDIO:.1f}s")
else:
    NOTES.append("media: no video.mp4 yet")
for s in shorts:
    p = f"{D}/shorts/{s['slug']}.mp4"
    if not os.path.exists(p): fail("media", f"missing {p}"); continue
    info = probe(p); v = [x for x in info["streams"] if x["codec_type"] == "video"][0]
    if (v["width"], v["height"]) != (1080, 1920): fail("media", f"{s['slug']} is {v['width']}x{v['height']} (want 1080x1920)")
    if float(info["format"]["duration"]) > 180: fail("media", f"{s['slug']} is over 3 minutes, so it won't be a Short")
    if not any(x["codec_type"] == "audio" for x in info["streams"]): fail("media", f"{s['slug']} has no audio")
    if os.path.getsize(p) > 10 * 1024 * 1024: NOTES.append(f"media: {s['slug']}.mp4 is over 10 MB; Jordan will need to pick it in the file chooser")
th = f"{D}/thumbnail.jpg"
if os.path.exists(th):
    from PIL import Image
    if Image.open(th).size != (1280, 720): fail("media", f"thumbnail is {Image.open(th).size} (want 1280x720)")
    if os.path.getsize(th) > 2 * 1024 * 1024: fail("media", "thumbnail is over 2 MB")
cues = re.findall(r"(\d\d):(\d\d):(\d\d),(\d+) --> (\d\d):(\d\d):(\d\d),(\d+)", open(f"{D}/captions.srt").read())
ts = [(int(a) * 3600 + int(b) * 60 + int(c) + int(d) / 1000, int(e) * 3600 + int(f) * 60 + int(g) + int(h) / 1000) for a, b, c, d, e, f, g, h in cues]
if any(b < a for a, b in ts) or any(b[0] < a[0] for a, b in zip(ts, ts[1:])): fail("media", "captions.srt cues are out of order")
if ts and ts[-1][1] > AUDIO + 0.5: fail("media", "captions.srt runs past the end of the episode")

# ---------- 7. live readback ----------
if LIVE:
    for k, v in EXPECT.items():
        for f in ("title", "description", "tags"):
            p = f"{LIVE}/{k}.{f}.txt"
            if not os.path.exists(p):
                fail("live", f"no readback for {k} {f} ({p})"); continue
            got = open(p).read().strip()
            want = v[f].strip()
            if f == "tags":
                got, want = sorted(x.strip().lower() for x in got.replace("\n", ",").split(",") if x.strip()), sorted(x.strip().lower() for x in want.split(",") if x.strip())
            if got != want:
                fail("live", f"{k} {f} on YouTube differs from episodes-src/{NNN}/youtube/{k}.{f}.txt")

# ---------- 8. trace: every sentence we wrote, next to where he said it ----------
# Writes episodes-src/NNN/trace.md. A reviewer reads it line by line; weakly supported sentences fail.
WIN = [(SEGS[i][0], " ".join(x for _, _, x in SEGS[i:i + 4])) for i in range(len(SEGS))]
WINSETS = [set(content(w)) for _, w in WIN]
trace = [f"# Trace for episode {N}\n\nEach sentence we wrote, the passage where Jordan said it, and how much of it he said "
         "(share of its content words found there). Read every row: wording may differ, meaning may not.\n"]
for name, text in WRITTEN.items():
    trace.append(f"\n## {name}\n")
    for sent in re.split(r"(?<=[.!?])\s+|\n+", text):
        cw = set(content(sent))
        if len(cw) < 3:
            continue
        best = max(range(len(WIN)), key=lambda i: len(cw & WINSETS[i]))
        score = len(cw & WINSETS[best]) / len(cw)
        t = WIN[best][0]
        if name in SUMMARIES:  # summaries span the episode: every content word must be his, somewhere
            score = sum(said_word(w) for w in cw) / len(cw)
        flag = "✗" if score < 0.35 else "?" if score < 0.6 else "✓"
        trace.append(f"- {flag} {score:.0%} **{sent.strip()}**\n  - [{int(t) // 60:02d}:{int(t) % 60:02d}] {WIN[best][1][:400]}")
        if score < 0.35:
            fail("trace", f"{name}: weakly supported: \"{sent.strip()[:90]}\" (see trace.md)")
open(f"{D}/trace.md", "w").write("\n".join(trace) + "\n")

# ---------- report ----------
for n in NOTES: print("  · " + n)
for f in FAILS: print("  ✗ " + f)
print(f"\n{len(FAILS)} problem(s), {len(NOTES)} note(s). Expected YouTube text: episodes-src/{NNN}/youtube/")
sys.exit(1 if FAILS else 0)
