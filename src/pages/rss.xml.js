import rss from "@astrojs/rss";
import { getCollection } from "astro:content";
import { SITE } from "../site.js";

export async function GET(context) {
  const posts = (await getCollection("blog", (p) => !p.data.draft)).sort((a, b) => b.data.date - a.data.date);
  return rss({
    title: `${SITE.name} blog`,
    description: SITE.description,
    site: context.site,
    items: posts.map((p) => ({ title: p.data.title, pubDate: p.data.date, description: p.data.description, link: `/blog/${p.id}/` })),
  });
}
