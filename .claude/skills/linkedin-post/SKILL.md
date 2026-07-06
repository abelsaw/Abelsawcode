---
name: linkedin-post
description: Generate 3 LinkedIn post options (60-150 words each, 200 hard cap) plus matching 7-slide carousels on workforce and transformation best practices for a Chief Transformation Officer (CTRO), sourced from 2026 research reports across Mercer, Aon, McKinsey, WEF, BCG, WTW, Deloitte, Gallup and other credible firms. Carousels render in one of three locked styles (hr-linkedin-option1 chip icons / option2 TOC tiles / option3 photo cover). The skill can actively discover NEW credible 2026 sources during research and append them to the catalog. Use when the user wants fresh LinkedIn content — phrases like "give me LinkedIn post options", "draft a LinkedIn carousel", "create LinkedIn content", "I need new posts", or invokes /linkedin-post.

Persona note: the account voice is a **Chief Transformation Officer (CTRO)** — the repositioning from HR/CHRO to Transformation as of 2026-06-21. The carousel brand tag is `CTRO`, the closing-slide source line is `CTRO Read`, and the action-slide label is `What CTROs are doing now`. The subject matter is still workforce, people, AI-adoption, and organizational transformation sourced from the 2026 research catalog; only the persona/branding shifted. Real source names keep their exact spelling (Gartner "CHRO Priorities 2026", the "CHRO Association", Conference Board "CHRO Confidence Index" are report/firm proper nouns, not our branding — never alter a citation).
---

# LinkedIn post + carousel — on-demand

You are running the `linkedin-post` skill. Produce **3 LinkedIn post options
(each 60-150 words, 200 hard cap)** with matching **7-slide carousels**,
sourced from 2026 HR research, ready for the user to review and publish.

## Optional arguments (parsed from the skill `args` string)

- `with /hr-linkedin-option<N>` — carousel style. **Default: `option1`.** Pick the carousel design preset:
  - `option1` — playful-iconic with geometric chip icons (default; most general-purpose)
  - `option2` — playful-iconic with numbered TOC tiles (best for structured 4-part frameworks)
  - `option3` — photo-driven cover (the user supplies a photo; pass `--palette cool` for cool-toned photos)
  Each is a registered project skill with its own SKILL.md and renderer scripts.
- `region: <apac|global>` — geographic lens. **Default: `apac`.** Asia Pacific is the default audience and source-weighting for this CTRO. Pass `region: global` to remove the regional anchor.
- `theme: <topic>` — scope the posts to one topic (e.g. `theme: AI in HR`, `theme: pay transparency`). Default: surface the most-mentioned 2026 themes across the catalog.
- `sources: +<Firm1>, +<Firm2>` — include named firms in addition to the catalog. Use `-<Firm>` to exclude.
- `count: N` — produce N post options instead of the default 3 (cap at 5).
- `discover: off` — disable the new-source discovery pass (default: on).

If args are empty, run the default flow: `region: apac`, default themes, 3 options, discovery on, carousel style `option1`.

A common workflow: run once to produce drafts + carousels in one style, then the user re-invokes with a different `/hr-linkedin-optionN` (and/or a supplied photo) to re-render the SAME post bodies in another style. Save each style's output in a sibling directory (see Output locations) so all renderings stay available.

## Primary objective — drive high LinkedIn engagement

Every post is optimized for **engagement** (stops, dwell time, comments, saves, reshares, profile visits) — not just for being correct. Engagement is the goal the drafting, the carousel, and the option-ranking all serve. The rule is: **earn the engagement, don't bait it.** This means no clickbait, no manufactured outrage, no "comment YES if you agree", no withheld-payoff teasing — those conflict with the locked professional/progressive/bold voice and erode a CTRO's credibility. Instead, engagement comes from genuine signal:

- **A scroll-stopping first line.** LinkedIn truncates at ~140-210 chars ("…see more"). The opening line must carry a complete, surprising, or counter-intuitive claim that earns the click to expand. Lead with the sharpest idea, never a windup.
- **One memorable number or reframe** the reader will repeat. A single concrete stat (the lead firm's anchor) or an inversion ("It's not a pipeline problem, it's a role-design problem") is what gets quoted in comments and screenshots.
- **Save-worthiness.** Posts that read like something a CTRO would bookmark for a board deck get saves — the strongest ranking signal LinkedIn weights. Concrete frameworks, named stats, and a clear "what to do" beat generic observation.
- **A real conversation opener, not a loaded one.** End on a forward-looking question or a take that invites a peer to add their view ("Where does this sit in your 2026 plan?") — never a gotcha or a yes/no engagement-bait prompt.
- **Carousel as dwell-time engine.** The 7-slide format exists to maximize dwell time (LinkedIn rewards in-feed time). Slide 1 must hook, slides 2-5 must each reward the swipe with a distinct stat, slide 7 must close with a takeaway worth a save.
- **First-30-minutes comment fuel.** A post that gives readers something specific to react to (a number to debate, a reframe to extend, a peer experience to share) earns early comments, which drive the algorithm's reach decision.

This objective is measured at Step 6, where the options are ranked by predicted engagement and the reasoning is shown to the user.

## Anti-AI-slop — protect reach

High engagement is wasted if the post is suppressed before it reaches a feed. Since 2025-26, LinkedIn down-ranks content its classifiers read as low-effort AI-generated and rewards specific-practitioner knowledge. **This is one system with the engagement objective: earn attention AND avoid the slop filter.**

The paradox: polish and consistency read as slop. A recognizable formula repeated across an account is itself a suppression signal. Variety and a genuine human fingerprint beat a "perfect" template.

### Hard bans (non-negotiable AI fingerprints)

- **No em-dashes** (`—` or `–`). A notorious AI tell. Use a period, comma, colon, or parentheses instead.
- **No "It's not X, it's Y" inversions** and close variants ("X isn't A. It's B.", "The lever isn't the form, it's the coach."). This two-beat reversal is a signature AI-slop move — we over-used it badly in early runs. Make the point directly instead.
- **No template phrases:** "not a perk", "the cheapest X you already own", "unlock" (as a noun), "the [X] lever", "isn't a [thing], it's [infrastructure]", "here's the thing", "the truth is", "let that sink in", "game-changer", "in today's landscape", "navigating the".
- **No forced rule-of-three.** Vary the count of stats, action items, and beats. Not every post gets exactly three of anything.

### Structural variety across the batch (enforced)

The N options in a run MUST each use a DIFFERENT architecture — never three clones of one skeleton (that's what pattern-flags the whole account). Rotate:

- **Observation / POV-led** — opens with a specific first-person practitioner beat, then the data supports it. **Exactly one option per run is this type** (see below).
- **Single-stat-led** — one dominant number carries the post; interpret it in depth rather than stacking three stats.
- **Contrarian-claim-led** — opens with a claim that challenges the conventional wisdom on the topic, then earns it with evidence. Contrarian ≠ inversion: state the claim directly, do NOT use the banned "not X, it's Y" form.

When `count > 3`, add: question-led (a genuine problem the reader is living) or sequence-led (a short before/after or trajectory).

### One POV option per run — sourced from the user, not invented

Exactly one of the N options is written in an explicit first-person seasoned transformation-leader (CTRO) voice — a lived observation, a genuine stance, or a mild disagreement with the data. This is the single strongest anti-slop + reach lever, because it is content only a real practitioner could write; the algorithm and the reader both reward it.

**The POV comes from the user, never fabricated.** Before drafting the POV option, ASK the user for their **"POV of the week"** — a one-to-two-line genuine take, stance, or observation from their actual experience. Build the POV post around what they give you; do not invent a practitioner anecdote, a specific number they didn't state, or a stance they don't hold. A fabricated "in my experience…" is worse than no POV post — it reads false and risks their credibility.

Practical flow:
- **Ask once per week.** The "POV of the week" applies to the POV option in every run that week. Don't re-ask on each same-week run unless the user offers a new one or the week's themes have moved on.
- **When to ask:** after the scout's brief is in (so you can tell the user which themes surfaced and invite a POV that fits one of them), and before drafting. A good prompt: "Which of these themes do you have a personal take on this week, and what's your one-line view?"
- **If the user gives no POV** (declines, unavailable, or it's a quick test): skip the POV option and draft all N options evidence-led — but STILL enforce the 3-distinct-structures rule (e.g. single-stat-led, contrarian-claim-led, question-led). Note in the final report that no POV was supplied this run.
- **Keep it theirs.** Lightly shape their words for LinkedIn (tighten, add the supporting stat, fit ≤50 words) but preserve their actual position and voice. Show them the POV draft and confirm it still reflects their view before it counts as final.

### The human gate (final review before presenting)

Before showing drafts at Step 6, run every post through one test: **"Would a specific, smart, experienced CTRO write this exact sentence — or does it read like a research digest any tool could generate?"** Where a line reads generic, rewrite it with a concrete detail, a real stance, or plainer words. Reduce stat density (one well-interpreted number beats three stacked). Vary sentence rhythm — not every line is one short sentence. This gate applies to the post body; the carousel slide copy follows the same bans (no em-dashes, no inversions, no template phrases).

---

## Step 1 — Read the source catalog, usage history, and attached PDFs

Read **three** inputs before invoking the scout:

1. `.claude/skills/linkedin-post/sources.md` — the canonical Tier 1 / Tier 2 source catalog (Tier 3 was excluded 2026-05-22; an archive of the removed entries remains at the bottom of the file) plus any auto-discovered sources from prior runs, AND the **Lead-firm utilization (last 9 posts)** tracker.
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
  - "With `region: apac` (default), apply APAC as a **relevance filter on themes**, not a separate source tier. **Topic filter:** only surface themes applicable to APAC employers. Drop themes that are US-only or Europe-only and don't reach APAC (e.g. US-specific NLRB rulings, US state-level labor law). Themes that touch APAC multinationals via global rules pass (e.g. EU Pay Transparency landing on European subsidiaries of APAC firms). **Sources:** use Tier 1 and Tier 2 only. Pull APAC regional breakouts of Tier 1/2 firms (Mercer Asia, McKinsey Asia, BCG Southeast Asia, Deloitte APAC, WTW APAC, KPMG APAC) when they add value — these are regional cuts of catalog firms, not a separate tier. **Tier 3 is excluded as of 2026-05-22** — do not cite Hays, Robert Walters, Michael Page, INSEAD, ILO Asia-Pacific, ADB, Singapore MOM, AHRI, HKIHRM, People Matters, HR Asia, IFC, ManpowerGroup, or Korn Ferry APAC. **Data:** cite APAC stats as evidence when they materially differ from the global picture; otherwise universal stats are fine. **Don't write briefs that frame every theme as 'APAC's biggest…' — the goal is general best practices that happen to be relevant to APAC.**"
  - "With `region: global`, drop the regional filter entirely and surface globally-applicable Tier 1/2 findings."
- **The discovery directive (when `discover` is not `off`):** "During your searches, if you encounter 2026 HR research from a credible **global** firm NOT in the catalog that adds new convergence to a theme you're surfacing, USE it and report it back so it can be added to the catalog. Acceptable discovery candidates: major global consulting firms (Heidrick & Struggles, Russell Reynolds, Spencer Stuart, Egon Zehnder, Oliver Wyman, Accenture Research, Roland Berger), global research institutions (Brookings, MIT Sloan, Wharton, NBER, Stanford), or established global trade publications with primary research (HBR original surveys, MIT Sloan Management Review). **Do NOT propose APAC-only or country-specific firms** — the user excluded Tier 3 on 2026-05-22. Apply the discovery rules in `.claude/skills/linkedin-post/sources.md`."
- **The dedup exclusion set:** "The following parent themes have been used in /linkedin-post runs within the last 14 days and are OFF-LIMITS for this run unless the user explicitly overrides: {paste the list from usage-history.md}. Do not surface these themes as top candidates. If a brief candidate falls under an excluded parent theme, drop it and pick a different angle from a non-excluded theme. If fewer than 3 non-excluded themes meet the ≥2-firm bar, stop and report so the user can decide whether to relax the dedup window or accept a smaller set."
- **The source-balance directive (lead-firm rotation + coverage minimum):** "Read the **Lead-firm utilization** section of `.claude/skills/linkedin-post/sources.md` before proposing themes. **Rule 1 — Lead-firm rotation:** each of the N posts in this run must designate ONE lead firm (the firm whose stat anchors the headline of slide 2). Lead firms MUST be distinct across the N posts; the Big-3 firms (McKinsey, Deloitte, Aon) may not lead more than 1 post per 3-post run unless there is no other firm with a credible cross-firm corroborated stat for that theme. Supporting/corroborating firms may repeat across posts. **Rule 2 — 9-post coverage minimum:** in the rolling 9-post window covered by the utilization tracker, every Tier 1 firm must appear at least once, and at least 2 Tier 1 firms outside the Big 3 (Mercer / WTW / Gartner / WEF / Gallup) must lead at least one post. If today's run would leave any Tier 1 firm at zero appearances in the rolling window, prioritize themes that surface a stat from that firm. **Rule 3 — Underused-firm priority:** when two themes meet the ≥2-firm bar with similar evidence strength, prefer the one led by an under-represented firm. Specifically prioritize PwC (Workforce Hopes & Fears 2025/26 PDF is unused), Gallup (State of Global Workplace 2026), BCG, KPMG, and Tier 2 firms (SHRM, Bain, Conference Board, Gartner). Report the lead firm for each surfaced theme in the brief so the writer can verify rotation."
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

## Step 4 — Draft the posts and render the 7-slide carousels

Using the same dedup exclusion set and source-balance constraints you gave
the scout, draft the N post options and render their carousels. Do NOT draft
on an excluded parent theme; if the brief surfaces an angle that maps to one,
pick a different angle from a non-excluded theme.

**Before drafting, secure the POV.** Exactly one option is the first-person
POV post (see "One POV option per run" in the Anti-AI-slop section). Ask the
user for their **"POV of the week"** if you don't already have one for this
week — surface the scout's themes and invite a one-line personal take on
whichever fits. Build the POV option around their words; never fabricate a
stance. If they give none, draft all options evidence-led and still enforce
the 3-distinct-structures rule.

The N options must use N distinct structures (observation/POV-led ·
single-stat-led · contrarian-claim-led · +question/sequence-led when N>3),
and every post + carousel clears the Anti-AI-slop hard bans.

You can run this step inline (read the brief, write the draft markdown, render
the slides with the option scripts) or delegate the drafting to the
`hr-best-practices-writer` agent — but note that agent is wired to the legacy
Style C generator, so if you delegate, you must still re-render the carousels
with the option1/2/3 scripts below. Inline is the default in current practice.

### 4a — Write the post-draft markdown

Save `posts/drafts/best-practices-YYYY-MM-DD.md` (append `-run2`, `-run3`, …
for additional same-day runs). One `## Option N — <slug>` section per post,
each with a `---POST---` / `---END---` block holding the publishable body, plus
metadata (lead firm, theme, source reports, carousel dir, slide specs, word
count). Mirror the structure of prior drafts in `posts/drafts/`.

### 4b — Render the carousel (7 slides, in the chosen style)

The carousel style comes from the `with /hr-linkedin-option<N>` argument
(default `option1`). Each style is a registered skill with its own renderer
scripts in `scripts/`. **Every carousel is 7 slides:**

- **Slide 1** — cover (style-specific: chip icons / TOC tiles / photo)
- **Slides 2-5** — four data/insight slides
- **Slide 6** — action list ("What CTROs are doing now") — pass a multi-line
  `--lead` (literal `\n` between items), drop `--bold`
- **Slide 7** — dark-background conclusion (the ONLY dark slide in the carousel)

The body shape on every content slide is two-part: a **headline** (the
observation), a muted-regular **lead** (the bridge phrase), and a bold
**payoff** (the punchline). Slide 7 must land as a **conclusion, not a
question** — the bold payoff is the screenshot-worthy takeaway.

Renderer scripts per style:

| Style | Cover script | Content (slides 2-6) | Dark conclusion (slide 7) |
|---|---|---|---|
| option1 (chip icons) | `scripts/generate_post_image_playful_cover.py` | `scripts/generate_post_image_playful_content.py` | `scripts/generate_post_image_playful_dark_conclusion.py` |
| option2 (TOC tiles) | `scripts/generate_post_image_playful_v2_cover.py` | `scripts/generate_post_image_playful_v2_content.py` | `scripts/generate_post_image_playful_v2_dark_conclusion.py` |
| option3 (photo cover) | `scripts/generate_post_image_photo_cover.py` | `scripts/generate_post_image_photo_content.py` | `scripts/generate_post_image_photo_dark_conclusion.py` |

The full CLI flags, palettes, fonts, and slide conventions for each style live
in the style's own SKILL.md (`.claude/skills/hr-linkedin-option1/`,
`.../option2/`, `.../option3/`). Read the relevant one before rendering.

Style-specific notes:
- **option2** — the cover passes a `--tiles "01:WORD,02:WORD,03:WORD,04:WORD"`
  TOC; each content slide's `--tile-color` must match the cover-tile position
  (slide 2 coral, 3 navy, 4 mustard, 5 dark_coral; slide 6 reuses mustard).
- **option3** — the user supplies a photo (copy it into the carousel dir as
  `source-photo.*`). Add `--palette cool` for cool-toned photos (navy
  interiors, blue/steel, AI/holographic, cityscapes); default palette is warm.
- **Lead-firm stat anchors slide 2.** The lead firm designated for each post
  (per the source-balance rotation) is the firm whose stat headlines slide 2.

Default brand tag is `CTRO` (repositioned from `CHRO` on 2026-06-21; the "Abel Saw" tag was removed 2026-06-02). The closing-slide source line is `CTRO Read` and the action slide is `What CTROs are doing now`.

### 4c — Environment notes

A fresh container may be missing Pillow and/or poppler-utils. If a render
fails with "Pillow not installed", run `pip install Pillow`. If PDF text
extraction is needed and fails, run `apt-get update && apt-get install -y
poppler-utils`.

## Step 5 — Voice & word-count enforcement

Each post body must be **highly professional, progressive, and bold** — first-person senior transformation-leader (CTRO) voice. The writer takes a clear position and points forward without picking fights:

- **Bold** = stands behind a view, doesn't hedge, owns the take. Strong declaratives.
- **Progressive** = forward-looking. Frames the opportunity ahead, not the blame for what's broken.
- **Professional** = measured tone. No adversarial framing, no "you're doing it wrong" jabs, no rhetorical gotchas ("defensible in court?"), no attacks on roles or groups.

Voice rules:
- Open with a clear claim or forward-looking observation, not a headline restatement.
- Vary sentence rhythm. Short sentences work, but not every line one-per-line every post — that cadence is itself an AI tell now.
- No corporate jargon, no emojis, no hype words.
- No AI-tells: delve, tapestry, navigating the landscape, in conclusion, moreover, furthermore.
- **Apply the Anti-AI-slop hard bans** (see the "Anti-AI-slop" section above): no em-dashes, no "It's not X, it's Y" inversions, no template phrases, no forced rule-of-three.
- **The 3 options must use 3 different structures** (observation/POV-led · single-stat-led · contrarian-claim-led), and **exactly one is the first-person POV option.**
- Reflective questions ("Where does X sit in your stack?") are fine; loaded ones are not.
- 3-4 hashtags max, and vary them across the batch — don't put the same `#CHRO #FutureOfWork` on all three.
- **Run the human gate** before presenting: would a specific experienced CTRO write this exact sentence, or is it a digest any tool could produce?

**Engagement craft (serves the Primary objective above):**
- **First line is the hook.** It must stand alone as a complete, scroll-stopping claim within ~140 chars — before LinkedIn's "…see more" fold. If the first line needs the second line to make sense, rewrite it.
- **Front-load the sharpest stat or reframe.** The single most quotable element (the lead firm's anchor number, or a clean inversion) belongs in the first two lines, not buried at the end.
- **Earn it, don't bait it.** No "comment X if…", no "agree?", no withheld payoff, no outrage framing. Engagement-bait reads as desperation and clashes with the CTRO voice. The hook is a real idea, not a tease.
- **Leave room for the reader to add value.** The strongest comment-drivers give peers something specific to extend — a number to debate, a reframe to apply to their org, an experience to share. Either close works: a bold declarative take that invites agreement/challenge ("Fund the humans.") OR a forward-looking question ("Where does this sit in your 2026 plan?"). What kills comments is a closed, self-contained summary that leaves nothing to add.
- **One idea per post.** A post that argues one thing well out-engages one that lists three. Save breadth for the carousel.
- **Whitespace.** One idea per line, blank lines between beats. Dense paragraphs kill dwell time on mobile.

**APAC framing (when `region: apac`):**
- **Universal best-practices framing is the default.** Don't open posts with "APAC's biggest..." or "APAC moved past..." style leads. Write as a senior transformation leader (CTRO) sharing a general insight that happens to land in APAC.
- **Weave APAC data into the body as evidence**, not as the headline. Example: instead of "APAC's medical trend is the highest in the world," write "Medical inflation is rewriting benefits strategy. WTW 2026: global 10.3%, with APAC leading at 14%."
- **Filter, don't force.** If a topic doesn't apply to APAC employers (e.g. US-only NLRB rulings, US state labor law), don't draft a post on it. If a topic applies universally, treat it universally and only invoke APAC where the data adds material dimension.
- **Hashtags default to universal.** `#APAC`, `#FutureOfWorkAsia`, `#ASEAN`, `#SingaporeHR`, `#AsiaCHRO` are optional — use only when the post specifically targets APAC employers (e.g. regional regulatory deadlines).

**Word count: target 60-150 words, hard cap 200 (including hashtags).**

The old ≤50-word cap forced terse, stat-stacked lines that read as AI slop. The carousel carries the dense data; the *post* carries voice, framing, and one or two anchor stats, not a data dump. Give the writing room to sound like a person: a micro-observation, a short setup, a genuine beat. Do not pad to hit a number, but do not compress a human thought into a telegram either.

- **Sweet spot: 60-150 words.** Long enough to breathe, short enough to stay scannable on mobile.
- **Hard cap: 200 words.** Beyond this, dwell drops and it stops being a "post."
- **First ~140 chars still carry the hook** (before the "see more" fold) regardless of total length.
- **Stat density over length is the real risk.** A 130-word post with one well-interpreted stat and a human voice beats a 50-word post that stacks three. Fewer facts, more thought.

Verify each option's word count:
```bash
python3 scripts/linkedin_post.py posts/drafts/best-practices-YYYY-MM-DD.md \
  --slug <slug> --dry-run
```
The script prints `Words: N` — confirm `N ≤ 200` for every option, and that it lands in the 60-150 sweet spot unless there's a reason to run longer.

## Step 6 — Present compactly to the user

For each option, show:
- Slug, theme, sources, word count
- **Structure label** — which architecture it uses (observation/POV-led · single-stat-led · contrarian-claim-led), so the batch variety is visible at a glance. Confirm exactly one is the POV option.
- The post body (in a blockquote)
- Path to the carousel directory
- **An engagement-likelihood note** ranking the options against the Primary objective (most likely to perform on LinkedIn and why). Score each on the levers that drive reach: hook strength (first-line stop power), one-quotable-element, save-worthiness, early-comment fuel, and audience scope. Name the single highest-engagement pick and say why it beats the others.

Before presenting, confirm the **human gate** and **anti-slop hard bans** passed for every option (no em-dashes, no inversions, no template phrases, 3 distinct structures, 1 POV option). If any post still reads like a digest, rewrite it, don't ship it.

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

## Step 6.6 — Update the lead-firm utilization tracker

After the writer has produced the drafts, update the **Lead-firm utilization (last 9 posts)** section of `.claude/skills/linkedin-post/sources.md`. For each post drafted, append one row to the rolling tally:

```markdown
| YYYY-MM-DD | slug-here | Lead firm | Supporting firms |
```

After appending, prune the tracker to the **most recent 9 rows** — older rows roll off so the table always reflects the rolling 9-post window. The next run's scout reads this section to enforce the rotation + coverage rules from Step 2.

If today's run leaves any Tier 1 firm (Mercer, Aon, McKinsey, WEF, BCG, WTW, Deloitte, Gallup) at zero appearances in the rolling 9-post tally, flag it in your final report so the next run prioritizes that firm.

## Step 7 — Publish on approval

When the user picks a specific option, delegate to `linkedin-publisher`:

```bash
python3 scripts/linkedin_post.py posts/drafts/best-practices-YYYY-MM-DD.md \
  --slug <chosen-slug> \
  --carousel-dir posts/drafts/carousels/<carousel-dir-for-chosen-style> \
  --image-alt "<slide-1 headline>" \
  --dry-run
```

Use the carousel directory that matches the style the user wants to publish
(e.g. `…-option-1/` for chip icons, `…-option-1-tiles/` for TOC tiles,
`…-option-1-photo/` for the photo cover — see Output locations).

Show the dry-run output. On explicit "yes" / "publish", re-run without
`--dry-run`. Never batch-publish without confirmation per option.

If `LINKEDIN_ACCESS_TOKEN` or `LINKEDIN_AUTHOR_URN` aren't set, walk the user
through the setup steps in `.env.example` instead of attempting to publish.

---

## Output locations (recap)

- Research brief: `posts/drafts/best-practices-research-YYYY-MM-DD.md` (append `-run2`, `-run3` for same-day reruns)
- Post drafts: `posts/drafts/best-practices-YYYY-MM-DD.md` (same `-runN` suffix)
- Carousel slides: `posts/drafts/carousels/YYYY-MM-DD[-runN]-option-N[-STYLE]/slide-M.png`
  - chip icons (option1): no style suffix — `…-option-1/`
  - TOC tiles (option2): `…-option-1-tiles/`
  - photo cover (option3): `…-option-1-photo/` (plus `-photo-v2/`, `-photo-v3/` for alternate photos)
  - Each post's slides are `slide-1.png` … `slide-7.png`.
- Source catalog + lead-firm tracker: `.claude/skills/linkedin-post/sources.md`
- Usage history (theme dedup ledger): `.claude/skills/linkedin-post/usage-history.md`
- Carousel style presets: `.claude/skills/hr-linkedin-option1/`, `…/option2/`, `…/option3/`

## Hard rules

- **2026-only sources.** No 2025-or-earlier reports cited as 2026.
- **60-150 words per post body (200 hard cap)**, including hashtags. The carousel carries the data; the post carries voice. Fewer facts, more thought — don't compress a human thought into a telegram.
- **No fabrication.** Every stat traces back to a source in the brief.
- **7 slides per option, every time.** Three posts = three carousels = twenty-one PNGs. Slide 1 cover, slides 2-5 data/insight, slide 6 action list, slide 7 dark conclusion.
- **Slide 7 ends with a conclusion, not a question.** The bold payoff is the takeaway.
- **Engagement is the objective, earned not baited.** Every post is optimized for reach (hook, dwell, comments, saves, reshares) via genuine signal — a scroll-stopping first line, one quotable stat/reframe, save-worthy substance, a real conversation opener. Never via clickbait, engagement-bait prompts, outrage, or withheld payoffs (see "Primary objective" up top). The post-body question on the page and the carousel question are different surfaces — the *post* may end on an inviting question; the *carousel slide 7* ends on a conclusion.
- **Anti-AI-slop is mandatory (protects reach from suppression).** Hard bans: no em-dashes, no "It's not X, it's Y" inversions, no template phrases ("not a perk", "unlock", "the X lever", etc.), no forced rule-of-three. The 3 options must use 3 distinct structures, exactly one written in first-person CTRO POV. Every post clears the human gate ("would a specific experienced CTRO write this exact sentence?") before presenting. See the "Anti-AI-slop" section for the full list.
- **Persistence is silent but visible.** When you add a discovered source, mention it in your final report to the user ("Added Korn Ferry's 2026 Workforce Survey to the catalog — first time seen.") so they can audit the growing catalog.
- **No theme overlap with prior runs.** Before drafting, the skill reads `.claude/skills/linkedin-post/usage-history.md` and excludes parent themes used within 14 days. After drafting, the skill appends the newly-used themes to the ledger. The user can manually delete an entry to allow recycling. If fewer than 3 non-excluded themes meet the cross-firm bar, stop and ask before drafting a smaller set.
- **Lead-firm rotation across the rolling 9-post window.** Big-3 firms (McKinsey, Deloitte, Aon) may not lead more than 1 of every 3 posts in a single run. In the rolling 9-post window, every Tier 1 firm (Mercer, Aon, McKinsey, WEF, BCG, WTW, Deloitte, Gallup) must appear at least once, and at least 2 non-Big-3 Tier 1 firms (Mercer / WTW / Gartner / WEF / Gallup) must lead at least one post. Track utilization in `sources.md` after every run. If the rule blocks all available themes, surface the conflict in the brief and ask the user to relax it explicitly.
