---
name: viral-watch-singapore
description: Variant of /viral-watch locked to Singapore only. Top 10 viral Singapore news of the window in a single LinkedIn post, CTO voice (Business Strategy + HR + IT remit), with per-story LinkedIn-worthiness gate + post-level review. Use when the user says "viral watch Singapore", "top 10 viral SG", "viral Singapore news", or invokes /viral-watch-singapore.
---

# Viral watch — Singapore only

Thin wrapper over `/viral-watch`. **Read `.claude/skills/viral-watch/SKILL.md` for the full workflow** (Steps 1-9, the Step 4.5 per-story LinkedIn-worthiness gate, Step 6 post-level review, CTO voice rules, surge bar, dedup-relaxation rule, translation-on-fetch logic, and hard rules). This file specifies only the overrides for this Singapore-only variant.

## Overrides vs the parent /viral-watch defaults

- **Region:** **locked to `sg`** (Singapore only). No region override is accepted for this variant — if the user wants Malaysia alone, use `/viral-watch-malaysia`; if broader (my+sg, sea, apac), use `/viral-watch` directly.
- **Topic filter:** Stories must originate in or materially affect Singapore. Pure Malaysia-anchored stories without a clear Singapore angle are dropped. Cross-border MY-SG stories (RTS Link, FOMO Pay DuitNow, scam-ring extraditions involving Singapore victims/perpetrators, Johor-Singapore SEZ) count when Singapore is materially involved.
- **Source weighting:** Singapore Tier-1 outlets are the primary cross-citation sources:
  - **English:** The Straits Times, Channel News Asia (CNA), The Business Times Singapore, TODAY Online, Mothership (specialty), AsiaOne (specialty), Stomp (community), The Edge Singapore, BERG (Business Times)
  - **Mandarin (Singapore):** Lianhe Zaobao, Shin Min Daily News, Wanbao
  - **Tamil (Singapore):** Tamil Murasu
  - **Government primary sources:** PMO Singapore, MAS, MOM, MTI, MHA, HDB, EDB press releases
  - Global Tier-1 (Reuters, BBC, AP, FT, Bloomberg, SCMP, Nikkei Asia) supply **second citations** for Singapore stories.
  - Malaysia outlets supply second citation only when the story has clear Singapore impact.
- **Slug:** `top-10-viral-singapore-{YYYY-MM-DD}`
- **Output file:** `posts/drafts/viral-watch-singapore-{YYYY-MM-DD}.md`
- **Usage history (own ledger):** `.claude/skills/viral-watch-singapore/usage-history.md`. Recurrence is checked against THIS variant's history only, not against the parent's or sibling's.
- **Source catalog (shared, unchanged):** `.claude/skills/viral-watch/sources.md`
- **Translation languages:** Mandarin Singapore (Lianhe Zaobao, Shin Min Daily News, Wanbao), Tamil Singapore (Tamil Murasu). Bahasa Malaysia / Mandarin Malaysia / Tamil Malaysia dropped from default.
- **Hashtag defaults:** Pick 3-5 from `#Singapore`, `#SGBusiness`, `#SingaporeLeadership`, `#SingaporeHR`, `#SingaporeBusiness`, `#SGCorporate`, `#CBDSingapore`, `#SmartNationSG`.
- **Country split metric:** Replaced by **"Sector spread: Government N / Business N / Civic-cultural N / Cross-border N"** in the metadata block.
- **Engagement specificity (Step 6B):** Opening hook should grab a CTO in CBD, Marina Bay, one-north, Jurong Innovation District, or Tampines hub. Local actors: PM, named Ministers and SMSes, MAS, MOM, MTI, EDB, HDB, GIC, Temasek, named GLCs (DBS/OCBC/UOB, ST Engineering, Singtel), Workfare/WIS/PWCS programs, named GRCs/SMCs.

## Inherited unchanged from /viral-watch

- Surge bar (≥3 catalog outlets in 48-72h, ≥1 Tier-1 anchor)
- Lens fit (workforce/labor + culture/equity/values)
- Per-story LinkedIn-worthiness gate (Step 4.5, 5 criteria: business relevance / comment-worthy / reshareable / non-partisan / clear business implication)
- Post-level LinkedIn-worthiness review (Step 6)
- CTO voice (first-person, bold AND humble, no AI-tells, no hype, no emojis)
- Length: 400-600 words / under 2,900 characters
- Relaxed dedup (recurring stories allowed if still demonstrably viral)
- Numbered 1-10 uniform flat list (no deep-dive/mini-entry split)
- Ranked by surge magnitude × lens-fit × region-fit (or by raw citation count if user requests "rank by mentions")
- linkedin-publisher integration on approval

## Hard rules (this variant)

- **Singapore-only.** No Malaysia-anchored stories unless the Singapore angle is primary and explicit in the CTO take.
- **Slug uses `top-10-viral-singapore-{date}`.**
- **Output file uses `viral-watch-singapore-{date}.md`.**
- **Own usage-history ledger** at `.claude/skills/viral-watch-singapore/usage-history.md`.
- **All other rules from parent `/viral-watch` apply unchanged.**
