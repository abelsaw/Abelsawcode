---
name: hr-linkedin-option1
description: Render a 7-slide LinkedIn carousel in HR Option 1 — playful-iconic with geometric chip icons. Cream / navy / coral / mustard palette. Slide 1 cover features a brand tag, big bold sans navy title, mustard accent rule, italic serif subtitle, and a row of 4 geometric chip icons (circle / square / triangle / diamond). Slides 2-6 keep sans throughout — a large coral slide number with a mustard wayfinder rule top-left, bold sans navy headline, two-part body (muted regular lead + navy bold payoff). Slide 7 is the closing on a navy dark background — the only dark slide — same body structure, inverted (cream text on navy with the coral slide #). Use when the user invokes /hr-linkedin-option1 or asks for "HR LinkedIn Option 1".
---

# hr-linkedin-option1 — playful-iconic with geometric chips

The default modern carousel preset for HR LinkedIn posts. Sans
throughout, four palette colors, geometric chip icons on the cover act
as decorative anchors without veering into clip-art.

## What it looks like

### Slide 1 (cover)

```
┌──────────────────────────────────────────────────┐
│ CTRO                                  │ ← brand tag tracked caps
│ ──                                                │   + coral mini-stripe
│                                                  │
│ Internal                                         │ ← bold sans navy title
│ Mobility                                         │   (1-2 lines, auto-fit)
│ ───                                              │ ← mustard accent rule
│ The retention asset you already own.             │ ← italic serif subtitle
│                                                  │   (muted)
│                                                  │
│   ●        ■        ▲        ◆                   │ ← 4 geometric chip icons
│  HIRE     KEEP     GROW     MOVE                 │   in palette colors
│                                                  │   + tracked-caps labels
│ — MERCER GLOBAL TALENT TRENDS 2026               │ ← em-dash source
│                                       01 / 05    │ ← counter (stacked)
└──────────────────────────────────────────────────┘
```

### Slides 2-6 (content)

```
┌──────────────────────────────────────────────────┐
│ 02                                                │ ← large coral slide #
│ ───                                               │ ← mustard wayfinder rule
│                                                  │
│ External hiring is                               │ ← bold sans navy headline
│ contracting.                                     │
│                                                  │
│ The career inside                                │ ← muted sans regular lead
│ is the new retention asset.                      │ ← navy sans bold payoff
│                                                  │
│ MERCER 2026                          02 / 05     │ ← navy source + counter
└──────────────────────────────────────────────────┘
```

## Palette

- `BG` cream — `(244, 235, 220)` — `#F4EBDC`
- `NAVY` deep navy — `(27, 49, 71)` — `#1B3147` (titles, headlines, payoff bold)
- `CORAL` warm coral — `(226, 106, 75)` — `#E26A4B` (slide #, chip 1 & 4, mini-stripe)
- `MUSTARD` rich mustard — `(212, 154, 56)` — `#D49A38` (accent rules, chip 3)
- `MUTED` warm gray-brown — `(108, 95, 80)` — `#6C5F50` (subtitle, lead, counter)

## Fonts (deliberate sans-throughout)

- **Sans bold** (DejaVu Sans Bold) — title, headline, slide #, payoff, source, counter, chip labels
- **Sans regular** (DejaVu Sans) — body lead (muted)
- **Italic serif** (Liberation Serif Italic) — subtitle on the cover only

Italic serif used sparingly creates the single contrast element on the
cover; everything else stays sans for a modern, crisp feel.

## Renderers

| Slide | Script |
|---|---|
| Slide 1 (cover) | `scripts/generate_post_image_playful_cover.py` |
| Slides 2-6 (content) | `scripts/generate_post_image_playful_content.py` |
| Slide 7 (dark conclusion) | `scripts/generate_post_image_playful_dark_conclusion.py` |

### Cover CLI

```bash
python3 scripts/generate_post_image_playful_cover.py \
  --tag "CTRO" \
  --title "Internal\nMobility" \
  --subtitle "The retention asset\nyou already own." \
  --chips "HIRE,KEEP,GROW,MOVE" \
  --source "Mercer Global Talent Trends 2026" \
  --slide "1/7" \
  --output posts/sets/<date>/<slug>/slide-01.png
```

| Flag | Required | Use |
|---|---|---|
| `--tag`      | no  | Brand tag tracked caps. Default `"CTRO"`. |
| `--title`    | yes | Bold sans title. Supports `\n` for forced breaks. |
| `--subtitle` | no  | Italic serif subtitle. Supports `\n`. |
| `--chips`    | no  | Comma-separated 4 chip labels. Default `"HIRE,KEEP,GROW,MOVE"`. |
| `--source`   | no  | Em-dash + tracked small-caps source row. |
| `--slide`    | no  | `N/M` slide indicator. |
| `--output`   | yes | Output PNG path. |

### Content CLI

```bash
python3 scripts/generate_post_image_playful_content.py \
  --headline "External hiring is contracting." \
  --lead     "The career inside" \
  --bold     "is the new retention asset." \
  --source   "Mercer 2026" \
  --slide    "2/7" \
  --output   posts/sets/<date>/<slug>/slide-02.png
```

| Flag | Required | Use |
|---|---|---|
| `--headline` | yes | Bold sans navy headline. Supports `\n`. |
| `--lead`     | no  | Muted sans regular lead. Supports `\n` for action lists. |
| `--bold`     | no  | Navy sans bold payoff. |
| `--source`   | no  | Navy tracked-caps source row. |
| `--slide`    | no  | `N/M` slide indicator. |
| `--output`   | yes | Output PNG path. |

## Content-fit rules

The design carries the same two-part body shape across cover and
content slides:

1. **Title / Headline** — the observation in bold sans navy.
2. **Lead** (muted sans regular) — the bridge phrase.
3. **Payoff** (navy sans bold) — the punchline that completes the lead.
4. **Source** — short attribution (firm + year is enough).

### Action-list slide (slide 6 of 7)

Drop `--bold` and pass a multi-line `--lead` (use literal `\n` between
items). Each item stays on its own line in muted sans regular.

### Closing slide (slide 7 of 7) — dark background

Use `scripts/generate_post_image_playful_dark_conclusion.py` — the
ONLY dark slide in the carousel. Navy background, cream text, same
lead + bold structure as content slides. The bold payoff is the
screenshot-worthy takeaway.

```bash
python3 scripts/generate_post_image_playful_dark_conclusion.py \
  --headline "Internal mobility is not a perk." \
  --lead     "It is the cheapest, fastest" \
  --bold     "retention strategy you already own." \
  --source   "CTRO Read" \
  --slide    "7/7" \
  --output   posts/sets/<date>/<slug>/slide-07.png
```

The dark-conclusion CLI mirrors the content CLI (`--headline / --lead /
--bold / --source / --slide / --output`) — no extra flags.

### Cover chip labels

`--chips "HIRE,KEEP,GROW,MOVE"` — choose 4 short single-word labels
that thematically preview the four substance slides. Don't pass icons
literal to the topic (no "briefcase / chart / target"); the chip
shapes (circle / square / triangle / diamond) are abstract anchors.

## When to use

- Default modern carousel style for `/linkedin-post` runs.
- When the user invokes `/hr-linkedin-option1`.
- When the carousel is best served by a structured cover preview + clean
  word-focused content slides (most HR best-practice topics).

## When NOT to use

- When the carousel is a structured 4-part framework where a colored
  tile wayfinder reinforces the topic per slide → use
  `hr-linkedin-option2` instead.
- When the user wants the warm magazine / pull-quote feel → use
  `vintage-editorial`.

## Sample output

See `posts/design-tests/option2-v1/` for the locked reference set.
