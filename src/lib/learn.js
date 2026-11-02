import { readFile } from "node:fs/promises";
import { marked } from "marked";
import sync from "../data/content-sync.json";

// A project's educational content lives in its own repo (the single source of
// truth); `learn` names a manifest there. The commit is pinned in
// src/data/content-sync.json by the sync-content workflow, so a build is
// reproducible and a content change is a commit here, which redeploys the site.

const cache = new Map();

export const KINDS = [
  ["overview", "Start here"],
  ["tutorial", "Tutorials"],
  ["bug-caught", "Bugs our testing caught"],
  ["proof-spotlight", "Proof spotlights"],
  ["platform", "Platforms"],
  ["release", "Releases"],
];

const ref = (project) => sync[project.repo] ?? "main";
const raw = (project) => `https://raw.githubusercontent.com/${project.repo}/${ref(project)}/`;

// LEARN_LOCAL=/path/to/checkout previews a project's content from disk.
async function text(url) {
  if (cache.has(url)) return cache.get(url);
  let body;
  if (process.env.LEARN_LOCAL) {
    const path = url.replace(/^https:\/\/raw\.githubusercontent\.com\/[^/]+\/[^/]+\/[^/]+\//, "");
    body = await readFile(`${process.env.LEARN_LOCAL}/${path}`, "utf8").catch(() => null);
  } else {
    const res = await fetch(url);
    body = res.ok ? await res.text() : null;
  }
  cache.set(url, body);
  return body;
}

/** The project's pages, from its manifest; [] when it has none yet. */
export async function learnPages(project) {
  if (!project.learn) return [];
  const body = await text(raw(project) + project.learn);
  if (!body) return [];
  const pages = JSON.parse(body).pages ?? [];
  return pages.filter((p) => p.slug && p.title && p.path && p.kind);
}

/** One page rendered to HTML: frontmatter removed, relative links made absolute. */
export async function learnHtml(project, page) {
  const md = await text(raw(project) + page.path);
  if (md === null) return null;
  const dir = page.path.includes("/") ? page.path.slice(0, page.path.lastIndexOf("/") + 1) : "";
  const blob = `https://github.com/${project.repo}/blob/${ref(project)}/`;
  let html = await marked.parse(md.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, ""));
  return html
    .replace(/(src|srcset)="(?!https?:|#|\/\/|data:)([^"]+)"/g, (_, a, p) => `${a}="${raw(project)}${dir}${p}"`)
    .replace(/href="(?!https?:|#|\/\/|mailto:)([^"]+)"/g, (_, p) => `href="${new URL(p, blob + dir)}"`);
}

export const sourceUrl = (project, page) => `https://github.com/${project.repo}/blob/${ref(project)}/${page.path}`;

export const feedbackUrl = (project, page) =>
  `https://github.com/${project.repo}/issues/new?` +
  new URLSearchParams({ title: `Content: ${page.title}`, body: `Page: https://millillion.org/projects/${project.slug}/learn/${page.slug}/\n\n` });
