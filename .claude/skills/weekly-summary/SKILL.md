---
name: weekly-summary
description: Generate 3 LinkedIn weekly-summary post options (200-300 words each, text only) for a Chief Transformation Officer reflecting on the week across AI, Technology, HR, and strategy. Picks the 3 most-cited stories of the Mon-Fri window across a curated set of AI labs, big tech, strategy firms, and tier-1 news, weaves them around a shared theme, and produces the same 3 stories in 3 different framings. Use when the user says "give me a weekly summary post", "draft my week-in-review", "wrap up the week", or invokes /weekly-summary.
---

# Weekly summary — Friday wrap on AI, Technology, HR, and strategy

You are running the `weekly-summary` skill. Produce **3 LinkedIn post options
(each 200-300 words, text only, no image)** that bundle **the same 3 stories
of the week** into **3 different framings**, written in the first-person voice
of a **Chief Transformation Officer** reflecting on what shifted this week
across AI, Technology, HR, and strategy.

The skill is designed for a **Friday afternoon manual trigger** covering the
**Monday-Friday window of the current week**.

## Optional arguments (parsed from the skill `args` string)

- `week: previous` — cover Mon-Fri of the previous week instead of the current week. Default: current week.
- `week: YYYY-MM-DD..YYYY-MM-DD` — explicit window override.
- `theme: <topic>` — bias the picks toward a specific lens (e.g. `theme: agentic AI in HR`). Default: let the skill find the week's strongest cross-cutting theme.
- `sources: +<Source1>, -<Source2>` — add or exclude sources beyond the catalog.
- `count: N` — produce N options instead of 3 (cap at 5).

If args are empty, run defaults: current week Mon-Fri, theme discovered from the picks, 3 options.

---

## Step 1 — Read source catalog and usage history

Read **two** inputs before researching:

1. `.claude/skills/weekly-summary/sources.md` — the canonical AI / Tech / HR / strategy / news source catalog plus any auto-discovered sources from prior runs.
2. `.claude/skills/weekly-summary/usage-history.md` — every story URL and theme used in prior weekly-summary runs. If the file does not exist yet, treat the history as empty (this is the first run).

From the usage history, extract the **exclusion set**: every story URL used in the **last 3 weekly-summary runs**. Stories on this list are off-limits for this run — pick the next-strongest story instead. Theme overlap across weeks is allowed (some topics are sustained); story duplication is not.

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

**Ranking signal (most-cited across credible sources):** a story is more "popular" the more independent credible outlets covered it within the week. Cross-citation count is the primary signal; novelty and CTO relevance break ties.

Aim to surface **6-10 ranked candidates** before selecting the final 3.

## Step 4 — Pick 3 stories that share a theme

From the ranked candidates, select **exactly 3** stories that share an underlying theme — a through-line the CTO can name in one sentence ("the friction between speed and trust this week", "the new shape of the human-AI seam", "what scale is doing to org design").

If no 3 stories share a clean theme, widen to 4-5 candidates and look for a more abstract through-line, or pull a different mix of stories. **Do not pick 3 unrelated top stories** — the skill's value is the woven theme.

Each picked story must:
- Be inside the resolved week window.
- Come from at least 2 credible sources in the catalog (cross-citation bar).
- Not be on the exclusion set from the prior 3 runs.

If you cannot meet the bar with 3 cohesive stories, stop and report back so the user can relax constraints.

## Step 5 — Save the research brief

Save to `posts/drafts/weekly-research-YYYY-MM-DD.md` (date = the resolved Friday) using this template:

```markdown
# Weekly research brief — {Friday YYYY-MM-DD}
Window: {Mon YYYY-MM-DD} to {Fri YYYY-MM-DD}

## Theme (the through-line)
{One-sentence statement of the connecting thread, e.g. "The seam between AI capability and human accountability tightened this week."}

## Story 1 — {short slug}
- **Headline:** {original headline}
- **Lead source:** {Outlet}, {date}, {URL}
- **Also covered by:** {other outlets in the catalog, with dates}
- **Citation count:** {N credible outlets}
- **What happened:** {3-4 sentence factual summary, no interpretation}
- **Why a CTO cares:** {2-3 sentences on the implication}
- **Hook into the theme:** {one sentence connecting this story to the through-line}

## Story 2 — {short slug}
...

## Story 3 — {short slug}
...

## Candidates considered but not picked
- {headline} — {reason dropped, e.g. "below cross-citation bar", "didn't fit theme"}
```

## Step 6 — Persist any newly discovered sources

If your searches surfaced credible new outlets/firms not yet in `sources.md` that you actually cited in the brief, append them to the **Auto-discovered sources** section using this format:

```markdown
### {Source} — {What it is} ({Month YYYY})
- URL: {root URL}
- Contributed to: {story slug}
- Discovered: {YYYY-MM-DD}
```

Be conservative — only add sources that meet the discovery rules in `sources.md`.

## Step 7 — Draft 3 post options (same 3 stories, 3 framings)

Save to `posts/drafts/weekly-summary-YYYY-MM-DD.md`. Each option uses **all three stories** but with a different framing:

- **Option 1 — Synthesis framing.** Lead with the through-line. State the pattern. Walk through the 3 stories as evidence. Close with where the pattern is heading.
- **Option 2 — Question framing.** Lead with the unresolved question the week put on your desk. Walk the 3 stories as different angles on that question. Close with what you're still sitting with.
- **Option 3 — Learning framing.** Lead with something you're rethinking this week. Walk the 3 stories as the inputs that shifted your thinking. Close with what you're testing differently.

All three options stay within the **200-300 word body** (excluding hashtags). Hard cap at 320 to allow for hashtag overhead; hard floor at 180.

Use this file template (the `---POST---` / `---END---` markers matter — `linkedin-publisher` reads them to extract the publishable text):

```markdown
# Weekly summary — {Friday YYYY-MM-DD}

## Option 1 — {slug-1} (synthesis)
- **Theme:** {through-line}
- **Stories:** {story-1-slug}, {story-2-slug}, {story-3-slug}
- **Framing:** synthesis
- **Word count:** {N}
- **Status:** draft

---POST---
{200-300 word post body in the CTO voice. Source URLs inside the body, one per story.}

#Hashtag1 #Hashtag2 #Hashtag3
---END---

## Option 2 — {slug-2} (question)
...

## Option 3 — {slug-3} (learning)
...
```

## Step 8 — Voice & word-count enforcement

The CTO voice is **professional, progressive, bold, humble, and learning** — bold AND humble in the same breath. Take a position; show you're still figuring it out.

Voice rules:
- **First person.** "I sat with three stories this week." "I'm changing how I think about X." "I don't have the answer yet."
- **Bold.** Stand behind a view. Strong declaratives where you do have conviction. No hedging the whole post.
- **Progressive.** Forward-looking. Frame what's becoming possible, not what's broken.
- **Humble.** Name what you don't know. "I'm not sure yet." "This is the question I'm carrying." Worn lightly — confidence and curiosity together.
- **Learning.** Show the update. "Two weeks ago I would have said X; this week shifted me toward Y."
- **No corporate jargon, no hype words, no emojis.**
- **No AI-tells:** delve, tapestry, navigating the landscape, in conclusion, moreover, furthermore, in today's fast-paced world.
- **Short sentences. Often one per line.** LinkedIn rewards scannable.
- **One source URL per story, inside the body.** Don't trail them at the end.
- **3-5 hashtags max**, lowercase or CamelCase, off the themes of the week (e.g. `#FutureOfWork #AILeadership #Transformation`).

Word-count enforcement: before presenting to the user, **count words in each `---POST---` block (excluding hashtags) and confirm each is between 200 and 300.** If any option is outside the range, revise it. Report the word count to the user for each option.

## Step 9 — Present compactly to the user

For each option, show:
- Slug, framing, word count
- The first 120 characters of the post (the opening hook)
- The file path

Then list:
- The shared theme (the through-line)
- The 3 story slugs and their lead sources
- An **engagement-likelihood note** ranking the options (which framing is most likely to land on LinkedIn for a CTO audience and why).

End with: "Want me to revise any of these, or publish one?"

## Step 9.5 — Append to usage history

Immediately after the drafts are written (BEFORE the user picks one), append to `.claude/skills/weekly-summary/usage-history.md`:

```markdown
### Week of {Friday YYYY-MM-DD}
- Theme: {through-line}
- Story URLs:
  - {story-1-slug}: {URL}
  - {story-2-slug}: {URL}
  - {story-3-slug}: {URL}
- Option slugs: {slug-1}, {slug-2}, {slug-3}
- Date: {YYYY-MM-DD}
```

Append to the top of the "Past weeks (most recent first)" section. Create the file if it does not exist.

## Step 10 — Publish on approval

When the user picks a specific option, delegate to `linkedin-publisher`:

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
- Post drafts: `posts/drafts/weekly-summary-YYYY-MM-DD.md`
- Source catalog: `.claude/skills/weekly-summary/sources.md`
- Usage history: `.claude/skills/weekly-summary/usage-history.md`

## Hard rules

- **Mon-Fri window only.** Every story dates inside the resolved week. No older stories framed as this week's.
- **3 stories, 1 shared theme.** Not a listicle of unrelated top stories.
- **Each story cross-cited by ≥2 credible sources** in the catalog.
- **200-300 words per option body** (excluding hashtags). Verify before presenting.
- **No story repeats across the last 3 weekly summaries.** The usage history is the ledger.
- **No fabrication.** Every URL is one you actually fetched. Every claim traces to a source in the brief.
- **No images, no carousel.** Weekly summary is text-only by design.
- **Bold AND humble.** The voice takes positions and admits what it's still learning, in the same post.
