---
name: hr-linkedin-option4
description: Render a 7-slide LinkedIn carousel in HR Option 4 — broadsheet, a serif editorial / newspaper style. Warm off-white, near-black serif, one editorial accent (default red). Slide 1 is a masthead cover — centered tracked-caps brand rule, italic kicker + issue number, big bold serif headline, short accent rule, italic serif deck, a small serif body teaser. Slides 2-6 carry a tracked-caps section label + thin rule, a bold serif headline, an italic serif lead, and a bold serif payoff. Slide 6 is a numbered serif action list ("What CTROs are doing now"). Slide 7 is the only dark slide — an ink field with cream serif and the accent. No icons, no tiles, no photos: the type and the rules do the work. Use when the user invokes /hr-linkedin-option4 or wants a considered op-ed / thought-leadership look.
---

# hr-linkedin-option4 — broadsheet (serif editorial)

The op-ed carousel preset. Reads like a considered newspaper column, not a
designed template — the strongest "a real person wrote this" look in the set,
which is exactly what the anti-slop filter rewards. Best for POV / thought-
leadership posts.

## What it looks like

### Slide 1 (masthead cover)

```
┌──────────────────────────────────────────────────┐
│ ═══════════════════════════════════════════════  │ ← top rule
│           T H E   C T R O   R E A D              │ ← centered masthead
│ ───────────────────────────────────────────────  │ ← thin rule
│ Transformation Brief                     No. 07  │ ← italic kicker / issue no.
│                                                  │
│ The Skills-Based                                 │ ← big bold serif headline
│ Organization                                     │
│ ──                                               │ ← short accent rule
│ Why roles are giving way to                      │ ← italic serif deck
│ capabilities on the org chart.                   │
│                                                  │
│ Deloitte's 2026 read is blunt: the org chart is  │ ← small serif body teaser
│ becoming a skills graph...                       │
│ ───────────────────────────────────────────────  │
│ DELOITTE 2026                          01 / 07   │ ← source + counter
└──────────────────────────────────────────────────┘
```

### Slides 2-6 (content)

```
┌──────────────────────────────────────────────────┐
│ SIGNAL   02                                       │ ← tracked-caps section label
│ ───────────────────────────────────────────────  │ ← thin rule
│ External hiring is contracting.                  │ ← bold serif headline
│                                                  │
│ The career inside the company                    │ ← italic serif lead
│ is the new retention asset.                      │ ← bold serif payoff
│                                                  │
│ ───────────────────────────────────────────────  │
│ DELOITTE 2026                          02 / 07   │
└──────────────────────────────────────────────────┘
```

Slide 6 drops the headline/lead/bold body for a numbered serif action list
under a "What CTROs are doing now" label. Slide 7 inverts to an ink field
(cream serif, accent kicker + payoff) — the only dark slide.

## Palette

`--palette` selects the accent world. All slides in a run use the SAME value.

| Palette | Accent | Feel |
|---|---|---|
| `classic-red` (default) | editorial red `#962D23` | classic broadsheet |
| `ink-blue` | deep blue `#264A78` | cooler, corporate |
| `forest` | muted green `#346042` | calm, natural |

Base tones: warm off-white BG `#FAF7F0`, near-black serif INK `#1A1816`,
muted MUT `#786E62` for decks/leads/source.

## Fonts

- **Serif bold** (Liberation Serif Bold) — headlines, title, payoff, action numbers
- **Serif italic** (Liberation Serif Italic) — deck, lead, kicker
- **Serif regular** (Liberation Serif) — masthead, body teaser, source, counter

Deliberately serif-throughout. The newspaper voice is the point.

## Renderer

One script, every slide kind via `--kind`:

| Slide | Command |
|---|---|
| Slide 1 (cover) | `generate_post_image_broadsheet.py --kind cover` |
| Slides 2-5 (content) | `--kind content` |
| Slide 6 (action list) | `--kind action` |
| Slide 7 (dark close) | `--kind dark` |

### Cover CLI

```bash
python3 scripts/generate_post_image_broadsheet.py \
  --kind cover --palette classic-red \
  --tag      "The CTRO Read" \
  --kicker   "Transformation Brief" \
  --no       "No. 07" \
  --title    "The Skills-Based\nOrganization" \
  --subtitle "Why roles are giving way to\ncapabilities on the org chart." \
  --body     "Deloitte's 2026 read is blunt: the org chart is becoming a skills graph." \
  --source   "Deloitte 2026" \
  --slide    "1/7" \
  --output   posts/.../slide-1.png
```

### Content / action / dark CLI

```bash
# content (slides 2-5): --kicker is the section label (Signal / Evidence / ...)
python3 scripts/generate_post_image_broadsheet.py --kind content --palette classic-red \
  --kicker "Signal" --headline "External hiring is contracting." \
  --lead "The career inside the company" --bold "is the new retention asset." \
  --source "Deloitte 2026" --slide "2/7" --output posts/.../slide-2.png

# action (slide 6): multi-line --lead becomes a numbered list
python3 scripts/generate_post_image_broadsheet.py --kind action --palette classic-red \
  --kicker "What CTROs are doing now" \
  --lead "Map roles to skills, not titles.\nStand up an internal talent market.\nFund capability, not headcount." \
  --source "CTRO Read" --slide "6/7" --output posts/.../slide-6.png

# dark (slide 7): the only dark slide
python3 scripts/generate_post_image_broadsheet.py --kind dark --palette classic-red \
  --kicker "The Takeaway" --headline "Manage the skills graph." \
  --lead "The org chart is the map." --bold "The skills are the territory." \
  --source "CTRO Read" --slide "7/7" --output posts/.../slide-7.png
```

| Flag | Kinds | Use |
|---|---|---|
| `--kind`     | all | `cover` / `content` / `action` / `dark`. |
| `--palette`  | all | `classic-red` (default) / `ink-blue` / `forest`. Same on all 7 slides. |
| `--tag`      | cover | Masthead brand. Default `"The CTRO Read"`. |
| `--kicker`   | all | cover: italic dateline; content: section label; action/dark: header. |
| `--no`       | cover | Issue number, e.g. `"No. 07"`. |
| `--title`    | cover | Bold serif headline. Supports `\n`. |
| `--subtitle` | cover | Italic serif deck. Supports `\n`. |
| `--body`     | cover | Small serif body teaser. |
| `--headline` | content/dark | Bold serif observation. Supports `\n`. |
| `--lead`     | content/action/dark | Italic serif lead; multi-line on `action` = numbered list. |
| `--bold`     | content/dark | Bold serif payoff. |
| `--source`   | all | Tracked-caps source row. |
| `--slide`    | all | `N/M` counter. |
| `--output`   | all | Output PNG path. |

## When to use

- When the user invokes `/hr-linkedin-option4`.
- POV / thought-leadership posts, where a considered editorial voice beats
  data-graphic slides.
- When you want the least "designed template" look in the rotation.

## When NOT to use

- When one big number should own the slide → `hr-linkedin-option5` (stat poster).
- When the post is trend/data-heavy and wants drawn charts → `hr-linkedin-option6`
  (blueprint).
