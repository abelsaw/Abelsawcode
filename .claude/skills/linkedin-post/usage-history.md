# /linkedin-post usage history

Every successful run of the `/linkedin-post` skill appends to this ledger.
Before drafting, the skill reads this file and **excludes themes already
used** so carousels don't overlap with prior runs.

## Dedup policy

- **Default window: 14 days.** A parent theme used in the last 14 days is excluded from candidate selection.
- **After 14 days**, a theme becomes eligible again *only if* there's a materially fresh stat or angle (e.g. a new report dropped that updates the picture). The writer must cite the new data in the brief, not recycle the old stats.
- **Same parent theme, different angle** = blocked by default. Override only on explicit user request ("I want a different angle on managers").
- **To force-recycle a theme**, manually delete its entry from this file.

When excluding, match on **parent theme**, not slug — two slugs about "Human-AI work redesign" share the same parent and both count as used.

---

## Used themes (most recent first)

### CEO ownership of AI upskilling — budget + personal time (NEW parent theme)
- Slugs: budget-shows-belief
- Source stats: BCG AI Radar 2026 — Trailblazer/Pragmatist/Follower CEOs allocate 60%/27%/24% of AI budget to upskilling and retraining; 72% of CEOs now main AI decision-maker (double last year); 8+ hrs/week of CEO personal AI upskilling time (search-only, BCG); KPMG 2026 CEO Outlook — 83% of CEOs prioritize workforce reskilling (search-only); Mercer GTT 2026 — 62% of employees say leaders underestimate AI's emotional impact (search-only); WEF Reskilling Revolution pledge — 120M workers by 2030 (search-only)
- Distinct from theme #15 (AI literacy & reskilling at scale — about workforce-level deployment vs reskilling rates) and theme #1 (AI value-capture / 12% vanguard — about realized value differential). This theme is specifically about CEO as the upskilling-budget owner and personal-time investor.
- Lead firm: BCG (Tier 1 non-Big-3)
- Commits: (pending this run-4)
- Date(s): 2026-06-02

### Performance management reinvented — process to purpose (NEW parent theme)
- Slugs: rebuild-performance-management
- Source stats: WTW Reinventing Performance Management + Pay for Performance 2026 (from 2025 Global PM Focus Group) — ~50% of orgs say productivity would rise 10%+ if PM optimized (search-only); Gartner CHRO Priorities 2026 — embedding culture in daily work delivers up to 34% performance lift; AI-evolved HR ops adds up to 29% productivity [PDF: gartner/chro-top-priorities-2026.pdf]; Mercer GTT 2026 — 63% C-suite vs 46% HR on whether redesigning work for AI is top ROI lever (search-only); Deloitte HCT 2026 — adaptability built into work (search-only)
- Distinct from theme #14 (Human-AI work redesign — about task allocation between humans and AI) and theme #22 (Organizational adaptability — about org topology / structure to flow). This theme is specifically about the PM SYSTEM itself — goal-setting, calibration, reward linkage, manager coaching — being rewired.
- Lead firm: WTW (Tier 1 non-Big-3)
- Commits: (pending this run-4)
- Date(s): 2026-06-02

### The clarity gap — workers want clarity / leaders run on speed (NEW parent theme)
- Slugs: clarity-is-the-multiplier
- Source stats: PwC Workforce Hopes & Fears 2025 (50,000 workers, 28 sectors, 48 economies; rolled forward to 2026 commentary) — workers most aligned with leadership goals are 78% more motivated; workers most trusting their direct manager are 72% more motivated (search-only, PwC press); WTW 2026 Global EX Market Study — four-part Clarity / Confidence / Capability / Connection frame; 58% → 91% AI changes EX 3yr→10yr (search-only); Deloitte HCT 2026 — only 27% say org manages change effectively, 1/3 saw 15+ major changes last year (search-only); WEF Davos 2026 — engagement depends less on perks more on trust (search-only). PwC Malaysia cut shows higher APAC optimism on AI productivity (50% vs 41%) [PDF: pwc/workforce-hopes-and-fears-2025.pdf]
- Distinct from theme #21 (Personalized EVP — about EVP architecture for rewards/benefits) and theme #23 (Purpose/belonging — about social connection). This theme is specifically about INFORMATION ASYMMETRY between leadership intent and employee comprehension — a communication/cadence/credibility failure.
- Lead firm: PwC (Tier 2 non-Big-3 — first PwC lead in rolling-9 window)
- Commits: (pending this run-4)
- Date(s): 2026-06-02

### Opportunity equity / D&I matures, not retreats (NEW parent theme)
- Slugs: opportunity-is-the-next-equity
- Source stats: Aon HCT 2026 — 84% ensure equal pay, only 14% ensure equal career progression (Ch 2, p.28) [PDF: aon/human-capital-trends-2026.pdf]; McKinsey State of Orgs 2026 Shift #7 — 90% of leaders still call D&I a priority; APAC 84% / EU 83% / NA 75% maintaining or expanding [PDF: mckinsey/state-of-organizations-2026.pdf, pp.53-56]; Deloitte HCT 2026 — belonging delivers 56% performance lift, 50% lower turnover risk (search-only)
- Distinct from theme #18 (Pay transparency execution — about EU Pay Transparency Directive mechanics) — this theme is about D&I evolution from pay equity to opportunity/career equity.
- Commits: (pending this run-3)
- Date(s): 2026-06-02

### People & Performance (P&P) organizations — high-performance edge (NEW parent theme)
- Slugs: built-to-outperform
- Source stats: McKinsey State of Orgs 2026 Shift #6 — P&P orgs 4.3x more likely to maintain top-tier financial performance 9 of 10 years [PDF: mckinsey/state-of-organizations-2026.pdf, pp.46-49]; Aon HCT 2026 — 77% of employees with regular development conversations feel motivated vs 21% without (Ch 2, pp.24-27) [PDF: aon/human-capital-trends-2026.pdf]; WTW Reinventing Performance Management 2026 — only 20% of leaders believe non-financial rewards meaningfully boost performance (search-only); Deloitte 2026 HCT — 47% cite limited career progression as top barrier (search-only)
- Distinct from theme #16 (Manager engagement & leadership pipeline — about Gallup engagement scores) and theme #17 (Wellbeing & FOBO — about thriving %). This theme is specifically about the P&P org category as a high-performance discipline (development conversations, dev cadence, non-comp rewards).
- Commits: (pending this run-3)
- Date(s): 2026-06-02

### Decision rights as productivity lever (NEW parent theme)
- Slugs: speed-runs-on-decision-rights
- Source stats: Deloitte HCT 2026 — 67% of leaders want orgs fast & nimble, only 7% report great progress (search-only / press); McKinsey State of Orgs 2026 Shift #3 — managers spend 40-65% of time on cross-functional work without accountability for outcomes; end-to-end redesign lifts engagement 25pp [PDF: mckinsey/state-of-organizations-2026.pdf, pp.35-40]; WTW & Aon corroborating
- Distinct from theme #22 (Organizational adaptability over structural redesign — used today's run-2; McKinsey Shift #5 about structure-to-flow, complexity reduction). This theme is McKinsey Shift #3 specifically about decision rights and authority distribution, not structure/complexity. The "reorgs don't fix productivity" thread is shared, but the diagnostic and lever are distinct: Shift #5 = simplify the structure; Shift #3 = define who decides what.
- Commits: (pending this run-3)
- Date(s): 2026-06-02

### Geopolitical fragmentation as workforce planning input (NEW parent theme)
- Slugs: geopolitics-is-planning-input
- Source stats: McKinsey State of Orgs 2026 — 72% of leaders say geopolitical shifts already affected operating context (Shift #4: finding value in a new geopolitical context) [PDF: mckinsey/state-of-organizations-2026.pdf, p.28]; CHRO Association 2026 — geopolitics ranks as #1 external concern [PDF: chro-association/chro-survey-key-findings-2026.pdf]; Aon HCT 2026 — 39% pursuing M&A as workforce reshape [PDF: aon/human-capital-trends-2026.pdf]; Mercer GTT 2026 — talent foresight as scenario discipline (search-only)
- Distinct from theme #4 (Scenario-based workforce planning under AI uncertainty — was about AI-future scenarios) and theme #7 (Global mobility reinvention — was about long-term vs short-term expat). This theme is specifically about geopolitical risk shaping hiring, comp, and footprint decisions.
- Commits: (pending this run-2)
- Date(s): 2026-06-02

### Purpose, belonging, social connection as retention infrastructure (NEW parent theme)
- Slugs: connection-is-infrastructure
- Source stats: Deloitte Gen Z/Mill 2026 — Gen Z with close work friend 15pp more likely to stay 5+ years (48% vs 33%); millennials 18pp (61% vs 43%); 96/97% say purpose drives satisfaction; 41% Gen Z / 39% millennials rejected employer on ethics [PDF: deloitte/gen-z-millennial-survey-2026.pdf, p.41-44]; Aon HCT 2026 — culture/leadership/belonging central to sustainable wellbeing [PDF: aon/human-capital-trends-2026.pdf]; Gartner CHRO Priorities 2026 — only 47% of CHROs say culture drives performance (culture atrophy) [PDF: gartner/chro-top-priorities-2026.pdf]
- Distinct from theme #17 (Wellbeing & FOBO — about Mercer 44% thriving / AI fear) and theme #11 (Internal mobility — about retention via mobility). This theme is about purpose + connection as the retention mechanism, not wellbeing dashboards or career mobility.
- Commits: (pending this run-2)
- Date(s): 2026-06-02

### Organizational adaptability over structural redesign (NEW parent theme)
- Slugs: flow-over-structure
- Source stats: McKinsey State of Orgs 2026 — 2 of 3 leaders say orgs overly complex; 43% rank productivity as top priority; end-to-end process redesign 3x decision speed; only 13% blame lack of capex [PDF: mckinsey/state-of-organizations-2026.pdf, p.5, p.36-37]; Aon HCT 2026 — adaptability ranked #1 critical workforce skill ahead of AI literacy [PDF: aon/human-capital-trends-2026.pdf, p.23]; Mercer GTT 2026 — work redesign for AI as #1 ROI lever (search-only); Deloitte HCT 2026 — reinvention as operating baseline (search-only)
- Distinct from theme #14 (Human-AI work redesign — about BCG 50-55% AI work design) and theme #10 (Skills-based workforce planning — about Mercer 5% advanced). This theme is about organizational process flow and end-to-end simplification, not AI augmentation or skills inventory.
- Commits: (pending this run-2)
- Date(s): 2026-06-02

### Personalized EVP as competitive moat (NEW parent theme)
- Slugs: evp-is-architecture
- Source stats: Aon HCT 2026 — only 19% of orgs have a clearly defined EVP; EVP-clear orgs lead peers by 34pp on visible leadership wellbeing commitment, 21pp on retirement gender-gap action, 20pp on benefit personalization; 84% employers say wellbeing strategy works vs 72% employees still report high stress [PDF: aon/human-capital-trends-2026.pdf, p.7, p.26]; Deloitte Gen Z/Mill 2026 — 96/97% say purpose drives satisfaction [PDF: deloitte/gen-z-millennial-survey-2026.pdf, p.41]; WTW Dynamic Total Rewards 2026 + 2026 Global EX Market Study (search-only); Mercer GTT 2026 (search-only)
- Distinct from theme #13 (Medical inflation & benefits redesign — about cost trend) and theme #18 (Pay transparency execution — about salary disclosure). This theme is about EVP as the architecture for rewards/benefits/career allocation, not the cost or comp pieces individually.
- Commits: (pending this run)
- Date(s): 2026-06-02

### Knowledge continuity & the great workforce handoff (NEW parent theme)
- Slugs: knowledge-on-a-clock
- Source stats: Deloitte Gen Z/Mill 2026 — only 54% Gen Z / 60% millennials confident team holds performance if a key expert leaves; top barriers 32% no incentive, 29% no time, ~25% confidentiality [PDF: deloitte/gen-z-millennial-survey-2026.pdf, p.48]; McKinsey State of Organizations 2026 — workforce shifts named one of three tectonic forces [PDF: mckinsey/state-of-organizations-2026.pdf, p.2]; WEF Future of Jobs aging-workforce themes (search-only)
- Distinct from all 18 prior exclusions — no parent theme has touched generational handoff / institutional-memory transfer. Closest adjacency: theme #16 manager engagement, but that one is about manager bench depth / engagement scores, not knowledge transfer.
- Commits: (pending this run)
- Date(s): 2026-06-02

### Leadership redesign + Gen Z opt-out (NEW parent theme)
- Slugs: leadership-the-job-not-the-pipeline
- Source stats: Deloitte Gen Z/Mill 2026 — only 6% rank leadership as top career goal; 50% cite stress, 41-46% cite work-life; top draws comp 53/57%, flex 42/44%, clarity 36/35% [PDF: deloitte/gen-z-millennial-survey-2026.pdf, p.14, p.15]; McKinsey State of Organizations 2026 — 30% reflective leaders see orgs as adaptive vs 17% non-reflective [PDF: mckinsey/state-of-organizations-2026.pdf, p.5]; Aon HCT 2026 — leadership & people management ranked #2 critical workforce skill [PDF: aon/human-capital-trends-2026.pdf, p.23]; Gartner CHRO Priorities 2026 — Priority 3, routinize change [PDF: gartner/chro-top-priorities-2026.pdf]
- Distinct from theme #16 (Manager engagement — about Gallup engagement scores) and theme #11 (Internal mobility — about retention via mobility). This theme is the redesign of the leadership ROLE itself + generational rejection of the legacy model.
- Commits: (pending this run)
- Date(s): 2026-06-02

### AI value-capture / 12% vanguard (PDF-recycle on theme #12)
- Slugs: the-twelve-percent-vanguard
- Source stats: PwC 29th Global CEO Survey 2026 — 12% of CEOs capture both AI revenue and cost gains; 56% see neither; vanguard apply AI across multiple business areas 44% vs 17% [PDF: pwc/29th-global-ceo-survey-2026.pdf]
- Recycle basis: fresh PDF segmentation reveals the 12% vanguard practice; earlier theme #12 post focused on the failure mode (56% see nothing). New angle focuses on what winners do differently.
- Commits: (pending this run)
- Date(s): 2026-05-22

### CHRO ambition vs. AI execution capability (NEW parent theme)
- Slugs: the-ambition-execution-gap
- Source stats: CHRO Association 2026 — 91% of CHROs rank AI as #1 priority [PDF: chro-association/chro-survey-key-findings-2026.pdf]; Deloitte HCT 2026 — 66% of leaders recognize need for human-AI interaction design, only 6% making great progress [PDF: deloitte/global-human-capital-trends-2026.pdf]
- Distinct from theme #9 (Culture as AI bottleneck — about cultural readiness) and theme #13 (AI governance — about formal committees/decision rights). This theme is specifically about the gap between CHRO-level priority and leader-level execution discipline.
- Commits: (pending this run)
- Date(s): 2026-05-22

### Climate / heat as labor productivity (PDF-recycle on theme #15)
- Slugs: climate-is-already-here
- Source stats: IFC Hidden Potential 2026 — 370 million workers (10% of global workforce) already see tasks shifting due to climate [PDF: ifc/employers-accelerate-inclusive-jobs-green-transitions-2026.pdf]; ILO heat-stress baseline — 2.4 billion workers exposed [PDF: ilo/heat-stress-labour-productivity.pdf]
- Recycle basis: earlier theme #15 post used 2030 projections (70% workforce, 3.8% hours lost). New angle uses IFC's already-shifted finding (370M workers, present tense) — materially different evidence and frame.
- Commits: (pending this run)
- Date(s): 2026-05-22

### Climate / heat as labor productivity issue
- Slugs: climate-is-an-hr-variable
- Source stats: ILO 2026 — 70% of global workforce (2.4B workers) exposed to excessive heat at work; by 2030, heat stress could cost 3.8% of global working hours; APAC and South Asia highest exposure
- Commits: (pending this run)
- Date(s): 2026-05-19
- Distinct from #10 (Job quality & informality) — that one is informal-economy quality, this is heat-stress productivity loss, different mechanism

### Scenario-based workforce planning under AI uncertainty
- Slugs: plan-for-multiple-futures
- Source stats: McKinsey 2026 — 75% of current jobs will need redesign, upskilling, or redeployment by 2030; BCG 2026 — future-built firms upskill 50%+ on AI vs 20% for laggards
- Commits: (pending this run)
- Date(s): 2026-05-19
- Distinct from #11 (Skills-based workforce planning, HR capability gap) — that one is skills inventory/tool maturity, this is scenario modeling under uncertainty, different planning discipline

### AI productivity paradox / value-capture gap
- Slugs: ai-value-is-a-measurement-problem
- Source stats: PwC 2026 — 56% of CEOs got nothing from AI investments; BCG 2026 — only 5% capture substantial financial gains
- Commits: (pending this run)
- Date(s): 2026-05-19
- Distinct from #7 (Human-AI work redesign) — this is about value capture and measurement discipline, not work-redesign mechanics

### AI governance inside HR (decision rights & oversight)
- Slugs: hr-and-the-ai-governance-room
- Source stats: SHRM 2026 — 49% have AI policies / 25% trust them / 52% don't involve HR; IBM IBV May 2026 — 76% of orgs have CAIO
- Commits: (pending this run)
- Date(s): 2026-05-19
- Distinct from #9 (Culture as AI bottleneck) — this is formal governance architecture, not cultural readiness

### Global mobility reinvention (short-term/virtual replacing long-term expat)
- Slugs: expat-package-retired
- Source stats: BCG 2026 — cross-border mobility down 8.5% YoY (220k fewer high-skill moves); KPMG 2026 — 70% leverage short-term assignments; Mercer — 18% expect long-term assignment increase, 53% expect flat
- Commits: (pending this run)
- Date(s): 2026-05-19
- Distinct from all 11 prior exclusions

### Culture as AI-transformation bottleneck
- Slugs: culture-is-the-ai-bottleneck
- Source stats: Deloitte 2026 — 85% of leaders call adaptability critical, only 7% excel; 34% report culture is inhibiting AI work
- Commits: d2aee45
- Date(s): 2026-05-19

### Job quality & informality risk
- Slugs: job-quality-stewardship
- Source stats: ILO Asia-Pacific 2026 — SEA wages -0.3%/yr; WEF Davos 2026 — 1.3B informal workers globally; Singapore MOM Q1 2026 — net hiring +5k vs +17.7k prior
- Commits: d2aee45
- Date(s): 2026-05-19

### Skills-based workforce planning (HR capability gap angle)
- Slugs: hr-skills-blind-spot
- Source stats: Mercer 2026 — under 5% of HR leaders advanced on skills-based talent tools; 60% offer training but few measure skills built
- Commits: d2aee45
- Date(s): 2026-05-19

### Internal mobility as retention lever
- Slugs: internal-mobility-is-the-asset
- Source stats: Deloitte 2026 — internal mobility doubles tenure (7.4 vs 4.1 years); McKinsey 2026 — 47% leaders name limited career progression as top culture barrier
- Commits: 1ffa92f
- Date(s): 2026-05-19

### Pay/mobility expectation gap
- Slugs: apac-pay-expectation-gap, retention-is-the-expectation-gap
- Source stats: WTW APAC 2026 — 5.2% budgets (India 9%, Singapore 4%, HK 3.5%); Robert Walters 2026 — 83% employees expect >10%, 27% employers can offer
- Commits: 9f2ad7b, f2dc9b0
- Date(s): 2026-05-19

### Medical inflation & benefits redesign
- Slugs: apac-medical-trend, medical-inflation-rewrites-benefits
- Source stats: WTW 2026 — global 10.3%, APAC 14%; Cancer drives ~70% of cost, cardiovascular ~67%
- Commits: 9f2ad7b, f2dc9b0
- Date(s): 2026-05-19

### Human-AI work redesign
- Slugs: ai-is-work-design, adoption-is-racing-design-isnt, apac-past-pilots-work-design-next
- Source stats: BCG 2026 — 50-55% of jobs reshaped within 3 years; McKinsey 2026 — 46% of SEA firms past pilots vs 35% globally; Deloitte APAC 2026 — only 6% leaders confident in human-AI interaction design
- Commits: c2400ef, 9f2ad7b, f2dc9b0
- Date(s): 2026-05-19

### AI literacy & reskilling at scale
- Slugs: ai-strategy-is-reskill-rate
- Source stats: Aon 2026 — 73% organizations deployed AI, only 18% reskilled most of their workforce
- Commits: c2400ef
- Date(s): 2026-05-19

### Manager engagement & leadership pipeline
- Slugs: managers-are-the-multiplier
- Source stats: Gallup 2026 — manager engagement 31% (2022) → 22% (2025); 8.7× transformation rate with AI-supportive manager
- Commits: c2400ef
- Date(s): 2026-05-19

### Wellbeing & FOBO
- Slugs: wellbeing-is-the-velocity-gate
- Source stats: Mercer 2026 — 44% thriving at work (vs 66% in 2024); AI job-loss fear 28% → 40%
- Commits: 1ffa92f
- Date(s): 2026-05-19

### Pay transparency execution
- Slugs: pay-transparency-is-a-strategy-test
- Source stats: EU Pay Transparency Directive lands June 2026; WTW 2026 — US salary budgets stable at 3.4%
- Commits: 1ffa92f
- Date(s): 2026-05-19
