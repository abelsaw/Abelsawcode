# Weekly summary — source catalog (Tech & AI, engagement-ranked)

This is the curated source set the `weekly-summary` skill uses. It has **two layers** since the refactor to engagement-ranking:

1. **Discovery layer** — news outlets, AI labs, and big-tech newsrooms used to identify CANDIDATE tech/AI stories from the window.
2. **Engagement-platform layer** — LinkedIn, X/Twitter, Hacker News, Reddit. This is where the actual RANKING signal comes from.

The skill ranks stories by **cross-platform engagement signal count** (how many of the four engagement platforms showed measurable engagement on the story) — not by news-catalog citation count.

**Fidelity caveat:** Engagement is approximated via WebSearch and publicly visible like/upvote/point counts. It is not API-measured. Numbers are sampled, not exhaustive. Some platforms (especially LinkedIn) hide counts behind login walls — those stories show as "engagement visible: partial."

**Out of scope (do not include):** HR / workforce / talent / layoffs / org-design / culture / DEI / benefits / compensation stories. Even when a tech company runs a layoff cycle, only the tech-strategy shift may be included.

---

## ENGAGEMENT LAYER (primary ranking signal)

### LinkedIn
- Base URL: https://www.linkedin.com/
- Query pattern: `site:linkedin.com/posts "<story keywords>" "<month> 2026"`
- Articles pattern: `linkedin.com pulse "<topic>" <month> 2026`
- Engagement signals visible: like count, comment count, reshare count when shown; often hidden for non-followed posts
- When counts are hidden, record "engagement visible: hidden" and rely on other platforms

### X (Twitter)
- Base URL: https://x.com/
- Query patterns:
  - `site:x.com "<story keywords>"`
  - `site:twitter.com "<story keywords>"` (legacy URLs still indexed)
- Engagement signals: like count, repost count, reply count, view count when visible
- Many X posts indexed via news-aggregator quotes — search `"X post" "<story keywords>" likes`

### Hacker News
- Base URL: https://news.ycombinator.com/
- Query pattern: `site:news.ycombinator.com "<story keywords>"`
- Engagement signals: point count, comment count — both publicly visible in search snippets
- Note: HN tends to surface canonical source URLs. A high-point HN submission usually means deep developer/builder engagement
- HN's audience filter favors infra, chips, AI research, dev tools — light on enterprise SaaS / pricing

### Reddit (these subs are the AI/tech core)
- Base URL: https://www.reddit.com/
- Subs to query:
  - r/MachineLearning — research + frontier model news
  - r/singularity — AI futurism, model launches, capability discussions
  - r/OpenAI — OpenAI-specific
  - r/Anthropic — Anthropic-specific
  - r/LocalLLaMA — open-weights, local inference, GPU/hardware
  - r/programming — dev tools, infra
  - r/technology — broad tech news
  - r/hardware — chip and silicon discussions
  - r/cybersecurity — infosec discussions
- Query pattern: `site:reddit.com r/<sub> "<story keywords>"`
- Engagement signals: upvote count, comment count — both publicly visible
- A single Reddit thread with 3k+ upvotes in r/MachineLearning is a strong signal; lower bar in r/technology

### Scoring weights (for tie-break within same signal-count)
When ranking stories that tie on platform-signal count (e.g. both showed engagement on 3 of 4 platforms), use these heuristic weights to break ties by aggregate engagement volume:

- HN point: ×10 (rare, curated audience)
- LinkedIn like: ×2 (when visible)
- X like: ×1
- Reddit upvote: ×1 (in the AI/tech subs above)
- Comment counts on HN/Reddit: ×0.5 (discussion depth signal)

These weights are heuristic, not authoritative. Document them in the brief when they affect ranking order.

---

## DISCOVERY LAYER (candidate universe — NOT the ranking signal)

These outlets help identify WHICH tech/AI stories landed in the window. The skill uses them in Step 3 to assemble 15-25 candidate stories. Then Step 4 takes those candidates to the engagement-platform layer for ranking.

### Tier-1 news — US (global business + tech)
- TechCrunch — https://techcrunch.com/
- Financial Times — https://www.ft.com/
- Wall Street Journal — https://www.wsj.com/
- New York Times — Business + DealBook — https://www.nytimes.com/section/business
- Bloomberg — https://www.bloomberg.com/
- Reuters — https://www.reuters.com/technology/
- The Information — https://www.theinformation.com/
- CNBC — Technology — https://www.cnbc.com/technology/
- The Economist — https://www.economist.com/business
- Axios — https://www.axios.com/technology

### Tier-1 news — global / APAC
- BBC News — Technology — https://www.bbc.com/news/technology
- The Guardian — Technology — https://www.theguardian.com/technology
- Nikkei Asia — https://asia.nikkei.com/
- FT Asia — https://www.ft.com/world/asia-pacific
- Reuters Asia — https://www.reuters.com/world/asia-pacific/
- South China Morning Post — Tech — https://www.scmp.com/tech
- Straits Times — Tech — https://www.straitstimes.com/tech
- Korea Herald — Tech — https://www.koreaherald.com/list.php?ct=020800000000

### Tier-1 tech thought leadership
- MIT Technology Review — https://www.technologyreview.com/
- Stanford HAI — https://hai.stanford.edu/news
- Stratechery (Ben Thompson) — https://stratechery.com/
- HBR — tech pieces only — https://hbr.org/topic/technology
- MIT Sloan Management Review — tech pieces only — https://sloanreview.mit.edu/topic/technology/

### AI labs (primary sources for model + product news)
- Anthropic — https://www.anthropic.com/news
- OpenAI — https://openai.com/news
- Google DeepMind — https://deepmind.google/discover/blog/
- Google AI / Research blog — https://blog.google/technology/ai/
- Meta AI — https://ai.meta.com/blog/
- Mistral — https://mistral.ai/news/
- Cohere — https://cohere.com/blog
- xAI — https://x.ai/news
- Stability AI — https://stability.ai/news

### Big tech newsrooms
- Microsoft — https://news.microsoft.com/, https://blogs.microsoft.com/ai/, https://azure.microsoft.com/en-us/blog/
- AWS — https://aws.amazon.com/blogs/aws/
- Google Cloud — https://cloud.google.com/blog
- NVIDIA — https://nvidianews.nvidia.com/ and https://blogs.nvidia.com/
- IBM — https://newsroom.ibm.com/
- Intel — https://newsroom.intel.com/
- Oracle — https://www.oracle.com/news/
- Apple — https://www.apple.com/newsroom/
- Meta — engineering / news — https://engineering.fb.com/ and https://about.fb.com/news/
- Broadcom — https://investors.broadcom.com/news-releases
- AMD — https://www.amd.com/en/newsroom

### Tech-research / analyst firms
- Gartner press room — https://www.gartner.com/en/newsroom
- Forrester research blog — https://www.forrester.com/blogs/
- IDC press — https://www.idc.com/about/press
- SemiAnalysis (chip beat) — https://semianalysis.com/
- McKinsey Digital — https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights
- BCG X / BCG Tech — https://www.bcg.com/x
- Bain Technology — https://www.bain.com/insights/topics/technology/
- Deloitte Tech Trends — https://www2.deloitte.com/us/en/insights/focus/tech-trends.html

### IT / CIO / enterprise tech specialty (also useful as discovery for cyber / infra stories)
- CIO.com — https://www.cio.com/
- The Register — https://www.theregister.com/
- InfoQ — https://www.infoq.com/news/
- VentureBeat — https://venturebeat.com/category/ai/
- SiliconANGLE — https://siliconangle.com/
- Cybersecurity Dive — https://www.cybersecuritydive.com/
- SecurityWeek — https://www.securityweek.com/
- The New Stack — https://thenewstack.io/
- DataCenterDynamics — https://www.datacenterdynamics.com/
- DigiTimes (Asia chip beat) — https://www.digitimes.com/

---

## Do not count — excluded discovery sources

These may surface in WebSearch but **must not** be used as the lead source for a candidate story:

- MEXC and other crypto-exchange newsrooms
- OneKey, cryptobriefing.com, generic crypto blogs
- IBTimes (cite the underlying primary instead)
- Slashdot (syndication-only)
- Tom's Hardware **when syndicating** (only when original reporting)
- Yahoo Finance (count once for the underlying wire)
- Aggregator / SEO-spam AI blogs: mean.ceo, llm-stats.com, releasebot.io, ai2.work, finalroundai.com, AICC, dentro.de/ai, originbrief, buildfastwithai
- Mid-tier finance content farms when summary-only: insidermonkey, marketscreener, stocktitan, gurufocus
- Personal Substack opinion posts (unless from a recognized analyst)

---

## Out-of-scope sources (HR / workforce — removed by design)

- HR-specialty trade press (SHRM, HR Dive, HR Executive, HR Brew, Personnel Today, People Matters, HR Asia, ETHRWorld, AHRI, HKIHRM, HR Reporter)
- HR-specialty consultancies (Mercer, WTW, Aon, Gallup, Korn Ferry)
- Layoff trackers (layoffhedge, layoffs.fyi, trueup, skillsyncer)
- Reddit subs primarily about workplace/career (r/cscareerquestions, r/recruitinghell, etc.)

---

## Discovery rules

The skill MAY add a new source to **Auto-discovered sources** below when ALL of the following are true:

1. The source published the story in question within the resolved window (discovery) OR is a credible engagement platform with measurable signals (engagement).
2. The source is a recognized tech firm, lab, university, government body, tier-1 publication, or active tech/AI community — not on the exclusion list, and not HR / workforce.
3. The story is independently cross-cited or cross-engaged on at least one already-cataloged source.
4. The source is reachable via WebSearch (so future runs can verify).

When you add a discovered source, mention it in the final report to the user.

---

## Auto-discovered sources

<!-- Append entries here as the skill discovers new credible sources. Format:

### {Source} — {What it is} — {discovery layer | engagement layer} ({Month YYYY})
- URL: {root URL}
- Contributed to: {story slug}
- Discovered: {YYYY-MM-DD}

-->
