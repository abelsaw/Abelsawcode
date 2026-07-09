---
name: hr-linkedin-option6
description: Render a 7-slide LinkedIn carousel in HR Option 6 — blueprint, a monospace analyst-brief style in Muji earth tones. Warm unbleached graph paper, walnut mono ink, one muted natural accent (clay / sage / ochre), with drawn data marks. Slide 1 cover has a "// CTRO.brief" tag, a mono title, and a drawn trend chart plotted in the accent. Slides 2-5 carry a "# finding[0N]" comment label, a mono headline, an optional drawn bar chart, a "# lead" comment line, and a bold payoff. Slide 6 is a "$ ctro --do" mono checklist ("[x] item"). Slide 7 is the only dark slide — a warm dark-walnut terminal with a "$ ctro --conclude" prompt and the accent payoff. Reads like a strategist's working deck, not a designed template. Use when the user invokes /hr-linkedin-option6 or wants a trend/data post with an analytic, charted look.
---

# hr-linkedin-option6 — blueprint (mono data brief, Muji earth tones)

The analyst-brief carousel preset. Monospace throughout on warm graph paper,
with drawn data marks (a trend line on the cover, bars on content slides).
Reads like a working deck — high credibility for trend / data posts.

## What it looks like

### Slide 1 (cover)

```
┌──────────────────────────────────────────────────┐
│ // CTRO.brief                                     │ ← accent mono tag
│ transformation_signal[07]                         │ ← muted sub-label
│ THE SKILLS-BASED                                 │ ← mono bold title
│ ORGANIZATION                                     │
│ roles --> capabilities                            │ ← muted mono subtitle
│ ┌───────────────────────────────────────────┐    │
│ │ skills-based hiring, % of roles          ／│    │ ← drawn trend chart
│ │                              ○──○──○──○  ／ │    │   (accent line + nodes)
│ │ '22                                    '27 │    │
│ └───────────────────────────────────────────┘    │
│ src: Deloitte 2026                     [01/07]   │
└──────────────────────────────────────────────────┘
```

### Slides 2-5 (content)

```
┌──────────────────────────────────────────────────┐
│ # finding[02]                                     │ ← accent comment label
│ External hiring is contracting.                  │ ← mono bold headline
│ fill source, 2026                                 │ ← optional drawn bar chart
│ ██████████████████████  internal                 │
│ █████████████  external                          │
│ # the career inside is the asset                 │ ← muted mono lead
│ retention > requisition                          │ ← bold mono payoff
│ src: Deloitte 2026                     [02/07]   │
└──────────────────────────────────────────────────┘
```

Bars are optional (`--bars`); drop them for a text-only finding. Slide 6 is a
`$ ctro --do` checklist. Slide 7 flips to a warm dark-walnut terminal with a
`$ ctro --conclude` prompt and the accent payoff — the only dark slide.

## Palette (Muji earth tones)

`--palette` selects the accent; all slides in a run use the SAME value.

| Palette | Paper | Ink | Accent |
|---|---|---|---|
| `kraft-clay` (default) | kraft `#E3DAC9` | walnut `#3A322A` | muted clay `#A66242` |
| `oat-sage` | oat `#E8E4D8` | dark olive `#34382E` | muted sage `#748866` |
| `sand-ochre` | sand `#E7DECB` | walnut `#3C3228` | muted ochre `#AC864A` |

Content slides sit on a faint graph-paper grid. The closing slide (slide 7)
is a warm dark-walnut terminal (`#282218`-ish), not a cold near-black, with a
brighter accent for the payoff.

## Fonts

- **Mono bold** (DejaVu Sans Mono Bold) — tag, title, headlines, payoff, checklist
- **Mono regular** (DejaVu Sans Mono) — sub-labels, leads, chart labels, source

Monospace throughout is the whole voice — do not substitute a proportional font.

## Renderer

One script, every slide kind via `--kind`:

| Slide | Command |
|---|---|
| Slide 1 (cover + trend) | `generate_post_image_blueprint.py --kind cover` |
| Slides 2-5 (content + bars) | `--kind content` |
| Slide 6 (checklist) | `--kind action` |
| Slide 7 (terminal close) | `--kind dark` |

### CLI

```bash
# cover: draws the trend chart from --chartlabel/--xl/--xr (fixed sample curve)
python3 scripts/generate_post_image_blueprint.py --kind cover --palette kraft-clay \
  --tag "CTRO.brief" --kicker "transformation_signal[07]" \
  --title "THE SKILLS-BASED\nORGANIZATION" --subtitle "roles --> capabilities" \
  --chartlabel "skills-based hiring, % of roles" --xl "'22" --xr "'27" \
  --source "Deloitte 2026" --slide "1/7" --output posts/.../slide-1.png

# content: --bars "name:frac,name:frac" (0..1) draws a bar mark; omit for text-only
python3 scripts/generate_post_image_blueprint.py --kind content --palette kraft-clay \
  --kicker "finding" --headline "External hiring is contracting." \
  --bars "internal:0.62,external:0.38" --chartlabel "fill source, 2026" \
  --lead "# the career inside is the asset" --bold "retention > requisition" \
  --source "Deloitte 2026" --slide "2/7" --output posts/.../slide-2.png

# action (slide 6): multi-line --lead becomes a [x] checklist
python3 scripts/generate_post_image_blueprint.py --kind action --palette kraft-clay \
  --kicker "what CTROs are doing now" \
  --lead "map roles to skills, not titles\nstand up an internal talent market\nfund capability, not headcount" \
  --source "CTRO Read" --slide "6/7" --output posts/.../slide-6.png

# dark (slide 7): terminal close
python3 scripts/generate_post_image_blueprint.py --kind dark --palette kraft-clay \
  --kicker "the takeaway" --headline "Manage the skills graph." \
  --lead "> the chart is the map" --bold "the skills are the territory" \
  --source "CTRO Read" --slide "7/7" --output posts/.../slide-7.png
```

| Flag | Kinds | Use |
|---|---|---|
| `--kind`       | all | `cover` / `content` / `action` / `dark`. |
| `--palette`    | all | `kraft-clay` (default) / `oat-sage` / `sand-ochre`. Same on all 7 slides. |
| `--tag`        | cover | Mono `// tag`. Default `"CTRO.brief"`. |
| `--kicker`     | all | cover: sub-label; content: `# finding` label; action/dark: header. |
| `--title`      | cover | Mono bold title. Supports `\n`. |
| `--subtitle`   | cover | Muted mono subtitle. |
| `--chartlabel` | cover/content | Chart caption (trend on cover, bars on content). |
| `--xl` / `--xr`| cover | Trend chart left/right axis labels (e.g. `'22` / `'27`). |
| `--headline`   | content/dark | Mono bold headline. Supports `\n`. |
| `--bars`       | content | `"name:frac,name:frac"` (0..1) drawn bar mark. Optional. |
| `--lead`       | content/action/dark | `# comment` lead; multi-line on `action` = checklist. |
| `--bold`       | content/dark | Bold mono payoff. |
| `--source`     | all | `src:` source row. |
| `--slide`      | all | `N/M` counter (rendered `[NN/MM]`). |
| `--output`     | all | Output PNG path. |

## When to use

- When the user invokes `/hr-linkedin-option6`.
- Trend / data posts where a drawn chart earns the analytic credibility.
- When you want the "strategist's working deck" feel.

## When NOT to use

- When the post is a considered argument with no data to plot →
  `hr-linkedin-option4` (broadsheet).
- When one number should own the slide → `hr-linkedin-option5` (stat poster).

## Note on chart data

The cover trend uses a fixed ascending sample curve (illustrative, not read
from real data). `--bars` values are literal fractions you pass. Only present
a chart when the underlying stat is real and sourced — never imply a data
series the brief didn't provide.
