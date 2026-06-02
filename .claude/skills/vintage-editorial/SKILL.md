---
name: vintage-editorial
description: Render a 5-slide LinkedIn carousel in the immersed editorial pull-quote style — hairline antique-gold frame, oversized opening-quote glyph, italic serif setup over a thin gold rule, muted sans lead + bold sans payoff, em-dash small-caps source attribution, slide number top-left + counter bottom-right. Cream / espresso / antique-gold earth-tone palette. Use when the user wants polished, magazine-grade slides ("render in vintage-editorial", "use the v5 design", "make the carousel in editorial style") or when /linkedin-post is invoked and the user's default carousel style is vintage-editorial.
---

# vintage-editorial — 5-slide carousel design preset

This is **Option 1 (locked v5)** — the immersed editorial pull-quote
design the user chose on 2026-06-02 as the default carousel style.

## What it looks like

```
┌─────────── antique-gold hairline frame ──────────┐
│ 02                                                │  ← slide # (sans bold) +
│ ──                                                │     thin gold rule under
│                                                   │
│     "                                             │  ← oversized opening
│     setup line in italic serif                    │     quote glyph (gold)
│     ──────────────────────                        │  ← thin gold rule closes
│                                                   │     the setup
│     muted lead phrase                             │  ← sans regular, muted
│     BOLD SANS PAYOFF PHRASE                       │  ← sans bold, espresso
│                                                   │
│ — MERCER GLOBAL TALENT TRENDS 2026                │  ← source row
│                                       02 / 12     │  ← counter row
└───────────────────────────────────────────────────┘
```

Every element reads top-to-bottom as a single editorial arc: orientation
(slide #) → quoted observation (glyph + italic setup + rule) → punchline
(muted lead + bold payoff) → attribution (em-dash source + counter).

## Palette

Three earth tones (+ one tonal muted variant):

- `BG` cream — `(239, 229, 208)` — `#EFE5D0`
- `INK` espresso — `(38, 30, 22)` — `#261E16` (used only for the bold payoff)
- `GOLD` antique gold — `(160, 122, 64)` — `#A07A40` (frame, glyph, rules)
- `MUTED` warm gray-brown — `(120, 102, 84)` — `#786654` (italic setup, lead, source, counter)

## Fonts (four roles, mixed)

- **Sans tracked caps** (DejaVu Sans Bold) — slide #, source, counter
- **Display serif bold** (DejaVu Serif Bold) — opening quote glyph
- **Italic serif** (Liberation Serif Italic) — setup line
- **Sans regular + bold** (DejaVu Sans / DejaVu Sans Bold) — body lead + payoff

## Renderer

`scripts/generate_post_image_simple_vintage_v5.py`

```bash
python3 scripts/generate_post_image_simple_vintage_v5.py \
  --setup "External hiring is contracting." \
  --lead  "The career inside" \
  --bold  "is the new retention asset." \
  --source "Mercer Global Talent Trends 2026" \
  --slide "1/5" \
  --output posts/sets/<date>/<slug>/slide-01.png
```

### CLI flags

| Flag | Required | Use |
|---|---|---|
| `--setup`  | yes | Italic serif setup line. Supports `\n` for forced breaks. |
| `--lead`   | no  | Muted sans regular phrase below the rule. Supports `\n` (use for action-list slides). |
| `--bold`   | no  | Bold sans payoff phrase below the lead. |
| `--source` | no  | Em-dash + tracked small-caps source row (e.g. `"Mercer 2026"`). |
| `--slide`  | no  | Slide indicator as `N/M` (e.g. `"2/5"`). |
| `--output` | yes | Output PNG path. |

## Content-fit rules

The design is built around a specific information shape per slide. When
authoring carousel copy, split each slide's idea into:

1. **Setup** (italic) — the observation, the framing, the contrast.
   _One short sentence._ This is the "voice."
2. **Lead** (muted regular) — the bridge to the punchline.
   _Half a sentence, ending mid-thought._
3. **Bold** (sans bold) — the payoff that completes the lead.
   _Half a sentence; together with the lead it forms one complete sentence._
4. **Source** — short attribution (firm + year is enough).

### Action-list slide (slide 4 of 5)

For the "what to do" slide, drop `--bold` and pass a multi-line `--lead`
(use literal `\n` between items). Each item stays on its own single
line in muted sans regular.

```bash
--setup "What CHROs are doing now."
--lead  "Open roles internally first.\nMap adjacent skills, not titles.\nMake mobility a manager KPI."
--source "CHRO Playbook"
--slide "4/5"
```

### Closing slide (slide 5 of 5)

Slide 5 must land as a **conclusion, not a question**. Use the same
setup / lead / bold structure as data slides — the bold payoff is the
takeaway readers can screenshot.

## When to use

- Any `/linkedin-post` run where the user hasn't asked for a different style.
- When the user says "render in vintage-editorial" or "use v5 design."
- When the carousel needs editorial polish over infographic density.

## When NOT to use

- When the slide carries a single dominant stat as its hook
  (use `vintage-bignumber` / v3 instead).
- When the user wants a colorful, icon-driven cover slide
  (use Option 2 — `playful-iconic` — once it ships).

## Related variants (kept for reference, not the default)

| Variant | Script | Use |
|---|---|---|
| v2 (no frame) | `scripts/generate_post_image_simple_vintage.py` | Original two-part body, no frame, no glyph. |
| v3 (big-number) | `scripts/generate_post_image_simple_vintage_v3.py` | One giant rust-colored stat per slide. |
| v4 (pull-quote only) | `scripts/generate_post_image_simple_vintage_v4.py` | Single italic serif quote inside a gold frame. |

v5 (this skill) is the locked combination of v2 + v4.
