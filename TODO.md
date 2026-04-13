# TODO — NDP Transition Research Archive

Active work to move this project toward automated daily updates via Claude Code Desktop.

## Setup — Claude Code Desktop

- [ ] Open this repo folder in Claude Code Desktop
- [ ] Verify `CLAUDE.md` is picked up on session start (ask Claude "what project is this?")
- [ ] Verify `gh` CLI is installed and authenticated on your Mac (`gh auth status` in any terminal)
- [ ] Verify `defuddle` is installed globally on your Mac (`npm install -g defuddle`)
- [ ] Test a manual run: ask Claude Code to fetch one article with Defuddle, format it, and save it to the right folder

## Write CLAUDE.md

- [ ] Review the draft `CLAUDE.md` in this commit — adjust anything that doesn't match your intent
- [ ] Confirm Claude Code reads it on session start
- [ ] Test formatting: give Claude an article URL and ask it to add it to the archive — check the output matches existing files
- [ ] Iterate on the `CLAUDE.md` instructions until output is consistently right

## Build the Source List

- [ ] Identify RSS feeds for target outlets:
  - [ ] ndp.ca/news
  - [ ] CBC Politics
  - [ ] The Tyee
  - [ ] Rabble
  - [ ] Jacobin (Canada tag)
  - [ ] Global News Politics
  - [ ] Common Dreams
  - [ ] Others as identified
- [ ] For each feed, confirm the URL returns valid RSS/Atom content
- [ ] Document the feed list in a `sources.md` or similar file in the repo
- [ ] Identify paywalled outlets that will need manual stub creation (La Presse, Le Devoir, Globe and Mail, Bloomberg)

## Write the Fetch Script

The scheduled task should not re-derive RSS parsing and deduplication logic from scratch every day. A short Node script handles the mechanical work (fetching feeds, parsing XML, checking for duplicates, running Defuddle). Claude's scheduled task then handles the editorial work (formatting, frontmatter, file naming, PR creation).

- [ ] Write `scripts/fetch-new-articles.js` — a Node script that:
  - [ ] Reads `sources.md` for the list of RSS feed URLs
  - [ ] Fetches each feed and parses the XML for article entries
  - [ ] Filters to articles published since yesterday
  - [ ] Filters out articles already in the archive (by comparing URLs against `source:` fields in existing frontmatter)
  - [ ] Runs `defuddle parse <url> --md` on each new article
  - [ ] Saves raw Defuddle output to a `staging/` folder, one file per article, with the source URL and metadata in a simple header
- [ ] Add `staging/` to `.gitignore` (it's a working directory, not archive content)
- [ ] Test the script manually: `node scripts/fetch-new-articles.js`
- [ ] Confirm it produces clean raw markdown in `staging/` with no duplicates

## Create the Scheduled Task

- [ ] Open Claude Code Desktop, go to Schedule in the sidebar
- [ ] Create a new local task:
  - **Name:** `ndp-daily-archive`
  - **Folder:** this repo's local path
  - **Frequency:** Daily (choose a morning time, e.g., 9:00 AM Pacific)
  - **Prompt:** (draft below — refine after manual testing)
- [ ] Configure permissions: allow Bash (node, git, gh), Read, Write, Edit
- [ ] Run it manually once with "Run now" and review the output
- [ ] Review the session — check that articles are formatted correctly, branch is created, PR is opened
- [ ] Iterate on the task prompt until the output is reliable
- [ ] Enable the repeating schedule
- [ ] Monitor for a week — review each daily PR for quality

### Draft scheduled task prompt

```
Run the fetch script to check for new articles:
  node scripts/fetch-new-articles.js

If the staging/ folder is empty, there's nothing new — stop here.

For each file in staging/:
1. Read the raw content and metadata
2. Format as a markdown file following the conventions in CLAUDE.md
3. Name the file following the convention: YYYY-MM-DD — outlet-slug-description.md
4. Save to the correct date folder (create the folder if needed)

After processing all staged articles:
1. Clear the staging/ folder
2. Create a branch named daily/YYYY-MM-DD
3. Commit all new files with a descriptive message
4. Push the branch and open a PR with a summary of what was added
```

## Test the Dispatch Workflow (Mobile)

- [ ] From your phone, send Dispatch a URL with a message like "add this to the NDP archive"
- [ ] Confirm Dispatch spawns a Code session against this repo
- [ ] Check that the session reads `CLAUDE.md`, uses Defuddle, and creates a PR
- [ ] Test the paywalled case: paste article text + source URL to Dispatch, confirm it creates the file without Defuddle
- [ ] Confirm you get a push notification when the session finishes or needs approval

## Content — Ongoing (Manual)

- [ ] Archive full coverage from La Presse and Le Devoir (paywalled — add manually or via Dispatch)
- [ ] Archive full Bloomberg profile (paywalled — add manually or via Dispatch)
- [ ] Complete `transcript-archive/` with remaining relevant video transcripts
- [ ] Expand `stephen-lewis/` — currently three archival speeches
- [ ] Add `march-27-28/` folder for convention run-up coverage
- [ ] Continue expanding `april-01/` and beyond with post-transition coverage

## Astro Site — Hardened for Automation

Done in this session (Cowork, April 13):
- [x] Dynamic section discovery — nav, home page, section indexes, and breadcrumbs now derive from content collection at build time. New date folders are picked up automatically.
- [x] Pinned Astro and Pagefind versions exactly (no caret ranges) to prevent surprise breakage on CI
- [x] Added validation constraints to `CLAUDE.md` so Claude never produces frontmatter that breaks the Zod schema
- [x] Created `src/lib/sections.ts` as single source of truth for section slugs, labels, and nav

Still to do:
- [ ] **Verify the build works** — run `pnpm install && pnpm build` in Claude Code Desktop after committing these changes
- [ ] Fix topnav short date names — three letters, not four (Mar not Marc, Apr not Apri)
- [ ] Dated entries in nav should appear in a dropdown rather than listed one-by-one
- [ ] Include days of the week in the index cards (e.g., "March 29 — Saturday") but not in the nav entries
- [ ] Consolidate `transcript-archive/` — move entries into their dated folders
- [ ] Rename `speeches/` section label to "Avi Lewis Speeches"
- [ ] Add light/dark toggle
- [ ] Add OpenGraph and meta tags (not urgent — do when content is substantial)
- [ ] Enable search engine indexing — update `robots.txt` to `Allow: /` once ready
- [ ] Add `sitemap.xml` when content warrants it
- [ ] Consider custom domain when the archive has enough gravity to justify it

---

*Last updated: 2026-04-13*
