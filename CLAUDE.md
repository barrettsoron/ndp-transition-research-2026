# NDP Transition Research Archive

Public archive of research materials related to the NDP leadership transition following the election of Avi Lewis as federal NDP leader, March 29, 2026.

## What this project is

A curated, date-organized collection of news coverage, transcripts, speeches, and primary sources about the NDP leadership transition. The content is public-facing and hosted on GitHub Pages via Astro. Everything here is public, non-internal, non-strategic material reproduced under Canadian fair dealing (Copyright Act, s. 29).

**This is a content archive, not a web app.** The Astro site is a thin rendering layer. The real work is the markdown files.

## Repo structure

```
daily/                 # All date-based coverage folders
  march-29/            # Convention results, first ballot, election night
  march-30/            # Post-convention reaction
  march-31/            # Stephen Lewis's death
  april-01/            # Continuing coverage
  april-NN/            # New folders added as coverage continues
speeches/              # Primary texts — Avi Lewis's showcase and victory speeches
stephen-lewis/         # Curated public record — speeches, commentary
src/                   # Astro site source (layouts, pages, content config)
scripts/               # Utility scripts (link checker, alerts fetcher)
```

Transcripts go inline in the relevant date folder alongside other content from that day — not in a separate directory. A transcript from April 16 belongs in `daily/april-16/`, named following the standard convention.

New dated folders are added as coverage continues — always inside `daily/` (e.g., `daily/april-19/`, `daily/april-20/`).

## File naming convention

Every content file follows this pattern:

```
YYYY-MM-DD — outlet-slug-description.md
```

The date matches the folder date. The slug is lowercase, hyphenated, derived from the outlet name and a short description of the content. The em dash (—) is literal, not a hyphen.

Examples:
- `2026-03-29 — cbc-ndp-new-leader-analysis.md`
- `2026-03-30 — jacobin-avi-lewis-ndp.md`
- `2026-03-31 — seth-klein-stephen-lewis-farewell.md`

## Frontmatter format

Every markdown file has YAML frontmatter. The fields vary by type.

### Articles

```yaml
---
title: "Headline as published"
date: 2026-03-29
source: https://original-url.com/article
author: Author Name
outlet: Outlet Name
language: en
type: article
---
```

### Stubs (paywalled or unavailable content)

```yaml
---
title: "Headline as published"
date: 2026-03-29
source: https://original-url.com/article
outlet: Outlet Name
language: fr
type: article
stub: true
---

> *Note: full article behind paywall. Metadata preserved for reference.*
```

### Statements and primary sources

```yaml
---
title: "Descriptive title"
date: 2026-03-29
author: Author Name
outlet: Issuing organization
language: en
type: statement
---
```

### Transcripts

```yaml
---
title: "Descriptive title"
date: 2026-04-01
source: https://youtube.com/watch?v=...
outlet: Outlet Name
language: en
type: transcript
note: "Context about the transcript — when recorded, why it matters"
speakers:
  - Speaker One
  - Speaker Two
---
```

## Validation constraints (Astro build)

The Astro site validates every markdown file's frontmatter at build time. If these constraints are violated, the build fails and the site won't deploy. **These are strict — do not deviate.**

- `type` must be one of: `article`, `speech`, `transcript`, `statement`
- `language` must be one of: `en`, `fr`, `en-fr`
- `source` must be a valid URL (include the protocol: `https://...`)
- `date` must be a valid date (e.g., `2026-03-29`, not `March 29, 2026`)
- `stub` must be `true` or omitted entirely (not `false`, not a string)

## Content formatting rules

- Body text is plain markdown. No unnecessary formatting.
- Subheadings from the original article are preserved as `##` headings.
- Block quotes use `>` for direct quotations.
- Tables are used where the original content was tabular (e.g., vote results).
- Corrections or editor's notes from the original are preserved at the bottom, italicized, with a horizontal rule above.
- No editorializing. The content reflects what was published.

## Fair dealing

All third-party content is reproduced under the fair dealing provisions of the Copyright Act (Canada), s. 29. Every file attributes source, author, and outlet. Links to originals are provided. No commercial use is made.

## Astro site

The repo includes an Astro 5 static site with Pagefind search, deployed to GitHub Pages via a GitHub Actions workflow. The Astro config is minimal (`astro.config.mjs`). The site renders the markdown content — don't break the build by moving files out of the expected structure.

The site dynamically discovers sections from the content collection at build time. New date folders inside `daily/` (e.g., `daily/april-19/`, `daily/april-20/`) are automatically picked up — no code changes needed. Section pages, navigation, and the home page all update themselves.

**Do not remove or modify the Astro scaffolding** (`src/`, `astro.config.mjs`, `package.json`, `.github/workflows/`). If making structural changes, verify the build with `pnpm build`.

## Tools

- **Defuddle** (`defuddle parse <url> --md`): Used to extract clean markdown from web pages. Strips nav, ads, and clutter. Preferred over raw fetching.
- **gh CLI**: Used for creating branches and PRs.

## Handling paywalled content

When Defuddle returns only nav elements, a stub, or a login wall, use this fallback chain:

**1. Wayback Machine** — try `defuddle parse "https://web.archive.org/web/<url>" --md`. Non-profit, trustworthy, but coverage of paywalled Canadian news is inconsistent.

**2. archive.ph** — try `defuddle parse "https://archive.ph/<url>" --md`. Coverage is better than Wayback for recent Canadian outlets.

> **Known risk with archive.ph**: In January–February 2026, archive.today's operator was documented weaponizing its CAPTCHA page to route visitor traffic into a DDoS attack, and Wikipedia banned the service after finding evidence of tampered snapshots. Using archive.ph as a *reading* tool is lower-risk than citing it as a source, but the platform is not trustworthy. Treat content extracted via archive.ph as plausibly accurate but not authoritative, and prefer Wayback Machine whenever it has coverage.

**3. Stub** — if both fail, create a stub with `stub: true` in the frontmatter. A stub is the right outcome for content that genuinely can't be extracted; it preserves the metadata and source URL for future reference.

## Worktree discipline

If this session is running inside a git worktree (check with `git worktree list`), do all work — file creation, branch creation, builds, and the dev server — within that worktree directory. Never `cd` to the main repo directory to work around the worktree. If the worktree branch is wrong for the task, check out the correct branch inside the worktree. Splitting work across the worktree and main repo causes the dev server to show a different branch than the one being edited.

## Workflow

This project is maintained through Claude Code Desktop. A scheduled task runs daily to fetch new coverage from RSS feeds, format it using these conventions, and open a PR for review. Manual additions (paywalled sources, transcripts) are done interactively through Claude Code Desktop or Dispatch.

### Adding a single article (Dispatch or interactive)

When given a URL to add to the archive:

1. Use `defuddle parse <url> --md` to extract clean content
2. Determine the article's publication date, outlet, author, and language
3. Create the markdown file with correct frontmatter (see formats above)
4. Name the file following the convention: `YYYY-MM-DD — outlet-slug-description.md`
5. Place it in the correct date folder under `daily/` (create `daily/YYYY-MM-DD/` if it doesn't exist)
6. If Defuddle can't extract the content (paywall, 403, etc.), create a stub instead
7. Create a branch, commit, push, and open a PR via `gh pr create`

When given raw article text (e.g., pasted from a paywalled source) along with the source URL:

1. Skip the Defuddle step — use the provided text directly
2. Follow steps 2–7 above

## What not to include

- Internal strategy, private communications, donor information
- Unpublished analysis or personal commentary
- Content that doesn't relate to the NDP leadership transition or its immediate context
- Anything that would compromise individuals' privacy
