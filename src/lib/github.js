import { marked } from "marked";
import pins from "../data/content-sync.json";

const cache = new Map();

// Fetch at the commit the sync-content workflow pinned (so a README edit is a
// commit here, which redeploys the site); links point at main for readers.
const pinned = (repo) => pins[repo]?.readme ?? "main";

async function readme(repo, path) {
  const key = `${repo}/${path}`;
  if (cache.has(key)) return cache.get(key);
  const res = await fetch(`https://raw.githubusercontent.com/${repo}/${pinned(repo)}/${path}`);
  const md = res.ok ? await res.text() : null;
  cache.set(key, md);
  return md;
}

/** Render README markdown with absolute links: relative files to github.com, `#section` to the README there. */
async function render(md, repo, path) {
  const raw = `https://raw.githubusercontent.com/${repo}/${pinned(repo)}/`;
  const blob = `https://github.com/${repo}/blob/main/`;
  const dir = path.includes("/") ? path.slice(0, path.lastIndexOf("/") + 1) : "";
  return (await marked.parse(md))
    .replace(/(src|srcset)="(?!https?:|#|\/\/|data:)([^"]+)"/g, (_, a, p) => `${a}="${raw}${dir}${p}"`)
    .replace(/href="#([^"]+)"/g, (_, anchor) => `href="${blob}${path}#${anchor}"`)
    .replace(/href="(?!https?:|#|\/\/|mailto:)([^"]+)"/g, (_, p) => `href="${blob}${dir}${p}"`);
}

/** A whole README, rendered. */
export async function readmeHtml(repo, path = "README.md") {
  const md = await readme(repo, path);
  return md === null ? null : render(md, repo, path);
}

/** A README's opening: everything before its first `## ` section, the project's hook. */
export async function readmeOpeningHtml(repo, path = "README.md") {
  const md = await readme(repo, path);
  if (md === null) return null;
  const cut = md.search(/^## /m);
  return render(cut < 0 ? md : md.slice(0, cut), repo, path);
}

export const readmeUrl = (repo) => `https://github.com/${repo}#readme`;
