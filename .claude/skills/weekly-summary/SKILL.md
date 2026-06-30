---
name: weekly-summary
description: Generate a single LinkedIn weekly-summary post for a Chief Technology Officer focused purely on technology and AI — covering the 10 most-engaged tech/AI stories of the Mon-Fri window ranked by cross-platform engagement signal across LinkedIn, X/Twitter, Hacker News, and Reddit. Engagement is approximated via public visibility (WebSearch + visible like/upvote/point counts) — not API-measured. Use when the user says "give me a weekly summary post", "draft my week-in-review", "wrap up the week", or invokes /weekly-summary.
---

# Weekly summary — Friday wrap on Technology & AI (engagement-ranked)

You are running the `weekly-summary` skill. Produce **one LinkedIn post (text only, no image)** that surfaces the **10 most-engaged tech/AI stories of the Mon-Fri window**, ranked by **cross-platform engagement signal** across LinkedIn, X/Twitter, Hacker News, and Reddit, written in the first-person voice of a **Chief Technology Officer whose remit is AI strategy, infrastructure, and enterprise technology** — reflecting on what the practitioner community engaged with most this week.

## Fidelity caveat — read this first

This skill **does not call any social-platform engagement API**. It approximates engagement using publicly visible signals via WebSearch:

- LinkedIn posts surfaced in search results — visible like / comment / reshare counts when shown
- X/Twitter posts — visible like / repost / reply counts when shown
- Hacker News submissions — point count and comment count (publicly visible)
- Reddit submissions — upvote count and comment count (publicly visible)

The result is an **approximation, not a measurement**. Numbers are sampled, not exhaustive. Some platforms (especially LinkedIn) hide engagement counts behind login walls. State this caveat in every research brief and post so the reader knows the ranking is signal-based, not metric-perfect.

## Three lenses to keep balanced across the top 10

- **AI models & research** — frontier-lab releases, capability shifts, evaluations, safety, AI policy/regulation
- **Infrastructure & compute** — chips, data centers, capex, networking, hyperscaler buildouts
- **Enterprise tech & security** — adoption patterns, dev tools, productivity software, cybersecurity, enterprise AI deployment

Not every week will have a 3-3-4 split. Rank by cross-platform engagement first, then check for at least one story per lens — if a lens has zero entries in the top 10, name that in the brief.

The skill is designed for a **Friday afternoon manual trigger** covering the **Monday-Friday window of the current week**.

## Optional arguments (parsed from the skill `args` string)

- `week: previous` — cover Mon-Fri of the previous week instead of the current week. Default: current week.
- `week: YYYY-MM-DD..YYYY-MM-DD` — explicit window override.
- `theme: <topic>` — bias the picks toward a specific tech lens (e.g. `theme: agentic AI in enterprise`, `theme: AI chips`). Default: pure engagement ranking, no theme filter.
- `platforms: +<P1>, -<P2>` — add or exclude engagement platforms beyond the catalog default (LinkedIn / X / HN / Reddit).
- `count: N` — produce a ranked list of N stories instead of 10 (cap at 15).
- `urls: on` — include source URLs inline in the post body. Default: off (URLs live in the research brief only).

If args are empty, run defaults: current week Mon-Fri, no theme filter, 10 ranked stories, URLs off, all four platforms.

---

## Step 1 — Read source catalog and usage history

Read **two** inputs before researching:

1. `.claude/skills/weekly-summary/sources.md` — the canonical catalog: discovery-layer news outlets PLUS the engagement-platform sources (LinkedIn / X / HN / Reddit).
2. `.claude/skills/weekly-summary/usage-history.md` — every story used in prior weekly-summary runs. If the file does not exist yet, treat the history as empty (this is the first run).

From the usage history, extract the **exclusion set**: every story slug used in the **last 3 weekly-summary runs**. Stories on this list are off-limits for this run — pick the next-strongest by engagement instead. Theme overlap across weeks is allowed (some topics are sustained); story duplication is not.

## Step 2 — Compute the week window

- Today's date is provided in context. The Friday of the current week is the end of the window.
- If today is Mon-Thu, the default window is the prior Mon-Fri (the most recently completed week). Tell the user you're covering the prior week and proceed.
- If `week: previous` is passed, shift the window back one week.
- If `week: YYYY-MM-DD..YYYY-MM-DD` is passed, use that exact range.
- Print the resolved window before researching: `Window: {start} to {end}`.

## Step 3 — Discovery (find candidate stories)

The news catalog in `sources.md` is the **discovery layer** — it tells you what events HAPPENED inside the window. Sweep it the way prior versions of this skill did, but **only to assemble a candidate pool of 15-25 tech/AI stories** — not to rank.

Cover these discovery groups:
- **Tier-1 news (US + global/APAC):** TechCrunch, FT, WSJ, NYT, Bloomberg, Reuters, The Information, CNBC, The Economist, Axios, BBC, Guardian, Nikkei Asia, SCMP, Straits Times.
- **AI labs:** Anthropic, OpenAI, Google DeepMind, Meta AI, Mistral, Cohere, xAI.
- **Big tech newsrooms:** Microsoft, AWS, Google, NVIDIA, IBM, Intel, Oracle, Apple, Meta.

**Out of scope (do not include):** HR / workforce / talent / layoffs / org-design / culture / DEI. Even when a tech company runs a layoff cycle, the workforce angle is excluded by design.

## Step 4 — Engagement sampling (the new ranking signal)

For EACH candidate story from Step 3, run **targeted WebSearch queries against the four engagement platforms** to gauge how the community engaged with it.

Recommended query patterns:

**LinkedIn**
- `site:linkedin.com/posts "<story keywords>" "<month> 2026"` — surfaces individual public posts; check visible like/comment/reshare counts where shown
- `linkedin.com pulse "<topic>" <month> 2026` — surfaces LinkedIn articles (longer-form)
- Note: LinkedIn often hides counts behind login; record "engagement visible: yes/no/partial"

**X/Twitter**
- `site:x.com "<story keywords>"` and `site:twitter.com "<story keywords>"` — visible likes/reposts/replies when shown
- News aggregators often quote viral X posts with their numbers — search `"X post" "<story keywords>" likes`

**Hacker News**
- `site:news.ycombinator.com "<story keywords>"` — point count and comment count are publicly visible
- Hacker News rewards original-source submissions; expect to find the canonical story URL submitted there

**Reddit** (these subs are the AI/tech core)
- `site:reddit.com r/MachineLearning "<story keywords>"`
- `site:reddit.com r/singularity "<story keywords>"`
- `site:reddit.com r/OpenAI "<story keywords>"`
- `site:reddit.com r/Anthropic "<story keywords>"`
- `site:reddit.com r/LocalLLaMA "<story keywords>"`
- `site:reddit.com r/programming "<story keywords>"`
- `site:reddit.com r/technology "<story keywords>"`
- Reddit upvotes and comment counts are publicly visible

For each candidate, record:
- **Platform-signal count** (0-4): how many of the four platforms showed measurable engagement on this story
- **Visible engagement numbers per platform** (when available): "HN 1,247 points / 423 comments · Reddit r/MachineLearning 3.4k upvotes · LinkedIn ~12k likes (sampled) · X 8.2k reposts"
- **A rough engagement tier**: high / medium / low (qualitative — based on whether numbers stand out vs typical platform baselines for tech content)

## Step 5 — Rank by cross-platform engagement signal

Rank the candidates by, in this order:

1. **Platform-signal count first** — a story that lands measurably on 4 of 4 platforms ranks above a story that lands on 2, all else equal. This is the analogue of "cross-citation count" from prior versions.
2. **Within the same signal-count, by visible engagement volume** — sum the engagement signals where they're visible. Heuristic weights for unit-normalization:
   - HN point ×10 (rare, curated audience)
   - Reddit upvote ×1 (in the AI/tech subs above)
   - LinkedIn like ×2 (when visible)
   - X like ×1 (when visible)
   - HN/Reddit comment counts add a 0.5× multiplier (discussion depth signal)
3. **Tie-break by novelty and technical significance** — the original ranking signal moves down here.

Each ranked story must:
- Be inside the resolved week window (the underlying news event, not necessarily the engagement). It's fine if engagement accrued through Saturday; the underlying story must have broken Mon-Fri.
- Show measurable engagement on **at least 2 of 4 platforms** (cross-platform bar — analogue of the prior 2-citation rule).
- Not be on the exclusion set from the prior 3 runs.
- Be a tech / AI story (HR / workforce / culture excluded per Step 3).

If fewer than 10 stories clear the 2-platform bar, fill to 10 with the next-strongest single-platform candidates and **flag in the brief** which entries cleared by a thinner margin. If fewer than 6 clear the bar, stop and report back so the user can relax constraints.

A **shared theme is optional**. If a clean through-line emerges, name it. If not, present the ranked list as a landscape view.

## Step 6 — Save the research brief

Save to `posts/drafts/weekly-research-YYYY-MM-DD.md` using this template:

```markdown
# Weekly research brief — {Friday YYYY-MM-DD}
Window: {Mon YYYY-MM-DD} to {Fri YYYY-MM-DD}

## Fidelity note
Engagement is approximated via WebSearch + publicly visible counts.
Not API-measured. Numbers are sampled, not exhaustive.

## Through-line (optional)
{One-sentence statement of the connecting thread, or "No single through-line this week — see ranked landscape below."}

## Three-lens balance check (Models / Infra / Enterprise tech)
- Models & research: {ranks}
- Infrastructure & compute: {ranks}
- Enterprise tech & security: {ranks}

## Ranked top 10 (most-engaged → least-engaged)

### 1. {short slug} — engagement: {signal count}/4 platforms
- **Headline:** {original headline}
- **Lead source (discovery):** {Outlet}, {date}, {URL}
- **Engagement signal:**
  - LinkedIn: {visible likes/comments/reshares OR "counts hidden / sampled"}
  - X: {visible likes/reposts OR "not surfaced"}
  - Hacker News: {points / comments OR "not surfaced"}
  - Reddit: {sub / upvotes / comments OR "not surfaced"}
- **What happened:** {3-4 sentence factual summary, no interpretation}
- **Why a CTO cares:** {1-2 sentences on the technical or deployment implication}

### 2. {short slug} — engagement: {signal count}/4 platforms
...

### 10. {short slug} — engagement: {signal count}/4 platforms
...

## Candidates considered but not in the top 10
- {headline} — {signal count}/4 — {reason ranked below the cut}
```

## Step 7 — Persist any newly discovered sources

If your searches surfaced credible new discovery outlets OR engagement-platform subs not yet in `sources.md`, append them to **Auto-discovered sources** using the catalog's format.

## Step 8 — Draft one ranked-digest post

Save to `posts/drafts/weekly-summary-YYYY-MM-DD.md`. Produce **one post** with this shape:

- **Opening (50-80 words):** short CTO framing — note that ranking is by community engagement, not news coverage, and the through-line if one emerged.
- **Ranked items 1-10:** each entry is **2-3 sentences (~30-45 words)** — the headline as one line, then the CTO read on it. Numbered explicitly.
- **Closing (40-80 words):** the one move the CTO is making off the back of the week, or the open question they're carrying.
- **3-5 hashtags** off the week's tech themes.

Target body length: **400-600 words** excluding hashtags. **Hard cap: 2,900 characters** (LinkedIn's limit is 3,000).

Use this file template (the `---POST---` / `---END---` markers matter):

```markdown
# Weekly summary — {Friday YYYY-MM-DD}

## Post 1 — {slug}
- **Through-line:** {one-line if any, else "engagement landscape view"}
- **Ranking signal:** cross-platform engagement (LinkedIn / X / HN / Reddit), approximated via public visibility
- **Stories ranked 1-10:** {comma-separated slugs in ranked order}
- **Three-lens balance:** Models {N} · Infra {M} · Enterprise tech {K}
- **Word count:** {N} (excl. hashtags)
- **Character count:** {M}
- **Source URLs in body:** {on|off}
- **Status:** draft

---POST---
{Opening framing — mention "what the practitioner community engaged with most" rather than "what got covered most".}

1. {Story 1 headline}. {1-2 sentence CTO read.}

2. {Story 2 headline}. {1-2 sentence CTO read.}

...

10. {Story 10 headline}. {1-2 sentence CTO read.}

{Closing — the move or the open question.}

#Hashtag1 #Hashtag2 #Hashtag3
---END---
```

## Step 9 — Voice & length enforcement

Voice rules unchanged from prior versions:
- **First person.** "I sat with ten stories this week." "What I'm watching in the stack." "I don't have the answer yet."
- **Bold.** Stand behind the ranking. Strong declaratives in the CTO reads.
- **Technical, not technicalist.** Use real numbers when they sharpen the point.
- **Progressive.** Forward-looking.
- **Humble.** Name what you don't know.
- **Learning.** Show updates ("two weeks ago I would have said X").
- **No corporate jargon, no hype words, no emojis.**
- **No AI-tells:** delve, tapestry, navigating the landscape, in conclusion, moreover, furthermore.
- **Each ranked item is 2-3 sentences max.**
- **3-5 hashtags max.**

**Engagement-ranking-specific voice notes:**
- Mention up front that the ranking reflects what the community **engaged with**, not what news outlets covered. That difference is the value of this version.
- When a story has dramatic single-platform engagement (e.g. 5K HN points), call that out — it's a signal of depth, not just breadth.
- When a heavily-covered news story didn't generate platform engagement, that's worth naming in the closing — "the news cycle isn't always the practitioner cycle."

Length enforcement: before presenting, count words in the `---POST---` block (excluding hashtags) and confirm 400-600. Confirm chars under 2,900.

## Step 10 — Present compactly to the user

Show, in this order:

1. **Resolved window** and **through-line** (or "engagement landscape view").
2. **The ranked top 10** — slug, platform-signal count, key engagement number, one-line headline.
3. **Three-lens balance** — Models / Infra / Enterprise tech counts.
4. **The drafted post** — slug, word count, character count, first 200 chars of the body.
5. **Path to the draft file and research brief.**
6. **Fidelity reminder** — "ranking signal approximated via WebSearch, not API-measured."

End with: "Want me to revise it, or publish?"

## Step 10.5 — Append to usage history

Append to `.claude/skills/weekly-summary/usage-history.md` immediately after the draft is written:

```markdown
### Week of {Friday YYYY-MM-DD}
- Ranking signal: cross-platform engagement (LinkedIn / X / HN / Reddit)
- Through-line: {one-liner if any, else "engagement landscape view"}
- Three-lens balance: Models {N} · Infra {M} · Enterprise tech {K}
- Ranked stories 1-10:
  1. {slug-1}: {URL} — {signal-count}/4 — {key engagement number}
  2. {slug-2}: {URL} — {signal-count}/4 — {key engagement number}
  ...
- Post slug: {post-slug}
- Date: {YYYY-MM-DD}
```

## Step 11 — Publish on approval

When the user approves:

```bash
python3 scripts/linkedin_post.py posts/drafts/weekly-summary-YYYY-MM-DD.md \
  --slug <chosen-slug> \
  --dry-run
```

Show the dry-run. On explicit "yes" / "publish", re-run without `--dry-run`.

---

## Output locations (recap)

- Research brief: `posts/drafts/weekly-research-YYYY-MM-DD.md`
- Post draft: `posts/drafts/weekly-summary-YYYY-MM-DD.md`
- Source catalog: `.claude/skills/weekly-summary/sources.md`
- Usage history: `.claude/skills/weekly-summary/usage-history.md`

## Hard rules

- **Mon-Fri window only** for the underlying story; engagement may accrue through the weekend.
- **Top 10 ranked by cross-platform engagement signal.** Most-engaged at rank 1.
- **Each story shows measurable engagement on ≥2 of 4 platforms** (flag thin entries).
- **Pure tech / AI scope** — no HR, workforce, layoffs, talent, culture, DEI.
- **400-600 words per post body** (excluding hashtags). **Under 2,900 characters.**
- **No story repeats across the last 3 weekly summaries.**
- **No fabrication.** Every URL is one you actually fetched. Every engagement number traces to a visible source — if a number can't be verified, write "not visible" rather than guessing.
- **Fidelity caveat** stated in every brief and once in the post or its accompanying note.
- **No images, no carousel.** Weekly summary is text-only.
- **URLs default off** in post body — `urls: on` to include them. Citations always remain in the research brief.
- **Bold AND humble.** Take positions on what the community engaged with and admit when the engagement signal is approximate.
