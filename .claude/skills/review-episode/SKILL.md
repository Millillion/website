---
name: review-episode
description: Verify a Millillion podcast episode and its blog post before (and after) publishing — audio quality, feed validity, links, transcript, and that the blog post never says anything Jordan didn't. Use as step 12 of publish-episode, or whenever Jordan asks to check or review an episode or post.
---

# Review an episode

One rigorous pass, not repeated reviews. Automated checks cover the mechanical things; your judgment is only needed where words can drift from what Jordan said.

## 1. Automated checks (must all pass)
`episodes-src/check_episode.sh episodes-src/NNN/episode.mp3`. Run it once locally before pushing (feed checks may fail until deploy) and again after deploy. It checks:
- Loudness −17.5…−14.5 LUFS, true peak ≤ −1 dBFS.
- ID3 title, artist and album, plus embedded cover art.
- Feed XML parses; the enclosure `length` equals the file size; every feed URL returns 200; the audio supports byte ranges (Apple requires this).
- Episode, blog, podcast, home and RSS pages return 200.

If you find a failure the script doesn't catch, add a check to the script.

## 2. Listen to the edges (spot check)
Render the first 20 s and the 20 s around the end of speech. Confirm the intro dissolves under the voice, nothing is clipped at the start or end, and the reprise doesn't cover words. Use `ebur128` momentary loudness if you can't listen: the voice should sit around −16 to −20, and the music under it around −20 to −25.

## 3. Transcript
- Grep the transcript for anything `vocab.tsv` should have fixed, plus new proper nouns, product names and model names. Add the fixes to `vocab.tsv` and regenerate the transcript; never hand-edit it.
- Check that the timestamps are offset to the mastered episode (the voice enters at 11 s).

## 4. Blog post vs. transcript (the judgment step)
List every factual claim in the post: dates, numbers, names, products, events, opinions and quotes. For each one, find the supporting words in `episodes-src/NNN/raw.txt`.
- Unsupported or overstated: fix the post to match what he said. Example from episode 1: "going to buy" was corrected to his word "use", and "not scared" was softened to his "not necessarily scared".
- Hedges he used ("I believe", "maybe", "I think") stay hedged.
- Nothing invented: no stats, stories or opinions he didn't give.
- `adaptedFrom` is set, the byline renders "By Jordan Last, with AI", and there's no claim that he reviewed the post.
- Links resolve. The mark is written **ɛ∞ɜ** (U+025B U+221E U+025C) if it appears.

## 5. Done means
All automated checks pass after deploy, every blog claim traces to the transcript, and new lessons are appended to `publish-episode` → Lessons. Report in one or two lines; don't ask Jordan to review unless something genuinely needs his judgment.
