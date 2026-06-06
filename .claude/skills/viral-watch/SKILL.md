---
name: viral-watch
description: Generate a single LinkedIn post for a Chief Transformation Officer (Business Strategy + HR + IT remit) covering the top 10 viral SEA news stories of the window, ranked most-cited → least-cited and presented in a uniform flat list with one CTO take per story. Default region is Southeast Asia (Singapore, Indonesia, Malaysia, Thailand, Philippines, Vietnam, Cambodia, Laos, Myanmar, Brunei). Surge bar: ≥3 catalog outlets in 48-72h, ≥1 Tier-1 anchor, workforce/labor or culture/equity/values lens. Output goes through a LinkedIn-worthiness review before saving. Use when the user says "what's gone viral in SEA", "top 10 viral SEA", "viral watch", or invokes /viral-watch.
---

# Viral watch — LinkedIn post on top 10 viral SEA news

You are running the `viral-watch` skill. Produce **one LinkedIn post (text only, no image)** that lists the **top 10 viral SEA news stories** of the resolved window — ranked most-cited → least-cited — each carrying implications for **workforce/labor** and/or **culture/equity/values**, written in the first-person voice of a **Chief Transformation Officer whose remit spans Business Strategy, HR, and IT**.

This is **LinkedIn-publishable output**, not internal research. The voice is first-person, bold-and-humble CTO — professional, progressive, measured, and engaging for a LinkedIn professional audience.

## Optional arguments (parsed from the skill `args` string)

- `window: <N>d` — look back N days from today (default: `7d`, max: `14d`).
- `lens: <workforce|culture|both>` — restrict the lens (default: `both`).
- `region: <sea|apac|us|global|eu>` — bias toward stories landing in the named region. **Default: `sea`**.
- `rank: <N>` — produce a ranked list of N stories instead of 10 (default: `10`, range: `5-15`).
- `urls: on` — include source URLs inline. Default: off (citations in metadata block, not in the publishable body).

If args are empty, run defaults: 7-day window, both lenses, SEA, ranked top 10, URLs off in body.

---

## Step 1 — Read source catalog and usage history

Read **two** inputs before researching:

1. `.claude/skills/viral-watch/sources.md` — the SEA-tuned catalog.
2. `.claude/skills/viral-watch/usage-history.md` — prior runs (used for awareness, NOT for hard exclusion — see Step 3 dedup-relaxation note).

## Step 2 — Compute the window

- Today's date is in context. Default window: today minus 7 days through today.
- If `window: <N>d` is passed, use that.
- Print the resolved window before researching: `Window: {start} to {end}`.

## Step 3 — Surge research (the viral signal)

A story qualifies as "viral" when it meets ALL of:

1. **Cross-media surge:** ≥3 catalog news outlets within a 48-72h cluster inside the resolved window.
2. **Tier-1 anchor:** ≥1 of those outlets is from a Tier-1 group in `sources.md`.
3. **Lens fit:** clear implication for workforce/labor and/or culture/equity/values.

Sweep WebSearch against the catalog. For candidates that look promising, WebFetch the lead source to confirm dates and key facts.

**Dedup is RELAXED in this version of the skill.** A story that appeared in a prior run **may recur in the current run** if it is still demonstrably viral within the resolved window (still being covered by ≥3 catalog outlets inside the window, not just trailing coverage). The goal is to capture **the actual top 10 viral SEA stories of the period** — even if some recur week to week.

When a recurring story is picked, note it in the metadata block as `[recurring from {prior-run-date}]` so the reader can see the persistence — but do not drop it from the ranking on that basis.

**Region weighting (default `sea`):** prioritize SEA-originating or SEA-impacting stories; SEA Tier-1 outlets (Straits Times, CNA, Jakarta Post, Bangkok Post, Inquirer, Rappler, The Star Malaysia, VnExpress, etc.) are the primary cross-citation sources; global Tier-1 (Reuters, BBC, AP, FT) supply second citations for SEA stories. Pure US/EU stories without SEA resonance are dropped.

Aim to surface **15-20 surge candidates**, then rank the top `rank:` (default 10) by surge magnitude × lens-fit weight × region-fit weight. **If fewer than `rank:` stories clear the bar**, present at actual length and explicitly flag the gap in the metadata block — do not pad below the bar.

## Step 4 — Verify and separate fact from hype

For each ranked story:

1. **Identify and confirm the primary source.** WebFetch where reachable.
2. **Note what is verifiable from primary sources** vs. amplified secondhand.
3. **Track the audience framings** so the post can land its take without strawmanning any audience.

### Translation-on-fetch (for non-English SEA sources)

When the source is in a non-English SEA language, use WebFetch's prompt parameter to translate during extraction. Pattern preserved from prior skill version. Native-language sources to consider: Kompas.id, Tempo, Detik.com, CNN Indonesia (Indonesian); Matichon, Thairath, Prachatai, Khaosod (Thai); VnExpress Vietnamese, Tuoi Tre, Thanh Nien, Lao Dong (Vietnamese); Inquirer Pilipino, ABS-CBN/GMA Filipino (Tagalog); Berita Harian, Sinar Harian, Utusan (Bahasa Malaysia); RFA Khmer, VOD (Khmer); Frontier Myanmar Burmese, Mizzima (Burmese); Lianhe Zaobao (Mandarin Singapore); Sin Chew Daily (Mandarin Malaysia).

## Step 5 — Write the LinkedIn post

Save to `posts/drafts/viral-watch-YYYY-MM-DD.md` using this template (matches the `linkedin-publisher` slug-extraction format):

```markdown
# Viral watch — top 10 viral SEA news (week of {Friday YYYY-MM-DD})

## Post 1 — top-10-viral-sea-{YYYY-MM-DD}
- **Window:** {Mon YYYY-MM-DD} to {Fri YYYY-MM-DD}
- **Region focus:** SEA
- **Lens:** {workforce | culture | both}
- **Stories ranked 1-10:** {slug-1}, {slug-2}, ..., {slug-10} [note any `[recurring from {prior-date}]`]
- **Three-lens balance:** Workforce {N} / Culture {N} / both {N}
- **Regional spread:** {SEA countries represented}
- **Word count:** {N} (excl. hashtags)
- **Character count:** {M}
- **LinkedIn-worthiness review:** pass | revise — see Step 6 notes
- **Status:** draft

---POST---
{Opening: CTO framing of the SEA week — 50-80 words. First person. Bold AND humble. Name what made the week distinctive in SEA.}

1. {Story 1 headline.} {1-2 sentence CTO take — what it means for the people / institutions / decisions a CTO of Strategy+HR+IT would be tracking in SEA.}

2. {Story 2 headline.} {CTO take.}

...

10. {Story 10 headline.} {CTO take.}

{Closing: one move the CTO is making off this week, or the open question being carried into next week. 40-80 words. Invite engagement — a real question, a specific claim, an action.}

#Hashtag1 #Hashtag2 #Hashtag3 #Hashtag4
---END---

## Sources (for audit, not in publishable body)
1. {slug-1}: {primary URL}
2. {slug-2}: {primary URL}
...
10. {slug-10}: {primary URL}

## Recurring stories (if any)
- {slug}: recurring from {prior-run-date} — {1 line why it's still viral}
```

Target body length: **400-600 words (excluding hashtags)**. Hard cap at **2,900 characters** to stay under LinkedIn's 3,000-char limit.

## Step 6 — LinkedIn-worthiness review

Before saving the final draft, **run this review** and either pass or revise:

### A. Voice and tone checks
- First person used throughout (not third-person analytical).
- **Bold AND humble** — at least one place where a position is stated firmly; at least one place where uncertainty is named.
- **Progressive** — forward-looking framing (what's becoming possible, not what's broken).
- **Professional** — measured tone, no adversarial jabs, no rhetorical gotchas.
- **No AI-tells:** delve, tapestry, navigating the landscape, in today's fast-paced world, in conclusion, moreover, furthermore — search and remove.
- **No hype/jargon:** game-changer, revolutionary, must-read, synergy, leverage, unlock value — search and remove.
- **No emojis** in the body.

### B. Engagement checks (LinkedIn-professional audience)
- **Specific opening hook** — the first sentence is something a CTO in Singapore, KL, Jakarta, Manila, Bangkok, HCMC would actually stop scrolling for. Not generic ("Here are 10 stories from SEA this week" is generic; "Three things happened in SEA this week that should change how every CTO budgets for Q3" is specific).
- **Each story entry has a take, not just a summary** — the 1-2 sentence CTO read should add interpretation a LinkedIn reader can't get from a headline alone.
- **Stories are named with regional specificity** — country names, named institutions, named actors. SEA professional readers know the difference between "in Indonesia" and "Jakarta," between "a senator" and "Jinggoy Estrada."
- **Closing invites engagement** — a real question, a specific claim, or an action. Not a generic call to "share your thoughts."
- **Hashtags** are 3-5, lowercase or CamelCase, oriented to the week's themes and the SEA professional audience (e.g. `#FutureOfWorkAsia`, `#ASEAN`, `#SEALeadership`, `#WorkforceTransformation`).

### C. Length and format checks
- **Word count: 400-600** (excluding hashtags). Run `python3 scripts/linkedin_post.py posts/drafts/viral-watch-YYYY-MM-DD.md --slug <slug> --dry-run` and confirm.
- **Character count: under 2,900** (LinkedIn limit is 3,000).
- **Numbered 1-10** ranked list — uniform format, no separate deep-dives or mini-entries (per skill design).
- **Each entry: headline + 1-2 sentence take** — no "what's verified" or "contested framings" sections; that's research-grade output for `/viral-watch`'s prior version. This skill produces publishable content.

### D. Truth and verification checks
- Every factual claim in the post traces to a source in the Sources block.
- No quotes attributed to people or institutions without a verifiable primary source.
- Recurring stories from prior runs are clearly named as still-viral, not freshly broken.
- If a story is `[search-only]` (primary source unreachable), the CTO take must be hedged accordingly ("reports suggest…") rather than asserted.

### E. Reviewer decision
- **Pass:** body publishable as written; set `LinkedIn-worthiness review: pass` in metadata.
- **Revise:** name the specific failing check(s) and revise the body. Re-run the review until pass.

## Step 7 — Append to usage history

After save, append to `.claude/skills/viral-watch/usage-history.md`:

```markdown
### Run of {YYYY-MM-DD}
- Window: {start} to {end}
- Region: SEA (or other)
- Lens(es): {lens}
- Stories covered (with rank):
  1. {slug-1}: {primary URL} [note `[recurring from {prior-date}]` if applicable]
  2. {slug-2}: {primary URL}
  ...
  10. {slug-10}: {primary URL}
- Three-lens balance: W {N} / C {N} / both {N}
- Regional spread: {countries}
- LinkedIn-worthiness review: pass | revise iterations: N
- Post slug: top-10-viral-sea-{YYYY-MM-DD}
- Date: {YYYY-MM-DD}
```

Append to the top of "Past runs (most recent first)." Recurrence is noted but does NOT block a story from this run's top 10.

## Step 8 — Present compactly to the user

Show, in this order:

1. **Resolved window**, **lens(es)**, and **region**.
2. **The ranked top 10** as a short table (rank, slug, headline, outlets, lens, recurring-from if applicable).
3. **Three-lens balance** and **regional spread** counts.
4. **The post body** (the full text between `---POST---` and `---END---`).
5. **LinkedIn-worthiness review result** — pass/revise iterations.
6. **Sources block path** (`posts/drafts/viral-watch-YYYY-MM-DD.md`).
7. **Recurring stories noted** (if any).

End with: "Want me to revise the tone, swap a story, or publish to LinkedIn?"

## Step 9 — Publish on approval

When approved, delegate to `linkedin-publisher`:

```bash
python3 scripts/linkedin_post.py posts/drafts/viral-watch-YYYY-MM-DD.md \
  --slug top-10-viral-sea-YYYY-MM-DD \
  --dry-run
```

Dry-run preview first; on explicit "yes" / "publish," re-run without `--dry-run`.

---

## Output locations (recap)

- LinkedIn post draft: `posts/drafts/viral-watch-YYYY-MM-DD.md`
- Source catalog: `.claude/skills/viral-watch/sources.md`
- Usage history (relaxed dedup ledger): `.claude/skills/viral-watch/usage-history.md`
- Prior internal-research-format reports (historical): `reports/viral-watch/`

## Hard rules

- **Top 10 ranked, uniform flat list** — most-cited → least-cited by cross-citation count. Ties broken by velocity (24-48h cluster ranks above 72h). **No deep-dives; no mini-entries split. One entry format for all 10.**
- **≥3 catalog news outlets covering the story within 48-72h** — viral bar.
- **≥1 Tier-1 catalog anchor** in the qualifying outlet set.
- **Lens fit required** — workforce/labor and/or culture/equity/values implication.
- **Dedup RELAXED** — recurring stories from prior runs MAY appear in the current top 10 if they remain demonstrably viral inside the resolved window. Note recurrence in the metadata but do not exclude.
- **First-person CTO voice** (Business Strategy + HR + IT remit). Bold AND humble. Progressive. Professional. No AI-tells, no hype, no emojis.
- **400-600 words / under 2,900 characters** in the post body. Verified before save.
- **LinkedIn-worthiness review (Step 6) must pass** before save. The review explicitly checks engagement for a SEA professional audience.
- **Sources block kept in the file for audit** but does NOT appear in the publishable body (unless `urls: on` is set).
- **No fabrication.** Every claim traces to a named source.
- **Three-lens balance and regional spread are monitored** and shown in the metadata block. If a lens has zero entries, the closing should acknowledge it.
- **Output is LinkedIn-publishable** — the skill writes for posting, not internal research.
