---
name: make-videos
description: Make the YouTube videos for a Millillion podcast episode — vertical Shorts with karaoke captions (the main reach), the full faceless episode video, an optional illustrated "visual essay" chapter, the thumbnail and the YouTube text. Use after publish-episode has produced episodes-src/NNN/episode.mp3, or when Jordan asks for Shorts, clips or a video of an episode.
---

# Make the videos for an episode

Jordan loves the current format; keep it. Everything is ink on washi paper (`#f6f2ea` paper, `#161412` ink, `#57524b` soft ink, `#b3341f` shu red), Shippori Mincho type, the ɛ∞ɜ logo, no faces. Run from the `Millillion/website` repo root. Needs `episodes-src/NNN/episode.mp3` and `raw.json` (from publish-episode), ffmpeg with libass, headless `google-chrome`, Whisper, and the fonts in `~/.cache/millillion/fonts` (`episodes-src/setup_audio_tools.sh`).

Videos, PNGs and WAVs are gitignored. Commit the scripts and text (`shorts.tsv`, `.srt`/`.ass`, `youtube-description.txt`), never media.

## 1. Shorts (do these first; they grow the channel)
1. Read `episodes-src/NNN/transcript.md` and pick 3–5 self-contained moments of 20–60 s: the thesis line, a funny or relatable story, a sharable idea. Each must make sense with no context and end on a complete thought.
2. Add one row per Short to `episodes-src/NNN/shorts.tsv`, tab-separated: `slug`, `raw_start_s`, `raw_end_s`, `first words`, `last words`, `hook title`, `youtube description`, `tags`. See `episodes-src/001/shorts.tsv`.
   - Times are in the **raw** recording (as in `raw.json`), padded a few seconds either side. The script trims exactly to the first and last phrase.
   - The first and last words must appear verbatim in Whisper's word-level transcript of the clip. If the script says `phrase not found`, open `shorts/<slug>-wide.json` and copy the words from there.
   - Hook title: Jordan's own claim, short, first person where he said it that way ("I did my taxes with AI in 24 hours"). Never invent a claim.
   - Description: one or two sentences in **his words from that clip**, saying what the moment is about. Reuse his phrasing ("we as humans can sometimes fill in those gaps") rather than paraphrasing ("humans fill in the gaps"). Paraphrase is how hedges get lost.
   - Tags: 4–6 comma-separated phrases he actually said in the episode ("jagged intelligences", "tax return"), plus `Millillion, podcast`. No topics he didn't discuss, and no products he didn't name.
3. Render: `episodes-src/make_shorts.sh NNN` → `episodes-src/NNN/shorts/<slug>.mp4` (1080×1920, logo and hook at the top, word-by-word karaoke captions, ink waveform, "MILLILLION PODCAST · EP N" footer).
4. Check each one: grab frames (`ffmpeg -ss <t> -i x.mp4 -frames:v 1 f.png`) and read the `.srt`. Look for mishearings (fix them in `vocab.tsv`, never by hand), split numbers or model names, a cut mid-word, or a lowercase sentence start. Captions fade over 120 ms, so a frame grabbed mid-fade looks grey; that's expected.

## 2. Full episode video (the archive)
`python3 episodes-src/make_video.py NNN "N. Title" 11` → `video.mp4` (title card over the intro, captions on paper, ink waveform), `thumbnail.jpg` (1280×720) and `captions.srt` (uploaded to YouTube as subtitles). The `11` is the seconds of intro before the voice. On its own this format won't grow an audience; it's there for completeness and search.

## 3. Visual essay chapter (optional; the most engaging)
`episodes-src/make_visual_chapter.py` draws motion graphics with PIL, timed to word timestamps, so visuals land on the words that trigger them. It's currently written for episode 1's "Jagged intelligence" chapter (`python3 episodes-src/make_visual_chapter.py 001 1109 1197`). For a new episode, pick the one chapter with the most visual idea (a graph, a contrast, a list) and adapt the cues (`at("phrase")`) and drawing code. Keep it restrained: one idea, brush-like strokes, shu red only for emphasis, quotes in his exact words.

## 4. YouTube text
Write `episodes-src/NNN/youtube-description.txt` for the full video, following episode 1:
- A 1–2 sentence summary of what the episode is about.
- Chapters: the first at `00:00 Intro`, then `00:11` onward from the transcript times plus the 11 s intro offset (transcript times already include it). Use at least 3 chapters, each ≥ 10 s, in ascending order.
- Links: blog post, transcript page, Apple Podcasts, Spotify, the support page, these skills (`https://github.com/Millillion/website/tree/main/.claude/skills`), and the sign-off `Millillion: impossibly ambitious AI. https://millillion.org`.

Write the full video's tags to `episodes-src/NNN/youtube-tags.txt`: phrases and names he actually said (check with `grep -i`).

You don't assemble the Short text by hand: `check_text.py` builds the exact title, description and tags for every video into `episodes-src/NNN/youtube/<slug|full>.{title,description,tags}.txt`. Upload pastes from those files only. For reference, each Short's YouTube description is its `shorts.tsv` description followed by:
```
From episode N of the Millillion podcast, "<Episode Title>".
Full episode, transcript and blog post: https://millillion.org/podcast/NNN-<slug>/

Millillion: impossibly ambitious AI. https://millillion.org
```
Its title is the hook title plus ` #shorts`.

## 5. Check, then hand off
Run the `review-episode` skill. `python3 episodes-src/check_text.py NNN` must exit 0, and you must have read every row of `trace.md` before anything is uploaded. Then run the `upload-youtube` skill. Jordan has approved public publishing; don't hold videos for his review.

## Lessons (append; newest last)
- Whisper word timestamps split tokens ("GPT" "5" ".2", "y" "-axis"). The scripts glue pieces without a leading space onto the previous word and join model names to versions ("GPT-5.2"). False starts like "or 3, 5.3" are dropped.
- Cut the Short's audio from the 44.1 kHz mastered episode, not the 16 kHz Whisper copy, or it sounds dull.
- Capitalize the first word of each caption group that starts a sentence.
- Episode 1's first Short descriptions paraphrased Jordan and lost his hedges ("isn't equally capable everywhere" for "not necessarily the same level"), and the tags included topics he never discussed ("Claude Code", "AI hallucinations"). `check_text.py` now catches both.
- Captions on paper alone are too plain to grow a channel (Jordan agreed). Lead with Shorts and illustrated chapters.
- Episode 2: hooks of 3–4 lines collided with the fixed-position brush rule, and long 4-word caption groups ran off the frame edge. `make_short.py` now puts the rule under the hook and caps caption groups at about 20 characters.
- Whisper small on a short clip can silently drop a sentence or a hedge ("kind of easy" became "easy"). Diff each Short's `.srt` against `raw.json` for the same range; if words are missing, nudge the clip's padding by a second or two and re-render (the transcription changes with the window).
