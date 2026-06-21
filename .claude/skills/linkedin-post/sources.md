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

## Regional lens directive

When the skill runs with **`region: apac` (default)**, APAC functions as a
**relevance filter on themes**, not a separate tier of sources:

1. **Topic filter:** only surface themes applicable to APAC employers. Drop themes that are US-only or Europe-only and don't reach APAC (e.g. US-specific NLRB rulings, US state-level labor law). Themes that touch APAC multinationals via global rules (EU Pay Transparency, etc.) pass.
2. **APAC regional breakouts of Tier 1/2 reports:** Mercer Asia, McKinsey Asia, BCG Southeast Asia, Deloitte APAC, WTW APAC, KPMG APAC. These are regional cuts of catalog firms — not a separate tier.
3. **Data weaving:** cite APAC-specific stats as evidence when they materially differ from the global picture. When the global stat is enough, use it. Don't force APAC numbers where they don't add insight.
4. **Framing:** universal best-practices voice is the default. Don't lead posts with "APAC's biggest…" or "APAC moved past…" — write general CHRO insight and use APAC data inside the body where it lands naturally.

When the skill runs with **`region: global`**, drop the regional filter
entirely and surface globally-applicable findings.

US-centric Tier 2 sources (SHRM, Conference Board) are de-emphasized but
not excluded in `region: apac`; cite them when they speak to issues APAC
employers also face (cross-border talent flows, multinational HR
governance).

**APAC-specific research firms outside the Tier 1/2 catalog (Hays, Robert Walters, Michael Page, INSEAD, ILO Asia-Pacific, ADB, Singapore MOM, AHRI, HKIHRM, People Matters, HR Asia, IFC, ManpowerGroup, Korn Ferry APAC) are out of scope as of 2026-05-22.** The user explicitly excluded a separate Tier 3 from the catalog. If a finding from one of those firms is necessary, the scout should flag it for the user rather than cite it directly.

---

## Discovery rules

The scout may add NEW 2026 sources to the **Auto-discovered sources** section
below when **all** of these are true:

- The firm is a credible **global** consulting / research firm (Heidrick & Struggles, Russell Reynolds, Spencer Stuart, Egon Zehnder, Oliver Wyman, IBM Institute for Business Value, Accenture Research, EY People Advisory, Roland Berger), an established research institution (Brookings, MIT Sloan, Wharton, NBER, Stanford), or an established global trade publication with primary research (HBR original surveys, MIT Sloan Management Review).
- The publication is dated **2026** (release year, not just topic).
- The finding adds new convergence to a theme — it's not just restating a Tier 1 firm's same point.
- The source is **NOT** an APAC-only / regional / country-specific research firm. (Tier 3 is out of scope as of 2026-05-22.)

**Do NOT add:**
- APAC-only / country-specific research firms (the user excluded Tier 3)
- Blog posts without primary data
- Single-author opinion pieces
- Press syndication of another firm's research
- Marketing collateral or product launch posts
- Vendor-sponsored "research" without disclosed methodology

When the scout adds a source here, note (briefly) which theme the source
contributed to, so a human reviewing the catalog can see the context.

---

## Lead-firm utilization (last 9 posts)

The scout reads this table at the start of every run and applies the
**lead-firm rotation + 9-post coverage minimum** (see SKILL.md Step 2).
After each draft, the skill appends new rows here and prunes to the
most recent 9 (older rows roll off).

| Date | Slug | Lead firm | Supporting firms |
|---|---|---|---|
| 2026-06-14 | productivity-hides-in-redesign | Mercer | Deloitte, BCG, McKinsey |
| 2026-06-14 | embedded-or-absorbed | Gartner | Mercer, CHRO Association, Deloitte |
| 2026-06-14 | manager-wellbeing-is-infrastructure | Gallup | Mercer, Deloitte, McKinsey |
| 2026-06-21 | fund-the-humans | WEF | PwC, Mercer, BCG |
| 2026-06-21 | decisions-that-echo | Deloitte | BCG, Mercer, Aon |
| 2026-06-21 | hr-is-the-steady-hand | Conference Board | SHRM, Aon, Mercer |
| 2026-06-21 | pay-transparency-is-a-board-question | Aon | Mercer, WTW |
| 2026-06-21 | choice-replaces-cost-share | Mercer | Aon, WTW |
| 2026-06-21 | the-lever-is-the-coach | WTW | McKinsey, Deloitte |

(Earlier 2026-06-02 entries — clarity-is-the-multiplier, rebuild-performance-management, budget-shows-belief — rolled off the rolling-9 window after this run-2 was added.)

### Rolling tally (last 9 posts as lead firm)

- Mercer: 2 ✅ (rotated again as Theme 2 lead this run)
- WTW: 1 ✅ (rotated again)
- Aon: 1 ✅ Big-3 (NEW lead this run — rotated-back priority slot)
- Deloitte: 1 ✅ Big-3 (from this morning)
- WEF: 1 ✅ (from this morning)
- Conference Board: 1 ✅ (from this morning)
- Gartner: 1 ✅
- Gallup: 1 ✅
- McKinsey: 0 ❌ Big-3 (still rolled off — priority for next run)
- BCG: 0 ❌ (rolled off when budget-shows-belief left the window)
- PwC: 0 ❌ (rolled off when clarity-is-the-multiplier left the window)

### Big-3 lead share in rolling 9

- Now: 2/9 (22%) — Aon 1 + Deloitte 1
- Was last window: 1/9 (11%)
- Trend: still well below the 1/3 cap; healthy

### Next-run flag

- **McKinsey priority — still at 0 leads.** Should lead next run if a credible theme exists from State of Organizations 2026 Shifts not yet led (Speed/Resilience, Embracing Imperfection, productivity→performance) or other McKinsey 2026 work.
- **BCG and PwC also rolled off (0 leads now).** Strong secondary priority — BCG AI Radar / Henderson Institute, PwC Workforce Hopes & Fears 2025/26.
- **Mercer now at 2 leads.** Avoid Mercer leading a third post in the next 1-2 runs to let other firms catch up.
- **Aon led today; avoid Aon leading again immediately.** Big-3 rotation should swing to McKinsey next.

Sources to surface in the next run:
- **McKinsey State of Organizations 2026** — Shifts #1 (Speed/Resilience), #8 (Embracing imperfection), #3 (productivity→performance — not the same as the PM-rebuild we just covered)
- **BCG AI Radar 2026 / Henderson Institute 2026** — beyond AI upskilling budget (used) and reshape stats (used)
- **PwC Workforce Hopes & Fears 2026** — PDF on disk, only led once
- **Gallup State of Global Workplace 2026** — beyond manager engagement (used)
- **WEF Future of Jobs 2026** — beyond Reskilling Revolution scale (used)

---

## Auto-discovered sources

<!-- Append new entries below this line as: -->
<!-- ### {Firm} — {Report title} ({Month YYYY}) -->
<!-- - URL: {url} -->
<!-- - Contributed to theme: {short theme label} -->
<!-- - Discovered: {YYYY-MM-DD} -->

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

### CHRO Association — 2026 CHRO Survey Key Findings
- URL: (PDF attached by user 2026-05-22; published in partnership with University of South Carolina Darla Moore School of Business)
- Contributed to theme: CHRO agenda convergence (AI and workplace digitization as #1 priority for 91% of CHROs; geopolitical/inflation/regulatory as top external concerns)
- Discovered: 2026-05-22
- Tier: Tier 2 (national CHRO research body; ~150 CHROs surveyed)

---

### Removed from catalog 2026-05-22 (Tier 3 exclusion)

The following auto-discovered sources were Tier 3 (APAC-focused / regional /
multilateral). The user excluded Tier 3 from the catalog on 2026-05-22, so
these entries are archived here for reference only. They are **not** active
sources going forward. To re-activate one, move it back into the auto-discovered
list above and update its tier.

- **Korn Ferry — Talent Trends 2026: APAC edition** (was Tier 3) — https://www.kornferry.com/about-us/events-webinars/talent-acquisition-trends-2026-apac
- **IFC — Hidden Potential: Inclusive Jobs in Green Transitions (2026)** (was Tier 3) — https://www.ifc.org/content/dam/ifc/doc/2026/how-employers-can-accelerate-inclusive-jobs-in-green-transitions.pdf
- **ManpowerGroup — Global Talent Barometer 2026** (was Tier 3) — https://www.manpowergroup.com/insights/global-talent-barometer

The Tier 3 firms that were in the original catalog (Hays, Robert Walters, Michael Page, INSEAD, ILO Asia-Pacific, ADB, Singapore MOM, AHRI, HKIHRM, People Matters, HR Asia, and regional sub-practices Mercer Asia / WTW APAC / Deloitte APAC) are also out of scope as direct citation sources. The regional sub-practices remain accessible as APAC breakouts within their Tier 1 parent firms.
