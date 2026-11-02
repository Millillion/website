// Pins, per project with `learn` content (src/site.js), the latest commit on
// main that touched the manifest's directory. Run by .github/workflows/sync-content.yml.
import { readFileSync, writeFileSync } from "node:fs";
import { PROJECTS } from "../src/site.js";

const file = new URL("../src/data/content-sync.json", import.meta.url);
const pins = JSON.parse(readFileSync(file, "utf8"));
const headers = { accept: "application/vnd.github+json", ...(process.env.GH_TOKEN && { authorization: `Bearer ${process.env.GH_TOKEN}` }) };

for (const project of PROJECTS.filter((p) => p.learn)) {
  const dir = project.learn.slice(0, project.learn.lastIndexOf("/")) || project.learn;
  // The manifest lists files outside its directory too (release notes), so pin the
  // latest commit to either.
  const latest = [];
  for (const path of [dir, ...(await manifestPaths(project))]) {
    const res = await fetch(`https://api.github.com/repos/${project.repo}/commits?sha=main&per_page=1&path=${encodeURIComponent(path)}`, { headers });
    if (!res.ok) throw new Error(`${project.repo} ${path}: HTTP ${res.status}`);
    const [commit] = await res.json();
    if (commit) latest.push({ sha: commit.sha, date: commit.commit.committer.date });
  }
  if (!latest.length) continue;
  latest.sort((a, b) => b.date.localeCompare(a.date));
  if (pins[project.repo] !== latest[0].sha) console.log(`${project.repo}: ${pins[project.repo] ?? "(none)"} -> ${latest[0].sha}`);
  pins[project.repo] = latest[0].sha;
}
writeFileSync(file, JSON.stringify(pins, null, 2) + "\n");

async function manifestPaths(project) {
  const res = await fetch(`https://raw.githubusercontent.com/${project.repo}/main/${project.learn}`);
  if (!res.ok) return [];
  const dirs = new Set((await res.json()).pages?.map((p) => p.path.slice(0, p.path.lastIndexOf("/"))).filter(Boolean));
  return [...dirs];
}
