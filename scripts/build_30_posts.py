#!/usr/bin/env python3
"""Generate the 30-post LinkedIn batch for 2026-05-22.

Each post is defined as a tuple: (slug, theme_label, accent, sources,
post_body, slide_specs). Post bodies are validated for ≤50 words.
Carousel slides and single-image covers are generated via the existing
scripts/generate_post_image.py.

Outputs:
- posts/drafts/best-practices-2026-05-22-batch-30.md (drafts file)
- posts/drafts/carousels/2026-05-22-option-N/slide-M.png (5 slides × 30)
- posts/drafts/images/2026-05-22-option-N.png (30 covers)
"""
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/user/Abelsawcode")
DATE = "2026-05-22"
GEN = REPO / "scripts" / "generate_post_image.py"

# (slug, theme_label, accent, sources, slide_specs[(tag, headline) x5], post_body)
POSTS = [
    # ============================================================
    # Block 1: AI / Future of Work (Options 1-8)
    # ============================================================
    (
        "sea-agentic-ai-deployment",
        "Agentic AI deployment in Southeast Asia",
        "navy",
        "McKinsey AI in Southeast Asia 2026 [PDF]",
        [
            ("Future of work", "Agentic AI moved from concept to deployment in 2026."),
            ("McKinsey 2026", "Nearly 90% of Southeast Asia firms now use AI agents in IT functions."),
            ("McKinsey 2026", "Customer-facing adoption still lags. Trust and accuracy are the bottlenecks."),
            ("The CHRO read", "Agentic capacity is the new capability gap."),
            ("Your move", "Where are AI agents replacing process — and where are they replacing trust?"),
        ],
        "Agentic AI moved from concept to deployment in 2026.\n\nMcKinsey 2026 (Southeast Asia): nearly 90% of SEA firms now use AI agents in IT functions. Customer-facing adoption lags — trust and accuracy are the bottlenecks.\n\nAgentic capacity is the new capability gap.\n\n#AIatWork #FutureOfWork #APAC",
    ),
    (
        "the-eighteen-percent-reskill-rate",
        "AI reskilling gap (18% reskill rate)",
        "rust",
        "Aon 2026 Human Capital Trends [PDF]",
        [
            ("Reskilling", "AI deployment is racing. Reskilling isn't."),
            ("Aon 2026", "44% of organizations have deployed AI. Another 29% are piloting."),
            ("Aon 2026", "Only 18% report that most of their workforce has participated in AI reskilling."),
            ("The CHRO read", "Deployment without reskilling is theatre at scale."),
            ("Your move", "What is your real reskill rate this quarter?"),
        ],
        "AI deployment is racing. Reskilling isn't.\n\nAon 2026 (Human Capital Trends Study): 44% of organizations have deployed AI; another 29% are piloting. Only 18% report most of their workforce has participated in AI reskilling.\n\nDeployment without reskilling is theatre at scale.\n\n#Reskilling #AIatWork #HumanResources",
    ),
    (
        "people-analytics-undervalued",
        "People analytics underused vs. its own potential",
        "moss",
        "WTW 2026 Global Medical Trends [PDF]; Mercer Global Talent Trends 2026 [PDF]",
        [
            ("People analytics", "Most HR functions sit on data they don't use."),
            ("Mercer 2026", "55% of executives say their organization underutilizes the workforce intelligence it already has."),
            ("Mercer 2026", "Only 27% of executives believe HR effectively analyzes data for talent decisions."),
            ("The CHRO read", "The data was never the problem. The discipline was."),
            ("Your move", "What workforce question is your data already answering?"),
        ],
        "Most HR functions sit on data they don't use.\n\nMercer 2026: 55% of executives say their organization underutilizes the workforce intelligence it already has. Only 27% believe HR effectively analyzes data for talent decisions.\n\nThe data isn't the problem. Discipline is.\n\n#PeopleAnalytics #HumanResources #PeopleStrategy",
    ),
    (
        "fifty-two-percent-no-hr-in-ai",
        "HR exclusion from enterprise AI strategy",
        "plum",
        "CHRO Association 2026 [PDF]; Deloitte HCT 2026 [PDF]; Mercer GTT 2026 [PDF]",
        [
            ("Governance", "The function that owns people is often the function left out of AI."),
            ("Mercer 2026", "52% of companies don't involve HR in their overall AI strategy."),
            ("CHRO Association 2026", "Yet 91% of CHROs rank AI as their #1 priority."),
            ("The CHRO read", "An AI strategy without HR is a deployment plan, not a people plan."),
            ("Your move", "Is HR at the table when your AI roadmap is set?"),
        ],
        "The function that owns people is often the one left out of AI.\n\nMercer 2026: 52% of companies don't involve HR in their AI strategy. CHRO Association 2026: 91% of CHROs rank AI as their #1 priority.\n\nAI without HR is a deployment, not a people plan.\n\n#AIatWork #HumanResources #Leadership",
    ),
    (
        "data-that-predicts-attrition-causes-it",
        "Workforce data trust gap (AI + analytics)",
        "slate",
        "Deloitte 2026 Global Human Capital Trends [PDF]; Deloitte Beyond Productivity [PDF]",
        [
            ("People analytics", "The data you collect to predict attrition can become the reason for it."),
            ("Deloitte 2026", "60% of workers say turnover rose after their employer fused worker data into AI."),
            ("Deloitte 2026", "Only 28% of workers strongly agree their leadership uses data responsibly."),
            ("The CHRO read", "Worker data needs a trust strategy, not just a privacy policy."),
            ("Your move", "Have you asked employees what data is fair to use?"),
        ],
        "The data you collect to predict attrition can become the reason for it.\n\nDeloitte 2026: 60% of workers say turnover rose after their employer fused worker data into AI. Only 28% strongly agree leadership uses data responsibly.\n\nWorker data needs a trust strategy.\n\n#PeopleAnalytics #DataPrivacy #HumanResources",
    ),
    (
        "knowledge-work-needs-orchestration",
        "Work orchestration — moving beyond jobs to mission",
        "navy",
        "Deloitte 2026 Global Human Capital Trends [PDF]",
        [
            ("Future of work", "Knowledge work is moving from jobs to missions."),
            ("Deloitte 2026", "88% of leaders say orchestrating people, skills, and resources is critical."),
            ("Deloitte 2026", "Only 7% say they are making great progress on it."),
            ("The CHRO read", "Job architecture is a constraint when work is fluid."),
            ("Your move", "How fluidly does work move across your organization today?"),
        ],
        "Knowledge work is moving from jobs to missions.\n\nDeloitte 2026: 88% of leaders say orchestrating people, skills, and resources is critical. Only 7% say they are making great progress.\n\nJob architecture is a constraint when the work is fluid.\n\n#FutureOfWork #PeopleStrategy #HumanResources",
    ),
    (
        "ai-roi-is-a-workflow-problem",
        "AI workflow redesign as the value lever",
        "rust",
        "Deloitte 2026 Global Human Capital Trends [PDF]; BCG 2026; McKinsey 2026",
        [
            ("Future of work", "AI ROI isn't about the model. It's about the workflow around it."),
            ("Deloitte 2026", "One European telco: 90% of AI budget on redesign = 30% productivity gain."),
            ("Deloitte 2026", "5% on tools alone = 5% gain. The leverage is in the redesign."),
            ("The CHRO read", "The work changes before the tool does."),
            ("Your move", "What workflow did you redesign before your last AI rollout?"),
        ],
        "AI ROI isn't about the model. It's about the workflow around it.\n\nDeloitte 2026 (European telco case): 90% of AI budget on redesign produced a 30% productivity gain. 5% on tools alone produced 5%.\n\nThe work changes before the tool does.\n\n#FutureOfWork #AIatWork #PeopleStrategy",
    ),
    (
        "ai-emotional-impact-blind-spot",
        "Leaders underestimate AI's emotional impact on workforce",
        "moss",
        "Mercer Global Talent Trends 2026 [PDF]",
        [
            ("Wellbeing", "Leaders are tracking AI's productivity gains. Not its emotional gains and losses."),
            ("Mercer 2026", "62% of employees believe leaders underestimate AI's emotional impact."),
            ("Mercer 2026", "Only 19% of HR leaders factor it into digital strategy."),
            ("The CHRO read", "If employees feel unseen, AI deployment slows itself down."),
            ("Your move", "How do you measure how your workforce feels about AI?"),
        ],
        "Leaders track AI's productivity gains. Not its emotional gains and losses.\n\nMercer 2026: 62% of employees believe leaders underestimate AI's emotional impact. Only 19% of HR leaders factor it into digital strategy.\n\nIf employees feel unseen, AI deployment slows itself down.\n\n#Wellbeing #AIatWork #PeopleStrategy",
    ),

    # ============================================================
    # Block 2: Talent, Comp, Benefits (Options 9-16)
    # ============================================================
    (
        "the-eighty-three-twenty-seven-gap",
        "Pay expectation gap (APAC focus)",
        "plum",
        "Robert Walters 2026 [search-only]; WTW 2026 [PDF + search-only]",
        [
            ("Compensation", "The 2026 retention squeeze is the expectation gap."),
            ("Robert Walters 2026", "83% of employees expect pay rises above 10%."),
            ("Robert Walters 2026", "Only 27% of employers can offer it."),
            ("The CHRO read", "Retention now turns on what you fund beyond cash."),
            ("Your move", "What's in your non-cash retention stack?"),
        ],
        "The 2026 retention squeeze is the expectation gap.\n\nRobert Walters 2026: 83% of employees expect pay rises above 10%. Only 27% of employers can offer it. WTW: salary budgets stay in single digits across most markets.\n\nRetention turns on what you fund beyond cash.\n\n#Compensation #Retention #PeopleStrategy",
    ),
    (
        "single-digit-pay-decade",
        "Stable salary budgets are the structural reality",
        "slate",
        "WTW 2026 Salary Budget Planning [search-only]; Aon Human Capital Trends 2026 [PDF]",
        [
            ("Compensation", "Salary budgets are entering a third year of single-digit normal."),
            ("WTW 2026", "Global salary budgets stable in single digits across most markets."),
            ("Aon 2026", "Yet 86% of employers agree AI will require new skills and new pay structures."),
            ("The CHRO read", "If budgets won't grow, pay design has to."),
            ("Your move", "Where are you investing in pay design, not just pay levels?"),
        ],
        "Salary budgets are entering a third year of single-digit normal.\n\nWTW 2026: global salary budgets stable in single digits. Aon 2026: 86% of employers agree AI will require new skills and new pay structures.\n\nIf budgets won't grow, pay design has to.\n\n#Compensation #PayStrategy #PeopleStrategy",
    ),
    (
        "internal-mobility-doubles-tenure",
        "Internal mobility as retention infrastructure",
        "navy",
        "Deloitte 2026 Global Human Capital Trends [PDF]; McKinsey State of Organizations 2026 [PDF]",
        [
            ("Talent strategy", "The retention lever sits inside your own walls."),
            ("Deloitte 2026", "Internal mobility nearly doubles tenure: 7.4 vs 4.1 years."),
            ("McKinsey 2026", "47% of leaders name limited career progression as the top culture barrier."),
            ("The CHRO read", "External hiring is contracting. The career inside is the asset."),
            ("Your move", "How fluid is the career inside your walls?"),
        ],
        "The retention lever sits inside your own walls.\n\nDeloitte 2026: internal mobility nearly doubles tenure (7.4 vs 4.1 years). McKinsey 2026: 47% of leaders name limited career progression as the top barrier to high-performance culture.\n\nThe career inside is now the asset.\n\n#Retention #InternalMobility #SkillsFirst",
    ),
    (
        "skills-mapping-still-the-minority",
        "Skills-based workforce planning maturity",
        "rust",
        "Mercer 2025/2026 Skills Snapshot [PDF]",
        [
            ("Talent strategy", "Skills-based talent management is no longer rare. Mature is."),
            ("Mercer 2026", "55% of organizations now map skills to jobs — nearly double the 28% in 2022."),
            ("Mercer 2026", "But 53% still don't manage skill proficiencies at all."),
            ("The CHRO read", "Mapping is the easy half. Managing is the hard half."),
            ("Your move", "Are skills a label in your system, or a layer?"),
        ],
        "Skills-based talent management is no longer rare. Mature is.\n\nMercer 2026: 55% of organizations now map skills to jobs — nearly double the 28% in 2022. But 53% still don't manage skill proficiencies at all.\n\nMapping is the easy half. Managing is the hard half.\n\n#SkillsFirst #TalentStrategy #HumanResources",
    ),
    (
        "apac-medical-fourteen",
        "APAC medical trend hits 14% — highest globally",
        "moss",
        "WTW 2026 Global Medical Trends [PDF]; Aon Global Medical Trend Rates 2026 [PDF]",
        [
            ("Benefits", "Medical inflation is rewriting benefits strategy."),
            ("WTW 2026", "Global medical trend: 10.3%. APAC: 14% — highest of any region."),
            ("WTW 2026", "55% of insurers expect elevated cost levels to persist beyond three years."),
            ("The CHRO read", "Benefits redesign isn't a CFO project. It's a retention strategy."),
            ("Your move", "When did you last test benefits against employee needs?"),
        ],
        "Medical inflation is rewriting benefits strategy.\n\nWTW 2026: global medical trend at 10.3%, with APAC leading at 14% — highest of any region. 55% of insurers expect elevated cost levels to persist beyond three years.\n\nBenefits redesign isn't a CFO project.\n\n#Benefits #Wellbeing #PeopleStrategy",
    ),
    (
        "glp-one-rewrites-benefits",
        "GLP-1 drugs are rewriting benefits architecture",
        "plum",
        "WTW 2026 Global Medical Trends [PDF]; CHRO Association 2026 [PDF]",
        [
            ("Benefits", "GLP-1 drugs are quietly rewriting the benefits architecture."),
            ("WTW 2026", "68% of insurers expect GLP-1 usage to increase — 78% in the Americas."),
            ("WTW 2026", "Yet 64% of insurers still exclude GLP-1 obesity coverage from standard plans."),
            ("The CHRO read", "The coverage decision is no longer 'if' — it's 'who pays, how, and when.'"),
            ("Your move", "What's your GLP-1 policy this open enrollment?"),
        ],
        "GLP-1 drugs are quietly rewriting the benefits architecture.\n\nWTW 2026: 68% of insurers expect usage to increase (78% in the Americas). 64% still exclude obesity GLP-1 coverage. CHRO Association 2026: 46% of CHROs plan to add coverage.\n\nThe decision isn't if — it's how.\n\n#Benefits #Wellbeing #PeopleStrategy",
    ),
    (
        "cancer-is-the-new-cost-driver",
        "Cancer as the fastest-growing claim category",
        "slate",
        "WTW 2026 Global Medical Trends [PDF]",
        [
            ("Benefits", "Cancer is now the fastest-growing claim category — and rising in younger workers."),
            ("WTW 2026", "57% of insurers cite cancer as the fastest-growing diagnosis globally."),
            ("WTW 2026", "Three in four insurers have seen rising cancer incidence in workers under 40."),
            ("The CHRO read", "Benefits design has to follow demographics, not stand alone from them."),
            ("Your move", "Does your benefits design reflect a younger cancer-risk profile?"),
        ],
        "Cancer is the fastest-growing claim category — and rising fastest in younger workers.\n\nWTW 2026: 57% of insurers cite cancer as the fastest-growing diagnosis globally. Three in four have seen rising incidence in workers under 40.\n\nBenefits design has to follow demographics.\n\n#Benefits #Wellbeing #PeopleStrategy",
    ),
    (
        "hdhps-are-now-standard",
        "HDHPs as the new default benefits architecture",
        "navy",
        "CHRO Association 2026 [PDF]",
        [
            ("Benefits", "High-deductible plans are no longer the alternative. They're the default."),
            ("CHRO Association 2026", "86% of US CHROs offer high-deductible health plans with HSAs."),
            ("CHRO Association 2026", "62% increased employee cost-sharing this year."),
            ("The CHRO read", "Cost-shifting solves the budget. It doesn't solve retention."),
            ("Your move", "Does your benefits architecture still feel like a recruit-and-retain tool?"),
        ],
        "High-deductible plans are no longer the alternative. They are the default.\n\nCHRO Association 2026: 86% of US CHROs offer high-deductible health plans with HSAs. 62% increased employee cost-sharing this year.\n\nCost-shifting solves the budget. It doesn't solve retention.\n\n#Benefits #PeopleStrategy #HumanResources",
    ),

    # ============================================================
    # Block 3: Workforce / Generations (Options 17-22)
    # ============================================================
    (
        "gen-z-delays-the-american-dream",
        "Gen Z + millennials delaying major life decisions",
        "rust",
        "Deloitte 2026 Gen Z and Millennial Survey [PDF]",
        [
            ("Talent strategy", "Gen Z and millennials are delaying their own lives."),
            ("Deloitte 2026", "55% of Gen Zs and 52% of millennials are delaying major life decisions due to financial pressure."),
            ("Deloitte 2026", "47% of both generations are living paycheck to paycheck."),
            ("The CHRO read", "Stability is the new aspiration. Build EVP for it."),
            ("Your move", "Does your EVP speak to stability, or to ambition?"),
        ],
        "Gen Z and millennials are delaying their own lives.\n\nDeloitte 2026 (22,500 respondents, 44 countries): 55% of Gen Zs and 52% of millennials are delaying major life decisions due to financial pressure. 47% are living paycheck to paycheck.\n\nStability is the new aspiration.\n\n#GenZ #TalentStrategy #PeopleStrategy",
    ),
    (
        "burnout-blocks-the-leadership-pipeline",
        "Stress as Gen Z's barrier to leadership",
        "moss",
        "Deloitte 2026 Gen Z and Millennial Survey [PDF]",
        [
            ("Leadership pipeline", "Gen Z still wants to lead. They're not sure they can survive it."),
            ("Deloitte 2026", "50% of Gen Zs cite stress and burnout as the top barrier to taking on leadership."),
            ("Deloitte 2026", "76% are still interested in pursuing executive leadership eventually."),
            ("The CHRO read", "If we don't redesign leadership work, we lose the next leaders."),
            ("Your move", "What does leadership cost in your organization — and is it sustainable?"),
        ],
        "Gen Z still wants to lead. They're not sure they can survive it.\n\nDeloitte 2026: 50% of Gen Zs cite stress and burnout as the top barrier to leadership. 76% are still interested in executive leadership eventually.\n\nRedesign leadership work, or lose the next leaders.\n\n#Leadership #FutureOfWork #PeopleStrategy",
    ),
    (
        "managers-are-the-multiplier",
        "Managers as the AI ROI multiplier",
        "plum",
        "Gallup State of the Global Workplace 2026 [search-only]; Mercer GTT 2026 [PDF]",
        [
            ("Leadership", "Your managers are the bottleneck and the multiplier."),
            ("Gallup 2026", "Employees whose manager backs AI use are 8.7× more likely to say work has transformed."),
            ("Mercer 2026", "Yet only 8% of C-suite see HR as embedded in strategic decisions on managers."),
            ("The CHRO read", "Manager development isn't a soft investment. It's where AI ROI shows up."),
            ("Your move", "What did you put behind your manager layer this quarter?"),
        ],
        "Your managers are the bottleneck and the multiplier.\n\nGallup 2026: employees whose manager backs AI use are 8.7× more likely to say work has transformed. Mercer 2026: only 8% of C-suite see HR as embedded in strategic decisions.\n\nManager development is where AI ROI shows up.\n\n#Leadership #ManagerDevelopment #PeopleStrategy",
    ),
    (
        "forty-four-percent-thriving",
        "Workforce wellbeing collapse",
        "slate",
        "Mercer Global Talent Trends 2026 [PDF]",
        [
            ("Wellbeing", "Employee thriving has collapsed."),
            ("Mercer 2026", "44% of employees report thriving at work — down sharply from 66% in 2024."),
            ("Mercer 2026", "AI job-loss concern climbed from 28% to 40% in two years."),
            ("The CHRO read", "Depleted workforces don't ship the productivity AI promises."),
            ("Your move", "Where is wellbeing measured in your operating model?"),
        ],
        "Employee thriving has collapsed.\n\nMercer 2026: 44% of employees report thriving at work — down sharply from 66% in 2024 (worse than pandemic levels). AI job-loss concern climbed from 28% to 40% in two years.\n\nDepleted workforces don't ship the productivity AI promises.\n\n#Wellbeing #FutureOfWork #PeopleStrategy",
    ),
    (
        "gen-z-now-uses-ai-daily",
        "Gen Z + millennial AI adoption acceleration",
        "navy",
        "Deloitte 2026 Gen Z and Millennial Survey [PDF]",
        [
            ("AI at work", "The Gen Z AI adoption curve is now vertical."),
            ("Deloitte 2026", "74% of Gen Zs and millennials use AI in their day-to-day work."),
            ("Deloitte 2026", "Up sharply from 57% (Gen Zs) and 56% (millennials) in 2025."),
            ("The CHRO read", "Adoption is no longer the question. Governance and capability are."),
            ("Your move", "Is your AI policy keeping pace with how employees already use AI?"),
        ],
        "The Gen Z AI adoption curve is now vertical.\n\nDeloitte 2026 (22,500 respondents): 74% of Gen Zs and millennials use AI in day-to-day work, up sharply from ~57% in 2025.\n\nAdoption is no longer the question. Governance and capability are.\n\n#GenZ #AIatWork #FutureOfWork",
    ),
    (
        "mid-manager-ai-fear",
        "Mid-level manager AI threat perception",
        "rust",
        "CHRO Association 2026 [PDF]; Mercer GTT 2026 [PDF]",
        [
            ("Leadership", "The AI fear that matters most sits in the middle of your org chart."),
            ("CHRO Association 2026", "17% of CHROs report mid-level managers see AI as threatening their roles."),
            ("Mercer 2026", "62% of employees believe leaders underestimate AI's emotional impact."),
            ("The CHRO read", "If middle managers stall, AI value stalls."),
            ("Your move", "What does your AI rollout look like from the middle layer?"),
        ],
        "The AI fear that matters most sits in the middle of your org chart.\n\nCHRO Association 2026: 17% of CHROs report mid-level managers see AI as a threat. Mercer 2026: 62% of employees say leaders underestimate AI's emotional impact.\n\nIf middle managers stall, AI value stalls.\n\n#Leadership #AIatWork #PeopleStrategy",
    ),

    # ============================================================
    # Block 4: Labor Market / Geopolitics / Climate (Options 23-30)
    # ============================================================
    (
        "informal-employment-is-asia",
        "Informal employment dominates Asia-Pacific",
        "moss",
        "ILO Employment and Social Trends 2026 [PDF]",
        [
            ("Workforce", "Two-thirds of Asia-Pacific employment lives outside the formal sector."),
            ("ILO 2026", "65.4% of employment in Asia-Pacific is informal — around 330 million workers."),
            ("ILO 2026", "2.1 billion workers globally are in informal employment."),
            ("The CHRO read", "Workforce strategy has to widen beyond headcount."),
            ("Your move", "Where does informal and contingent work sit in your plan?"),
        ],
        "Two-thirds of Asia-Pacific employment lives outside the formal sector.\n\nILO 2026: 65.4% of Asia-Pacific employment is informal — around 330 million workers. Globally, 2.1 billion workers are in informal employment.\n\nWorkforce strategy has to widen beyond headcount.\n\n#Workforce #FutureOfWork #APAC",
    ),
    (
        "trade-costs-shrink-asian-wages",
        "Trade-cost shock and APAC wage decline",
        "plum",
        "ILO Employment and Social Trends 2026 [PDF]",
        [
            ("Workforce", "Trade tensions are quietly compressing Asian wages."),
            ("ILO 2026", "SEA wages projected to decline 0.3% per year on rising trade costs."),
            ("ILO 2026", "Southern Asia projected to decline 0.45% per year over 5 years."),
            ("The CHRO read", "Comp benchmarks have to absorb a geopolitical risk premium."),
            ("Your move", "Have you stress-tested your APAC comp plan against trade scenarios?"),
        ],
        "Trade tensions are quietly compressing Asian wages.\n\nILO 2026: SEA wages are projected to decline 0.3% per year on rising trade costs; Southern Asia 0.45% per year over five years.\n\nComp benchmarks have to absorb a geopolitical risk premium.\n\n#Compensation #APAC #PeopleStrategy",
    ),
    (
        "africa-will-have-the-workers",
        "Demographic dividend in Africa, talent shrinkage elsewhere",
        "slate",
        "ILO Employment and Social Trends 2026 [PDF]",
        [
            ("Talent strategy", "The labor force of 2030 lives in different markets."),
            ("ILO 2026", "Africa's labor force projected to grow from 230 million (1995) to 610 million (2030)."),
            ("ILO 2026", "High-income country labor forces flat or shrinking."),
            ("The CHRO read", "Global talent strategy now has to be locally specific."),
            ("Your move", "Where does your talent plan reach the labor force of 2030?"),
        ],
        "The labor force of 2030 lives in different markets.\n\nILO 2026: Africa's labor force will grow from 230 million (1995) to 610 million (2030). High-income country labor forces are flat or shrinking.\n\nGlobal talent strategy now has to be locally specific.\n\n#TalentStrategy #FutureOfWork #PeopleStrategy",
    ),
    (
        "climate-shifts-export-economies",
        "Climate risk in APAC export economies",
        "navy",
        "IFC Hidden Potential 2026 [PDF]; ILO Heat Stress [PDF]",
        [
            ("Climate risk", "Climate is now a payroll line in Asia's export economies."),
            ("IFC 2026", "Pakistan and Bangladesh could lose $65.8B in export earnings by 2030 without climate adaptation."),
            ("ILO", "2.4 billion workers are exposed to excessive heat at work."),
            ("The CHRO read", "Climate adaptation is workforce strategy, not just ESG."),
            ("Your move", "Where does climate sit in your APAC workforce plan?"),
        ],
        "Climate is a payroll line in Asia's export economies.\n\nIFC 2026: Pakistan and Bangladesh could lose $65.8 billion in export earnings by 2030 without climate adaptation. ILO: 2.4 billion workers are exposed to excessive heat at work.\n\nClimate adaptation is workforce strategy, not just ESG.\n\n#ClimateRisk #APAC #PeopleStrategy",
    ),
    (
        "heat-will-cost-india-thirty-four-million-jobs",
        "India heat-stress productivity loss",
        "rust",
        "ILO Working on a Warmer Planet [PDF]",
        [
            ("Climate risk", "India's heat exposure is a workforce planning issue, not a climate one."),
            ("ILO", "India alone could lose the equivalent of 34 million full-time jobs to heat stress by 2030."),
            ("ILO", "Southern Asia is projected to lose 5.3% of working hours — highest globally."),
            ("The CHRO read", "Shift patterns, cooling, and heat policy belong in HR's strategy deck."),
            ("Your move", "Is heat a workforce risk in your operations today?"),
        ],
        "India's heat exposure is a workforce planning issue, not a climate one.\n\nILO: India could lose the equivalent of 34 million full-time jobs to heat stress by 2030. Southern Asia projected to lose 5.3% of working hours — highest globally.\n\nHeat policy belongs in HR's strategy deck.\n\n#ClimateRisk #FutureOfWork #PeopleStrategy",
    ),
    (
        "geopolitics-is-the-new-hr-risk",
        "Geopolitical instability as a CHRO concern",
        "moss",
        "CHRO Association 2026 [PDF]; PwC 29th Global CEO Survey 2026 [PDF]",
        [
            ("Risk", "Geopolitics has moved from boardroom briefing to people strategy."),
            ("CHRO Association 2026", "46% of CHROs cite geopolitical instability as the top external force shaping their business."),
            ("PwC 2026", "84% of CEOs say their company has been moderately or significantly affected by geopolitical risk."),
            ("The CHRO read", "People strategy now needs scenario plans, not just succession plans."),
            ("Your move", "How does your workforce plan respond to a sudden trade shift?"),
        ],
        "Geopolitics has moved from boardroom briefing to people strategy.\n\nCHRO Association 2026: 46% of CHROs cite geopolitical instability as the top external force on their business. PwC 2026: 84% of CEOs say their company has been moderately or significantly affected.\n\nPeople strategy needs scenario plans now.\n\n#Risk #PeopleStrategy #Leadership",
    ),
    (
        "tariffs-meet-payroll",
        "Tariff exposure cascading into people decisions",
        "plum",
        "PwC 29th Global CEO Survey 2026 [PDF]; CHRO Association 2026 [PDF]",
        [
            ("Risk", "Tariffs aren't only a margin problem. They're a workforce problem."),
            ("PwC 2026", "29% of CEOs expect tariffs to reduce their company's net profit margin in the year ahead."),
            ("CHRO Association 2026", "35% of CHROs cite tariffs as a top external force."),
            ("The CHRO read", "Headcount decisions made under tariff pressure tend to be the ones most regretted later."),
            ("Your move", "Is your workforce plan tariff-pressure tested?"),
        ],
        "Tariffs aren't only a margin problem. They're a workforce problem.\n\nPwC 2026: 29% of CEOs expect tariffs to reduce net profit margin in the year ahead. CHRO Association 2026: 35% of CHROs cite tariffs as a top external force.\n\nTariff-pressure headcount decisions are the most-regretted ones.\n\n#Risk #PeopleStrategy #Leadership",
    ),
    (
        "adaptive-leadership-multiplies",
        "Reflective / adaptive leaders multiply organizational adaptability",
        "slate",
        "McKinsey State of Organizations 2026 [PDF]; Gartner 2026 [PDF]",
        [
            ("Leadership", "Reflective leaders see their organizations adapt — at almost double the rate."),
            ("McKinsey 2026", "30% of reflective leaders believe their org adapts quickly to change."),
            ("McKinsey 2026", "Only 17% of non-reflective leaders say the same."),
            ("The CHRO read", "Reflection isn't soft. It's a leverage point."),
            ("Your move", "Where does reflection live in your leadership operating rhythm?"),
        ],
        "Reflective leaders see their organizations adapt — at almost double the rate.\n\nMcKinsey 2026 (10,000 leaders, 16 countries): 30% of reflective leaders believe their org adapts quickly to change. Only 17% of non-reflective leaders say the same.\n\nReflection is a leverage point, not a soft skill.\n\n#Leadership #FutureOfWork #PeopleStrategy",
    ),
]

assert len(POSTS) == 30, f"Expected 30 posts, got {len(POSTS)}"


def word_count(text: str) -> int:
    return len(text.split())


def main():
    # Validate word counts (post body is the last element of each tuple)
    failures = []
    for i, p in enumerate(POSTS, 1):
        wc = word_count(p[5])
        if wc > 50:
            failures.append((i, p[0], wc))
    if failures:
        print("WORD COUNT FAILURES:")
        for i, slug, wc in failures:
            print(f"  Option {i:2d} ({slug}): {wc} words — OVER LIMIT")
        sys.exit(1)
    print(f"All 30 posts pass word-count check (max: {max(word_count(p[5]) for p in POSTS)} words)")

    # Write the draft markdown file
    out = [f"# Daily HR best-practices posts — {DATE} (batch of 30)", ""]
    out.append(f"Source brief: posts/drafts/pdf-findings-2026-05-22.md (18 PDFs read directly) + search-only catalog for firms without attached PDFs.")
    out.append("Regional lens: APAC relevance filter, universal framing.")
    out.append("Batch produced via scripts/build_30_posts.py — 30 distinct themes across AI/future-of-work, talent/comp/benefits, workforce/generations, and labor market/geopolitics/climate.")
    out.append("")
    out.append("All posts validated ≤50 words. PDF-grade evidence tagged `[PDF]` where the underlying report was read directly; `[search-only]` for snippet-cited claims.")
    out.append("")
    out.append("---")
    out.append("")
    for i, (slug, theme, accent, sources, slides, body) in enumerate(POSTS, 1):
        out.append(f"## Option {i} — {slug}")
        out.append(f"- **Theme:** {theme}")
        out.append(f"- **Accent:** {accent}")
        out.append(f"- **Sources:** {sources}")
        out.append(f"- **Carousel (5 slides):** posts/drafts/carousels/{DATE}-option-{i}/")
        for j, (tag, headline) in enumerate(slides, 1):
            out.append(f"  - slide-{j} · {tag} · \"{headline}\"")
        out.append(f"- **Image alt:** {slides[0][1]}")
        out.append(f"- **Word count:** {word_count(body)}")
        out.append(f"- **Status:** draft")
        out.append("")
        out.append("---POST---")
        out.append(body)
        out.append("---END---")
        out.append("")
        out.append("---")
        out.append("")

    draft_path = REPO / "posts" / "drafts" / f"best-practices-{DATE}-batch-30.md"
    draft_path.write_text("\n".join(out))
    print(f"Wrote draft file: {draft_path}")

    # Generate carousels + cover images in parallel
    print(f"Generating {len(POSTS) * 6} images...")
    procs = []
    for i, (slug, theme, accent, sources, slides, body) in enumerate(POSTS, 1):
        carousel_dir = REPO / "posts" / "drafts" / "carousels" / f"{DATE}-option-{i}"
        carousel_dir.mkdir(parents=True, exist_ok=True)
        for j, (tag, headline) in enumerate(slides, 1):
            slide_path = carousel_dir / f"slide-{j}.png"
            procs.append(subprocess.Popen([
                "python3", str(GEN),
                "--accent", accent,
                "--slide", f"{j}/5",
                "--tag", tag,
                "--headline", headline,
                "--output", str(slide_path),
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
        # Cover image (no slide indicator)
        cover_path = REPO / "posts" / "drafts" / "images" / f"{DATE}-option-{i}.png"
        cover_path.parent.mkdir(parents=True, exist_ok=True)
        procs.append(subprocess.Popen([
            "python3", str(GEN),
            "--accent", accent,
            "--tag", slides[0][0],
            "--headline", slides[0][1],
            "--output", str(cover_path),
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
        # Throttle: wait every 30 procs to avoid OOM
        if len(procs) >= 30:
            for proc in procs:
                proc.wait()
            procs = []
    for proc in procs:
        proc.wait()

    # Verify
    carousel_count = len(list((REPO / "posts" / "drafts" / "carousels").glob(f"{DATE}-option-*/slide-*.png")))
    cover_count = len(list((REPO / "posts" / "drafts" / "images").glob(f"{DATE}-option-*.png")))
    print(f"Generated {carousel_count} carousel slides + {cover_count} cover images")
    print(f"Expected {len(POSTS) * 5} slides + {len(POSTS)} covers = {len(POSTS) * 6} total")
    return 0


if __name__ == "__main__":
    sys.exit(main())
