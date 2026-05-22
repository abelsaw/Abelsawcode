#!/usr/bin/env python3
"""Generate a Word document of the /linkedin-post source catalog.

Reads the structured data inline (kept in sync with
.claude/skills/linkedin-post/sources.md) and produces a clean
docx at docs/HR-Source-Catalog-{YYYY-MM-DD}.docx — one row per
report, grouped by tier with a verification preface.
"""
from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Pt, RGBColor, Cm


TIER1 = [
    ("Mercer",   "Global Talent Trends 2026 (Feb 2026)",                              "https://www.mercer.com/about/newsroom/mercer-s-global-talent-trends-2026-report/"),
    ("Mercer",   "2025/2026 Skills Snapshot Survey",                                  "https://www.mercer.com/insights/talent-and-transformation/skill-based-talent-management/rebuilding-reward-and-career-frameworks-based-on-skills/"),
    ("Mercer",   "Talent Mobility insights 2026",                                     "https://www.mercer.com/solutions/talent-and-rewards/talent-mobility/"),
    ("Mercer",   "Mercer Marsh Benefits Asia 2026",                                   ""),
    ("Aon",      "2026 Human Capital Outlook: 5 Forces to Act On",                    "https://www.aon.com/en/insights/articles/2026-human-capital-outlook-5-forces-to-act-on"),
    ("Aon",      "2026 Human Capital Trends Study (Apr 2026)",                        "https://www.aon.com/en/insights/reports/human-capital-trends-study"),
    ("Aon",      "US Employer Health Care Costs +9.5% in 2026 (Sept 2025)",           "https://aon.mediaroom.com/2025-09-10-Aon-U-S-Employer-Health-Care-Costs-Expected-to-Rise-9-5-Percent-in-2026"),
    ("McKinsey", "The State of Organizations 2026",                                   "https://www.mckinsey.com/capabilities/people-and-organizational-performance/our-insights/the-state-of-organizations"),
    ("McKinsey", "Where AI Will Create Value and Where It Won't (2026)",              "https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/where-ai-will-create-value-and-where-it-wont"),
    ("McKinsey", "The Critical Role of Strategic Workforce Planning in the Age of AI (2026)", "https://www.mckinsey.com/capabilities/people-and-organizational-performance/our-insights/the-critical-role-of-strategic-workforce-planning-in-the-age-of-ai"),
    ("McKinsey", "The State of AI in Southeast Asia (2026)",                          "https://www.mckinsey.com/featured-insights/asia-pacific/the-state-of-ai-in-southeast-asia"),
    ("WEF",      "Davos 2026 jobs and skills transformation stories (Jan 2026)",      "https://www.weforum.org/stories/2026/01/davos-here-s-what-to-know-about-jobs-and-skills-transformation/"),
    ("WEF",      "Reskilling Revolution update (Jan 2026)",                           "https://www.weforum.org/press/2026/01/world-economic-forum-reskilling-revolution-on-track-to-reach-over-850-million-people/"),
    ("WEF",      "The AI-Driven Workforce Is Here (Feb 2026)",                        "https://www.weforum.org/stories/2026/02/workforce-transformation-ai-jobs/"),
    ("WEF",      "Climate crisis impact on jobs / workforce",                         "https://www.weforum.org/stories/2023/10/climate-crisis-impacting-jobs-workforce/"),
    ("BCG",      "AI Will Reshape More Jobs Than It Replaces (2026)",                 "https://www.bcg.com/publications/2026/ai-will-reshape-more-jobs-than-it-replaces"),
    ("BCG",      "Making AI Productivity Deliver Real Value (2026)",                  "https://www.bcg.com/publications/2026/making-ai-productivity-deliver-real-value"),
    ("BCG",      "AI Transformation Is a Workforce Transformation (2026)",            "https://www.bcg.com/publications/2026/ai-transformation-is-a-workforce-transformation"),
    ("BCG",      "As AI Investments Surge, CEOs Take Lead on Decision Making and Upskilling (Jan 2026)", "https://www.bcg.com/press/15january2026-as-ai-investments-surge-ceos-take-lead"),
    ("BCG",      "Global Talent Mobility Is Slowing and Shifting",                    "https://www.bcg.com/publications/2025/global-talent-mobility-is-slowing-and-shifting"),
    ("WTW",      "2026 Global Medical Trends Survey (Oct 2025)",                      "https://www.wtwco.com/en-in/insights/2025/10/2026-global-medical-trends-survey"),
    ("WTW",      "Countering Disruptions with Dynamic Total Rewards Strategies (Jan 2026)", "https://www.wtwco.com/en-us/insights/2026/01/countering-disruptions-with-dynamic-total-rewards-strategies-actions-for-2026"),
    ("WTW",      "2026 Salary Budget Planning Survey",                                "https://worldatwork.org/publications/workspan-daily/wtw-poll-reflects-2026-salary-budget-stability-3-4-increases-planned"),
    ("Deloitte", "2026 Global Human Capital Trends: From Tensions to Tipping Points", "https://www.deloitte.com/us/en/insights/topics/talent/human-capital-trends.html"),
    ("Deloitte", "Activating the Internal Talent Marketplace",                        "https://www.deloitte.com/us/en/insights/topics/talent/internal-talent-marketplace.html"),
    ("Deloitte", "Navigating the Data Dilemma (workforce monitoring & analytics)",    "https://www.deloitte.com/us/en/insights/topics/talent/monitoring-employees-in-the-workplace.html"),
    ("Deloitte", "Global Gen Z and Millennial Survey 2026 (15th edition)",            "https://www.deloitte.com/global/en/issues/work/genz-millennial-survey.html"),
    ("Gallup",   "State of the Global Workplace 2026 (Apr 2026)",                     "https://www.gallup.com/workplace/349484/state-of-the-global-workplace.aspx"),
]

TIER2 = [
    ("PwC",              "29th Global CEO Survey 2026 (Jan 2026; 4,454 CEOs across 95 countries)", "https://www.pwc.com/gx/en/news-room/press-releases/2026/pwc-2026-global-ceo-survey.html"),
    ("PwC",              "Workforce Hopes and Fears 2026",                                          ""),
    ("SHRM",             "2026 CHRO Priorities and Perspectives (129 CHROs)",                       "https://www.shrm.org/topics-tools/research/2026-chro-priorities-and-perspectives"),
    ("SHRM",             "State of AI in HR 2026 (May 2026)",                                       "https://www.shrm.org/topics-tools/research/state-of-ai-hr-2026/full-report"),
    ("Bain",             "Aura labor market data (Q4 2025 / 2026)",                                 ""),
    ("KPMG",             "2026 CEO Outlook (people section)",                                       "https://kpmg.com/us/en/articles/2026/ceo-outlook-ungated.html"),
    ("KPMG",             "2026 Mobility data (industry round-ups)",                                 ""),
    ("Conference Board", "CHRO Confidence Survey Q1 2026",                                          "https://www.conference-board.org/topics/chro-confidence/press/chro-confidence-survey-q1-2026"),
    ("Gartner",          "Top CHRO Priorities for 2026 (426 CHROs, 23 industries, 4 regions)",     "https://www.gartner.com/en/newsroom/press-releases/2025-10-02-gartner-says-chros-top-priorities-for-2026-center-around-realizing-ai-value-and-driving-performance-amid-uncertainty"),
]

TIER3 = [
    ("Hays",                       "Hays Asia Salary Guide 2026; Asia Workforce Trends",                       ""),
    ("Robert Walters",             "Salary Survey 2026 (Singapore, HK, China, Japan, Australia volumes)",      "https://www.robertwalters.com.sg/insights/career-advice/salary-survey-2026.html"),
    ("Michael Page",               "Talent Trends 2026 APAC",                                                  ""),
    ("INSEAD",                     "Global Talent Competitiveness Index 2026; INSEAD Knowledge HR pieces",     ""),
    ("Mercer Asia",                "APAC breakouts of Global Talent Trends 2026",                              ""),
    ("WTW APAC",                   "APAC breakouts of Global Medical Trends; APAC Salary Budget Planning",     ""),
    ("Deloitte APAC",              "APAC Human Capital Trends 2026",                                            "https://www.deloitte.com/global/en/issues/work/human-capital-trends-asia-pacific.html"),
    ("ILO Asia-Pacific",           "World Employment and Social Outlook 2026",                                  "https://www.ilo.org/publications/major-publications/world-employment-and-social-outlook-trends-2026"),
    ("ILO",                        "Heat-stress and labour productivity data (updated 2026)",                  "https://www.ilo.org/resource/news/increase-heat-stress-predicted-bring-productivity-loss-equivalent-80"),
    ("ADB",                        "Asia Productivity / Work research 2026",                                    ""),
    ("Singapore MOM",              "Labour Market Report Q1 2026; Manpower Research",                          ""),
    ("AHRI (Australia)",           "Pulse Survey 2026; HR research papers",                                    ""),
    ("HKIHRM",                     "Industry surveys 2026",                                                     ""),
    ("People Matters (India)",     "India HR Industry surveys 2026; State of HR Tech",                          ""),
    ("HR Asia",                    "Best Companies to Work for in Asia 2026 awards research",                  ""),
]

AUTO_DISCOVERED = [
    ("Korn Ferry",                       "Tier 3", "Talent Trends 2026: Human-AI Power Couple (APAC edition)",      "https://www.kornferry.com/about-us/events-webinars/talent-acquisition-trends-2026-apac"),
    ("Korn Ferry",                       "Tier 3", "Engaging the Next Generation of Gen Z Leaders in APAC",         "https://www.kornferry.com/insights/featured-topics/talent-recruitment/engaging-the-next-generation-of-gen-z-leaders-in-apac"),
    ("IBM Institute for Business Value", "Tier 2", "CEO Study: Reshaping C-suite Roles for the AI Era (May 2026)",  "https://newsroom.ibm.com/2026-05-04-ibm-study-ceos-are-reshaping-c-suite-roles-for-the-ai-era"),
    ("EY People Advisory",               "Tier 2", "2026 Mobility Reimagined Survey",                                "https://www.ey.com/en_gl/insights/workforce/mobility-reimagined-survey"),
    ("IFC",                              "Tier 3", "Hidden Potential: Inclusive Jobs in Green Transitions (2026)",  "https://www.ifc.org/content/dam/ifc/doc/2026/how-employers-can-accelerate-inclusive-jobs-in-green-transitions.pdf"),
    ("ManpowerGroup",                    "Tier 3", "Global Talent Barometer 2026",                                    "https://www.manpowergroup.com/insights/global-talent-barometer"),
]


def set_cell_shading(cell, color_hex):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color_hex)
    tc_pr.append(shd)


def add_tier_section(doc, heading, intro, rows, include_tier_col=False):
    doc.add_heading(heading, level=1)
    p = doc.add_paragraph()
    run = p.add_run(intro)
    run.italic = True
    run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    cols = 4 if include_tier_col else 3
    table = doc.add_table(rows=1, cols=cols)
    table.style = "Light Grid Accent 1"
    hdr = table.rows[0].cells
    if include_tier_col:
        hdr[0].text = "Firm"
        hdr[1].text = "Tier"
        hdr[2].text = "Report"
        hdr[3].text = "URL"
    else:
        hdr[0].text = "Firm"
        hdr[1].text = "Report"
        hdr[2].text = "URL"
    for cell in hdr:
        for para in cell.paragraphs:
            for r in para.runs:
                r.bold = True
        set_cell_shading(cell, "1E3A8A")
        for para in cell.paragraphs:
            for r in para.runs:
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for row in rows:
        cells = table.add_row().cells
        if include_tier_col:
            firm, tier, report, url = row
            cells[0].text = firm
            cells[1].text = tier
            cells[2].text = report
            cells[3].text = url if url else "(URL not on file)"
        else:
            firm, report, url = row
            cells[0].text = firm
            cells[1].text = report
            cells[2].text = url if url else "(URL not on file)"
        for cell in cells:
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            for para in cell.paragraphs:
                for r in para.runs:
                    r.font.size = Pt(9.5)
    doc.add_paragraph()


def main():
    doc = Document()

    for section in doc.sections:
        section.left_margin = Cm(1.8)
        section.right_margin = Cm(1.8)
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)

    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(10.5)

    title = doc.add_heading("HR Research Source Catalog — 2026", level=0)
    for r in title.runs:
        r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    sub = doc.add_paragraph()
    sr = sub.add_run(
        "Canonical 2026 source catalog used by the /linkedin-post Claude Code skill. "
        "33 firms / institutions across three tiers, including five auto-discovered this session."
    )
    sr.italic = True
    sr.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    today = date.today().isoformat()
    meta = doc.add_paragraph()
    mr = meta.add_run(f"Generated: {today}  ·  Branch: claude/linkedin-hr-news-agents-p9Qkv")
    mr.italic = True
    mr.font.size = Pt(9)
    mr.font.color.rgb = RGBColor(0x77, 0x77, 0x77)

    note_p = doc.add_paragraph()
    note_p.add_run("Verification note: ").bold = True
    note_p.add_run(
        "All reports cited in this catalog were referenced via search-engine-indexed "
        "content (snippets, press releases, partner summaries) — not direct PDF reads. "
        "The remote container's network policy blocked WebFetch on every firm domain "
        "during research runs. Numbers and quotes should be re-verified against the "
        "original publications before external use."
    )

    add_tier_section(
        doc,
        "Tier 1 — Required coverage every run (8 firms)",
        "Global big-brand HR / consulting / research firms with strong 2026 publication cadence. "
        "The scout searches these on every run.",
        TIER1,
    )

    add_tier_section(
        doc,
        "Tier 2 — Swept when relevant (6 firms + 2 auto-discovered)",
        "Global firms with credible 2026 research that the scout sweeps when relevant. "
        "IBM IBV and EY People Advisory were added to this tier on 2026-05-19.",
        TIER2,
    )

    add_tier_section(
        doc,
        "Tier 3 — Asia Pacific–focused (14 firms + 3 auto-discovered)",
        "APAC-focused research firms, multilateral bodies, government statistics offices, "
        "and regional HR institutes. Weighted when the skill runs with region: apac (default). "
        "Korn Ferry APAC, IFC, and ManpowerGroup were added to this tier on 2026-05-19.",
        TIER3,
    )

    add_tier_section(
        doc,
        "Auto-discovered this session (added 2026-05-19)",
        "Sources discovered by the scout during runs and persisted to the catalog. "
        "Each entry includes its assigned tier alongside the firm.",
        AUTO_DISCOVERED,
        include_tier_col=True,
    )

    doc.add_heading("Summary", level=1)
    summary_data = [
        ("Tier 1 (global)", "8 firms", "28 specific 2026 publications cited"),
        ("Tier 2 (global, swept)", "8 firms (6 original + 2 auto-discovered)", "9 publications"),
        ("Tier 3 (APAC-focused)", "17 firms (14 original + 3 auto-discovered)", "17 publications"),
        ("Grand total", "33 sources", "~54 specific 2026 publications referenced"),
    ]
    tbl = doc.add_table(rows=1, cols=3)
    tbl.style = "Light Grid Accent 1"
    h = tbl.rows[0].cells
    h[0].text = "Tier"
    h[1].text = "Firms"
    h[2].text = "Publications cited"
    for c in h:
        set_cell_shading(c, "1E3A8A")
        for p in c.paragraphs:
            for r in p.runs:
                r.bold = True
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    for tier, firms, pubs in summary_data:
        cells = tbl.add_row().cells
        cells[0].text = tier
        cells[1].text = firms
        cells[2].text = pubs

    out_dir = Path(__file__).resolve().parent.parent / "docs"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / f"HR-Source-Catalog-{today}.docx"
    doc.save(out_path)
    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
