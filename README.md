# millillion.org

The Millillion website: home, projects, blog, podcast, meetup and support. It's built with [Astro](https://astro.build) and deployed to Cloudflare Pages.

## Single source of truth
- **Home page** = the org profile README in [Millillion/.github](https://github.com/Millillion/.github/blob/main/profile/README.md).
- **Project pages** = each project's own README, fetched from GitHub at build time.

To change those pages, edit the README on GitHub and rebuild. Don't copy the text into this repo.

## Content
- Blog posts: `src/content/blog/<slug>.md` with frontmatter `title`, `date`, `description` (and optional `draft: true`).
- Podcast episodes: `src/content/podcast/<slug>.md` with `title`, `date`, `description`, `audio` (R2 URL), `audioBytes`, `duration` ("HH:MM:SS"), and optional `youtube` (video id) and `blog` (companion post slug). The body holds show notes and the transcript.

## Feeds
- `/rss.xml`: the blog feed.
- `/podcast.xml`: the podcast feed, the URL submitted to Apple Podcasts and Spotify.

## Develop
```bash
npm install
npm run dev
npm run build
```

## Deploy (Cloudflare Pages)
- Build command: `npm run build`
- Output directory: `dist`
- Rebuild on pushes to this repo. Add a deploy hook so README edits elsewhere also trigger a rebuild.
