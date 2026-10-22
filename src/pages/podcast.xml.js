import { getCollection } from "astro:content";
import { PODCAST } from "../site.js";

const esc = (s = "") => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

// Podcast RSS with the iTunes namespace (Apple Podcasts, Spotify, and everything that reads Apple's directory).
export async function GET(context) {
  const site = context.site;
  const eps = (await getCollection("podcast", (p) => !p.data.draft)).sort((a, b) => b.data.date - a.data.date);
  const items = eps.map((e) => `
    <item>
      <title>${esc(e.data.title)}</title>
      <description>${esc(e.data.description)}</description>
      <link>${new URL(`/podcast/${e.id}/`, site)}</link>
      <guid isPermaLink="false">millillion-podcast-${esc(e.id)}</guid>
      <pubDate>${e.data.date.toUTCString()}</pubDate>
      <enclosure url="${esc(e.data.audio)}" length="${e.data.audioBytes}" type="audio/mpeg"/>
      <itunes:duration>${esc(e.data.duration)}</itunes:duration>
      <itunes:explicit>${PODCAST.explicit ? "true" : "false"}</itunes:explicit>
    </item>`).join("");
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:atom="http://www.w3.org/2005/Atom">
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
