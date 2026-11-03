import rss from "@astrojs/rss";
import { SITE } from "../site.js";
import { STREAMS, streamItems, learnUrl, kindLabel, AI_NOTE } from "./learn.js";

/** One Learn stream's feed, newest first. */
export async function streamRss(context, slug) {
  const stream = STREAMS.find((s) => s.slug === slug);
  const items = (await streamItems(stream)).sort((a, b) => String(b.page.date).localeCompare(String(a.page.date)));
  return rss({
    title: `${SITE.name}: Learn · ${stream.name}`,
    description: `${stream.blurb} ${AI_NOTE}`,
    site: context.site,
    items: items.map(({ project, page }) => ({
      title: page.title,
      pubDate: new Date(page.date),
      description: `${project.name} · ${kindLabel(page.kind)}. ${page.description ?? ""} (AI-generated)`,
      link: learnUrl(project, page),
    })),
  });
}
