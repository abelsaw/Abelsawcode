---
name: linkedin-post
description: Generate 3 LinkedIn post options (≤50 words each) plus matching 5-slide bold-editorial carousels on HR best practices for a CHRO, sourced from 2026 research reports across Mercer, Aon, McKinsey, WEF, BCG, WTW, Deloitte, Gallup and other credible firms. The skill can actively discover NEW credible 2026 sources during research and append them to the catalog. Use when the user wants fresh LinkedIn content — phrases like "give me LinkedIn post options", "draft a LinkedIn carousel", "create LinkedIn content", "I need new posts", or invokes /linkedin-post.
---

# LinkedIn post + carousel — on-demand

You are running the `linkedin-post` skill. Produce **3 LinkedIn post options
(each ≤50 words)** with matching **5-slide bold-editorial carousels**, sourced
from 2026 HR research, ready for the user to review and publish.

## Optional arguments (parsed from the skill `args` string)

- `region: <apac|global>` — geographic lens. **Default: `apac`.** Asia Pacific is the default audience and source-weighting for this CHRO. Pass `region: global` to remove the regional anchor.
- `theme: <topic>` — scope the posts to one topic (e.g. `theme: AI in HR`, `theme: pay transparency`). Default: surface the most-mentioned 2026 themes across the catalog.
- `sources: +<Firm1>, +<Firm2>` — include named firms in addition to the catalog. Use `-<Firm>` to exclude.
- `count: N` — produce N post options instead of the default 3 (cap at 5).
- `discover: off` — disable the new-source discovery pass (default: on).

If args are empty, run the default flow: `region: apac`, default themes, 3 options, discovery on.

---

## Step 1 — Read the source catalog

Read `.claude/skills/linkedin-post/sources.md`. It contains the canonical
Tier 1 and Tier 2 firms, plus any auto-discovered sources from prior runs.
This is the input for the scout phase.

## Step 2 — Delegate to `hr-best-practices-scout`

Invoke the `hr-best-practices-scout` agent with a prompt that includes:

- Today's date (compute from context).
- A 2026-only window directive.
- The full source catalog content (Tier 1 + Tier 2 + Tier 3 + Auto-discovered).
- The user's `theme:` override and any `+sources` / `-sources` adjustments.
- **The regional lens directive (default `apac`):**
  - "Apply the regional lens from `.claude/skills/linkedin-post/sources.md`. With `region: apac`, prioritize APAC regional breakouts of Tier 1/2 reports (e.g. Mercer Asia Talent Trends, McKinsey Asia, BCG Southeast Asia), sweep Tier 3 sources (Hays, Robert Walters, Michael Page, INSEAD, ILO Asia-Pacific, ADB, Singapore MOM, AHRI, HKIHRM, People Matters, HR Asia), and prefer APAC stats over global averages when both exist. Run queries like `'Mercer Asia Talent Trends 2026 findings'`, `'Hays Asia Salary Guide 2026'`, `'Robert Walters APAC Salary Survey 2026'`, `'Michael Page Talent Trends 2026 Singapore'`, `'INSEAD GTCI 2026'`, `'ILO Asia-Pacific Employment 2026'`. Surface APAC regulatory/market context where it adds dimension."
  - "With `region: global`, treat Tier 3 as supplementary and prioritize globally-applicable findings."
- **The discovery directive (when `discover` is not `off`):** "During your searches, if you encounter 2026 HR research from a credible firm NOT in the catalog that adds new convergence to a theme you're surfacing, USE it and report it back so it can be added to the catalog. In APAC mode, weight discovery toward APAC-credible firms (e.g. Korn Ferry APAC, IBM IBV APAC, Egon Zehnder APAC, regional NUS / HKUST research centers). Apply the discovery rules in `.claude/skills/linkedin-post/sources.md`."
- Reminder of environment limits: if WebFetch returns 403, fall back to search-indexed content and mark claims `[search-only]`.

Wait for the scout to save `posts/drafts/best-practices-research-YYYY-MM-DD.md`.
Sanity-check that the brief has ≥3 themes meeting the ≥2-Tier-1-firms bar.
In APAC mode, also confirm at least 2 themes carry APAC-specific data (not
just global averages).

## Step 3 — Persist any newly discovered sources

If the scout's report names new credible sources that were used in the brief,
append them to the **Auto-discovered sources** section of
`.claude/skills/linkedin-post/sources.md` using this format:

```markdown
### {Firm} — {Report title} ({Month YYYY})
- URL: {url}
- Contributed to theme: {short theme label}
- Discovered: {YYYY-MM-DD}
```

Be conservative — only add what passes the discovery rules in the catalog.

## Step 4 — Delegate to `hr-best-practices-writer`

Invoke the `hr-best-practices-writer` agent. The writer reads the research
brief and produces:

- `posts/drafts/best-practices-YYYY-MM-DD.md` with the N post options (default 3).
- 5-slide carousels at `posts/drafts/carousels/YYYY-MM-DD-option-N/slide-M.png`.

Style is locked: **bold editorial** (Style C) — top color band with the topic
tag (white, uppercase) and oversized slide number; cream body with a big sans
headline; short accent rule bottom-left. Accent rotates per option: navy (1),
rust (2), moss (3). Plum (4) and slate (5) for runs with `count: 4` or `5`.

All images are generated via `scripts/generate_post_image.py`.

## Step 5 — Voice & word-count enforcement

Each post body must be **highly professional, progressive, and bold** — first-person senior-CHRO voice. The writer takes a clear position and points forward without picking fights:

- **Bold** = stands behind a view, doesn't hedge, owns the take. Strong declaratives.
- **Progressive** = forward-looking. Frames the opportunity ahead, not the blame for what's broken.
- **Professional** = measured tone. No adversarial framing, no "you're doing it wrong" jabs, no rhetorical gotchas ("defensible in court?"), no attacks on roles or groups.

Voice rules:
- Open with a clear claim or forward-looking observation, not a headline restatement.
- Short sentences. Often one per line.
- No corporate jargon, no emojis, no hype words.
- No AI-tells: delve, tapestry, navigating the landscape, in conclusion, moreover, furthermore.
- Reflective questions ("Where does X sit in your stack?") are fine; loaded ones are not.
- 3-4 hashtags max.

**APAC framing (when `region: apac`):**
- Anchor at least one of the three options in an APAC-specific market reality where the brief supports it: Singapore/Hong Kong as regional hubs, ASEAN talent flows, India scaling, Japan/Korea workstyle reforms, Australia Fair Work, China labor law, or how global rules (EU Pay Transparency, US enforcement) reach APAC multinationals.
- Cite APAC stats when both APAC and global versions of a number exist (e.g. APAC thriving rate over the global one).
- Use APAC-leaning hashtags when relevant: `#APAC`, `#FutureOfWorkAsia`, `#ASEAN`, `#SingaporeHR`, `#AsiaCHRO` — alongside the global ones, not replacing them.
- Avoid parochialism — posts should still read for a global LinkedIn feed; APAC context adds dimension, doesn't wall the audience off.

**≤50 words per post body, including hashtags.** Hard cap. Verify each option's
word count by running:
```bash
python3 scripts/linkedin_post.py posts/drafts/best-practices-YYYY-MM-DD.md \
  --slug <slug> --dry-run
```
The script prints `Words: N` — confirm `N ≤ 50` for every option before
presenting to the user.

## Step 6 — Present compactly to the user

For each option, show:
- Slug, theme, sources, word count
- The post body (in a blockquote)
- Path to the carousel directory
- **An engagement-likelihood note** ranking the options (which is most likely to perform on LinkedIn and why — comment volume, controversy, save-worthiness, audience scope).

End with: "Want me to revise any of these, or publish one?"

## Step 7 — Publish on approval

When the user picks a specific option, delegate to `linkedin-publisher`:

```bash
python3 scripts/linkedin_post.py posts/drafts/best-practices-YYYY-MM-DD.md \
  --slug <chosen-slug> \
  --carousel-dir posts/drafts/carousels/YYYY-MM-DD-option-<N> \
  --image-alt "<slide-1 headline>" \
  --dry-run
```

Show the dry-run output. On explicit "yes" / "publish", re-run without
`--dry-run`. Never batch-publish without confirmation per option.

If `LINKEDIN_ACCESS_TOKEN` or `LINKEDIN_AUTHOR_URN` aren't set, walk the user
through the setup steps in `.env.example` instead of attempting to publish.

---

## Output locations (recap)

- Research brief: `posts/drafts/best-practices-research-YYYY-MM-DD.md`
- Post drafts: `posts/drafts/best-practices-YYYY-MM-DD.md`
- Carousel slides: `posts/drafts/carousels/YYYY-MM-DD-option-N/slide-M.png`
- Source catalog: `.claude/skills/linkedin-post/sources.md`

## Hard rules

- **2026-only sources.** No 2025-or-earlier reports cited as 2026.
- **≤50 words per post body**, including hashtags.
- **No fabrication.** Every stat traces back to a source in the brief.
- **5 slides per option, every time.** Three posts = three carousels = fifteen PNGs.
- **Persistence is silent but visible.** When you add a discovered source, mention it in your final report to the user ("Added Korn Ferry's 2026 Workforce Survey to the catalog — first time seen.") so they can audit the growing catalog.
