---
name: upload-youtube
description: Upload a Millillion episode's Shorts and full video to the Millillion YouTube channel (@millillionai) through YouTube Studio in Chrome, with titles, descriptions, thumbnail, captions and Public visibility, then link the video from the site. Use after make-videos, or when Jordan asks to put videos on YouTube.
---

# Upload to YouTube

Channel: **Millillion** (@millillionai), id `UCsGdEXgpldl_V0gg0TJtJGw`. It's a Brand Account owned by Jordan's Google account and is already branded (banner, avatar, description, links) and phone-verified, so custom thumbnails work. Work in YouTube Studio through the Claude in Chrome tools. Jordan wants this done for him, and wants everything **Public**: never Unlisted or Private unless he asks.

## Limits (read first)
- Chrome's `file_upload` tool only takes files **≤ 10 MB** from inside the **session's working directory**. YouTube accepts much larger files; the limit is the tool's.
- Clicking "Select files" opens the operating system's file chooser, which you can't see or operate.
- The safety classifier blocks page scripts that build a large file in the page (for example from R2 pieces) and put it into YouTube's file input. Don't try to work around that.
- So: **Shorts (under 10 MB) you upload yourself. The full video needs Jordan to pick the file once** (about 10 seconds of his time); you do everything else. A future option is the YouTube Data API, but until Google audits the app it forces uploads to Private.

## 0. Stage the files
Copy the media into a gitignored folder inside the session's working directory, e.g. `<cwd>/.upload-staging/`: each `shorts/<slug>.mp4`, `thumbnail.jpg`, `captions.srt`, and the full video renamed `millillion-episode-NNN.mp4`. Make sure the folder is gitignored in that repo, and delete it once everything is published.

## 1. Each Short (you do all of it)
1. Open `https://studio.youtube.com/channel/UCsGdEXgpldl_V0gg0TJtJGw/videos/upload?d=ud`. Find the hidden file input (`find` "file input") and use `file_upload` with the Short's path.
2. **Details**: select all in the title (ctrl+a) and type `<hook title> #shorts`. Type the description from make-videos §4. Under Audience choose **"No, it's not made for kids"**.
3. Click Next through Video elements and Checks. Under **Visibility** choose **Public**, then **Publish**.
4. YouTube recognises a vertical video of 3 minutes or less as a Short. Shorts don't take custom thumbnails or chapters here; skip those.

## 2. Full episode (Jordan picks the file)
1. Open the upload dialog (URL above) and tell Jordan exactly: click **Select files**, go to `<cwd>/.upload-staging/`, choose `millillion-episode-NNN.mp4`, click Open, then say "done".
2. While it uploads, fill in **Details**:
   - Title: `<Episode Title> | Millillion Podcast Ep. N`.
   - Description: paste `episodes-src/NNN/youtube-description.txt`; the chapters come from it.
   - Thumbnail: `file_upload` with `thumbnail.jpg`.
   - Audience: "No, it's not made for kids".
3. **Video elements → Subtitles → Add → Upload file → With timing**: `file_upload` with `captions.srt`, language English.
4. **Visibility: Public → Publish.** Copy the video link.

## 3. After publishing
- Add the full video's YouTube id to the episode's frontmatter (`youtube:` in `src/content/podcast/NNN-*.md`) so the page embeds it. Build, commit and push.
- In Studio → Content, confirm every upload says **Public** and the checks have finished. Clear any copyright or audience flags.
- Delete `.upload-staging/` and any temporary R2 objects (`cf r2 buckets objects list --bucket-name millillion-podcast`). The bucket should hold only `episodes/*.mp3`.
- Report the links to Jordan in a few lines. Append anything new to Lessons below.

## Lessons (append; newest last)
- Episode 1: four Shorts uploaded directly via `file_upload`. The 175 MB full video hit the 10 MB tool limit, and the R2 split-and-rejoin page script was blocked by the safety classifier; Jordan picked the file himself.
- To change visibility from the Content list, open the visibility cell's dropdown arrow, choose Public, then Save. Clicking the label text alone sometimes does nothing.
- Don't upload as Unlisted "to check first". Jordan expects Public.
