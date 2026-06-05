---
name: weekly-summary
description: Generate a single LinkedIn weekly-summary post for a Chief Transformation Officer covering the 10 most-cited stories of the Mon-Fri window across AI, Technology, HR, and strategy — ranked most-mentioned to least across a curated set of AI labs, big tech, strategy firms, and tier-1 news. Use when the user says "give me a weekly summary post", "draft my week-in-review", "wrap up the week", or invokes /weekly-summary.
---

# Weekly summary — Friday wrap on AI, Technology, HR, and strategy

You are running the `weekly-summary` skill. Produce **one LinkedIn post (text only, no image)** that surfaces the **10 most-cited stories of the Mon-Fri window**, ranked from most-mentioned to least-mentioned across the source catalog, written in the first-person voice of a **Chief Transformation Officer** reflecting on what shifted this week across AI, Technology, HR, and strategy.

The skill is designed for a **Friday afternoon manual trigger** covering the **Monday-Friday window of the current week**.

## Optional arguments (parsed from the skill `args` string)

- `week: previous` — cover Mon-Fri of the previous week instead of the current week. Default: current week.
- `week: YYYY-MM-DD..YYYY-MM-DD` — explicit window override.
- `theme: <topic>` — bias the picks toward a specific lens (e.g. `theme: agentic AI in HR`). Default: pure cross-citation ranking, no theme filter.
- `sources: +<Source1>, -<Source2>` — add or exclude sources beyond the catalog.
- `count: N` — produce a ranked list of N stories instead of 10 (cap at 15).
- `urls: on` — include source URLs inline in the post body. Default: off (URLs live in the research brief only).

If args are empty, run defaults: current week Mon-Fri, no theme filter, 10 ranked stories, URLs off.

---

## Step 1 — Read source catalog and usage history

Read **two** inputs before researching:

1. `.claude/skills/weekly-summary/sources.md` — the canonical AI / Tech / HR / strategy / news source catalog plus any auto-discovered sources from prior runs.
2. `.claude/skills/weekly-summary/usage-history.md` — every story URL and ranked list used in prior weekly-summary runs. If the file does not exist yet, treat the history as empty (this is the first run).

From the usage history, extract the **exclusion set**: every story URL that appeared in the **last 3 weekly-summary runs**. Stories on this list are off-limits for this run — pick the next-strongest story instead. Theme overlap across weeks is allowed (some topics are sustained); story duplication is not.

## Step 2 — Compute the week window

- Today's date is provided in context. The Friday of the current week is the end of the window.
- If today is Mon-Thu, the default window is the prior Mon-Fri (the most recently completed week). Tell the user you're covering the prior week and proceed.
- If `week: previous` is passed, shift the window back one week.
- If `week: YYYY-MM-DD..YYYY-MM-DD` is passed, use that exact range.
- Print the resolved window before researching: `Window: {start} to {end}`.

## Step 3 — Research across AI, Technology, HR, and strategy

Run WebSearch queries against the catalog, biasing toward:

- **AI labs:** Anthropic, OpenAI, Google DeepMind — model releases, research papers, policy/safety announcements, enterprise launches.
- **Big tech research:** Microsoft, AWS, Google — enterprise AI, workforce-shaping product launches, infrastructure shifts.
- **Strategy firms:** McKinsey, BCG, Deloitte, WTW, Mercer, Gallup, WEF, Aon, PwC — published research, surveys, executive briefings.
- **Tier-1 news:** FT, WSJ, NYT, HBR, Bloomberg, Reuters, The Information, MIT Technology Review, MIT Sloan Management Review, The Economist — features and analyses on the above.
- **HR / future-of-work outlets:** SHRM, HR Dive, HR Executive — only when a story is genuinely cross-cited there.

For each candidate, **WebFetch the source** to confirm date, claims, and that it falls inside the resolved week. Never include a story you have not actually read.

**Ranking signal (most-cited across credible sources):** a story is more "popular" the more independent credible outlets covered it within the week. **Cross-citation count is the primary ranking signal** — most-cited at rank 1, least-cited at rank 10. Use novelty and CTO relevance only to break ties when two stories have the same citation count.

Aim to surface **15-20 ranked candidates** so you can confidently identify the top 10 by citation count (with the next 5-10 visible for tie-breaks and audit).

## Step 4 — Rank 10 stories by citation count

From the candidate pool, select the **top 10 by cross-citation count**, ranked most-cited (rank 1) to least-cited (rank 10).

Each ranked story must:
- Be inside the resolved week window.
- Come from at least 2 credible sources in the catalog (cross-citation bar).
- Not be on the exclusion set from the prior 3 runs.

If fewer than 10 stories clear the ≥2-citation bar, fill to 10 with the next-strongest candidates and **flag in the brief** which entries cleared by a thinner margin. If fewer than 6 clear the bar, stop and report back so the user can relax constraints.

A **shared theme is optional**, not required. If a clean through-line emerges from the top stories, name it in the brief and the post. If not, present the ranked list as a landscape view — the value is the ranking, not the synthesis.

## Step 5 — Save the research brief

Save to `posts/drafts/weekly-research-YYYY-MM-DD.md` (date = the resolved Friday) using this template:

```markdown
# Weekly research brief — {Friday YYYY-MM-DD}
Window: {Mon YYYY-MM-DD} to {Fri YYYY-MM-DD}

## Through-line (optional)
{One-sentence statement of the connecting thread if one emerges, or "No single through-line this week — see ranked landscape below."}

## Ranked top 10 (most-cited → least-cited)

### 1. {short slug} — {citation count}
- **Headline:** {original headline}
- **Lead source:** {Outlet}, {date}, {URL}
- **Also covered by:** {other outlets in the catalog, with dates}
- **What happened:** {3-4 sentence factual summary, no interpretation}
- **Why a CTO cares:** {1-2 sentences on the implication}

### 2. {short slug} — {citation count}
...

### 10. {short slug} — {citation count}
...

## Candidates considered but not in the top 10
- {headline} — {citation count} — {reason ranked below the cut}
```

## Step 6 — Persist any newly discovered sources

If your searches surfaced credible new outlets/firms not yet in `sources.md` that you actually cited in the brief, append them to the **Auto-discovered sources** section using the format in `sources.md`. Be conservative — only add sources that meet the discovery rules in the catalog.

## Step 7 — Draft one ranked-digest post

Save to `posts/drafts/weekly-summary-YYYY-MM-DD.md`. Produce **one post** with this shape:

- **Opening (50-80 words):** short CTO framing of the week — the through-line if one emerged, otherwise the landscape ("ten things landed this week; here they are in order of how loudly").
- **Ranked items 1-10:** each entry is **2-3 sentences (~30-45 words)** — the headline as one line, then the CTO read on it. Numbered explicitly. No source URLs by default (set `urls: on` to include them).
- **Closing (40-80 words):** the one move the CTO is making off the back of the week, or the open question they're carrying.
- **3-5 hashtags** off the week's themes.

Target body length: **400-600 words** excluding hashtags. **Hard cap: 2,900 characters** (LinkedIn's limit is 3,000).

Use this file template (the `---POST---` / `---END---` markers matter — `linkedin-publisher` reads them to extract the publishable text):

```markdown
# Weekly summary — {Friday YYYY-MM-DD}

## Post 1 — {slug}
- **Through-line:** {one-line if any, else "landscape view"}
- **Stories ranked 1-10:** {comma-separated slugs in ranked order}
- **Word count:** {N} (excl. hashtags)
- **Character count:** {M}
- **Source URLs in body:** {on|off}
- **Status:** draft

---POST---
{Opening framing.}

1. {Story 1 headline}. {1-2 sentence CTO read.}

2. {Story 2 headline}. {1-2 sentence CTO read.}

...

10. {Story 10 headline}. {1-2 sentence CTO read.}

{Closing — the move or the open question.}

#Hashtag1 #Hashtag2 #Hashtag3
---END---
```

## Step 8 — Voice & length enforcement

The CTO voice is **professional, progressive, bold, humble, and learning** — bold AND humble in the same breath. Take a position on the landscape; show you're still figuring it out.

Voice rules:
- **First person.** "I sat with ten stories this week." "What I'm watching." "I don't have the answer yet."
- **Bold.** Stand behind the ranking. Strong declaratives in the CTO reads. No hedging the whole post.
- **Progressive.** Forward-looking. Frame what's becoming possible, not what's broken.
- **Humble.** Name what you don't know. Worn lightly — confidence and curiosity together.
- **Learning.** Show the update where it lands ("two weeks ago I would have said X").
- **No corporate jargon, no hype words, no emojis.**
- **No AI-tells:** delve, tapestry, navigating the landscape, in conclusion, moreover, furthermore, in today's fast-paced world.
- **Each ranked item is 2-3 sentences max.** Numbered prefix. The headline first, then the CTO read.
- **3-5 hashtags max**, lowercase or CamelCase, off the themes of the week.

Length enforcement: before presenting to the user, **count words in the `---POST---` block (excluding hashtags) and confirm it is between 400 and 600. Confirm character count is under 2,900.** If outside the range, revise. Report both counts to the user.

## Step 9 — Present compactly to the user

Show, in this order:

1. **Resolved window** and **through-line** (or "landscape view, no single through-line").
2. **The ranked top 10** — slug, citation count, lead source, one-line headline. Most-cited at the top.
3. **The drafted post** — slug, word count, character count, first 200 chars of the body.
4. **Path to the draft file and research brief.**

End with: "Want me to revise it, or publish?"

## Step 9.5 — Append to usage history

Immediately after the draft is written (BEFORE the user picks publish), append to `.claude/skills/weekly-summary/usage-history.md`:

```markdown
### Week of {Friday YYYY-MM-DD}
- Through-line: {one-liner if any, else "landscape view"}
- Ranked stories 1-10:
  1. {slug-1}: {URL} — {citation count}
  2. {slug-2}: {URL} — {citation count}
  ...
  10. {slug-10}: {URL} — {citation count}
- Post slug: {post-slug}
- Date: {YYYY-MM-DD}
```

Append to the top of the "Past weeks (most recent first)" section. Create the file if it does not exist.

## Step 10 — Publish on approval

When the user approves, delegate to `linkedin-publisher`:

```bash
python3 scripts/linkedin_post.py posts/drafts/weekly-summary-YYYY-MM-DD.md \
  --slug <chosen-slug> \
  --dry-run
```

Show the dry-run output. On explicit "yes" / "publish", re-run without `--dry-run`. No carousel, no image — weekly summary is text-only.

If `LINKEDIN_ACCESS_TOKEN` or `LINKEDIN_AUTHOR_URN` are not set, walk the user through `.env.example` instead of attempting to publish.

---

## Output locations (recap)

- Research brief: `posts/drafts/weekly-research-YYYY-MM-DD.md`
- Post draft: `posts/drafts/weekly-summary-YYYY-MM-DD.md`
- Source catalog: `.claude/skills/weekly-summary/sources.md`
- Usage history: `.claude/skills/weekly-summary/usage-history.md`

## Hard rules

- **Mon-Fri window only.** Every story dates inside the resolved week. No older stories framed as this week's.
- **Top 10 ranked by cross-citation count.** Most-mentioned at rank 1. Ties broken by novelty and CTO relevance.
- **Each story cross-cited by ≥2 credible sources** in the catalog (flag any rank that clears by a thinner margin).
- **400-600 words per post body** (excluding hashtags). **Under 2,900 characters total.** Verify before presenting.
- **No story repeats across the last 3 weekly summaries.** The usage history is the ledger.
- **No fabrication.** Every URL is one you actually fetched. Every claim traces to a source in the brief.
- **No images, no carousel.** Weekly summary is text-only by design.
- **URLs default off** in post body — `urls: on` to include them. Citations always remain in the research brief.
- **Bold AND humble.** The voice takes positions on the ranking and admits what it's still learning, in the same post.
