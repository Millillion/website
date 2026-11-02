# millillion.org

The Millillion website: home, projects, blog, podcast, meetup and support. It's built with [Astro](https://astro.build) and deployed to Cloudflare Pages.

## Single source of truth
- **Home page** = the org profile README in [Millillion/.github](https://github.com/Millillion/.github/blob/main/profile/README.md).
- **Project pages** = each project's own README, fetched from GitHub at build time.

To change those pages, edit the README on GitHub and rebuild. Don't copy the text into this repo.

## Content
- Blog posts: `src/content/blog/<slug>.md` with frontmatter `title`, `date`, `description` (and optional `draft: true`).
- Podcast episodes: `src/content/podcast/<slug>.md` with `title`, `date`, `description`, `audio` (R2 URL), `audioBytes`, `duration` ("HH:MM:SS"), and optional `youtube` (video id) and `blog` (companion post slug). The body holds show notes and the transcript.

## Learn sections (AI-generated, per project)
- A project with `learn` in `src/site.js` gets `/projects/<slug>/learn/`: tutorials, bugs caught, proof spotlights, platforms and releases.
- The content lives in the project's own repo. Its manifest (Lasm: `content/index.json`) lists the pages, and Claude writes and publishes them automatically.
- Every page says it is AI-generated.
- `sync-content.yml` runs hourly. It pins each project's latest content commit in `src/data/content-sync.json`, and that commit redeploys the site.
- To preview a project's content from disk: `LEARN_LOCAL=/path/to/checkout npm run build`.

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

## AI skills (how episodes and posts are made)
- [`publish-episode`](.claude/skills/publish-episode/SKILL.md): a raw recording becomes a mastered episode, transcript, blog post, and is published.
- [`review-episode`](.claude/skills/review-episode/SKILL.md): automated checks, plus checking that the post says only what Jordan said.

Scripts live in `episodes-src/`. Each run appends to the skill's Lessons, so the process improves over time.
