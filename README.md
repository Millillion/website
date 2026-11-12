# millillion.org

The Millillion website: home, projects, blog, podcast, meetup and support. It's built with [Astro](https://astro.build) and deployed to Cloudflare Pages.

## Single source of truth
- **Home page** = the org profile README in [Millillion/.github](https://github.com/Millillion/.github/blob/main/profile/README.md).
- **Project pages** = the opening of each project's own README (everything before its first `##` section), fetched from GitHub at build time, with a link to the full README.

To change those pages, edit the README on GitHub; the site picks it up within the hour (see Staying in sync). Don't copy the text into this repo.

## Content
- Blog posts: `src/content/blog/<slug>.md` with frontmatter `title`, `date`, `description` (and optional `draft: true`).
- Podcast episodes: `src/content/podcast/<slug>.md` with `title`, `date`, `description`, `audio` (R2 URL), `audioBytes`, `duration` ("HH:MM:SS"), and optional `youtube` (video id) and `blog` (companion post slug). The body holds show notes and the transcript.

## Learn (AI-generated, per project)
- `/learn/` is its own section, next to Blog and Podcast. It covers every project with `learn` in `src/site.js`.
- **Streams.** `/learn/` is split into four streams, set by each page's `kind` (`STREAMS` in `src/lib/learn.js`). Each stream has its own page at `/learn/<stream>/` and its own feed at `/learn/<stream>/rss.xml`:
  - Tutorials: `overview` (pinned as "Start here") and `tutorial`;
  - Proofs: `proof-spotlight`;
  - Testing: `bug-caught` and `platform`;
  - Releases: `release`.
- `/learn/rss.xml` has everything. Each project also has a hub at `/learn/<project>/`. Page URLs are `/learn/<project>/<slug>/` whatever the stream.
- The content lives in the project's own repo. Its manifest (Lasm: `content/index.json`) lists the pages, and Claude writes and publishes them automatically.
- Every page says it is AI-generated.
- To preview a project's content from disk: `LEARN_LOCAL=/path/to/checkout npm run build`.

## Staying in sync
`sync-content.yml` runs hourly, except on a Sunday in US Eastern time (its crons skip Sunday, and its `sunday` job skips a late scheduled run that starts on Sunday). It pins, in `src/data/content-sync.json`, the latest commit of:
- each project's README;
- the org profile README;
- each project's Learn content.

A changed pin is a commit, and that commit redeploys the site, so edits on GitHub show here within the hour.

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
- Rebuild on pushes to this repo. README and content edits elsewhere arrive as `sync-content` commits.

## Meetup slides
The Greeneville AI Meetup slides are [Marp](https://marp.app/) Markdown in `meetup/slides.md`. Run `npm run slides` to rebuild `public/meetup/slides/` (HTML and PDF), then commit the output. They're served at millillion.org/meetup/slides/. In the browser, arrow keys move between slides, F goes full-screen and P opens presenter view with notes.

## AI skills (how episodes and posts are made)
- [`publish-episode`](.claude/skills/publish-episode/SKILL.md): a raw recording becomes a mastered episode, transcript, blog post, and is published.
- [`review-episode`](.claude/skills/review-episode/SKILL.md): automated checks, plus checking that the post says only what Jordan said.

Scripts live in `episodes-src/`. Each run appends to the skill's Lessons, so the process improves over time.
