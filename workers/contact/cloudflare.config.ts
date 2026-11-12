import { defineConfig } from "cf/config";

// Receives the contact form on millillion.org/contact/ and emails it to Jordan via Cloudflare Email Routing.
// Also receives Millillion event news sign-ups from millillion.org/meetup/, stores them in KV and emails Jordan.
export default defineConfig({
  worker: {
    name: "millillion-contact",
    entrypoint: "src/index.js",
    compatibilityDate: "2026-10-01",
    triggers: [
      { type: "fetch", pattern: "millillion.org/api/contact", zone: "millillion.org" },
      { type: "fetch", pattern: "millillion.org/api/events", zone: "millillion.org" },
    ],
    env: {
      MAIL: { type: "send-email", destinationAddress: "jordan.michael.last@gmail.com" },
      EVENTS: { type: "kv", id: "640131e27f3b4c92a593d526a55f0f19" }, // millillion-event-news: one key per email
    },
  },
});
