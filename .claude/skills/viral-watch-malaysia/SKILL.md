---
name: viral-watch-malaysia
description: Variant of /viral-watch locked to Malaysia only. Top 10 viral Malaysia news of the window in a single LinkedIn post, CTO voice (Business Strategy + HR + IT remit), with per-story LinkedIn-worthiness gate + post-level review. Use when the user says "viral watch Malaysia", "top 10 viral MY", "viral Malaysia news", or invokes /viral-watch-malaysia.
---

# Viral watch — Malaysia only

Thin wrapper over `/viral-watch`. **Read `.claude/skills/viral-watch/SKILL.md` for the full workflow** (Steps 1-9, the Step 4.5 per-story LinkedIn-worthiness gate, Step 6 post-level review, CTO voice rules, surge bar, dedup-relaxation rule, translation-on-fetch logic, and hard rules). This file specifies only the overrides for this Malaysia-only variant.

## Overrides vs the parent /viral-watch defaults

- **Region:** **locked to `my`** (Malaysia only). No region override is accepted for this variant — if the user wants Singapore alone, use `/viral-watch-singapore`; if broader (my+sg, sea, apac), use `/viral-watch` directly.
- **Topic filter:** Stories must originate in or materially affect Malaysia. Pure Singapore-anchored stories without a clear Malaysia angle are dropped. Cross-border MY-SG stories (RTS Link, FOMO Pay DuitNow, scam-ring extraditions involving Malaysian territory, Johor-Singapore SEZ) count when Malaysia is materially involved.
- **Source weighting:** Malaysia Tier-1 outlets are the primary cross-citation sources:
  - **English:** The Star Malaysia, Malay Mail, New Straits Times, Free Malaysia Today, Bernama (state agency), The Edge Malaysia, Malaysiakini
  - **Bahasa Malaysia:** Berita Harian, Sinar Harian, Utusan Malaysia, mStar
  - **Mandarin (Malaysia):** Sin Chew Daily, China Press, Nanyang Siang Pau
  - **Tamil (Malaysia):** Tamil Nesan, Makkal Osai, Malaysia Nanban
  - Global Tier-1 (Reuters, BBC, AP, FT, Bloomberg, SCMP, Nikkei Asia) supply **second citations** for Malaysia stories.
  - Singapore outlets supply second citation only when the story has clear Malaysia impact.
- **Slug:** `top-10-viral-malaysia-{YYYY-MM-DD}`
- **Output file:** `posts/drafts/viral-watch-malaysia-{YYYY-MM-DD}.md`
- **Usage history (own ledger):** `.claude/skills/viral-watch-malaysia/usage-history.md`. Recurrence is checked against THIS variant's history only, not against the parent's or sibling's.
- **Source catalog (shared, unchanged):** `.claude/skills/viral-watch/sources.md`
- **Translation languages:** Bahasa Malaysia (Berita Harian, Sinar Harian, Utusan, mStar), Mandarin Malaysia (Sin Chew Daily, China Press, Nanyang Siang Pau), Tamil Malaysia (Tamil Nesan, Makkal Osai, Malaysia Nanban). Singapore Mandarin/Tamil dropped from default.
- **Hashtag defaults:** Pick 3-5 from `#Malaysia`, `#MalaysiaLeadership`, `#KLCorporate`, `#MalaysiaBusiness`, `#MalaysiaHR`, `#KualaLumpur`, `#MalaysiaCorporate`, `#MadaniMalaysia`.
- **Country split metric:** Replaced by **"Geographic spread within Malaysia: Peninsula N / Sabah-Sarawak N / Federal-level N"** in the metadata block.
- **Engagement specificity (Step 6B):** Opening hook should grab a CTO in Kuala Lumpur, Cyberjaya, Penang, Iskandar Malaysia, or Kota Kinabalu. Local actors: Anwar Ibrahim, BN/PH/PN/Madani coalitions, Bank Negara, Bursa Malaysia, EPF, KWAP, PNB, Petronas, Petros, MITI, named state Menteri Besar.

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

- **Malaysia-only.** No Singapore-anchored stories unless the Malaysia angle is primary and explicit in the CTO take.
- **Slug uses `top-10-viral-malaysia-{date}`.**
- **Output file uses `viral-watch-malaysia-{date}.md`.**
- **Own usage-history ledger** at `.claude/skills/viral-watch-malaysia/usage-history.md`.
- **All other rules from parent `/viral-watch` apply unchanged.**
