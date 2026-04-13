# SOMEDAY — Deferred Decisions

Things we've discussed and decided to defer. Not forgotten, just not now.

## Move automation to GitHub Actions + API key

**Why defer:** The Claude Code Desktop scheduled task runs daily using the Max subscription. The daily volume (10-20 articles) is low enough that it fits within Max limits. The Desktop app's catch-up behaviour (runs one missed session on wake) is acceptable for now.

**When to revisit:** If missed runs become a real problem (travelling for a week with the laptop closed, consistently missing the window). If the project grows enough that the ~$30-50/month API cost is worth the "runs in the cloud, never misses a day" guarantee. If you want to separate the automation logic into a private repo for cleaner architecture.

**What it would look like:** Create a private `ndp-transition-engine` repo. Move the fetch-and-format logic into a GitHub Action with a cron schedule. Store `ANTHROPIC_API_KEY` as a repo secret. The Action would use `claude -p` (headless CLI mode) or the Claude API directly. Everything else stays the same — it creates a branch on the public repo and opens a PR.

## Private engine repo

**Why defer:** The Claude Code Desktop scheduled task keeps everything in one place. The task prompt lives in `~/.claude/scheduled-tasks/ndp-daily-archive/SKILL.md` and runs against this repo directly. No need for a separate repo yet.

**When to revisit:** If the automation logic gets complex enough that version-controlling it matters. If you move to GitHub Actions (above). If you want other people to be able to contribute to or audit the engine.

## Paywalled sources (La Presse, Le Devoir, Globe and Mail)

**Why defer:** Defuddle can't get past paywalls. These outlets require subscriptions. Automating access would mean storing credentials, which adds complexity and fragility (sessions expire, CAPTCHAs, ToS concerns).

**When to revisit:** If a significant number of stubs are accumulating and it's undermining the archive's usefulness. If one of these outlets launches an API or RSS feed with full text.

**What it would look like:** Manual additions for now. When you read a paywalled article that belongs in the archive, copy it into a markdown file using the existing conventions. The daily automation handles the free sources; you handle the paywalled ones. You can also use Dispatch from your phone — paste the article text and ask it to format and commit.

## Custom domain for the Astro site

**Why defer:** GitHub Pages works fine. The archive isn't being shared widely yet. A custom domain adds DNS management, SSL config, and a renewal to track.

**When to revisit:** When the archive is substantial enough to share with journalists or organizers. When the GitHub/Microsoft branding feels like a meaningful compromise. When you want the archive to be citable with a clean URL.

## Navigation and visual design for the Astro site

**Why defer:** The current rendering is functional. Investing in navigation, visual style, or landing page design before the content is substantial is premature.

**When to revisit:** When there are enough dated folders and articles that browsing becomes unwieldy without navigation. When you start sharing the site URL with people who aren't already familiar with the project.

## French-language content pipeline

**Why defer:** The Quebecois translation skill exists and works. But translating English coverage to French (or properly archiving French-language sources) is a separate editorial decision from automating English-language fetching.

**When to revisit:** When the La Presse and Le Devoir stub situation is addressed. When the archive has enough English content that a French layer would meaningfully expand the audience.

## Calendar interface

**Why defer:** The archive is small enough that section-based browsing works. A calendar view adds complexity (a component, date-based routing, possibly a library) for marginal benefit at current scale.

**When to revisit:** When the archive spans enough dates that scrolling through sections becomes unwieldy. When the site is being shared with people who want to browse by date range.

## CMD-K command bar and text-only navigation

**Why defer:** Pagefind search already covers keyword lookup. A command bar (CMD-K) and text-only nav are power-user features that don't justify the implementation cost for a small archive.

**When to revisit:** When the archive is large enough that search alone isn't sufficient for navigation. When accessibility or keyboard-first browsing becomes a priority.

---

*Last updated: 2026-04-13*
