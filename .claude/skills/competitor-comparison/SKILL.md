---
name: competitor-comparison
description: Generate 3 LinkedIn post options (≤50 words each) comparing the top 1 and top 2 players in a user-named industry, each with a generated head-to-head VS image (1080x1080). Sourced from 2026 research reports and the last 8-12 weeks of press. Voice = founder/CEO — punchy, opinionated, first-person. The three options take the same comparison angle but use different hooks (question, stat, contrarian take). Use when the user wants competitor comparison content — phrases like "compare top 2 in [industry]", "do a versus post on [industry]", "competitor comparison for [industry]", or invokes /competitor-comparison.
---

# Competitor comparison — head-to-head LinkedIn posts

You are running the `competitor-comparison` skill. The user names an
industry; you identify the top 1 and top 2 players, pick ONE strong
business-strategy angle that genuinely separates them in 2026, and draft
**3 LinkedIn post options (each ≤50 words)** in a founder/CEO voice. Each
option uses the SAME angle but a DIFFERENT hook (question, stat,
contrarian take). Each option gets a matching **head-to-head VS image**
(1080×1080 PNG).

## Arguments (parsed from the skill `args` string)

- `industry: <name>` — the industry/category to compare. Required for the default flow (e.g. `industry: big tech`, `industry: streaming`, `industry: ride-hailing`).
- `competitors: "<A> vs <B>"` — skip the leader-selection step and use this exact pair (e.g. `competitors: "Apple vs Microsoft"`).
- `angle: <topic>` — lock the comparison angle (e.g. `angle: AI strategy`, `angle: margin trajectory`, `angle: capital allocation`). Default: skill picks the sharpest cross-cutting angle from the research.
- `count: N` — produce N post options instead of the default 3 (cap at 5).

If neither `industry` nor `competitors` is supplied, ask the user which industry to cover before doing anything else.

---

## Step 1 — Read usage history and dedup

Read `.claude/skills/competitor-comparison/usage-history.md` and extract
the **exclusion set**: every `<Company A> vs <Company B>` pair (order-
independent) used within the last **30 days**. These pairs are off-limits
for this run unless the user explicitly overrides ("yes, do Apple vs
Microsoft again, fresh angle").

If the user passed `competitors:` and that pair is in the exclusion set,
stop and ask whether they want a fresh angle on the same pair or a
different pair.

## Step 2 — Identify the top 1 and top 2

If `competitors:` was supplied, skip to Step 3.

Otherwise, use `WebSearch` (and `WebFetch` for any specific source) to
identify the top 1 and top 2 players in the named industry as of **today
(2026)**. Selection criteria, in priority order:

1. **Market position** — market cap, revenue, market share, or category leadership in 2026. Use the dimension most relevant to the industry (revenue for retail, MAUs for social, market cap for big tech, GWP for insurance, etc.).
2. **Direct rivalry** — they actually compete in the same category. Don't pair an AWS with a Netflix.
3. **2026 relevance** — recent strategic moves, earnings, or repositioning. A company that was top 2 in 2024 but has fallen off doesn't qualify.

Confirm both names and the selection dimension in a one-line note. If
two candidates are genuinely tied for #2, pick the one with more 2026
news velocity (better material for posts).

## Step 3 — Research the comparison

Pull two streams in parallel via `WebSearch` and `WebFetch`:

- **2026 research reports.** McKinsey, BCG, Bain, Deloitte, PwC, Gartner, Forrester, IDC, Goldman Sachs sector notes, Morgan Stanley, etc. — whichever firm covers the industry well. Look for the latest 2026 industry outlook or sector deep-dive that names both companies. Filings (10-Ks, annual reports, investor day decks) count when freshly released in 2026.
- **Recent news & press (last 8-12 weeks).** Earnings calls, strategic announcements, executive moves, M&A, regulatory filings, major product launches. Reuters, Bloomberg, FT, WSJ, The Information, sector trade press.

For each company, capture 3-5 concrete data points across:
- Strategy / positioning shifts in 2026
- Financials (revenue growth, margin, capital return)
- Product or platform moves
- AI / tech bets where relevant
- Major risks or controversies

**Hard rules on research:**
- **No fabrication.** Every stat in a post must trace back to a real source you found. If you can't verify a number, don't use it.
- **2026 first.** Cite 2026 reports and 8-12 week-old news. A 2025 stat is acceptable ONLY if no 2026 equivalent exists and you flag it as 2025.
- **Both sides.** Don't write a hit piece. Get comparable evidence on both companies.

Save a one-page research note to
`posts/drafts/competitor-comparison-research-YYYY-MM-DD-<industry-slug>.md`
with the two companies, their 3-5 data points each, and 3-5 candidate
comparison angles ranked by sharpness.

## Step 4 — Pick the angle

Pick **one** comparison angle that genuinely separates the two companies
in 2026. Good angles are specific and contestable:

- "Bet-the-company AI strategy vs disciplined platform extension"
- "Margin expansion via pricing vs margin expansion via cost"
- "Owning the customer vs owning the rail"
- "Capital return vs capital reinvestment"
- "Vertical integration vs partner ecosystem"

Bad angles are generic or obvious:

- "Both are great companies"
- "AI is changing the industry"
- "Innovation"

If `angle:` was passed, use that. Otherwise pick the sharpest angle from
the research note and state it explicitly in your reply.

## Step 5 — Draft 3 posts (same angle, different hooks)

All three posts argue the SAME comparison angle. They differ only in the
**hook** (the first line) and the surrounding structure:

- **Option 1 — Stat hook.** Lead with the sharpest 2026 number. Then the read.
- **Option 2 — Question hook.** Lead with a pointed question the angle answers. Then the evidence and the take.
- **Option 3 — Contrarian hook.** Lead with the unconventional read (the thing most analysts miss). Then the evidence.

### Voice: founder / CEO

- **First person, operator's voice.** "I've been watching this for a year." "Here's what I'd do." "This is the call I'd make."
- **Punchy, opinionated.** Short sentences. Strong declaratives. Take a position. Pick a winner where the evidence supports one.
- **No corporate hedging.** No "interesting times," no "in conclusion," no "navigating the landscape."
- **No emojis. No jargon. No hype.**
- **3-4 hashtags max.** E.g. `#BigTech #Strategy #AI #Leadership`.
- **No AI-tells:** delve, tapestry, in today's fast-paced world, moreover, furthermore.

### Structure (target 35-50 words)

1. **Hook** (1 line — stat, question, or contrarian claim depending on option)
2. **Evidence** (1-2 lines — 2026 data points, attributed inline: "McKinsey 2026:", "Q1 2026 earnings:")
3. **The call** (1 line — your read of who's playing it better, or what to watch)
4. **Hashtags** (1 line, 3-4 tags)

### Hard rules

- **≤50 words per post body**, including hashtags. Hard cap.
- All 3 posts on the same angle. If you can't write three distinct hooks for one angle, you picked the wrong angle — go back to Step 4 and pick another.
- Pick a side where the evidence supports one. "Both are winning" is the laziest take.
- Don't fabricate. Don't cite a 2024 figure as 2026.

## Step 6 — Generate the head-to-head VS image for each post

One 1080×1080 VS card per option. Accent color rotates: option 1 = navy,
option 2 = rust, option 3 = moss. Use `scripts/generate_vs_image.py`:

```bash
python3 scripts/generate_vs_image.py \
  --left "<Company A>" \
  --right "<Company B>" \
  --left-stat "<one-line 2026 stat or descriptor for A>" \
  --right-stat "<one-line 2026 stat or descriptor for B>" \
  --tag "<industry tag, e.g. 'Big Tech 2026'>" \
  --option "Option <N>" \
  --tagline "<the post's hook line, ≤80 chars>" \
  --accent <navy|rust|moss> \
  --output posts/drafts/vs-cards/YYYY-MM-DD-<industry-slug>-option-<N>.png
```

You can run all three options in parallel via `&` and `wait`. Keep the
`--left-stat` / `--right-stat` lines short (≤60 chars each) — they sit
under the company names and auto-shrink, but short looks best. The
`--tagline` is the bottom anchor line — usually the post's hook.

## Step 7 — Save drafts

Write the three drafts to
`posts/drafts/competitor-comparison-YYYY-MM-DD-<industry-slug>.md` using
this template:

```markdown
# Competitor comparison — {Industry} — {YYYY-MM-DD}

Pair: **{Company A} vs {Company B}**
Selection basis: {one line — market cap, revenue, category leadership}
Angle: {the single comparison angle, one sentence}
Source research: posts/drafts/competitor-comparison-research-{YYYY-MM-DD}-{industry-slug}.md

## Option 1 — stat hook
- **VS card:** posts/drafts/vs-cards/{YYYY-MM-DD}-{industry-slug}-option-1.png
- **Sources:** {source 1; source 2}
- **Word count:** {N}

---POST---
{The post. ≤50 words. Founder/CEO voice. Stat-led hook.}
---END---

## Option 2 — question hook
{...}

## Option 3 — contrarian hook
{...}
```

## Step 8 — Present compactly to the user

Show:
- The pair, the selection basis, the angle (one line each)
- For each option: hook type, word count, VS card path, the post body in a blockquote
- An **engagement-likelihood note** ranking the three options for LinkedIn (which hook is most likely to drive comments / saves / shares and why)

End with: "Want me to revise any of these, swap the angle, or publish one?"

## Step 9 — Append to usage history

After the drafts are written (BEFORE the user picks one), append an entry to `.claude/skills/competitor-comparison/usage-history.md`:

```markdown
### {Company A} vs {Company B} — {Industry}
- Date: {YYYY-MM-DD}
- Angle: {one-line angle label}
- Slugs: option-1 (stat), option-2 (question), option-3 (contrarian)
- Draft: posts/drafts/competitor-comparison-{YYYY-MM-DD}-{industry-slug}.md
```

Append to the top of the "Used pairs (most recent first)" section.

## Step 10 — Publish on approval

When the user picks an option, delegate to `linkedin-publisher` using
`scripts/linkedin_post.py` with the chosen slug. Use the VS card as the
single image. Always dry-run first; never publish without an explicit
"yes" / "publish" from the user.

---

## Output locations (recap)

- Research note: `posts/drafts/competitor-comparison-research-YYYY-MM-DD-<industry-slug>.md`
- Drafts: `posts/drafts/competitor-comparison-YYYY-MM-DD-<industry-slug>.md`
- VS cards: `posts/drafts/vs-cards/YYYY-MM-DD-<industry-slug>-option-N.png`
- Usage history: `.claude/skills/competitor-comparison/usage-history.md`

## Hard rules (recap)

- **2026-first sources.** Reports and news from 2026 or the last 8-12 weeks. 2025 only as fallback, flagged.
- **≤50 words per post**, including hashtags.
- **Same angle, different hooks** across the three options.
- **Founder/CEO voice.** First-person, opinionated, short sentences. Pick a side where the evidence supports one.
- **No fabrication.** Every stat traces to a real source in the research note.
- **30-day pair dedup.** Don't recompare the same pair within 30 days unless the user explicitly overrides.
- **VS card per option.** Three posts = three head-to-head PNGs. Navy / rust / moss accents.
