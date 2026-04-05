import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const articles = defineCollection({
  loader: glob({
    pattern: "{march-*,april-*,speeches,stephen-lewis,transcript-archive}/[0-9]*.md",
    base: ".",
    generateId: ({ entry }) => {
      const [section, filename] = entry.split('/');
      // Derive slug from the part after " — " (space + em-dash + space), then slugify
      const afterDash = filename.replace(/\.md$/, '').split(' \u2014 ')[1]
        ?? filename.replace(/\.md$/, '');
      const slug = afterDash.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
      return `${section}/${slug}`;
    },
  }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    outlet: z.string().optional(),
    source: z.string().url().optional(),
    language: z.enum(["en", "fr", "en-fr"]).default("en"),
    type: z.enum(["article", "speech", "transcript", "statement"]).default("article"),
    author: z.string().optional(),
    speakers: z.array(z.string()).optional(),
    video: z.string().url().optional(),
    note: z.string().optional(),
    stub: z.boolean().optional(),
  }),
});

export const collections = { articles };
