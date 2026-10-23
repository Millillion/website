import { getCollection } from "astro:content";
import { marked } from "marked";
import { PODCAST } from "../site.js";

const esc = (s = "") => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

// "1. Title" -> episode 1, "Title" (Apple wants the number in <itunes:episode>, not the title)
const split = (t) => { const m = t.match(/^(\d+)\.\s+(.*)$/); return m ? [Number(m[1]), m[2]] : [null, t]; };

// Show notes for apps: the episode page body up to the transcript, plus links.
const notes = (e, site) => {
  const body = (e.body || "").split(/^## Transcript/m)[0].trim();
  const page = new URL(`/podcast/${e.id}/`, site);
  const links = [
    e.data.blog && `<a href="${new URL(`/blog/${e.data.blog}/`, site)}">Read it as a blog post</a>`,
    `<a href="${page}">Full transcript</a>`,
    e.data.youtube && `<a href="https://www.youtube.com/watch?v=${e.data.youtube}">Watch on YouTube</a>`,
    `<a href="${new URL("/support/", site)}">Support Millillion</a>`,
  ].filter(Boolean).join(" · ");
  return `${marked.parse(body)}<p>${links}</p><p>Millillion: impossibly ambitious AI. <a href="${site}">millillion.org</a></p>`;
};

// Podcast RSS with the iTunes namespace (Apple Podcasts, Spotify, and everything that reads Apple's directory).
export async function GET(context) {
  const site = context.site;
  const eps = (await getCollection("podcast", (p) => !p.data.draft)).sort((a, b) => b.data.date - a.data.date);
  const items = eps.map((e) => { const [n, title] = split(e.data.title); return `
    <item>
      <title>${esc(title)}</title>
      <itunes:title>${esc(title)}</itunes:title>${n ? `
      <itunes:episode>${n}</itunes:episode>` : ""}
      <itunes:episodeType>full</itunes:episodeType>
      <description>${esc(e.data.description)}</description>
      <content:encoded><![CDATA[${notes(e, site)}]]></content:encoded>
      <link>${new URL(`/podcast/${e.id}/`, site)}</link>
      <guid isPermaLink="false">millillion-podcast-${esc(e.id)}</guid>
      <pubDate>${e.data.date.toUTCString()}</pubDate>
      <enclosure url="${esc(e.data.audio)}" length="${e.data.audioBytes}" type="audio/mpeg"/>
      <itunes:duration>${esc(e.data.duration)}</itunes:duration>
      <itunes:explicit>${PODCAST.explicit ? "true" : "false"}</itunes:explicit>
    </item>`; }).join("");
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>${esc(PODCAST.title)}</title>
    <link>${site}</link>
    <atom:link href="${new URL("/podcast.xml", site)}" rel="self" type="application/rss+xml"/>
    <language>en-us</language>
    <description>${esc(PODCAST.description)}</description>
    <itunes:author>${esc(PODCAST.author)}</itunes:author>
    <itunes:owner><itunes:name>${esc(PODCAST.author)}</itunes:name><itunes:email>${esc(PODCAST.ownerEmail)}</itunes:email></itunes:owner>
    <itunes:image href="${new URL(PODCAST.cover, site)}"/>
    <itunes:category text="${esc(PODCAST.category)}"/>
    <itunes:explicit>${PODCAST.explicit ? "true" : "false"}</itunes:explicit>
    <itunes:type>episodic</itunes:type>${items}
  </channel>
</rss>`;
  return new Response(xml, { headers: { "Content-Type": "application/rss+xml; charset=utf-8" } });
}
