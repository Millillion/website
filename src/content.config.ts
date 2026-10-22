import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const blog = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/blog" }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    description: z.string(),
    draft: z.boolean().default(false),
  }),
});

const podcast = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/podcast" }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    description: z.string(),
    audio: z.string().url(), // R2 URL of the mp3
    audioBytes: z.number(), // file size, required by podcast feeds
    duration: z.string(), // "HH:MM:SS"
    youtube: z.string().optional(), // YouTube video id
    blog: z.string().optional(), // slug of the companion blog post
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog, podcast };
