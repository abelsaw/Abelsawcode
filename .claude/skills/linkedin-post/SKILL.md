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

## Step 1 — Read the source catalog, usage history, and attached PDFs

Read **three** inputs before invoking the scout:

1. `.claude/skills/linkedin-post/sources.md` — the canonical Tier 1 / Tier 2 / Tier 3 source catalog plus any auto-discovered sources from prior runs.
2. `.claude/skills/linkedin-post/usage-history.md` — every theme/slug used in prior runs of this skill.
3. `reports/2026/` — any user-attached full PDFs of 2026 research reports. List the directory recursively; note which firms have a PDF present. The scout uses these as primary sources, tagging extracted claims `[PDF: {filename}, p.{n}]` instead of `[search-only]`. A parent theme on the dedup ledger CAN recycle when a PDF surfaces a fresh sub-angle (cite page/exhibit).

From the usage history, extract the **exclusion set**: every parent theme whose entry is dated within the last **14 days** (the default dedup window). These themes are off-limits for this run unless the user explicitly overrides ("I want a different angle on managers" or similar).

Match exclusions on **parent theme**, not slug — two slugs about "Human-AI work redesign" share the same parent and both count as used.

## Step 2 — Delegate to `hr-best-practices-scout`

Invoke the `hr-best-practices-scout` agent with a prompt that includes:

- Today's date (compute from context).
- A 2026-only window directive.
- The full source catalog content (Tier 1 + Tier 2 + Tier 3 + Auto-discovered).
- The user's `theme:` override and any `+sources` / `-sources` adjustments.
- **The regional lens directive (default `apac` = relevance filter, not framing mandate):**
  - "With `region: apac` (default), apply APAC as a **relevance filter on themes**, not a framing mandate. **Topic filter:** only surface themes applicable to APAC employers. Drop themes that are US-only or Europe-only and don't reach APAC (e.g. US-specific NLRB rulings, US state-level labor law). Themes that touch APAC multinationals via global rules pass (e.g. EU Pay Transparency landing on European subsidiaries of APAC firms). **Sources:** still sweep Tier 3 (Hays, Robert Walters, Michael Page, INSEAD, ILO Asia-Pacific, ADB, Singapore MOM, AHRI, HKIHRM, People Matters, HR Asia) and pull APAC breakouts of Tier 1/2 when they add value. **Data:** cite APAC stats as evidence when they materially differ from the global picture; otherwise universal stats are fine. **Don't write briefs that frame every theme as 'APAC's biggest…' — the goal is general best practices that happen to be relevant to APAC.**"
  - "With `region: global`, treat Tier 3 as supplementary and prioritize globally-applicable findings."
- **The discovery directive (when `discover` is not `off`):** "During your searches, if you encounter 2026 HR research from a credible firm NOT in the catalog that adds new convergence to a theme you're surfacing, USE it and report it back so it can be added to the catalog. In APAC mode, weight discovery toward APAC-credible firms (e.g. Korn Ferry APAC, IBM IBV APAC, Egon Zehnder APAC, regional NUS / HKUST research centers). Apply the discovery rules in `.claude/skills/linkedin-post/sources.md`."
- **The dedup exclusion set:** "The following parent themes have been used in /linkedin-post runs within the last 14 days and are OFF-LIMITS for this run unless the user explicitly overrides: {paste the list from usage-history.md}. Do not surface these themes as top candidates. If a brief candidate falls under an excluded parent theme, drop it and pick a different angle from a non-excluded theme. If fewer than 3 non-excluded themes meet the ≥2-firm bar, stop and report so the user can decide whether to relax the dedup window or accept a smaller set."
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

Invoke the `hr-best-practices-writer` agent with the same dedup exclusion
set you gave the scout. The writer must NOT draft a post on an excluded
parent theme. If the brief surfaces an angle that maps to an excluded
parent theme, the writer should pick a different angle from a non-excluded
theme instead.

The writer reads the research brief and produces:

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
- **Universal best-practices framing is the default.** Don't open posts with "APAC's biggest..." or "APAC moved past..." style leads. Write as a senior CHRO sharing a general insight that happens to land in APAC.
- **Weave APAC data into the body as evidence**, not as the headline. Example: instead of "APAC's medical trend is the highest in the world," write "Medical inflation is rewriting benefits strategy. WTW 2026: global 10.3%, with APAC leading at 14%."
- **Filter, don't force.** If a topic doesn't apply to APAC employers (e.g. US-only NLRB rulings, US state labor law), don't draft a post on it. If a topic applies universally, treat it universally and only invoke APAC where the data adds material dimension.
- **Hashtags default to universal.** `#APAC`, `#FutureOfWorkAsia`, `#ASEAN`, `#SingaporeHR`, `#AsiaCHRO` are optional — use only when the post specifically targets APAC employers (e.g. regional regulatory deadlines).

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

## Step 6.5 — Append to usage history

Immediately after the writer has produced the drafts (BEFORE you ask the user to review), append entries to `.claude/skills/linkedin-post/usage-history.md` for **each option drafted**. This is what protects future runs from overlap. Format:

```markdown
### {Parent theme label}
- Slugs: {slug-1}, {slug-2 if multi-slug-for-same-theme}
- Source stats: {one-line summary of the key stats used}
- Commits: {commit hash once the run is committed}
- Date(s): {YYYY-MM-DD}
```

If a parent theme already has an entry in the file (from a prior run that the user has chosen to recycle), ADD the new slug and the new date to that entry rather than creating a duplicate.

Append the entries to the top of the "Used themes (most recent first)" section so the most recent runs are easy to scan.

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
- **No theme overlap with prior runs.** Before drafting, the skill reads `.claude/skills/linkedin-post/usage-history.md` and excludes parent themes used within 14 days. After drafting, the skill appends the newly-used themes to the ledger. The user can manually delete an entry to allow recycling. If fewer than 3 non-excluded themes meet the cross-firm bar, stop and ask before drafting a smaller set.
