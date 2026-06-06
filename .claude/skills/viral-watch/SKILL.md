---
name: viral-watch
description: Generate a single LinkedIn post for a Chief Transformation Officer (Business Strategy + HR + IT remit) covering the top 10 viral Malaysia and Singapore news stories of the window, ranked most-cited → least-cited and presented in a uniform flat list with one CTO take per story. Default region: Malaysia + Singapore (no SEA-wide reports by default). Two LinkedIn-worthiness gates: (1) per-story gate scores each ranked story on 5 criteria (business relevance / comment-worthy / reshareable / avoids partisan harm / clear business implication); stories scoring ≤2/5 are dropped. (2) Post-level review checks voice, engagement, length before save. Surge bar: ≥3 catalog outlets in 48-72h, ≥1 Tier-1 anchor, workforce/labor or culture/equity/values lens. Use when the user says "what's gone viral in Malaysia/Singapore", "top 10 viral MY SG", "viral watch", or invokes /viral-watch.
---

# Viral watch — LinkedIn post on top 10 viral Malaysia + Singapore news

You are running the `viral-watch` skill. Produce **one LinkedIn post (text only, no image)** that lists the **top 10 viral Malaysia and Singapore news stories** of the resolved window — ranked most-cited → least-cited — each carrying implications for **workforce/labor** and/or **culture/equity/values**, written in the first-person voice of a **Chief Transformation Officer whose remit spans Business Strategy, HR, and IT**.

This is **LinkedIn-publishable output**, not internal research. The voice is first-person, bold-and-humble CTO — professional, progressive, measured, and engaging for a Malaysia + Singapore professional audience.

Two gates protect quality:
- **Step 4.5 — Per-story LinkedIn-worthiness gate** scores each ranked story on 5 criteria (business relevance / comment-worthy / reshareable / avoids partisan harm / clear business implication). Stories that fail are dropped from the publishable list.
- **Step 6 — Post-level LinkedIn-worthiness review** checks the assembled post for voice, engagement, length, and verification before save.

## Optional arguments (parsed from the skill `args` string)

- `window: <N>d` — look back N days from today (default: `7d`, max: `14d`).
- `lens: <workforce|culture|both>` — restrict the lens (default: `both`).
- `region: <my-sg|my|sg|sea|apac|us|global|eu>` — bias toward stories landing in the named region. **Default: `my-sg`** (Malaysia + Singapore). Use `my` for Malaysia only, `sg` for Singapore only. `sea` widens back to the full Southeast Asia set; `apac` to all Asia-Pacific; `global` removes regional anchoring.
- `rank: <N>` — produce a ranked list of N stories instead of 10 (default: `10`, range: `5-15`).
- `urls: on` — include source URLs inline. Default: off (citations in metadata block, not in the publishable body).

If args are empty, run defaults: 7-day window, both lenses, **Malaysia + Singapore**, ranked top 10, URLs off in body.

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

**Region weighting (default `my-sg`):** prioritize stories that **originated in or materially affect Malaysia or Singapore**. Primary cross-citation sources are the Malaysia + Singapore Tier-1 outlets:
- **Singapore Tier-1:** The Straits Times, Channel News Asia (CNA), The Business Times Singapore, TODAY Online, Mothership (specialty), AsiaOne (specialty)
- **Malaysia Tier-1:** The Star Malaysia, Malay Mail, New Straits Times, Free Malaysia Today, Bernama (state news agency), The Edge Malaysia
- **Bahasa Malaysia:** Berita Harian, Sinar Harian, Utusan Malaysia
- **Mandarin (SG/MY):** Lianhe Zaobao (Singapore), Sin Chew Daily (Malaysia)
- **Tamil (SG/MY):** Tamil Murasu (Singapore), Tamil Nesan (Malaysia)

Global Tier-1 (Reuters, BBC, AP, FT, Bloomberg, SCMP, Nikkei Asia) supply **second citations** for Malaysia/Singapore stories. A story that originates outside Malaysia/Singapore but is being amplified inside MY/SG media (e.g. a US tech layoff that lands in Singapore regional staff; a Cambodian scam compound case affecting Malaysians) counts when there is clear local landing. **Pure other-country stories without Malaysia/Singapore resonance are dropped.**

Region overrides: `region: my` = Malaysia only; `region: sg` = Singapore only; `region: sea` widens back to all 10 SEA countries; `region: apac` widens further; `region: global` removes regional anchoring.

Aim to surface **15-20 surge candidates**, then rank the top `rank:` (default 10) by surge magnitude × lens-fit weight × region-fit weight. **If fewer than `rank:` stories clear the bar**, present at actual length and explicitly flag the gap in the metadata block — do not pad below the bar.

## Step 4 — Verify and separate fact from hype

For each ranked story:

1. **Identify and confirm the primary source.** WebFetch where reachable.
2. **Note what is verifiable from primary sources** vs. amplified secondhand.
3. **Track the audience framings** so the post can land its take without strawmanning any audience.

### Translation-on-fetch (for non-English Malaysia + Singapore sources)

When the source is in a non-English Malaysia/Singapore language, use WebFetch's prompt parameter to translate during extraction. Languages relevant to the default `my-sg` region:

- **Bahasa Malaysia:** Berita Harian, Sinar Harian, Utusan Malaysia, mStar (Malaysian Malay-language press)
- **Mandarin (Singapore):** Lianhe Zaobao, Shin Min Daily News, Wanbao
- **Mandarin (Malaysia):** Sin Chew Daily, China Press, Nanyang Siang Pau
- **Tamil (Singapore):** Tamil Murasu (Singapore Tamil daily)
- **Tamil (Malaysia):** Tamil Nesan, Makkal Osai, Malaysia Nanban

When using translated sources, **preserve original-language quotes inline** alongside the English translation so contested framings are auditable. Mark each translated source `[translated from {language}]` in the metadata.

When a region override widens scope (e.g. `region: sea`), the broader translation language set from the prior skill version applies (Indonesian, Thai, Vietnamese, Filipino, Khmer, Burmese, Lao).

## Step 4.5 — Per-story LinkedIn-worthiness gate

Before writing the post, **score each ranked story against 5 LinkedIn-worthiness criteria**. This is a separate filter from the surge bar in Step 3 — a story may be highly viral but unsuitable for a professional LinkedIn audience (pure entertainment, sports gossip, celebrity scandal, partisan flashpoint without a business angle).

### The 5 criteria (each scored Yes/No)

For each story, ask:

1. **Business / strategic relevance** — does the story inform a business or organizational decision a CTO of Strategy + HR + IT in Malaysia or Singapore would actually act on? (Hiring, regulation, capex, currency, supply chain, talent, vendor strategy, market entry, M&A, public-policy compliance.)

2. **Comment-worthy for a professional audience** — would a thoughtful LinkedIn reader (CEO / CFO / CHRO / CIO / CTO peer) have a substantive take they would want to share or respond to publicly?

3. **Reshareable without reputational risk** — would the LinkedIn audience member be comfortable being seen sharing this story to their network, vs. worried about reactions from clients, employees, board members, or family?

4. **Avoids partisan / divisive harm** — does the framing handle a politically or culturally polarizing topic in a way that does not alienate half the professional audience? Factual reporting on a divisive event can pass; one-sided take cannot. Sensitive topics (race, religion, geopolitics) require especially careful framing.

5. **Has clear business implication, not just news / gossip / entertainment** — does the story connect to an operational, strategic, or workforce decision a reader can act on? Pure sports incidents, celebrity scandals, viral-meme moments, and stranger-than-fiction one-offs typically fail this criterion.

### Decision rule

- **Pass (≥4 of 5 criteria met):** Story stays in the ranked top 10 and gets written into the post body.
- **Marginal (3 of 5 met):** Story stays but is flagged in metadata. Closing should not lean heavily on a marginal story.
- **Fail (≤2 of 5 met):** Story is **dropped** from the publishable top 10. If a non-recurring stronger candidate sits just below the surge bar, it can be promoted to backfill. Otherwise the ranked list shrinks — present at actual length per the no-padding rule.

### Edge cases

- **Politically sensitive stories that fail criterion 4 but otherwise pass** (e.g. major government scandal, civil-rights moment): keep them if the CTO take can stay factual and non-partisan. The framing matters more than the topic.
- **Workforce-only stories that look "boring" but are operationally significant** (wage cliffs, employment law changes, housing policy): pass criterion 1 strongly even if they would not feel "viral" to a casual reader. These are LinkedIn gold for HR/CHRO audiences.
- **Cross-border culture/sport moments** (regional rivalries, festivals, identity politics): typically fail criterion 5 unless there is a clear workforce or DEI dimension a CTO can act on.

### Output

Record the per-story scores in the post's metadata block as a small table:

```markdown
- **Per-story LinkedIn-worthiness scores (criteria 1/2/3/4/5):**
  - {slug-1}: {Y/N/Y/Y/Y} → 4/5 pass
  - {slug-2}: ...
  ...
- **Dropped from ranking by LinkedIn-worthiness gate:** {slug + reason}, {slug + reason}, ...
```

## Step 5 — Write the LinkedIn post

Save to `posts/drafts/viral-watch-YYYY-MM-DD.md` using this template (matches the `linkedin-publisher` slug-extraction format):

```markdown
# Viral watch — top 10 viral Malaysia + Singapore news (week of {Friday YYYY-MM-DD})

## Post 1 — top-10-viral-my-sg-{YYYY-MM-DD}
- **Window:** {Mon YYYY-MM-DD} to {Fri YYYY-MM-DD}
- **Region focus:** Malaysia + Singapore
- **Lens:** {workforce | culture | both}
- **Stories ranked 1-10:** {slug-1}, {slug-2}, ..., {slug-10} [note any `[recurring from {prior-date}]`]
- **Three-lens balance:** Workforce {N} / Culture {N} / both {N}
- **Country split:** Malaysia {N} / Singapore {N} / cross-border (both) {N}
- **Per-story LinkedIn-worthiness scores (criteria 1/2/3/4/5 → result):**
  - {slug-1}: Y/Y/Y/Y/Y → 5/5 pass
  - {slug-2}: Y/Y/Y/N/Y → 4/5 pass
  - ...
- **Dropped by LinkedIn-worthiness gate (if any):** {slug — reason}, ...
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
- **Specific opening hook** — the first sentence is something a CTO in Singapore CBD or Kuala Lumpur would actually stop scrolling for. Not generic ("Here are 10 stories from Malaysia and Singapore this week" is generic; "Three things happened in Singapore and Malaysia this week that should change how every CTO budgets for Q3" is specific).
- **Each story entry has a take, not just a summary** — the 1-2 sentence CTO read should add interpretation a LinkedIn reader can't get from a headline alone.
- **Stories are named with local specificity** — Malaysian and Singaporean readers know the difference between "the MAS" and "the Monetary Authority of Singapore," between "PM Anwar" and "Anwar Ibrahim's Unity Government," between "Johor" and "Putrajaya," between "Suntec" and "Marina Bay." Use the names locals use.
- **Closing invites engagement** — a real question, a specific claim, or an action. Not a generic call to "share your thoughts."
- **Hashtags** are 3-5, lowercase or CamelCase, oriented to the week's themes and the Malaysia + Singapore professional audience (e.g. `#Singapore`, `#Malaysia`, `#SGBusiness`, `#MalaysiaLeadership`, `#KLCorporate`, `#SingaporeHR`, `#WorkforceTransformation`, `#FutureOfWorkAsia`).

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
- Country split: Malaysia {N} / Singapore {N} / cross-border {N}
- LinkedIn-worthiness review: pass | revise iterations: N
- Post slug: top-10-viral-my-sg-{YYYY-MM-DD}
- Date: {YYYY-MM-DD}
```

Append to the top of "Past runs (most recent first)." Recurrence is noted but does NOT block a story from this run's top 10.

## Step 8 — Present compactly to the user

Show, in this order:

1. **Resolved window**, **lens(es)**, and **region**.
2. **The ranked top 10** as a short table (rank, slug, headline, outlets, lens, recurring-from if applicable).
3. **Three-lens balance**, **Malaysia/Singapore country split**, and **per-story LinkedIn-worthiness scores** (with any dropped stories named).
4. **The post body** (the full text between `---POST---` and `---END---`).
5. **Post-level LinkedIn-worthiness review result** (Step 6) — pass/revise iterations.
6. **Sources block path** (`posts/drafts/viral-watch-YYYY-MM-DD.md`).
7. **Recurring stories noted** (if any).

End with: "Want me to revise the tone, swap a story, or publish to LinkedIn?"

## Step 9 — Publish on approval

When approved, delegate to `linkedin-publisher`:

```bash
python3 scripts/linkedin_post.py posts/drafts/viral-watch-YYYY-MM-DD.md \
  --slug top-10-viral-my-sg-YYYY-MM-DD \
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
- **Per-story LinkedIn-worthiness gate (Step 4.5) runs before writing.** Stories scoring ≤2/5 on the 5 LinkedIn-worthiness criteria are dropped from the ranked list. Stories scoring 3/5 stay but are flagged as marginal. The ranked list may shrink — no padding.
- **Post-level LinkedIn-worthiness review (Step 6) must pass** before save. The review explicitly checks voice, engagement, length, and verification for a Malaysia + Singapore professional audience.
- **Sources block kept in the file for audit** but does NOT appear in the publishable body (unless `urls: on` is set).
- **No fabrication.** Every claim traces to a named source.
- **Default region is Malaysia + Singapore only.** Stories must originate in or materially affect Malaysia or Singapore. Use `region: sea` / `region: apac` / `region: global` to widen.
- **Three-lens balance and Malaysia/Singapore country split are monitored** and shown in the metadata block. If a lens has zero entries, the closing should acknowledge it. If only one country (MY or SG) appears, flag the skew.
- **Output is LinkedIn-publishable** — the skill writes for posting, not internal research.
