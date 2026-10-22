export const SITE = {
  name: "Millillion",
  tagline: "Impossibly ambitious AI",
  description:
    "Millillion goes after outrageously ambitious software projects, the ones that used to be just dreams, and builds them with AI. Everything is open source.",
  github: "https://github.com/Millillion",
  sponsors: "https://github.com/sponsors/lastmjs",
  patreon: "", // add once the Patreon page exists
  email: "", // add the business email once the domain is set up
};

// Each project page renders the project's own README from GitHub at build time.
export const PROJECTS = [
  { slug: "lasm", name: "Lasm", repo: "Millillion/lasm", blurb: "Lean 4 compiled ahead of time to WebAssembly." },
  { slug: "proofscript", name: "ProofScript", repo: "Millillion/proofscript", blurb: "TypeScript with dependent types and formal verification." },
  { slug: "ayeyaiyai", name: "AyeYaiYai", repo: "Millillion/ayeyaiyai", blurb: "An ahead-of-time compiler from JavaScript to WebAssembly." },
];

export const PODCAST = {
  title: "Millillion",
  author: "Jordan Last",
  description: "Thinking out loud about impossibly ambitious AI: what it lets us build, and building it.",
  category: "Technology",
  explicit: false,
  cover: "/podcast-cover.png", // 3000x3000 cover goes here before submitting to Apple/Spotify
  ownerEmail: "", // required by Apple/Spotify: the business email
};
