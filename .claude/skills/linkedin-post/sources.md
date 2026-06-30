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
| Conference Board | CHRO Confidence Survey Q1/Q2 2026; CEO Confidence Q2 2026 |
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
| 2026-06-21 | pay-transparency-is-a-board-question | Aon | Mercer, WTW |
| 2026-06-21 | choice-replaces-cost-share | Mercer | Aon, WTW |
| 2026-06-21 | the-lever-is-the-coach | WTW | McKinsey, Deloitte |
| 2026-06-21 | speed-is-a-design-choice | McKinsey | Deloitte, Mercer |
| 2026-06-21 | saved-time-leaks | BCG | McKinsey, Mercer |
| 2026-06-21 | the-cheapest-retention-lever | PwC | Mercer, WTW |
| 2026-06-21 | make-change-boring | Gartner | Deloitte, McKinsey |
| 2026-06-21 | the-longevity-dividend | WEF | Mercer, Aon |
| 2026-06-21 | the-thriving-gap | Gallup | Deloitte |

(The first three 2026-06-21 entries — fund-the-humans (WEF), decisions-that-echo (Deloitte), hr-is-the-steady-hand (Conference Board) — rolled off the rolling-9 window after this run-4 was added.)

### Rolling tally (last 9 posts as lead firm)

- Aon: 1 ✅ Big-3
- Mercer: 1 ✅
- WTW: 1 ✅
- McKinsey: 1 ✅ Big-3
- BCG: 1 ✅
- PwC: 1 ✅
- Gartner: 1 ✅ Tier 2 (NEW lead this run — 0-lead priority slot filled)
- WEF: 1 ✅ (NEW lead this run)
- Gallup: 1 ✅ Tier 1 (NEW lead this run — 0-lead priority slot filled)
- Deloitte: 0 ❌ Big-3 (rolled off — priority for next run)
- Conference Board: 0 ❌ (rolled off)

### Big-3 lead share in rolling 9

- Now: 2/9 (22%) — Aon 1 + McKinsey 1 (Deloitte rolled off)
- Trend across the day: 1/9 → 2/9 → 3/9 → 2/9. Self-correcting around the 22-33% band, well under control.

**Near-perfect distribution holds.** Every one of the 9 leads is a distinct firm. Gartner and Gallup (the two 0-lead firms flagged last run) were both filled this run — the rotation engine is doing exactly what it should.

### Next-run flag

- **Deloitte and Conference Board rolled off (0 leads).** Both priority fills for the next run; Deloitte is the only Big-3 at 0, so it's the natural Big-3 lead next time.
- **Big-3 at 2/9** — room for 1 more Big-3 lead next run (ideally Deloitte).
- **No firm over-rotated** — every firm at 0 or 1. Clean slate.

Sources to surface in the next run:
- **Deloitte HCT 2026** — chapters not yet led standalone (board oversight, risk reframing, productivity→performance)
- **Conference Board** — a survey cut beyond CHRO/CEO confidence (already used)
- **Gallup State of Global Workplace 2026** — intent-to-leave / choice-in-work (engagement + thriving now both used)
- **Newly discoverable credible global firms** via discovery pass

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
