---
name: hr-linkedin-option2
description: Render a 7-slide LinkedIn carousel in HR Option 2 — playful-iconic with numbered TOC tiles. Cream / navy / coral / mustard / dark-coral palette. Slide 1 cover features a brand tag, big bold sans navy title, italic serif subtitle, and a 2×2 grid of colored tiles (coral / navy / mustard / dark coral) — each tile carries a slide number + topic word as a TOC preview. Slides 2-6 open with a full-width colored wayfinder ribbon (the four cover-tile colors for slides 2-5, then a reused mustard ribbon for the slide 6 action takeaway), carrying the slide # + topic label, then sans bold navy headline + two-part body. Slide 7 is the closing on a navy dark background — the only dark slide — with a mustard "wayfinder residue" stripe at the top to bridge back to the content slides. Use when the user invokes /hr-linkedin-option2.
---

# hr-linkedin-option2 — playful-iconic with TOC tiles

The structured-framework carousel preset. The cover doubles as a
table-of-contents preview; content slides open with a colored
wayfinder ribbon that ties each slide back to its tile in the cover
grid.

## What it looks like

### Slide 1 (cover)

```
┌──────────────────────────────────────────────────┐
│ CTRO                                  │ ← brand tag tracked caps
│ ──                                                │   + coral mini-stripe
│                                                  │
│ Internal                                         │ ← bold sans navy title
│ Mobility                                         │
│ The retention asset you already own.             │ ← italic serif subtitle
│                                                  │
│ ┌──────────────┐  ┌──────────────┐               │
│ │ 01           │  │ 02           │               │ ← 2×2 tile grid
│ │              │  │              │               │   coral · navy
│ │       HIRE   │  │       KEEP   │               │
│ └──────────────┘  └──────────────┘               │
│ ┌──────────────┐  ┌──────────────┐               │
│ │ 03           │  │ 04           │               │
│ │              │  │              │               │   mustard · dark coral
│ │       GROW   │  │       MOVE   │               │
│ └──────────────┘  └──────────────┘               │
│ — MERCER GLOBAL TALENT TRENDS 2026               │ ← em-dash source
│                                       01 / 05    │ ← counter (stacked)
└──────────────────────────────────────────────────┘
```

### Slides 2-6 (content)

```
┌──────────────────────────────────────────────────┐
│ ████████████████████████████████████████████████ │
│ █ 02                                     HIRE  █ │ ← colored wayfinder
│ ████████████████████████████████████████████████ │   ribbon (matches
│                                                  │   the slide's tile)
│ External hiring is                               │ ← bold sans navy headline
│ contracting.                                     │
│                                                  │
│ The career inside                                │ ← muted sans regular lead
│ is the new retention asset.                      │ ← navy sans bold payoff
│                                                  │
│ MERCER 2026                          02 / 05     │ ← navy source + counter
└──────────────────────────────────────────────────┘
```

Each content slide's ribbon color tracks the cover-tile color (with
slide 6's ribbon reusing mustard for the action takeaway):

| Slide | Ribbon color | Default topic |
|---|---|---|
| 2 | coral | HIRE |
| 3 | navy | KEEP |
| 4 | mustard | GROW |
| 5 | dark coral | MOVE |
| 6 | mustard | PLAY (action list) |
| 7 | navy BG (dark conclusion) | — |

## Palette

- `BG` cream — `(244, 235, 220)` — `#F4EBDC`
- `NAVY` deep navy — `(27, 49, 71)` — `#1B3147` (title, headline, payoff, tile 2)
- `CORAL` warm coral — `(226, 106, 75)` — `#E26A4B` (tile 1, mini-stripe)
- `MUSTARD` rich mustard — `(212, 154, 56)` — `#D49A38` (tile 3)
- `DARK_CORAL` deep coral — `(175, 75, 55)` — `#AF4B37` (tile 4)
- `MUTED` warm gray-brown — `(108, 95, 80)` — `#6C5F50` (subtitle, lead, counter)
- `TILE_TEXT` cream — `BG` (text on colored tiles is the cream BG color)

## Fonts

- **Sans bold** (DejaVu Sans Bold) — title, headline, slide #, payoff, source, counter, tile number, tile label
- **Sans regular** (DejaVu Sans) — body lead (muted)
- **Italic serif** (Liberation Serif Italic) — cover subtitle only

## Renderers

| Slide | Script |
|---|---|
| Slide 1 (cover) | `scripts/generate_post_image_playful_v2_cover.py` |
| Slides 2-6 (content) | `scripts/generate_post_image_playful_v2_content.py` |
| Slide 7 (dark conclusion) | `scripts/generate_post_image_playful_v2_dark_conclusion.py` |

### Cover CLI

```bash
python3 scripts/generate_post_image_playful_v2_cover.py \
  --tag      "CTRO" \
  --title    "Internal\nMobility" \
  --subtitle "The retention asset you already own." \
  --tiles    "01:HIRE,02:KEEP,03:GROW,04:MOVE" \
  --source   "Mercer Global Talent Trends 2026" \
  --slide    "1/7" \
  --output   posts/sets/<date>/<slug>/slide-01.png
```

| Flag | Required | Use |
|---|---|---|
| `--tag`      | no  | Brand tag tracked caps. Default `"CTRO"`. |
| `--title`    | yes | Bold sans title. Supports `\n`. |
| `--subtitle` | no  | Italic serif subtitle. Supports `\n`. |
| `--tiles`    | no  | 4 comma-separated `NN:LABEL` pairs. Default `"01:HIRE,02:KEEP,03:GROW,04:MOVE"`. |
| `--source`   | no  | Em-dash source row. |
| `--slide`    | no  | `N/M` slide indicator. |
| `--output`   | yes | Output PNG. |

### Content CLI

```bash
python3 scripts/generate_post_image_playful_v2_content.py \
  --tile-num   "02" \
  --tile-label "Hire" \
  --tile-color coral \
  --headline   "External hiring is contracting." \
  --lead       "The career inside" \
  --bold       "is the new retention asset." \
  --source     "Mercer 2026" \
  --slide      "2/7" \
  --output     posts/sets/<date>/<slug>/slide-02.png
```

| Flag | Required | Use |
|---|---|---|
| `--tile-num`   | yes | Two-digit slide number for the ribbon (e.g. `"02"`). |
| `--tile-label` | yes | Topic word for the ribbon (e.g. `"Hire"`). |
| `--tile-color` | no  | One of `coral` / `navy` / `mustard` / `dark_coral`. Default `coral`. **Must match the cover tile color for that position.** |
| `--headline`   | yes | Bold sans navy headline. Supports `\n`. |
| `--lead`       | no  | Muted sans regular lead. Supports `\n` for action lists. |
| `--bold`       | no  | Navy sans bold payoff. |
| `--source`     | no  | Navy tracked-caps source. |
| `--slide`      | no  | `N/M` slide indicator. |
| `--output`     | yes | Output PNG. |

## Content-fit rules

Same two-part body shape as `hr-linkedin-option1`:

1. **Headline** in bold sans navy — the observation.
2. **Lead** (muted sans regular) — the bridge phrase.
3. **Payoff** (navy sans bold) — the punchline.
4. **Source** — short attribution.

### Tile color alignment

The cover's `--tiles` order locks the wayfinder ribbon color for each
content slide:

| Cover tile position | Color | Used on |
|---|---|---|
| Top-left (1st)     | coral      | Slide 2 |
| Top-right (2nd)    | navy       | Slide 3 |
| Bottom-left (3rd)  | mustard    | Slide 4 |
| Bottom-right (4th) | dark_coral | Slide 5 |

Don't reorder the colors — the carousel reads as a numbered framework,
and the visual consistency between the cover grid and the content
ribbons is the whole point.

### Action-list slide (slide 6 of 7)

Mustard ribbon (reused from the GROW tile). Drop `--bold` and pass a
multi-line `--lead`.

### Closing slide (slide 7 of 7) — dark background

Use `scripts/generate_post_image_playful_v2_dark_conclusion.py` — the
ONLY dark slide in the carousel. Navy background, cream text, mustard
"wayfinder residue" stripe across the top to bridge back to the
content slides, same lead + bold structure.

```bash
python3 scripts/generate_post_image_playful_v2_dark_conclusion.py \
  --headline "Internal mobility is not a perk." \
  --lead     "It is the cheapest, fastest" \
  --bold     "retention strategy you already own." \
  --source   "CTRO Read" \
  --slide    "7/7" \
  --output   posts/sets/<date>/<slug>/slide-07.png
```

The dark-conclusion CLI mirrors the content CLI minus the tile flags
(`--headline / --lead / --bold / --source / --slide / --output`).

## When to use

- When the user invokes `/hr-linkedin-option2`.
- When the carousel walks through an explicit 4-part framework
  ("5 things on X", "the 4-step playbook for Y") — the TOC preview +
  per-slide colored ribbon makes the structure unmistakable.
- When the user wants a more "infographic" feel than `hr-linkedin-option1`.

## When NOT to use

- When the carousel is a single argument that flows across slides
  (not 4 discrete topics) → use `hr-linkedin-option1` instead.
- When the user wants the warm magazine / pull-quote feel → use
  `vintage-editorial`.

## Sample output

See `posts/design-tests/option2-v2/` for the locked reference set.
