# LinkedIn-post skill — source catalog

This is the canonical list of credible 2026 HR research sources that the
`/linkedin-post` skill draws on. The scout reads this file at the start
of every run.

When a new credible 2026 source is discovered during a run and meaningfully
contributes to a brief, the scout appends it to **Auto-discovered sources**
below with the URL, firm name, report title, and discovery date.

---

## Tier 1 — required coverage every run (8 firms)

| Firm | 2026 publications routinely searched |
|---|---|
| Mercer | Global Talent Trends 2026; Skills Snapshot |
| Aon | 2026 Human Capital Outlook; Human Capital Trends Study; US Health Care Costs 2026 |
| McKinsey | The State of Organizations 2026; McKinsey Global Institute work research |
| WEF (World Economic Forum) | Future of Jobs 2026; Reskilling Revolution updates; Davos 2026 outputs |
| BCG | AI/Work research; "AI Will Reshape More Jobs Than It Replaces"; CEO AI Upskilling |
| WTW (Willis Towers Watson) | Global Medical Trends 2026; Dynamic Total Rewards 2026; Salary Budget Planning Survey |
| Deloitte | 2026 Global Human Capital Trends |
| Gallup | State of the Global Workplace 2026 |

## Tier 2 — swept when relevant (6 firms)

| Firm | 2026 publications |
|---|---|
| PwC | Workforce Hopes & Fears 2026 |
| SHRM | 2026 CHRO Priorities and Perspectives |
| Bain | Aura labor market data |
| KPMG | 2026 CEO Outlook (people section) |
| Conference Board | CHRO Confidence Survey Q1 2026 |
| Gartner | CHRO Priorities 2026 |

## Tier 3 — Asia Pacific–focused research

Firms and institutions with primary HR research focused on or originating
in Asia Pacific. Particularly weighted when the skill runs with
`region: apac` (the default).

| Source | Type | 2026 publications typically searched |
|---|---|---|
| Hays | Recruitment / pay research | Hays Asia Salary Guide 2026; Asia Workforce Trends |
| Robert Walters | Recruitment / pay research | Salary Survey 2026 (Singapore, HK, China, Japan, Australia volumes) |
| Michael Page | Recruitment / talent research | Talent Trends 2026 APAC |
| INSEAD | Academic / business school | Global Talent Competitiveness Index 2026; INSEAD Knowledge HR pieces |
| Mercer Asia | Regional consulting practice | APAC breakouts of Global Talent Trends 2026 |
| WTW APAC | Regional consulting practice | APAC breakouts of Global Medical Trends; APAC Salary Budget Planning |
| Deloitte APAC | Regional consulting practice | APAC Human Capital Trends |
| ILO Asia–Pacific | Multilateral / labor research | World Employment and Social Outlook 2026; Asia-Pacific Employment and Social Outlook |
| ADB (Asian Development Bank) | Multilateral | Asia Productivity / Work research |
| Singapore MOM | Government / labor stats | Labour Market Report; Manpower Research |
| AHRI (Australia HR Institute) | National HR professional body | Pulse Survey; HR research papers |
| HKIHRM | National HR professional body | Industry surveys |
| People Matters (India) | Trade publication with primary research | India HR Industry surveys; State of HR Tech |
| HR Asia | Regional publication | Best Companies to Work for in Asia research |

## Regional lens directive

When the skill runs with **`region: apac` (default)**, APAC functions as a
**relevance filter on themes**, not a framing mandate:

1. **Topic filter:** only surface themes applicable to APAC employers. Drop themes that are US-only or Europe-only and don't reach APAC (e.g. US-specific NLRB rulings, US state-level labor law). Themes that touch APAC multinationals via global rules (EU Pay Transparency, etc.) pass.
2. **Source sweep:** sweep Tier 3 for primary APAC research; pull APAC regional breakouts of Tier 1/2 reports when they add value.
3. **Data weaving:** cite APAC-specific stats as evidence when they materially differ from the global picture. When the global stat is enough, use it. Don't force APAC numbers where they don't add insight.
4. **Framing:** universal best-practices voice is the default. Don't lead posts with "APAC's biggest…" or "APAC moved past…" — write general CHRO insight and use APAC data inside the body where it lands naturally.

When the skill runs with **`region: global`**, treat Tier 3 as supplementary
— use it only when APAC data adds genuine convergence to a theme.

US-centric Tier 2 sources (SHRM, Conference Board) are de-emphasized but
not excluded in `region: apac`; cite them when they speak to issues APAC
employers also face (cross-border talent flows, multinational HR
governance).

---

## Discovery rules

The scout may add NEW 2026 sources to the **Auto-discovered sources** section
below when **all** of these are true:

- The firm is recognized as credible — a major consulting firm (Korn Ferry, Heidrick & Struggles, Russell Reynolds, Spencer Stuart, Egon Zehnder, Oliver Wyman, IBM Institute for Business Value, Accenture Research, EY People Advisory, Roland Berger), an established research institution (Brookings, MIT Sloan, Wharton, NBER, Stanford), a government / multilateral body (ILO, OECD, BLS, EU-OSHA), or an established trade publication that produced primary research (HBR original surveys, MIT Sloan Management Review).
- The publication is dated **2026** (release year, not just topic).
- The finding adds new convergence to a theme — it's not just restating a Tier 1 firm's same point.

**Do NOT add:**
- Blog posts without primary data
- Single-author opinion pieces
- Press syndication of another firm's research
- Marketing collateral or product launch posts
- Vendor-sponsored "research" without disclosed methodology

When the scout adds a source here, it should also note (briefly) which theme
the source contributed to, so a human reviewing the catalog can see the
context.

---

## Auto-discovered sources

<!-- Append new entries below this line as: -->
<!-- ### {Firm} — {Report title} ({Month YYYY}) -->
<!-- - URL: {url} -->
<!-- - Contributed to theme: {short theme label} -->
<!-- - Discovered: {YYYY-MM-DD} -->

### Korn Ferry — Talent Trends 2026: Human-AI Power Couple (APAC edition)
- URL: https://www.kornferry.com/about-us/events-webinars/talent-acquisition-trends-2026-apac
- Contributed to theme: Human-AI work redesign (APAC adoption lead)
- Discovered: 2026-05-19
- Tier: Tier 3 (APAC-focused)

### IBM Institute for Business Value — CEO Study, "Reshaping C-suite Roles for the AI Era" (May 2026)
- URL: https://newsroom.ibm.com/2026-05-04-ibm-study-ceos-are-reshaping-c-suite-roles-for-the-ai-era
- Contributed to theme: AI governance in HR (76% of organizations now have a CAIO, up from 26%)
- Discovered: 2026-05-19
- Tier: Tier 2 (global, primary research with disclosed methodology)

### EY People Advisory — 2026 Mobility Reimagined Survey
- URL: https://www.ey.com/en_gl/insights/workforce/mobility-reimagined-survey
- Contributed to theme: Global mobility reinvented (short-term/virtual replacing long-term expat)
- Discovered: 2026-05-19
- Tier: Tier 2 (global, primary research)

### IFC — "Hidden Potential: Inclusive Jobs in Green Transitions" (2026)
- URL: https://www.ifc.org/content/dam/ifc/doc/2026/how-employers-can-accelerate-inclusive-jobs-in-green-transitions.pdf
- Contributed to theme: Climate/heat as labor productivity issue (supporting)
- Discovered: 2026-05-19
- Tier: Tier 3 (multilateral, climate-labor)

### ManpowerGroup — Global Talent Barometer 2026
- URL: https://www.manpowergroup.com/insights/global-talent-barometer
- Contributed to theme: Gen Z stability shift (AI-confidence + generational signal)
- Discovered: 2026-05-19
- Tier: Tier 3 (primary survey research)
