import { defineConfig } from "cf/config";

// Receives the contact form on millillion.org/contact/ and emails it to Jordan via Cloudflare Email Routing.
export default defineConfig({
  worker: {
    name: "millillion-contact",
    entrypoint: "src/index.js",
    compatibilityDate: "2026-10-01",
    triggers: [{ type: "fetch", pattern: "millillion.org/api/contact", zone: "millillion.org" }],
    env: { MAIL: { type: "send-email", destinationAddress: "jordan.michael.last@gmail.com" } },
  },
});
