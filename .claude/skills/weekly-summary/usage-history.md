# Weekly summary — usage history

This is the rolling ledger of stories and themes used in past `/weekly-summary`
runs. The skill reads it before researching each new run and excludes any story
URL used in the **last 3 weekly runs** to avoid duplication. Theme overlap
across weeks is allowed (some topics are sustained); story duplication is not.

To allow a previously-used story to recycle (e.g. a multi-week regulatory
thread), manually delete its entry from the relevant week below.

## Past weeks (most recent first)

### Week of 2026-06-26 (ENGAGEMENT-RANKED — first run of new methodology, test pass)
- Window: 2026-06-22 to 2026-06-26
- Length: 10 of 10
- **Ranking signal:** cross-platform engagement (LinkedIn / X / HN / Reddit), approximated via WebSearch + visible counts
- **Fidelity:** approximated, not API-measured; LinkedIn counts often hidden
- **Test-pass deltas vs prior citation-ranked runs (f68c565 / 72306c3):**
  - PROMOTED: Amazon Q Developer CVE-2026-12957/12958 (climbed from outside top 10), METR cheating-rate / Terminal-Bench scores on Sol Ultra (new)
  - DEMOTED: NVIDIA ISC drops to #10; Microsoft 365 Copilot pricing / tokenmaxxing→efficiency / Claude enterprise updates / OpenSSL all dropped from top 10
- Through-line: Same week, ranked by community engagement, not news coverage. Top three held. Middle shifted. Two stories climbed from outside the news cycle.
- Three-lens balance: Models 4 · Infra 3 · Enterprise tech 3
- Ranked stories 1-10:
  1. gpt-5-6-sol-terra-luna-us-gov-gated: https://openai.com/index/previewing-gpt-5-6-sol/ — 4/4 (HN front-page 1,000+ points)
  2. openai-broadcom-jalapeno-chip: https://www.cnbc.com/2026/06/24/openai-and-broadcom-reveal-jalapeno-first-ai-chip-in-partnership.html — 4/4
  3. qualcomm-modular-4b-acquisition: https://www.bloomberg.com/news/articles/2026-06-22/qualcomm-is-said-to-near-deal-for-ai-chip-startup-modular — 4/4 (Lattner factor)
  4. amazon-q-developer-cve-mcp-cred-theft: https://www.wiz.io/blog/amazon-q-vulnerability — 4/4 ⭐ NEW
  5. anthropic-alibaba-qwen-distillation: https://www.cnbc.com/2026/06/24/anthropic-alibaba-distillation-campaign.html — 4/4
  6. anthropic-mythos-5-us-gov-cleared: https://edition.cnn.com/2026/06/26/tech/anthropic-mythos-release — 3-4/4
  7. openai-daybreak-expansion-patch-the-planet: https://openai.com/index/daybreak-securing-the-world/ — 3-4/4
  8. check-point-vpn-cve-cisa-emergency-directive: https://www.esecurityplanet.com/weekly-roundup/zero-days-ai-exploits-and-supply-chain-risks-define-this-week-in-cybersecurity-in-june-2026/ — 3-4/4
  9. metr-sol-ultra-cheating-detection-terminalbench: https://www.latent.space/p/ainews-openai-gpt-56-sol-terra-luna — 3/4 ⭐ NEW
  10. nvidia-isc-2026-bionemo-halos-eu: https://nvidianews.nvidia.com/news/latest — 2-3/4
- Post slug: what-the-community-actually-engaged-with
- Word count: 414 / Character count: 2,930 / LinkedIn cap 3,000
- Date: 2026-06-26 (test pass run on 2026-06-28)
- Post draft path: posts/drafts/weekly-summary-2026-06-26-engagement.md
- Research brief: posts/drafts/weekly-research-2026-06-26-engagement.md

### Week of 2026-06-26 (TECH-ONLY, OpenAI/Anthropic model releases EXCLUDED — filter-change re-rank)
- Window: 2026-06-22 to 2026-06-26
- Length: 10 of 10
- **Args:** `exclude the Open AI and Anthropic new model release`
- **Scope:** Pure tech & AI, with GPT-5.6 Sol/Terra/Luna and Anthropic Mythos 5 removed by user request
- **Dedup note:** Softened — prior tech-only Jun 22-26 run (f68c565) carryover. 2 new stories surface to fill the GPT-5.6 / Mythos 5 vacancies: OpenAI Daybreak expansion (Mon Jun 22) and Microsoft 365 Copilot Business permanent SKU transition (Jul 1 effective).
- Through-line: Set aside the two frontier model launches, and the week's story is cost-down, defense-up, dependency-real. The substrate is what moved.
- Three-lens balance: Models 2 · Infra 3 · Enterprise tech 5 (Models thin by design — excluding the frontier releases hollows out this lens)
- Ranked stories 1-10:
  1. openai-broadcom-jalapeno-chip: https://www.cnbc.com/2026/06/24/openai-and-broadcom-reveal-jalapeno-first-ai-chip-in-partnership.html — 7+
  2. qualcomm-modular-4b-acquisition: https://www.bloomberg.com/news/articles/2026-06-22/qualcomm-is-said-to-near-deal-for-ai-chip-startup-modular — 5+
  3. openai-daybreak-expansion-patch-the-planet: https://openai.com/index/daybreak-securing-the-world/ — 6+
  4. anthropic-alibaba-qwen-distillation: https://www.cnbc.com/2026/06/24/anthropic-alibaba-distillation-campaign.html — 4+
  5. nvidia-isc-2026-bionemo-halos-eu: https://nvidianews.nvidia.com/news/latest — 3+
  6. check-point-vpn-cve-cisa-emergency-directive: https://www.esecurityplanet.com/weekly-roundup/zero-days-ai-exploits-and-supply-chain-risks-define-this-week-in-cybersecurity-in-june-2026/ — 3+
  7. tokenmaxxing-to-efficiency-shift: https://www.cnbc.com/2026/06/26/openai-anthropic-new-ai-spending-reality-as-users-shift-to-efficiency.html — 3+
  8. microsoft-365-copilot-pricing-transition-permanent: https://learn.microsoft.com/en-us/partner-center/announcements/2026-june — 3+ [thin Tier-1]
  9. claude-enterprise-updates-batch: https://support.claude.com/en/articles/12138966-release-notes — 2+ [thin]
  10. openssl-pkcs7-rce-vulnerability: (OpenSSL Security Advisory, week of 2026-06-22) — 2+ [thin]
- Post slug: the-substrate-is-what-moved
- Word count: ~440 / Character count: 2,897 / LinkedIn cap 3,000
- Date: 2026-06-26 (run on 2026-06-28, filter-change re-rank)
- Post draft path: posts/drafts/weekly-summary-2026-06-26-no-model-releases.md
- Research brief: posts/drafts/weekly-research-2026-06-26-no-model-releases.md

### Week of 2026-06-26 (TECH-ONLY RE-RUN — scope-transition)
- Window: 2026-06-22 to 2026-06-26
- Length: 10 of 10
- **Scope:** Pure tech & AI (per refactored skill — HR / workforce / culture / DEI excluded by design)
- **Dedup note:** Softened dedup for this single run because the prior 2026-06-26 entry below ran under the OLD scope (CTO + HR + Business Strategy). 5 of this run's stories overlap with the prior run's tech stories (Jalapeño, Anthropic-Alibaba, Qualcomm-Modular, NVIDIA ISC, tokenmaxxing). Going forward, normal dedup applies against THIS entry.
- Through-line: Same Friday, OpenAI shipped GPT-5.6 and Anthropic shipped Mythos 5 — both under US-government limited preview. OpenAI also taped out its first custom chip with Broadcom (Jalapeño). The model layer and its substrate moved together.
- Three-lens balance: Models 3 · Infra 3 · Enterprise tech 4
- Ranked stories 1-10:
  1. gpt-5-6-sol-terra-luna-limited-preview: https://openai.com/index/previewing-gpt-5-6-sol/ — 7+
  2. anthropic-mythos-5-us-gov-cleared: https://edition.cnn.com/2026/06/26/tech/anthropic-mythos-release — 4+
  3. openai-broadcom-jalapeno-chip: https://www.cnbc.com/2026/06/24/openai-and-broadcom-reveal-jalapeno-first-ai-chip-in-partnership.html — 9+
  4. qualcomm-modular-4b-acquisition: https://www.bloomberg.com/news/articles/2026-06-22/qualcomm-is-said-to-near-deal-for-ai-chip-startup-modular — 7+
  5. anthropic-alibaba-qwen-distillation: https://www.cnbc.com/2026/06/24/anthropic-alibaba-distillation-campaign.html — 6+
  6. check-point-vpn-cve-cisa-emergency-directive: https://www.esecurityplanet.com/weekly-roundup/zero-days-ai-exploits-and-supply-chain-risks-define-this-week-in-cybersecurity-in-june-2026/ — 3+
  7. nvidia-isc-2026-bionemo-halos-eu: https://nvidianews.nvidia.com/news/latest — 4+
  8. tokenmaxxing-to-efficiency-shift: https://www.cnbc.com/2026/06/26/openai-anthropic-new-ai-spending-reality-as-users-shift-to-efficiency.html — 4+
  9. claude-enterprise-updates-batch: https://support.claude.com/en/articles/12138966-release-notes — 3+
  10. openssl-pkcs7-rce-vulnerability: (OpenSSL Security Advisory, week of 2026-06-22) — 2+ [thin]
- Post slug: frontier-and-substrate-rewired-same-week
- Word count: ~445 / Character count: 2,940 / LinkedIn cap 3,000
- Date: 2026-06-26 (run on 2026-06-28, scope-transition re-rank)
- Post draft path: posts/drafts/weekly-summary-2026-06-26-tech.md
- Research brief: posts/drafts/weekly-research-2026-06-26-tech.md

### Week of 2026-06-26 (Mon Jun 22 - Fri Jun 26)
- Window: 2026-06-22 to 2026-06-26 (clamped from user-requested Jun 21-28)
- Length: 10 of 10
- Through-line: The AI cost equation tightened across every lens — OpenAI's Jalapeño at ~50% GPU cost, Qualcomm-Modular CUDA challenger, Oracle 21K AI-driven cuts, VW 100K-job restructure threat, four senior Google→Anthropic exits in 6 days.
- Ranked stories 1-10:
  1. openai-broadcom-jalapeno-chip: https://www.cnbc.com/2026/06/24/openai-and-broadcom-reveal-jalapeno-first-ai-chip-in-partnership.html — 9+
  2. anthropic-alibaba-qwen-distillation: https://www.cnbc.com/2026/06/24/anthropic-alibaba-distillation-campaign.html — 9+
  3. vw-100k-layoffs-4-plants: https://www.cnn.com/2026/06/26/economy/volkswagen-job-cuts — 7+
  4. oracle-21k-ai-driven: https://www.bloomberg.com/news/articles/2026-06-22/oracle-layoffs-fueled-by-ai-reduces-workforce-by-21-000 — 6+
  5. qualcomm-modular-4b: https://www.bloomberg.com/news/articles/2026-06-22/qualcomm-is-said-to-near-deal-for-ai-chip-startup-modular — 7+
  6. google-anthropic-gemini-exodus: https://www.bloomberg.com/news/articles/2026-06-24/google-poised-to-lose-two-more-high-profile-ai-staffers-to-anthropic — 6+
  7. fedex-q4-fy26-earnings-beat: https://www.cnbc.com/2026/06/23/fedex-fdx-q4-2026-earnings.html — 5+
  8. carnival-q2-2026-record: https://www.investing.com/news/company-news/carnival-q2-2026-slides-record-results-amid-geopolitical-headwinds-93CH-4756051 — 5+
  9. nvidia-isc-2026-bionemo-halos-eu: https://nvidianews.nvidia.com/news/latest — 4+
  10. tokenmaxxing-to-efficiency-shift: https://www.cnbc.com/2026/06/26/openai-anthropic-new-ai-spending-reality-as-users-shift-to-efficiency.html — 4+
- Three-lens balance: IT 5 / HR 3 / Business Strategy 2 — all cleared
- Post slug: the-cost-equation-tightened
- Word count: 449 / Character count: 2,980 / LinkedIn cap 3,000
- Date: 2026-06-26 (run on 2026-06-28, standard post-Friday cadence)
- Post draft path: posts/drafts/weekly-summary-2026-06-26.md
- Research brief: posts/drafts/weekly-research-2026-06-26.md

### Week of 2026-06-19 (partial — Mon Jun 15 only, current-week early trigger)
- Window: 2026-06-15 to 2026-06-19, ranked off Mon Jun 15 events only
- Length: 5 of 10 (not padded) — partial-week run, only one trading day inside window
- Through-line: The week opened on geopolitics, not tech — US-Iran MOU re-priced oil and equities in one session; SpaceX kept climbing; FOMC Wednesday under a new Chair is the real hinge; BBC's 2,000-job restructure is the HR story.
- Ranked stories 1-5:
  1. us-iran-mou-hormuz-reopening: https://www.cnbc.com/2026/06/15/us-iran-deal-hormuz-markets.html — 10+
  2. spcx-day2-monday-ath: https://www.cnbc.com/2026/06/15/spacex-stock-record-ipo-debut.html — 7+
  3. fomc-june-warsh-debut-preview: https://www.cnbc.com/2026/06/17/fed-interest-rate-decision-june-2026.html — 6+
  4. bbc-2000-layoffs-budget-cut: https://www.theworkersrights.com/bbc-layoffs-2026-2000-job-cuts-impact/ — 5+
  5. pltr-monday-bounce-5pct: https://stockinvest.us/stock-news/a-very-strong-day-for-palantir-stock-price-on-monday-2026-06-15 — 4+ [adjacent to #1]
- Three-lens balance: Business Strategy 4 / HR 1 / IT 0 (gap named in closing)
- Post slug: week-opened-on-geopolitics
- Word count: 415 / Character count: 2,469 / LinkedIn cap 3,000
- Date: 2026-06-15 (early trigger; full Friday wrap to come)
- Post draft path: posts/drafts/weekly-summary-2026-06-19.md
- Research brief: posts/drafts/weekly-research-2026-06-19.md

### Week of 2026-06-12
- Through-line: The buyer and the seller showed up in the same news cycle — SpaceX listed above $2T, OpenAI confirmed a confidential S-1, Apple rebuilt Siri on Gemini, Anthropic shipped Fable 5, Oracle and Adobe printed record AI revenue. Palantir's Karp said the buyer's verdict out loud.
- Ranked stories 1-10:
  1. spacex-ipo-spcx-nasdaq-trillionaire: https://www.cnbc.com/2026/06/12/spacex-ipo-spcx-live-updates.html — 10+
  2. apple-wwdc-2026-siri-gemini-liquid-glass: https://www.cnbc.com/2026/06/08/apple-wwdc-2026-live-updates.html — 10+
  3. anthropic-claude-fable-5-mythos-public: https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5 — 8+
  4. oracle-q4-fy26-67b-ai-contracts: https://investor.oracle.com/investor-news/news-details/2026/Oracle-Announces-Record-Q4-and-FY-2026-Results-Driven-by-Cloud-Infrastructure--Cloud-Applications/default.aspx — 7+
  5. openai-confidential-s1-filing: https://www.cnbc.com/2026/06/08/openai-confidentially-files-for-ipo-prepping-wall-street-for-ai-debut.html — 7+
  6. adobe-q2-fy26-ai-first-arr-500m: https://www.sec.gov/Archives/edgar/data/0000796343/000079634326000109/adbeex991q226.htm — 6+
  7. palantir-karp-tokenmaxxing-unhappy: https://www.cnbc.com/2026/06/10/palantir-karp-enterprise-ai.html — 6+
  8. crowdstrike-2026-tech-threat-landscape: https://ir.crowdstrike.com/news-releases/news-release-details/crowdstrike-2026-technology-threat-landscape-report-china-steals — 5+
  9. gitlab-agentic-restructure-350-roles: https://skillsyncer.com/layoffs-tracker — 3+ [thinner Tier-1]
  10. amdocs-2900-role-reorganization: https://skillsyncer.com/layoffs-tracker — 3+ [thinner Tier-1]
- Three-lens balance: Business Strategy 5 / IT 4 / HR 2 (rank 7 crosses IT/Strategy)
- Post slug: buyer-and-seller-same-week
- Word count: 463 / Character count: 2,893 / LinkedIn cap 3,000
- Date: 2026-06-12
- Post draft path: posts/drafts/weekly-summary-2026-06-12.md
- Research brief: posts/drafts/weekly-research-2026-06-12.md

### Week of 2026-06-05 (user-specified window May 30 – June 5)
- Through-line: Capital markets did the talking — Alphabet ($85B), Meta (FT exclusive), HPE, CrowdStrike and Anthropic all moved at the funding layer. Microsoft Build set Windows up as an OS for agents. Washington narrowed its AI EO. The HR lens stayed quiet.
- Ranked stories 1-10:
  1. alphabet-85b-equity-raise: https://www.bloomberg.com/news/articles/2026-06-01/alphabet-to-raise-80-billion-in-equity-capital-for-ai-spending — 10+
  2. microsoft-build-autopilots: https://www.cnbc.com/2026/06/02/microsoft-unveils-new-ai-models-lessen-reliance-on-openai-lower-costs.html — 10+
  3. trump-ai-executive-order-voluntary: https://techcrunch.com/2026/06/02/trump-signs-narrower-executive-order-on-ai-oversight-after-industry-objections/ — 7+
  4. meta-equity-raise-ft-exclusive: https://www.cnbc.com/2026/06/05/meta-stock-sinks-on-report-company-could-raise-tens-of-billions-for-ai.html — 8+
  5. openai-codex-enterprise: https://techcrunch.com/2026/06/02/openai-launches-new-codex-tools-for-white-collar-work/ — 6+
  6. nvidia-rtx-spark-mediatek: https://www.cnbc.com/2026/06/02/nvidias-new-pc-chips-are-ceos-bid-to-own-every-part-of-ai-stack.html — 5+
  7. hpe-q2-fy26-earnings: https://www.sec.gov/Archives/edgar/data/0001645590/000164559026000052/ex-991x612026x8k.htm — 6+
  8. morgan-stanley-wealth-ai-agents: https://www.cnbc.com/2026/06/03/ai-agents-morgan-stanley-wealth-management-funnel.html — 5+
  9. crowdstrike-q1-charlotte-quiltworks: https://www.sec.gov/Archives/edgar/data/0001535527/000153552726000022/crwd-20260603xex991.htm — 4+ [thinner Tier-1]
  10. anthropic-confidential-ipo-filing: https://www.buildfastwithai.com/blogs/ai-news-today-june-1-2026 — 3+ [thinner Tier-1]
- Three-lens balance: Business Strategy 5 / IT 6 / HR 0 (HR gap named in post closing)
- Post slug: capital-and-the-quiet-hr-shelf
- Date: 2026-06-05

### Week of 2026-05-29 (ranked-top-10 re-run)
- Through-line: Thursday May 28 was the week's gravitational center — Anthropic flexed at $965B, Opus 4.8 shipped the same day, M&A clocked two more stack-layer deals, and earnings season started telling the AI revenue story aloud.
- Ranked stories 1-10:
  1. anthropic-series-h-965b: https://techcrunch.com/2026/05/28/anthropic-raises-65-billion-nears-1t-valuation-ahead-of-ipo/ — 10+
  2. claude-opus-4-8: https://techcrunch.com/2026/05/28/anthropic-releases-opus-4-8-with-new-dynamic-workflow-tool/ — 10+
  3. asana-stackai: https://techcrunch.com/2026/05/28/asana-acquires-no-code-agent-builder-stack-ai/ — 10+
  4. dell-fy27-q1-earnings: https://www.morningstar.com/stocks/dell-earnings-huge-ai-acceleration-fuels-historic-guidance-raise — 6+
  5. snowflake-q1-fy27-earnings: https://investingnews.com/top-tech-news/ — 6+
  6. palo-alto-portkey: https://www.paloaltonetworks.com/company/press/2026/palo-alto-networks-completes-acquisition-of-portkey-to-secure-ai-agents — 5+
  7. openai-frontier-governance-framework: https://openai.com/index/openai-frontier-governance-framework/ — 7+
  8. salesforce-q1-earnings-pressure: https://investingnews.com/top-tech-news/ — 4+
  9. ibm-project-lightwell-quantum: https://investingnews.com/top-tech-news/ — 4+
  10. openai-rosalind-biodefense: https://openai.com/news/ — 3+
- Post slug: ten-things-i-tracked
- Date: 2026-06-05
- Supersedes: prior 2026-06-01 entry for this week (old 3-option format)

### Week of 2026-05-22
- Theme: This was the week the agent stack and the workforce conversation finally collided in the open — capability shipped, enterprise control shipped, and a CEO said the quiet part out loud (then walked it back).
- Story URLs:
  - gemini-3-5-flash: https://techcrunch.com/2026/05/19/with-gemini-3-5-flash-google-bets-its-next-ai-wave-on-agents-not-chatbots/
  - anthropic-managed-agents: https://www.infoq.com/news/2026/05/code-with-claude/
  - stanchart-lower-value-human-capital: https://www.bloomberg.com/news/articles/2026-05-19/stanchart-ceo-says-ai-to-replace-lower-value-human-capital
- Option slugs: capability-control-consequence (synthesis), who-owns-the-language (question), what-shifted-me (learning)
- Date: 2026-05-23
