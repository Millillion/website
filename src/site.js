export const SITE = {
  name: "Millillion",
  tagline: "Impossibly ambitious AI",
  description:
    "Millillion goes after outrageously ambitious software projects, the ones that used to be just dreams, and builds them with AI. Everything is open source.",
  github: "https://github.com/Millillion",
  skills: "https://github.com/Millillion/website/tree/main/.claude/skills", // the AI process behind posts and episodes
  sponsors: "https://github.com/sponsors/lastmjs",
  email: "lastmjs@millillion.org",
  phone: "801-709-1860",
  x: "https://x.com/lastmjs",
};

// Each project page renders the project's own README from GitHub at build time.
export const PROJECTS = [
  { slug: "lasm", name: "Lasm", repo: "Millillion/lasm", blurb: "Lean 4 compiled ahead of time to WebAssembly." },
  { slug: "proofscript", name: "ProofScript", repo: "Millillion/proofscript", blurb: "TypeScript with dependent types and formal verification." },
  { slug: "wasmetal", name: "WasMetal", repo: "Millillion/wasmetal", blurb: "A WebAssembly CPU: a bare metal physical implementation of WebAssembly." },
];

export const PODCAST = {
  title: "Millillion",
  author: "Jordan Last",
  description: "Thinking out loud about impossibly ambitious AI: what it lets us build, and building it.",
  category: "Technology",
  explicit: false,
  cover: "/podcast-cover.jpg", // 3000x3000
  ownerEmail: "lastmjs@millillion.org",
  spotify: "https://open.spotify.com/show/2TSiR5A8vVDAHEeGNpTY7e",
  apple: "https://podcasts.apple.com/us/podcast/millillion/id6826041508",
  youtube: "https://www.youtube.com/@millillionai",
};
