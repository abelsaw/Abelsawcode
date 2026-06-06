---
name: viral-watch
description: On-demand research brief on viral news stories with implications for workforce/labor and/or culture/equity/values, with a default focus on Southeast Asia (Singapore, Indonesia, Malaysia, Thailand, Philippines, Vietnam, Cambodia, Laos, Myanmar, Brunei). Identifies stories that surged across ≥3 catalog news outlets within 48-72 hours, verifies the facts against primary sources, separates verified content from hype/distortion, and produces a 1-2 page analytical report per story (NOT for posting). Use when the user says "what's gone viral", "what's blowing up this week", "viral watch", "society pulse", or invokes /viral-watch.
---

# Viral watch — on-demand societal-implication brief

You are running the `viral-watch` skill. Produce a **research-grade Markdown report** on the top viral stories of the resolved window that carry implications for **workforce/labor** and/or **culture/equity/values**.

This skill is for **internal awareness and analysis** — NOT for LinkedIn publishing. The voice is analytical and sober, not first-person opinion.

## Optional arguments (parsed from the skill `args` string)

- `window: <N>d` — look back N days from today (default: `7d`, max: `14d`). Viral signal degrades quickly past two weeks.
- `lens: <workforce|culture|both>` — restrict the lens (default: `both`).
- `count: <N>` — produce N deep-dive entries (default: `3`, cap: `5`).
- `region: <sea|apac|us|global|eu>` — bias toward stories landing in the named region. **Default: `sea`** (Southeast Asia: Singapore, Indonesia, Malaysia, Thailand, Philippines, Vietnam, Cambodia, Laos, Myanmar, Brunei). Use `apac` to widen to all Asia-Pacific including India, Japan, Korea, China, Australia; `global` to remove regional anchoring; `us` or `eu` for those regions.

If args are empty, run defaults: 7-day window, both lenses, 3 deep dives, **SEA region**.

---

## Step 1 — Read source catalog and usage history

Read **two** inputs before researching:

1. `.claude/skills/viral-watch/sources.md` — the curated catalog of news / culture / labor / global outlets used to measure cross-media surge.
2. `.claude/skills/viral-watch/usage-history.md` — every story URL covered in prior runs. If the file doesn't exist yet, treat history as empty (first run).

From the usage history, extract the **exclusion set**: every story URL covered in the **last 3 runs**. Stories on the list are off-limits — pick a different angle or a different story instead.

## Step 2 — Compute the window

- Today's date is in context. Default window: today minus 7 days through today.
- If `window: <N>d` is passed, use that.
- Print the resolved window before researching: `Window: {start} to {end}`.

## Step 3 — Surge research (the viral signal)

A story qualifies as "viral" when it meets ALL of:

1. **Cross-media surge:** the story is covered by **≥3 catalog news outlets** within a **48-72 hour cluster** inside the resolved window. The cluster matters — slow-burn stories don't count as viral here even if total coverage is high.
2. **Tier-1 anchor:** at least one of those catalog outlets is from the **Tier-1 group** in `sources.md` (global tier-1 news, AI-era specialty culture/labor magazines of record, or a flagship public broadcaster).
3. **Lens fit:** the story carries a clear implication for at least one of the two lenses:
   - **Workforce & labor:** layoffs, automation, AI displacement, unions, gig work, education-to-work pipeline, immigration & talent flows, work-from-home shifts.
   - **Culture, equity & values:** identity, social movements, DEI, free speech, generational shifts, attention economy, religion, sport-as-culture, language, online community dynamics.

Sweep WebSearch against the catalog. For candidates that look promising, **WebFetch the lead source** to confirm dates and key facts. Never include a story you have not actually read.

**Velocity boost (tiebreaker):** when two stories have the same outlet count, the one that surged in a tighter window (24-48h) ranks higher than the one that spread across the full 72h.

**Region weighting (default `sea`):**
- **With `region: sea` (default),** apply SEA as a relevance and ranking weight. **Topic filter:** prioritize stories that originated in or materially affect at least one of the ten SEA countries (Singapore, Indonesia, Malaysia, Thailand, Philippines, Vietnam, Cambodia, Laos, Myanmar, Brunei). **Source weighting:** prefer the SEA Tier-1 outlets in `sources.md` (Straits Times, CNA, Jakarta Post, Bangkok Post, Inquirer, Rappler, The Star Malaysia, Malay Mail, VnExpress, etc.) as primary cross-citation sources; treat global Tier-1 (Reuters, BBC, AP, FT) as second citations when they cover the same SEA story. A story that's pure US/EU/non-SEA but is being amplified in SEA media still counts when it's clearly landing locally (e.g. a US tech layoff that hits regional staff). A pure US-domestic story without SEA resonance is dropped.
- **With `region: apac`,** widen to all Asia-Pacific (include India, Japan, Korea, China, Australia, NZ, plus SEA).
- **With `region: global`,** no regional anchoring; rank by raw surge magnitude across the full catalog.
- **With `region: us` or `region: eu`,** focus on that geography.

Aim to identify **8-12 surge candidates** in the window, then pick the top `count:` (default 3) by surge magnitude × lens-fit weight × region-fit weight.

## Step 4 — Verify and separate fact from hype

For each picked story:

1. **Identify the primary source** (the original report, court filing, government release, company statement, or first credible outlet).
2. **WebFetch the primary source if reachable.** Note what is directly verifiable from primary sources vs. what is being amplified secondhand.
3. **Track the framings** different outlets used. When a story is being read differently by different audiences (left/right, in-group/out-group, professional/lay, regional), capture those framings as observed facts — not as the brief's own positions.
4. **Flag hype patterns:** missing context, mis-attributed quotes, statistics from non-primary sources, viral-but-uncorroborated claims, AI-generated misinformation indicators.

The brief's voice is **sober and analytical**. It does not take sides between contested framings — it surfaces them.

## Step 5 — Save the report

Save to `reports/viral-watch/YYYY-MM-DD.md` (date = today). Use this template:

```markdown
# Viral watch — {YYYY-MM-DD}
Window: {start_date} to {end_date}
Lens(es): {workforce | culture | both}
Region focus: {us | global | apac | eu}

## Surge candidates considered ({N total})
- {slug} — {one-line headline} — {outlet count} — {tier-1 anchor: Y/N} — {lens fit}
- ...

## Deep-dive 1 — {slug}

### Headline & current framing
{1-2 sentences on what the story is and how it is being framed publicly.}

### Surge signals
- **Window of surge:** {YYYY-MM-DD HH:MM to YYYY-MM-DD HH:MM} ({hours} hours)
- **Catalog outlets covering:** {N} (Tier-1: {names}; second-citation: {names})
- **Notable velocity tells:** {e.g. "covered by both BBC and Fox in the same 6-hour window", "trended on Reddit r/news for 14h", "Wikipedia article created within 24h"}
- **Primary source:** {Outlet}, {date}, {URL}

### What's verified
{Facts that trace to the primary source or to ≥2 catalog Tier-1 outlets. List as bullets.}

### What's amplified or distorted
{Patterns of misframing, missing context, mis-attributed quotes, viral-but-uncorroborated claims. Specific, not vague.}

### Societal implication — Workforce & labor
{2-3 sentences on how this story sits in the workforce/labor landscape. Skip this subsection if lens is culture-only.}

### Societal implication — Culture, equity & values
{2-3 sentences on how this story sits in the culture/equity/values landscape. Skip this subsection if lens is workforce-only.}

### Contested framings observed
- **Framing A ({audience}):** {one sentence}
- **Framing B ({audience}):** {one sentence}
- **Framing C ({audience}):** {one sentence, if present}

### Open questions for the next 7-14 days
- {question}
- {question}

### Sources
- {Outlet}, {date} — {URL}
- ...

## Deep-dive 2 — {slug}
{same structure}

## Deep-dive 3 — {slug}
{same structure}

## Stories considered but not picked
- {slug} — {one-line headline} — {reason dropped, e.g. "below surge bar", "lens-fit thin", "primary source unreachable", "in exclusion set from prior run"}
```

## Step 6 — Persist any newly discovered sources

If a credible outlet surfaced repeatedly and meets the discovery rules in `sources.md`, append it to the **Auto-discovered sources** section. Be conservative.

## Step 7 — Append to usage history

Immediately after saving the report (BEFORE presenting):

```markdown
### Run of {YYYY-MM-DD}
- Window: {start} to {end}
- Lens(es): {lens(es)}
- Stories covered:
  1. {slug-1}: {primary URL}
  2. {slug-2}: {primary URL}
  3. {slug-3}: {primary URL}
- Report path: reports/viral-watch/{YYYY-MM-DD}.md
```

Append to the top of the "Past runs (most recent first)" section. Create the file if it does not exist.

## Step 8 — Present compactly to the user

Show, in this order:

1. **Resolved window** and **lens(es)**.
2. **Surge candidates considered** — short table of slugs + outlet counts.
3. **The 3 deep dives** — slug, the headline, and 2-3 lines summarizing the verified facts + the most important contested framing.
4. **The report path** (`reports/viral-watch/YYYY-MM-DD.md`).

End with: "Want a deeper dive on any one of these, a different window, or a different lens?"

---

## Hard rules

- **≥3 catalog news outlets covering the story within 48-72h** — that's the viral bar. Slow-burn or single-outlet stories don't qualify.
- **≥1 Tier-1 catalog anchor** in the qualifying outlet set.
- **Lens fit required** — workforce/labor and/or culture/equity/values implication must be specific, not generic ("everyone is talking about AI" is not a lens fit).
- **Verify the primary source** for each deep dive. If primary source is unreachable, mark `[primary source unverified]` and flag the brief as provisional.
- **Sober, analytical voice.** Third person. The brief surfaces contested framings — it does not take sides between them.
- **No fabrication.** Every URL is one you actually fetched (or attempted to fetch with the failure logged). Every claim traces to a named source.
- **No story duplication across the last 3 runs.** Usage history is the ledger.
- **Not for posting.** This is internal research. If the user wants a LinkedIn post, they should use `/weekly-summary`.

## Output locations (recap)

- Report: `reports/viral-watch/YYYY-MM-DD.md`
- Source catalog: `.claude/skills/viral-watch/sources.md`
- Usage history: `.claude/skills/viral-watch/usage-history.md`
