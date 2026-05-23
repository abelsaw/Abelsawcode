---
name: tuesday-perspective-post
description: Generate 2 LinkedIn post options (≤200 words each, text-only) sharing the user's personal perspective on the intersection of AI, HR, and technology — pegged to a recent (last 7 days) news story from top-tier business press or management/strategy publications, with an Asian-market lens. Each option follows a News → Implication → Action structure, uses emojis sparingly, and closes with 5–7 hashtags including the fixed #myperspective. Use when the user invokes /tuesday-perspective-post.
---

# Tuesday Perspective Post — on-demand

You are running the `tuesday-perspective-post` skill. Produce **2 LinkedIn post
options (each ≤200 words, text-only)** in the user's personal voice on the
intersection of AI, HR, and technology, anchored to a fresh news story from
the last 7 days, with an Asian-market lens.

The two options are differentiated:
- **Option A — Measured take.** Confident, evidence-led, professional. Safe to
  publish under any senior-leader profile.
- **Option B — Bolder take.** Sharper position, more declarative, a stronger
  point of view. Still professional, never adversarial.

---

## Optional arguments (parsed from the skill `args` string)

- `topic: <angle>` — scope the search to one angle (e.g. `topic: AI in hiring`,
  `topic: GenAI productivity`). Default: surface the strongest story across
  AI + HR + tech in the last 7 days.
- `story: <url>` — skip news scouting and write directly from this URL.
- `region: <asia|global>` — geographic lens. **Default: `asia`.**
- `tone: safer|bolder|both` — produce only one option, or both (default).

If args are empty, run the default flow: `region: asia`, last-7-days window,
both tones.

---

## Step 1 — Scout the news (skip if `story:` URL provided)

Search for the strongest **AI + HR + technology** news story from the **last 7 days**
with relevance to an Asian-market audience. Use WebSearch and WebFetch directly
(do not delegate — the existing `hr-news-scout` agent uses an 8-week window and
broader topic coverage that doesn't fit this skill).

**Priority outlets (sweep these first):**
- **Top-tier business press:** WSJ, FT, Reuters, Bloomberg, The Economist,
  Nikkei Asia, South China Morning Post, Straits Times, Business Standard,
  Mint, The Hindu BusinessLine.
- **Management/strategy publications:** Harvard Business Review, MIT Sloan
  Management Review, McKinsey Quarterly, McKinsey Insights, BCG Insights,
  Deloitte Insights, Bain Insights, INSEAD Knowledge.

**Story selection rules:**
1. **Recency:** published within the last 7 days from today's date (in context).
2. **Intersection:** the story must sit at the intersection of at least two of
   {AI, HR/workforce, technology}. A pure AI product launch with no workforce
   angle does not qualify. A workforce-policy story with no AI/tech angle does
   not qualify.
3. **Asian-market relevance:** either the story is from/about an Asian market,
   or it has clear implications for Asian employers and workforces. US-only
   regulatory stories with no APAC spillover do not qualify.
4. **Substance:** prefer stories with data, a named decision, or a concrete
   shift — not opinion pieces or evergreen think pieces.
5. **WebFetch to verify.** Never reference a story you haven't actually read.

Pick **the single strongest story**. If you have two close finalists, pick the
one with the sharpest CHRO/transformation-leader implication and note the
runner-up in your final report.

If no qualifying story exists in the 7-day window, **stop and report** —
ask whether to widen to 14 days or to write an evergreen perspective instead.
Do not fabricate a peg.

## Step 2 — Draft the two post options

Both options share the same structure but differ in stance and energy.

### Structure (locked): News → Implication → Action

1. **News (the peg).** Open with a tight reference to what happened. One or
   two sentences. Include a single concrete fact, stat, or decision so the
   reader trusts the post is grounded. Do not paraphrase the headline word-
   for-word.
2. **Implication (the perspective).** This is the part the reader came for.
   2–4 sentences on what it means for leaders running strategy, AI, tech, and
   HR. Connect dots the casual reader wouldn't. This is where the voice does
   its work.
3. **Action (the close).** 1–2 sentences pointing to a concrete next move a
   leader can take this week, this quarter. Specific over abstract.
4. **Hashtags.** 5–7 total, on the final line. **Always include `#myperspective`**.

### Voice (locked)

Write in the user's **personal first-person voice as a Chief Transformation
Officer overseeing strategy, AI, technology, and HR — but do not name the role
in the post copy.** Voice cues only:
- Cross-functional fluency. Speaks AI, tech, ops, and people in one breath.
- Forward-looking. Frames the opportunity ahead, not the blame for what's
  broken.
- Confident, not hedging. Owns the take.
- Measured. No adversarial framing, no "you're doing it wrong" jabs, no
  rhetorical gotchas, no attacks on roles or groups.
- Short sentences. Often one per line.
- No corporate jargon, no hype words.
- No AI-tells: delve, tapestry, navigating the landscape, in conclusion,
  moreover, furthermore, in today's fast-paced world.

### Emoji rules

- **Sparingly, where meaningful.** Aim for 1–2 per post, max 3.
- An emoji earns its place when it visually marks a beat (e.g. a single
  emoji opening the hook to catch the scroll), or it stands in for a noun
  the post otherwise repeats.
- No emoji strings, no emoji bullets, no decorative emoji clusters.

### Asian-market framing

- Weave the Asian-market lens into the body as evidence or stakes, not as a
  forced headline. Example: instead of "Asia's AI hiring boom is here,"
  write "Singapore's MOM just opened a new round of AI-skills funding —
  the signal for regional CHROs is clear."
- Don't open every post with "In Asia…". Treat the lens as a sharpening
  filter, not a frame.
- If the underlying story is global, name the specific Asian implication
  in the implication section rather than forcing it into the lead.

### Hashtag rules

- **5–7 hashtags total**, single line at the end.
- **`#myperspective` is mandatory** — it goes first or last, your call for
  rhythm.
- Topical tags should reflect the actual content. Useful pool:
  `#AI`, `#GenAI`, `#FutureOfWork`, `#HR`, `#HRTech`, `#Leadership`,
  `#DigitalTransformation`, `#WorkforceStrategy`, `#TalentStrategy`,
  `#Asia`, `#APAC`, `#FutureOfWorkAsia`, `#AsiaCHRO`, `#Singapore`,
  `#India`, `#TechLeadership`, `#AIstrategy`.
- Use Asia-tagged hashtags only when the post is meaningfully Asia-specific.

### Word count

- **≤200 words per post body, INCLUDING hashtags.** Hard cap.
- Count words for each option before presenting. If an option exceeds 200,
  tighten before showing the user.

### Differentiation between A and B

- **Same news peg, same broad implication area.** Different stance:
  - **A (Measured):** "Here's what this means and what to do about it."
  - **B (Bolder):** "Here's the take most people are missing — and the
    move that follows."
- Option B can lead with a sharper claim (a contrarian observation, a
  prediction, a call to retire an old assumption). It still respects every
  professionalism rule above.

## Step 3 — Present compactly in chat (no files saved)

Output destination is **chat only.** Do not write to `posts/drafts/` or any
other path.

For the user, render this exact shape:

```
**News peg:** {Headline} — {Outlet}, {publication date}
**URL:** {link}
**Why it matters this week:** {one-line so-what}

---

### Option A — Measured ({word count} words)

> {post body, including hashtags on the final line}

### Option B — Bolder ({word count} words)

> {post body, including hashtags on the final line}
```

Close with: **"Want me to revise either of these, sharpen the bolder one
further, or swap to a different story?"**

---

## Hard rules

- **Last-7-days news peg.** No older stories repackaged as fresh.
- **No fabrication.** The headline, outlet, date, and any stat must come from
  a source you actually fetched.
- **≤200 words per option, including hashtags.**
- **`#myperspective` is mandatory** on both options.
- **No images, no carousels, no files written.** Chat output only.
- **Voice, not role.** Do not name the user's title in the post body.
- **One post peg, two takes.** Both options anchor to the same news story
  unless the user explicitly asks for two different stories.
