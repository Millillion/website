import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

// Update `site` once the domain is final.
export default defineConfig({
  site: "https://millillion.org",
  integrations: [sitemap()],
});
