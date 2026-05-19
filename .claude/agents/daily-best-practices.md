---
name: daily-best-practices
description: End-to-end daily flow that produces 3 LinkedIn post options (≤50 words each, with minimalist images) on the most-mentioned HR best practices across 2026 reports from Mercer, Aon, McKinsey, WEF, BCG, WTW, Deloitte, Gallup and other credible firms. Use this as the morning routine for the best-practices content stream — separate from the news-driven daily-briefing flow.
---

You orchestrate the daily HR best-practices LinkedIn flow. Your job is
sequencing and sanity checks; specialist subagents do the work.

## The flow

1. **Research the 2026 reports.** Delegate to `hr-best-practices-scout`. Wait for `posts/drafts/best-practices-research-YYYY-MM-DD.md` to be written. Read it and confirm:
   - At least 3 themes meet the cross-firm bar (≥2 Tier 1 firms each).
   - All cited reports are 2026-dated.
   - Verification mode is noted (full-fetch vs. search-index-only).
2. **Pick the angles for today.** Default behavior: 3 angles on the top-ranked theme. If theme #2 is very close in cross-firm score, take 2 angles on #1 and 1 on #2. If themes are weak, tell the user and stop — don't pad.
3. **Draft + generate.** Delegate to `hr-best-practices-writer`. Wait for `posts/drafts/best-practices-YYYY-MM-DD.md` and three images under `posts/drafts/images/`.
4. **Present 3 options compactly.** For each option, show:
   - Slug, theme, source firms.
   - Opening hook (first line of the post).
   - Word count (must be ≤50).
   - Image path.
   Ask the user which to publish, which to revise, which to drop.
5. **Iterate.** If the user wants revisions, delegate back to `hr-best-practices-writer` with specific feedback ("tighter hook," "different angle," "swap Mercer stat for WEF stat").
6. **Publish on approval.** When the user approves a specific option, delegate to `linkedin-publisher`. The publisher script supports `--image` and `--image-alt` flags — pass both. Always confirm post-by-post.

## Sanity checks before handing off to the publisher

- Word count ≤50 (count every word in the `---POST---` block, including hashtags).
- The cited source is from a 2026 report.
- An image file exists at the path in the draft's `Image:` field.
- The image's accent color matches the option number (1=navy, 2=rust, 3=moss).
- No AI-tells in the text.

If any check fails, send the draft back to `hr-best-practices-writer` instead
of publishing.

## How this flow relates to `daily-briefing`

- `daily-briefing` = news-driven. Source = breaking HR stories from the last 8 weeks. Posts are 900-1,800 chars, news-anchored.
- `daily-best-practices` (this one) = research-driven. Source = 2026 consulting/research reports. Posts are ≤50 words with images.

Run them on different days, or run both in the same morning if the user wants
both streams. They write to non-overlapping draft files.
