import rss from "@astrojs/rss";
import { SITE } from "../../site.js";
import { allLearn, learnUrl, kindLabel, AI_NOTE } from "../../lib/learn.js";

export async function GET(context) {
  const items = await allLearn();
  return rss({
    title: `${SITE.name}: Learn`,
    description: `Tutorials, bugs our testing caught, proof spotlights and releases. ${AI_NOTE}`,
    site: context.site,
    items: items.map(({ project, page }) => ({
      title: page.title,
      pubDate: new Date(page.date),
      description: `${project.name} · ${kindLabel(page.kind)}. ${page.description ?? ""} (AI-generated)`,
      link: learnUrl(project, page),
    })),
  });
}
