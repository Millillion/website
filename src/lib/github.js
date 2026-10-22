import { marked } from "marked";

const cache = new Map();

/** Fetch a repo README from GitHub (raw) and render it to HTML with absolute links. */
export async function readmeHtml(repo, path = "README.md", branch = "main") {
  const key = `${repo}/${path}`;
  if (cache.has(key)) return cache.get(key);
  const raw = `https://raw.githubusercontent.com/${repo}/${branch}/`;
  const res = await fetch(raw + path);
  if (!res.ok) {
    cache.set(key, null);
    return null;
  }
  const dir = path.includes("/") ? path.slice(0, path.lastIndexOf("/") + 1) : "";
  const md = await res.text();
  let html = await marked.parse(md);
  // relative images -> raw files; relative links -> the file on github.com
  html = html
    .replace(/(src|srcset)="(?!https?:|#|\/\/|data:)([^"]+)"/g, (_, a, p) => `${a}="${raw}${dir}${p}"`)
    .replace(/href="(?!https?:|#|\/\/|mailto:)([^"]+)"/g, (_, p) => `href="https://github.com/${repo}/blob/${branch}/${dir}${p}"`);
  cache.set(key, html);
  return html;
}
