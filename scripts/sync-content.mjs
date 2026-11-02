// Pins the commits the site renders, in src/data/content-sync.json:
//   { "<repo>": { "readme": sha, "content": sha } }
// - readme: the latest commit touching each project's README.md (project pages)
//   and the org profile README (the home page);
// - content: the latest commit touching a project's Learn content (its
//   manifest's directory and every directory the manifest lists);
// - npm: the latest published version of the project's npm package, which
//   gates its release pages, so a new release appears once it publishes.
// A changed pin is a commit to main, which Cloudflare Pages deploys, so README
// and content edits reach the site within the hour.
// Run by .github/workflows/sync-content.yml.
import { readFileSync, writeFileSync } from "node:fs";
import { PROJECTS } from "../src/site.js";

const file = new URL("../src/data/content-sync.json", import.meta.url);
const pins = JSON.parse(readFileSync(file, "utf8"));
const headers = { accept: "application/vnd.github+json", ...(process.env.GH_TOKEN && { authorization: `Bearer ${process.env.GH_TOKEN}` }) };

async function latest(repo, paths) {
  let best = null;
  for (const path of paths) {
    const res = await fetch(`https://api.github.com/repos/${repo}/commits?sha=main&per_page=1&path=${encodeURIComponent(path)}`, { headers });
    if (!res.ok) throw new Error(`${repo} ${path}: HTTP ${res.status}`);
    const [commit] = await res.json();
    if (commit && (!best || commit.commit.committer.date > best.date)) best = { sha: commit.sha, date: commit.commit.committer.date };
  }
  return best?.sha;
}

async function manifestDirs(project) {
  const res = await fetch(`https://raw.githubusercontent.com/${project.repo}/main/${project.learn}`);
  if (!res.ok) return [];
  const pages = (await res.json()).pages ?? [];
  return [...new Set(pages.map((p) => p.path.slice(0, p.path.lastIndexOf("/"))).filter(Boolean))];
}

function pin(repo, key, sha) {
  if (!sha) return;
  pins[repo] ??= {};
  if (pins[repo][key] !== sha) console.log(`${repo} ${key}: ${pins[repo][key] ?? "(none)"} -> ${sha}`);
  pins[repo][key] = sha;
}

pin("Millillion/.github", "readme", await latest("Millillion/.github", ["profile/README.md"]));
for (const project of PROJECTS) {
  pin(project.repo, "readme", await latest(project.repo, ["README.md"]));
  if (project.learn) {
    const dir = project.learn.slice(0, project.learn.lastIndexOf("/")) || project.learn;
    pin(project.repo, "content", await latest(project.repo, [dir, ...(await manifestDirs(project))]));
  }
  if (project.npm) {
    const res = await fetch(`https://registry.npmjs.org/${project.npm}`, { headers: { accept: "application/vnd.npm.install-v1+json" } });
    if (!res.ok) throw new Error(`npm ${project.npm}: HTTP ${res.status}`);
    pin(project.repo, "npm", (await res.json())["dist-tags"]?.latest);
  }
}
writeFileSync(file, JSON.stringify(pins, null, 2) + "\n");
