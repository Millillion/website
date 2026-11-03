import { readFile } from "node:fs/promises";
import { marked } from "marked";
import pins from "../data/content-sync.json";
import { PROJECTS } from "../site.js";

// Learn: AI-generated educational content, one stream across projects. Each
// project keeps its content in its own repo (the single source of truth);
// `learn` in src/site.js names its manifest. Content is fetched at the commit
// the sync-content workflow pinned, so a content change is a commit here,
// which redeploys the site.

const cache = new Map();

export const KINDS = [
  ["overview", "Start here"],
  ["tutorial", "Tutorials"],
  ["bug-caught", "Bugs our testing caught"],
  ["proof-spotlight", "Proof spotlights"],
  ["platform", "Platforms"],
  ["release", "Releases"],
];
export const kindLabel = (kind) => KINDS.find(([k]) => k === kind)?.[1] ?? kind;

/** Learn's independent streams, each with its own page and RSS feed. Page URLs
 * stay /learn/<project>/<slug>/ whatever stream a page is in. */
export const STREAMS = [
  { slug: "tutorials", name: "Tutorials", kinds: ["overview", "tutorial"],
    blurb: "Step-by-step guides, each run in CI so its commands work as written." },
  { slug: "proofs", name: "Proofs", kinds: ["proof-spotlight"],
    blurb: "One theorem at a time: what it says, why it matters and where Lean checks it." },
  { slug: "testing", name: "Testing", kinds: ["bug-caught", "platform"],
    blurb: "Bugs our testing caught before users did, and how each platform is tested." },
  { slug: "releases", name: "Releases", kinds: ["release"],
    blurb: "What changed in each published version." },
];
export const streamOf = (kind) => STREAMS.find((s) => s.kinds.includes(kind));
export const streamUrl = (stream) => `/learn/${stream.slug}/`;

/** A stream's pages, [{ project, page }]: tutorials in reading order ("Start
 * here" first), every other stream newest first. */
export async function streamItems(stream) {
  const items = (await allLearn()).filter(({ page }) => stream.kinds.includes(page.kind));
  if (stream.slug !== "tutorials") return items;
  const rank = ({ page }) => (page.kind === "overview" ? -1 : page.order ?? 99);
  return items.sort((a, b) => rank(a) - rank(b));
}

const ref = (project) => pins[project.repo]?.content ?? "main";
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

/** The versions of the project's npm package that are published, or null when it has none or npm is unreachable. */
async function published(project) {
  if (!project.npm) return null;
  const key = `npm:${project.npm}`;
  if (!cache.has(key)) {
    const res = await fetch(`https://registry.npmjs.org/${project.npm}`, { headers: { accept: "application/vnd.npm.install-v1+json" } }).catch(() => null);
    cache.set(key, res?.ok ? new Set(Object.keys((await res.json()).versions ?? {})) : null);
  }
  return cache.get(key);
}

/** A project's pages, from its manifest; [] when it has none yet. A release
page appears only once its version is on npm (a version can be bumped, and
its notes written, before it publishes, or never publish at all). */
export async function learnPages(project) {
  if (!project.learn) return [];
  const body = await text(raw(project) + project.learn);
  if (!body) return [];
  const versions = await published(project);
  return (JSON.parse(body).pages ?? [])
    .filter((p) => p.slug && p.title && p.path && p.kind)
    .filter((p) => {
      if (p.kind !== "release" || !project.npm) return true;
      const version = p.title.match(/(\d+\.\d+\.\d+\S*)/)?.[1];
      return Boolean(versions && version && versions.has(version));
    });
}

/** Every project's pages, newest first: [{ project, page }]. */
export async function allLearn() {
  const all = [];
  for (const project of PROJECTS) for (const page of await learnPages(project)) all.push({ project, page });
  return all.sort((a, b) => String(b.page.date).localeCompare(String(a.page.date)));
}

/** One page rendered to HTML: frontmatter removed, relative links made absolute. */
export async function learnHtml(project, page) {
  const md = await text(raw(project) + page.path);
  if (md === null) return null;
  const dir = page.path.includes("/") ? page.path.slice(0, page.path.lastIndexOf("/") + 1) : "";
  const blob = `https://github.com/${project.repo}/blob/main/`;
  const html = await marked.parse(md.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, ""));
  return html
    .replace(/(src|srcset)="(?!https?:|#|\/\/|data:)([^"]+)"/g, (_, a, p) => `${a}="${raw(project)}${dir}${p}"`)
    .replace(/href="(?!https?:|#|\/\/|mailto:)([^"]+)"/g, (_, p) => `href="${new URL(p, blob + dir)}"`);
}

export const learnUrl = (project, page) => (page ? `/learn/${project.slug}/${page.slug}/` : `/learn/${project.slug}/`);
export const sourceUrl = (project, page) => `https://github.com/${project.repo}/blob/main/${page.path}`;
export const feedbackUrl = (project, page) =>
  `https://github.com/${project.repo}/issues/new?` +
  new URLSearchParams({ title: `Learn: ${page.title}`, body: `Page: https://millillion.org${learnUrl(project, page)}\n\n` });

export const AI_NOTE =
  "AI-generated: written by AI (Claude) from each project's repository and its CI results, and published automatically.";
