---
name: review-episode
description: Proofread and fact-check a Millillion episode and everything written about it (episode page, show notes, blog post, YouTube titles, descriptions, chapters, tags, Short hooks, captions) before and after publishing. Covers spelling, faithfulness to what Jordan actually said, links, feed, audio and video. Use as step 12 of publish-episode, after make-videos, after upload-youtube, or whenever Jordan asks to check or review anything.
---

# Review an episode

The standard: a careful human editor who knows Jordan would find nothing to fix. No typos, no broken links. Above all, **nothing attributed to Jordan that he didn't say, and nothing he said made stronger, weaker or different.** Scripts catch the mechanical problems. You must read for meaning.

## 1. Run the checks (all must pass)
1. `python3 episodes-src/check_text.py NNN` covers:
   - spelling of every piece of text
   - numbers, names and quotes against the transcript
   - Short hooks and descriptions against their own clip
   - tags against topics he actually discussed
   - YouTube chapter rules and chapter-to-speech match
   - YouTube length and character limits
   - consistent titles and URLs, and the mark written ɛ∞ɜ
   - every link returning 200
   - media: durations, Short format, thumbnail, captions
   - a sentence-by-sentence trace
2. `episodes-src/check_episode.sh episodes-src/NNN/episode.mp3` covers the audio (loudness, peak, ID3, cover) and the feed (XML, enclosure size, byte ranges, page status codes).

Run both before pushing; feed checks may fail until the site deploys. Run them again after deploy and after the YouTube upload.

Fixing findings:
- **Spelling.** A real misspelling: fix the text. A Whisper mishearing in captions or the transcript: add a rule to `vocab.tsv` and regenerate, never hand-edit. A correct word aspell doesn't know (a name, a product, jargon he used): add it to `episodes-src/wordlist.txt`.
- **Fidelity.** Change our text to match what he said. Only if the finding is genuinely fine (for example a widely used term for something he plainly described) add it to `episodes-src/NNN/checked-ok.txt` with the reason. Never add a line just to get to zero.

## 2. Read the trace (the judgment step)
`check_text.py` writes `episodes-src/NNN/trace.md`. Every sentence we wrote is paired with the passage where Jordan said it. Read **every row**, not just the ✗ and ? rows. A ✓ means the words overlap, not that the meaning matches. For each sentence, ask:

- **Did he say this?** Same claim, same subject, same direction. If it isn't there, cut it.
- **Same strength?** Keep his hedges ("I believe", "I think", "maybe", "not necessarily", "at least as far as I know", "for now"). Don't add intensifiers he didn't use. Episode 1 drifted on all of these:
  - "constantly" for his "so much"
  - "24 straight hours" for his "24 hours, literally"
  - "every number was correct" for "make sure this thing was correct"
  - "isn't equally capable" for "not necessarily the same level"
- **Same cause and order?** Don't invent a "so" or "because" or reorder events. He said the tax return took 24 hours *because he waited until the last minute*, not *because he takes taxes seriously*.
- **Quotes** in quotation marks are his words verbatim. Cut filler ("um", "like", "you know") and nothing else.
- **Nothing dropped that changes the meaning.** If he qualified a claim ("I had a meticulous human review process"), the qualifier stays.
- **Numbers, dates and names** match exactly: "late 2024" isn't "December 2024", and "GPT-5.1" isn't "GPT-5".
- **No invented stats, stories, opinions or motives.** That includes in hooks: a hook is his claim compressed, not a new claim.
- **The post's structure** may tighten and reorder his ideas into sections. It may not add ideas.

## 3. Read like a human editor (every surface)
Read each of these start to finish as the audience would:
- the episode page
- the post
- the full YouTube description
- each Short's title and description
- the chapter list

Look for:
- **Typos and grammar**, including ones a spell checker misses (homophones, "it's/its", wrong word). Look for doubled words and stray spaces, and for punctuation and capitalization in titles: sentence case for Short titles, title case for episode titles.
- **Consistency:** the episode title is identical everywhere, as are the episode number, the name spellings (Millillion, lastmjs, Jordan Last) and the mark ɛ∞ɜ. The byline reads "By Jordan Last, with AI" with `adaptedFrom` set, and never claims he reviewed anything.
- **Chapters:** `check_text.py` prints each chapter title next to the words spoken there. Confirm each title describes what's actually being discussed from that moment, and starts at a sentence boundary rather than mid-sentence.
- **Shorts:**
  - Watch, or frame-grab, the start, middle and end of each one.
  - The first and last words are complete, with no cut syllables.
  - Captions match the audio word for word, and names and numbers are written correctly ("GPT-5.2", not "GPT 5 .2").
  - Nothing is cropped off the 1080×1920 frame, and the hook text fits and is readable.
- **Thumbnail:** readable at small size, with the title spelled correctly.
- **Links:** open every link in the descriptions, show notes and post. Confirm it goes to the right place, not just that it returns 200 (the right episode, the right post).

## 4. After publishing
- **Site and feed:** rerun both scripts against the live site.
- **Apple and Spotify:** the episode appears with the right title and number.
- **YouTube:** follow upload-youtube §3 (readback verify).
  - The live title, description and tags must match `episodes-src/NNN/youtube/*.txt` character for character.
  - Every video is Public, with no notices or restrictions and checks complete.
  - Chapters show on the player, captions are listed, and the custom thumbnail is shown.
  - Each Short plays as a Short at youtube.com/shorts/<id>.

## 5. Done means
- Both scripts exit 0 after deploy.
- Every trace row has been read and every sentence traces to his words.
- The live YouTube readback says OK for every video.
- New lessons are appended to the relevant skill.

Report to Jordan in a few lines, and list anything you changed in his words' favour. Don't ask him to review unless something genuinely needs his judgment.
