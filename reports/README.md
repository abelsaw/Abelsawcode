# Attached reports

Drop downloaded 2026 HR research PDFs here. The `hr-best-practices-scout`
agent and the `/linkedin-post` skill will pick them up automatically
on the next run.

## Folder convention

```
reports/
  2026/
    mercer/
      global-talent-trends-2026.pdf
      skills-snapshot-2026.pdf
    deloitte/
      global-human-capital-trends-2026.pdf
      gen-z-millennial-survey-2026.pdf
    wtw/
      global-medical-trends-survey-2026.pdf
    ...
```

Sub-folder per firm. Lowercase, hyphenated. Year-anchored at the top
level so future years don't clutter.

## How the scout uses them

When the scout researches a firm during a run, it checks
`reports/2026/{firm-slug}/` first. If PDFs exist:

1. The scout **reads the PDF directly** (using the Read tool, which
   supports PDF). Findings extracted from PDFs are tagged `[PDF]`
   in the brief instead of `[search-only]`.
2. Multiple sub-angles can be surfaced from a single report —
   methodology details, regional/industry/role breakdowns,
   contrarian sub-points — instead of one parent theme per firm.
3. The dedup ledger can recycle a parent theme when a new PDF
   surfaces a genuinely fresh sub-angle (cite the PDF page or
   exhibit, not just the theme label).
4. If no PDF exists for a firm, the scout falls back to WebSearch
   snippets as today.

## Naming tips

- One file = one report. Don't concatenate.
- Keep the original publication title where possible — easier to
  cross-reference against the source catalog (`docs/HR-Source-Catalog-{date}.docx`).
- If the report is paywalled or under NDA, do not commit it. The
  `.gitignore` covers `.pdf` files only inside `reports/private/`
  if you want a local-only stash (create that folder yourself).

## What's allowed in the repo

- Publicly downloadable research PDFs from credible firms (Mercer,
  Deloitte, WTW, McKinsey, BCG, WEF, ILO, etc.) — **yes**, as long
  as their terms of use permit redistribution. Most public research
  PDFs do.
- Paywalled / proprietary / paid-license PDFs — **no**. Keep those
  outside the repo or in `reports/private/` (gitignored).
- Press-release pages and HTML excerpts — not needed; the scout
  already pulls those via WebSearch.

When in doubt, check the report's first or last page for terms of
use, or stash it under `reports/private/` to be safe.
