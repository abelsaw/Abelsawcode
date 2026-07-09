---
name: hr-linkedin-option5
description: Render a 7-slide LinkedIn carousel in HR Option 5 — stat poster, a brutalist Swiss type style in Muji earth tones. Warm unbleached paper, walnut ink, one muted natural accent (clay / sage / ochre). Slide 1 cover leads with ONE giant stat (e.g. "1 in 3") in the accent, a bold statement, a thick accent rule, brand tag + kicker. Slides 2-5 each front an oversized accent number/stat with a bold statement and a payoff line; one slide can drop the stat for rhythm. Slide 6 is a big numbered action list ("What CTROs are doing now"). Slide 7 flips to a deep-walnut field (the only tonal flip) with the accent kicker + payoff. Type is the graphic — oversized numbers, minimal chrome. Use when the user invokes /hr-linkedin-option5 or wants a single-stat post with maximum scroll-stop.
---

# hr-linkedin-option5 — stat poster (brutalist, Muji earth tones)

The single-stat carousel preset. One oversized number owns each slide; the
type is the graphic. Muji earth tones keep it calm and tactile rather than
loud. Best when a post rests on one dominant statistic.

## What it looks like

### Slide 1 (cover)

```
┌──────────────────────────────────────────────────┐
│ C T R O                                           │ ← brand tag + accent stub
│ ──                                                │
│ THE STAT THAT REFRAMES 2026                       │ ← muted kicker
│                                                  │
│ 1 in 3                                           │ ← GIANT accent stat
│                                                  │
│ roles will be defined by                         │ ← bold walnut statement
│ skills, not titles, by 2027.                     │
│ ████████████████████████████████████████████████ │ ← thick accent rule
│ DELOITTE 2026                          01 / 07   │
└──────────────────────────────────────────────────┘
```

### Slides 2-5 (content)

```
┌──────────────────────────────────────────────────┐
│ 02                                                │ ← muted slide #
│ 46%                                              │ ← oversized accent stat
│ of external hiring is                            │ ← bold walnut statement
│ now filled internally.                           │
│ The career inside is the asset.                  │ ← accent payoff line
│ DELOITTE 2026                          02 / 07   │
└──────────────────────────────────────────────────┘
```

`--stat` is optional on content slides — drop it on one slide for rhythm and
let the headline carry it. Slide 6 is a big numbered action list. Slide 7
flips to a deep-walnut field with the accent kicker, cream/paper headline,
and the accent payoff.

## Palette (Muji earth tones)

`--palette` selects the accent; all slides in a run use the SAME value.

| Palette | Paper | Ink | Accent |
|---|---|---|---|
| `kraft-clay` (default) | kraft `#E2D8C6` | walnut `#3C342B` | muted clay `#A86042` |
| `oat-sage` | oat `#E9E5D9` | dark olive `#38382E` | muted sage `#768A6C` |
| `sand-ochre` | sand `#E7DDC9` | walnut `#3E3428` | muted ochre `#AC864A` |

The closing slide (slide 7) flips to the walnut ink color as its field, with
paper-colored text and the accent — a calm tonal shift, not a bright pop.

## Fonts

- **Sans bold** (DejaVu Sans Bold) throughout — the oversized numbers and
  statements are the design. No serif, no mono.

## Renderer

One script, every slide kind via `--kind`:

| Slide | Command |
|---|---|
| Slide 1 (cover) | `generate_post_image_poster.py --kind cover` |
| Slides 2-5 (content) | `--kind content` |
| Slide 6 (action list) | `--kind action` |
| Slide 7 (walnut close) | `--kind dark` |

### CLI

```bash
# cover: --stat is the giant number; --subtitle is the statement
python3 scripts/generate_post_image_poster.py --kind cover --palette kraft-clay \
  --tag "CTRO" --kicker "The stat that reframes 2026" \
  --stat "1 in 3" --subtitle "roles will be defined by\nskills, not titles, by 2027." \
  --source "Deloitte 2026" --slide "1/7" --output posts/.../slide-1.png

# content: --stat optional big number, --headline statement, --bold payoff
python3 scripts/generate_post_image_poster.py --kind content --palette kraft-clay \
  --stat "46%" --headline "of external hiring is\nnow filled internally." \
  --bold "The career inside is the asset." \
  --source "Deloitte 2026" --slide "2/7" --output posts/.../slide-2.png

# action (slide 6): multi-line --lead becomes a big numbered list
python3 scripts/generate_post_image_poster.py --kind action --palette kraft-clay \
  --kicker "What CTROs are doing now" \
  --lead "Map roles to skills.\nBuild an internal talent market.\nFund capability, not headcount." \
  --source "CTRO Read" --slide "6/7" --output posts/.../slide-6.png

# dark (slide 7): walnut-field close
python3 scripts/generate_post_image_poster.py --kind dark --palette kraft-clay \
  --kicker "The takeaway" --headline "Fund the skills." \
  --bold "Not the boxes on the chart." \
  --source "CTRO Read" --slide "7/7" --output posts/.../slide-7.png
```

| Flag | Kinds | Use |
|---|---|---|
| `--kind`     | all | `cover` / `content` / `action` / `dark`. |
| `--palette`  | all | `kraft-clay` (default) / `oat-sage` / `sand-ochre`. Same on all 7 slides. |
| `--tag`      | cover | Brand tag. Default `"CTRO"`. |
| `--kicker`   | cover/action/dark | cover: label above the stat; action/dark: header. |
| `--stat`     | cover/content | The oversized number (e.g. `"1 in 3"`, `"46%"`, `"2x"`). Optional on content. |
| `--subtitle` | cover | Bold statement under the cover stat. Supports `\n`. |
| `--headline` | content/dark | Bold statement. Supports `\n`. |
| `--bold`     | content/dark | Accent payoff line. |
| `--lead`     | action | Multi-line action items (numbered). |
| `--source`   | all | Tracked-caps source. |
| `--slide`    | all | `N/M` counter. |
| `--output`   | all | Output PNG path. |

## When to use

- When the user invokes `/hr-linkedin-option5`.
- Single-stat posts — one dominant number the reader will screenshot.
- When you want the highest scroll-stop cover in the rotation.

## When NOT to use

- When the post is an argument that flows across slides rather than a stack of
  stats → `hr-linkedin-option4` (broadsheet).
- When the story is a trend and wants drawn charts → `hr-linkedin-option6`
  (blueprint).
