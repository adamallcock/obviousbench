---
title: ObviousBench Website Launch Plan
date: 2026-06-01
type: plan
status: parked
---

# ObviousBench Website Launch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and deploy a very simple ObviousBench project website, visually close to the SimpleBench project-page style, from a private GitHub repository to Cloudflare Pages.

**Architecture:** Keep the website as a separate static-site repository, with no private benchmark source data or provider logs. The site should publish only curated, release-safe artifacts from this repo: the paper PDF, headline answer-correctness leaderboard, brief method text, and links to public dataset/code once those are intentionally released. Use Cloudflare Pages Git integration for deploys and attach a custom domain after registration.

**Tech Stack:** Static HTML, CSS, optional tiny JSON data file for leaderboard rows, private GitHub repository, Cloudflare Pages Git integration, custom domain such as `obviousbench.com` if registered.

---

## Parked Status

Do not execute this plan until the user explicitly resumes it. The intended execution trigger is one of:

- domain registered, preferably `obviousbench.com` if available;
- final or preview-safe public links chosen for paper, dataset, and code;
- decision made on whether the public benchmark code lives in this repo, a stripped publication repo, or a release branch.

## Source Notes

- SimpleBench reference style: sparse project page, centered title/subtitle, author/team line, top navigation links, introduction, leaderboard, report/video/dataset/code links. Reference: <https://simple-bench.com/>.
- Cloudflare Pages Git integration supports automatic builds from GitHub/GitLab and supports both private and public GitHub repositories. Reference: <https://developers.cloudflare.com/pages/get-started/git-integration/>.
- Cloudflare Pages custom domains should be added through the Pages project custom-domain flow; apex domains require the domain to be in the relevant Cloudflare account/zone. Reference: <https://developers.cloudflare.com/pages/configuration/custom-domains/>.

## Proposed Public URL

Primary candidate:

- `https://obviousbench.com`

Fallbacks if unavailable or held:

- `https://obvious-bench.com`
- `https://obviousbench.org`
- `https://obvious-bench.org`

Execution rule:

- Verify domain availability and registration status at execution time.
- Do not put a final domain in repository metadata until the user confirms registration.

## Repository Decision

Recommended:

- Create a new private GitHub repo named `website-obviousbench-com`.
- Keep it separate from `/Users/adamallcock/Documents/Coding/benchmark-obviousbench`.
- Publish only copied/generated artifacts that are safe for the public site.

Rationale:

- The benchmark repo is noisy, research-heavy, and contains drafts, provider-output paths, and parked release decisions.
- A separate website repo keeps Cloudflare deployment permissions narrow.
- A private repo is fine for Pages deploys while the rendered site remains public.

## Site Information Architecture

First screen:

- Title: `ObviousBench`
- Subtitle: `Where obvious tasks still break language models`
- Author line: `Adam Allcock`
- Link row:
  - `Report`
  - `Leaderboard`
  - `Dataset`
  - `Code`
  - `Try Yourself` if/when a lightweight demo exists

Main page sections:

1. `Introduction`
   - One paragraph: short, objective prompts that humans solve directly but models still miss.
   - One paragraph: answer correctness is the headline score; strict compliance is reported separately.
2. `Leaderboard`
   - Small table ranked by answer correctness.
   - Columns: Rank, Model, Correct, 95% CI, Strict, Cost.
   - Include a clear `draft placeholder` banner until final sweep exists.
3. `Benchmark`
   - Task-family list with counts: character count, spelling transform, arithmetic, word count, ordering, format, negation, constraints.
   - Brief note that deterministic scorers are used.
4. `Report`
   - Link to PDF/arXiv once available.
   - Link to short methodology excerpt.
5. `Artifacts`
   - Dataset link once public.
   - Code link once public.
   - Citation BibTeX block once arXiv metadata exists.
6. `Contact`
   - `adamallcock@gmail.com`

## Visual Direction

SimpleBench-like, but not a clone:

- White background.
- Serif or system font; calm academic project-page feel.
- Centered title and subtitle.
- Sparse top links.
- Minimal horizontal rules.
- Compact tables.
- No marketing hero, gradients, decorative cards, or animations.
- Mobile-first table overflow handling.
- All draft values clearly marked as draft.

## Files In The Website Repo

Create:

- `README.md`
  - Purpose, deploy notes, public/private boundaries.
- `index.html`
  - Single static page.
- `assets/site.css`
  - Minimal responsive typography, layout, tables, badges.
- `assets/leaderboard.json`
  - Optional generated, release-safe rows.
- `assets/obviousbench-paper.pdf`
  - Optional copied paper PDF once public-preview-safe.
- `_headers`
  - Conservative security headers.
- `_redirects`
  - Optional redirect from legacy paths to root or paper.
- `.gitignore`
  - Ignore local build/cache files.

Do not create:

- raw provider logs;
- private result summaries;
- full unpublished datasets;
- local environment files;
- private draft PDFs unless intentionally published as preview.

## Task 1: Create Static Site Skeleton

**Files:**

- Create in new private repo: `README.md`
- Create in new private repo: `index.html`
- Create in new private repo: `assets/site.css`
- Create in new private repo: `.gitignore`

- [ ] **Step 1: Create the private GitHub repo**

Use GitHub UI or CLI:

```bash
gh repo create website-obviousbench-com --private --description "Static website for ObviousBench"
```

Expected:

- GitHub creates a private repo.
- No benchmark data is pushed.

- [ ] **Step 2: Clone the repo locally**

```bash
cd /Users/adamallcock/Documents/Coding
git clone git@github.com:adamallcock/website-obviousbench-com.git
cd website-obviousbench-com
```

Expected:

- Working tree exists at `/Users/adamallcock/Documents/Coding/website-obviousbench-com`.

- [ ] **Step 3: Add `.gitignore`**

```gitignore
.DS_Store
node_modules/
dist/
.wrangler/
.env
*.log
```

- [ ] **Step 4: Add `index.html`**

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>ObviousBench</title>
    <meta name="description" content="ObviousBench is a benchmark for short, obvious tasks that still break language models.">
    <link rel="stylesheet" href="assets/site.css">
  </head>
  <body>
    <main class="page">
      <header class="hero">
        <h1>ObviousBench</h1>
        <p class="subtitle">Where obvious tasks still break language models</p>
        <p class="byline">Adam Allcock</p>
        <nav class="links" aria-label="Project links">
          <a href="#leaderboard">Leaderboard</a>
          <a href="#benchmark">Benchmark</a>
          <a href="#report">Report</a>
          <a href="#artifacts">Artifacts</a>
          <a href="mailto:adamallcock@gmail.com">Contact</a>
        </nav>
      </header>

      <section id="intro">
        <h2>Introduction</h2>
        <p>
          ObviousBench measures short, objective prompts that a careful human can solve directly,
          but language models can still answer incorrectly.
        </p>
        <p>
          The headline score is answer correctness. Format and strict-compliance scores are reported
          separately, so a correct answer with extra prose is not treated as the main benchmark failure.
        </p>
      </section>

      <section id="leaderboard">
        <h2>Leaderboard</h2>
        <p class="notice">Draft placeholder layout. Replace with frozen paper-sweep results before public launch.</p>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Rank</th>
                <th>Model</th>
                <th>Correct</th>
                <th>95% CI</th>
                <th>Strict</th>
                <th>Cost</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>1</td>
                <td>Example model</td>
                <td>--</td>
                <td>--</td>
                <td>--</td>
                <td>--</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section id="benchmark">
        <h2>Benchmark</h2>
        <p>
          Current task families include character counting, spelling transforms, arithmetic,
          word counting, ordering, format compliance, negation, and constraint awareness.
        </p>
      </section>

      <section id="report">
        <h2>Report</h2>
        <p>
          The report link will be added after the arXiv-ready PDF and citation metadata are frozen.
        </p>
      </section>

      <section id="artifacts">
        <h2>Artifacts</h2>
        <ul>
          <li>Dataset: release link pending.</li>
          <li>Code: release link pending.</li>
          <li>Citation: arXiv metadata pending.</li>
        </ul>
      </section>
    </main>
  </body>
</html>
```

- [ ] **Step 5: Add `assets/site.css`**

```css
:root {
  color-scheme: light;
  --text: #1f2328;
  --muted: #5b616e;
  --rule: #d8dee8;
  --link: #1f5fa8;
  --notice-bg: #fff8e6;
  --notice-border: #dfb44f;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  background: #fff;
  color: var(--text);
  font-family: Georgia, "Times New Roman", serif;
  line-height: 1.55;
}

.page {
  width: min(920px, calc(100% - 32px));
  margin: 0 auto;
  padding: 48px 0 72px;
}

.hero {
  text-align: center;
  padding: 24px 0 36px;
  border-bottom: 1px solid var(--rule);
}

h1 {
  margin: 0;
  font-size: clamp(2.4rem, 7vw, 4.2rem);
  font-weight: 700;
  letter-spacing: 0;
}

.subtitle {
  margin: 10px 0 0;
  color: var(--muted);
  font-size: clamp(1.1rem, 3vw, 1.55rem);
}

.byline {
  margin: 14px 0 0;
}

.links {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px 18px;
  margin-top: 18px;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: 0.95rem;
}

a {
  color: var(--link);
  text-decoration-thickness: 1px;
  text-underline-offset: 3px;
}

section {
  padding: 28px 0;
  border-bottom: 1px solid var(--rule);
}

h2 {
  margin: 0 0 12px;
  font-size: 1.45rem;
}

p {
  margin: 0 0 12px;
}

.notice {
  padding: 10px 12px;
  border-left: 4px solid var(--notice-border);
  background: var(--notice-bg);
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: 0.92rem;
}

.table-wrap {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: 0.94rem;
}

th,
td {
  padding: 9px 8px;
  border-bottom: 1px solid var(--rule);
  text-align: left;
  white-space: nowrap;
}

th {
  font-weight: 650;
}

@media (max-width: 640px) {
  .page {
    width: min(100% - 24px, 920px);
    padding-top: 28px;
  }

  .hero {
    padding-top: 12px;
  }
}
```

- [ ] **Step 6: Add `README.md`**

```markdown
# ObviousBench Website

Static public website for ObviousBench.

Source policy:

- The repository may be private.
- The rendered Cloudflare Pages site is public.
- Do not commit raw provider logs, private benchmark drafts, unpublished datasets, API keys, or private result summaries.
- Copy only release-safe generated artifacts from the benchmark repository.

Deployment:

- Cloudflare Pages Git integration.
- Framework preset: None.
- Build command: leave blank.
- Build output directory: `/`.
```

- [ ] **Step 7: Local smoke**

```bash
python3 -m http.server 4173
```

Expected:

- `http://localhost:4173` renders the page.
- No broken local CSS path.
- Mobile width keeps the table scrollable.

- [ ] **Step 8: Commit skeleton**

```bash
git add .gitignore README.md index.html assets/site.css
git commit -m "feat: add static ObviousBench website skeleton"
```

## Task 2: Add Release-Safe Data Import

**Files:**

- Create in website repo: `scripts/update-leaderboard.mjs`
- Create in website repo: `assets/leaderboard.json`
- Modify in website repo: `index.html`
- Modify in website repo: `README.md`

- [ ] **Step 1: Create a small JSON contract**

Use this schema in `assets/leaderboard.json`:

```json
{
  "status": "draft_placeholder",
  "generated_at": "2026-06-01",
  "rows": [
    {
      "rank": 1,
      "model": "Example model",
      "correct": null,
      "ci": null,
      "strict": null,
      "cost": null
    }
  ]
}
```

- [ ] **Step 2: Add importer script**

`scripts/update-leaderboard.mjs` should read a curated CSV copied from the benchmark repo, not raw provider outputs.

```js
import fs from "node:fs";

const input = process.argv[2];
const output = process.argv[3] || "assets/leaderboard.json";

if (!input) {
  console.error("Usage: node scripts/update-leaderboard.mjs <curated-results.csv> [output.json]");
  process.exit(2);
}

const csv = fs.readFileSync(input, "utf8").trim().split(/\r?\n/);
const [headerLine, ...lines] = csv;
const headers = headerLine.split(",");

function rowObject(line) {
  const values = line.split(",");
  return Object.fromEntries(headers.map((header, index) => [header, values[index] ?? ""]));
}

const rows = lines.map(rowObject).slice(0, 20).map((row, index) => ({
  rank: index + 1,
  model: row.label || row.model || "Unknown",
  correct: row.answer_accuracy || "",
  ci: row.answer_ci || "",
  strict: row.strict_accuracy || "",
  cost: row.estimated_cost_usd || ""
}));

fs.writeFileSync(output, JSON.stringify({
  status: "draft_placeholder",
  generated_at: new Date().toISOString().slice(0, 10),
  rows
}, null, 2) + "\n");
```

- [ ] **Step 3: Add README import command**

Add this text to `README.md`:

```text
Update leaderboard data:

node scripts/update-leaderboard.mjs /path/to/curated-paper-results.csv
```

- [ ] **Step 4: Commit importer**

```bash
git add README.md scripts/update-leaderboard.mjs assets/leaderboard.json
git commit -m "feat: add release-safe leaderboard data contract"
```

## Task 3: Configure Cloudflare Pages

**Files:**

- No required repository files.
- Optional create in website repo: `_headers`

- [ ] **Step 1: Connect GitHub repo to Pages**

Cloudflare dashboard:

1. Go to `Workers & Pages`.
2. Create application.
3. Choose `Pages`.
4. Choose `Connect to Git`.
5. Select the private `website-obviousbench-com` GitHub repository.

Build settings:

- Framework preset: None.
- Build command: blank.
- Build output directory: `/`.
- Production branch: `main`.

- [ ] **Step 2: Confirm first deploy**

Expected:

- Cloudflare deploys the static files.
- The site is reachable on a temporary `*.pages.dev` URL.
- Pushing to `main` triggers a new deployment.

- [ ] **Step 3: Add `_headers`**

```text
/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=()
```

- [ ] **Step 4: Commit headers**

```bash
git add _headers
git commit -m "chore: add static site security headers"
```

## Task 4: Add Custom Domain

**Files:**

- Modify in website repo: `README.md`

- [ ] **Step 1: Register domain**

Preferred:

- `obviousbench.com`

Expected:

- Domain is registered and controlled by the user.
- Domain is added to the user's Cloudflare account as a zone if using apex domain deployment.

- [ ] **Step 2: Attach domain in Cloudflare Pages**

Cloudflare dashboard:

1. Open the Pages project.
2. Go to `Custom domains`.
3. Select `Set up a domain`.
4. Enter `obviousbench.com`.
5. Complete DNS/zone setup as requested by Cloudflare.

- [ ] **Step 3: Add `www` redirect or alias**

Preferred production behavior:

- `https://obviousbench.com` is canonical.
- `https://www.obviousbench.com` redirects to apex, or is configured as a second custom domain.

- [ ] **Step 4: Document production URL**

Add to `README.md`:

```markdown
Production:

- https://obviousbench.com
- Cloudflare Pages project: obviousbench
```

- [ ] **Step 5: Commit domain docs**

```bash
git add README.md
git commit -m "docs: record ObviousBench website production domain"
```

## Task 5: Launch Checklist

**Files:**

- Modify in website repo: `index.html`
- Modify in website repo: `assets/leaderboard.json`
- Modify in website repo: `README.md`

- [ ] Replace draft leaderboard values with frozen paper-sweep answer-correctness results.
- [ ] Link `Report` to arXiv or the stable PDF.
- [ ] Link `Dataset` only after the public dataset repo or artifact is approved.
- [ ] Link `Code` only after the public code repo or release branch is approved.
- [ ] Add BibTeX only after arXiv metadata exists.
- [ ] Remove or soften any claim not backed by a frozen artifact.
- [ ] Test desktop viewport.
- [ ] Test mobile viewport.
- [ ] Confirm Cloudflare deployment URL and custom domain both load.
- [ ] Confirm no private files are committed:

```bash
git status --short
git ls-files | rg 'provider|raw|secret|\\.env|human_baseline|results/summaries'
```

Expected:

- The `rg` command prints no private/raw artifact paths.

## Acceptance Criteria

- A private GitHub repo deploys a public static ObviousBench website through Cloudflare Pages.
- The first viewport clearly says `ObviousBench` and the benchmark tagline.
- The style is sparse and academic, similar in spirit to SimpleBench, without copying its exact page.
- The public site reports answer correctness as the headline metric.
- Strict/format compliance are visible but secondary.
- The site has no raw provider logs, unpublished datasets, private human-baseline data, or secrets.
- Domain setup is documented after registration.

## Parking Notes

This plan is intentionally not executed yet. When resumed, start by confirming:

1. domain choice and registration status;
2. whether the website repo should be created under Adam's personal GitHub account;
3. whether the site can show draft placeholder results or should wait for final paper-sweep artifacts.
