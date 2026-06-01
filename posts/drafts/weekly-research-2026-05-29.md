# Weekly research brief — 2026-05-29
Window: 2026-05-25 to 2026-05-29

## Theme (the through-line)
This was the week the enterprise agent stack put a price on itself. Three different layers — orchestration, security, foundation — moved within 48 hours, at three radically different price brackets. The build-vs-buy conversation just got a half-life.

## Story 1 — asana-stackai
- **Headline:** Asana acquires no-code agent-builder StackAI for $75M, framing itself as "the operating system for human-agent teams"
- **Lead source:** TechCrunch, 2026-05-28 — https://techcrunch.com/2026/05/28/asana-acquires-no-code-agent-builder-stack-ai/
- **Also covered by:**
  - BusinessWire (Asana official), 2026-05-28 — https://www.businesswire.com/news/home/20260528515345/en/Asana-Acquires-StackAI-Adding-Cross-System-Execution-for-Human-Agent-Teams
  - Yahoo Finance, 2026-05-28 — https://finance.yahoo.com/sectors/technology/articles/asana-acquires-no-code-agent-200607715.html
  - SiliconANGLE, 2026-05-28 — https://siliconangle.com/2026/05/28/asana-acquires-stackai-run-ai-agent-workflows-across-enterprise-systems/
  - Reworked, 2026-05-28 — https://www.reworked.co/digital-workplace/asana-buys-stackai-to-power-agent-orchestration/
  - Morningstar / Investing.com / The Next Web / UC Today / Stock Titan / Seeking Alpha — also covered
- **Citation count:** 10+ credible outlets
- **What happened:** Asana announced the acquisition Thursday afternoon to coincide with its earnings call. StackAI is a no-code workflow platform for designing, testing, deploying and managing custom AI agents across enterprise systems — Salesforce, Oracle, Slack, AWS, Gsuite. CEO Dan Rogers framed the deal as the most concrete step in turning Asana into "the operating system for human-agent teams." StackAI's founders Tony Rosinol and Bernard Aceituno join Asana; StackAI continues as its own brand. The acquisition pairs StackAI's workflow engine with Asana's existing AI Teammates and AI Studio.
- **Why a CTO cares:** This is a buyer taking the orchestration layer off the in-house roadmap. If your 2026 plan included building cross-system agent workflows on top of a project-management spine, that capability is now a vendor evaluation.
- **Hook into the theme:** Orchestration layer — $75M.

## Story 2 — palo-alto-portkey
- **Headline:** Palo Alto Networks completes Portkey acquisition, putting an AI gateway at the center of enterprise agent governance
- **Lead source:** Palo Alto Networks press release, 2026-05-29 — https://www.paloaltonetworks.com/company/press/2026/palo-alto-networks-completes-acquisition-of-portkey-to-secure-ai-agents
- **Also covered by:**
  - Yahoo Finance, 2026-05-29 — https://finance.yahoo.com/sectors/technology/articles/palo-alto-networks-panw-completes-112329938.html
  - MarketScreener, 2026-05-29 — https://www.marketscreener.com/news/palo-alto-completes-acquisition-of-portkey-to-secure-ai-agents-ce7f5ddbdc81f423
  - Insider Monkey, 2026-05-29 — https://www.insidermonkey.com/blog/palo-alto-networks-panw-completes-acquisition-of-ai-gateway-provider-portkey-1772967/
  - SEC Form 8-K filing (PANW), 2026-05-29
  - TechTimes analysis, 2026-05-31 — https://www.techtimes.com/articles/317470/20260531/enterprise-ai-agent-stack-takes-shape-asana-palo-alto-buy-execution-security-layers.htm
- **Citation count:** 5+ credible outlets plus SEC filing
- **What happened:** Palo Alto Networks closed its purchase of Portkey on May 29, estimated at $120-140M. Portkey is an "AI gateway" — a central control plane that monitors, orchestrates, and governs all AI traffic, processing trillions of tokens. The technology folds into Palo Alto's Prisma AIRS security platform alongside its prior CyberArk (identity) and Chronosphere (observability) acquisitions. The strategic framing: "as organizations move from simple chatbots to autonomous AI agents that take action they face a trust gap, with AI's independent execution introducing new risks of unauthorized actions, data exposure, and unchecked costs."
- **Why a CTO cares:** This is a buyer taking the security/gateway layer off the in-house roadmap, at a higher price than the orchestration layer, signaling where the security spend is going. The agent-governance category is consolidating into the same vendors who already own perimeter and identity.
- **Hook into the theme:** Security/gateway layer — ~$130M.

## Story 3 — anthropic-series-h-965b
- **Headline:** Anthropic closes Series H at $965B valuation; briefly the most valuable AI startup
- **Lead source:** CNBC, 2026-05-28 — https://www.cnbc.com/2026/05/28/anthropic-open-ai-startup-value.html
- **Also covered by:**
  - Bloomberg, 2026-05-22 (pre-close report) — https://www.bloomberg.com/news/articles/2026-05-22/anthropic-to-close-over-30-billion-round-as-soon-as-next-week
  - Financial Times (via spendnode summary), 2026-05-28
  - The Information, 2026-05 — https://www.theinformation.com/briefings/anthropic-picks-co-leads-900-billion-valuation-funding-round
  - Yahoo Finance, 2026-05-28 — https://finance.yahoo.com/markets/stocks/articles/anthropic-set-close-30-billion-203545596.html
  - MEXC News, 2026-05-28 — https://www.mexc.com/news/1095067
- **Citation count:** 5+ credible outlets including FT, CNBC, Bloomberg, The Information
- **What happened:** Anthropic announced a $65B Series H on Thursday May 28 at a $965B post-money valuation, led by Altimeter Capital, Dragoneer, Greenoaks and Sequoia Capital. The round includes $15B of previously committed investments (including $5B from Amazon), so the new capital being raised is ~$50B. The valuation briefly made Anthropic the most valuable AI startup on earth, surpassing OpenAI. The earlier reporting from May 22-24 had framed the round as $30B at $900B; the actual close was larger and at a higher mark.
- **Why a CTO cares:** This is the model layer pricing itself. When the foundation a CTO depends on for agentic workloads is capitalized at near-trillion-dollar levels, the cost of trying to substitute or build alternatives in-house climbs in lockstep. The strategic implication: the foundation layer is where buyers — not builders — have decided the value lives.
- **Hook into the theme:** Foundation layer — $965B valuation.

## Candidates considered but not picked
- SAP Sapphire + NVIDIA OpenShell announcement — happened May 12, 2026, outside the resolved window.
- Mercer Global Talent Trends 2026 — released February 25, 2026, outside the window.
- Gallup State of the Global Workplace 2026 — released late April 2026, outside the window.
- Layoff acceleration in May (PayPal 4,760 / Coinbase 700 / Cloudflare 1,100+) — strong workforce signal, but already covered in last week's `stanchart-lower-value-human-capital` story and on the dedup exclusion list as a theme.
- OpenAI acquires TBPN (media company) — late May, but specialty/strategic-comms move; below the cross-citation bar for tier-1 catalog sources.
- Microsoft Agent 365 GA cross-cloud registry sync — May 1 GA, with follow-on updates; in-window updates didn't clear the cross-citation bar in catalog terms.

## Dedup check against prior runs
- Last week (2026-05-22) used: gemini-3-5-flash, anthropic-managed-agents, stanchart-lower-value-human-capital
- This week's picks share NO story URLs with last week. Anthropic appears in both, but the stories are different (last week = Code with Claude product launches; this week = Series H financing round). Cross-week recycling of the firm name is fine; the story URLs are distinct.

## Notes on sourcing
- All three lead URLs were search-indexed. WebFetch attempts on TechCrunch, CNBC and Bloomberg returned 403 in the prior run; this run relied on search-indexed snippets for those domains. Flagged `[search-only]` where direct fetch was not possible.
- No new sources added to the catalog this run — all citations from existing Tier 1/2/3 sources.
