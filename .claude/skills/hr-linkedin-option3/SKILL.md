---
name: hr-linkedin-option3
description: Render a 7-slide LinkedIn carousel in HR Option 3 — photo-driven cover with palette-matched word slides. The user supplies a photo; it fills the top 600px of slide 1 (center-cropped) with a thin tan accent stripe separator and a warm cream typography band carrying brand tag, bold sans charcoal title, italic serif subtitle. Slides 2-6 drop the photo and carry its mood through a sampled palette (cream / charcoal / tan / muted gray-tan) — large tan slide # with thin charcoal rule, sans bold charcoal headline, two-part body (muted regular lead + charcoal bold payoff). Slide 7 is the closing on a charcoal dark background — the only dark slide — same body structure inverted (cream text on charcoal with tan slide #). Use when the user invokes /hr-linkedin-option3 or wants a photo-driven LinkedIn carousel.
---

# hr-linkedin-option3 — photo-driven cover, palette-matched content

The photo-driven carousel preset. The user supplies one image; that
image anchors slide 1 and its sampled palette carries the visual mood
through the rest of the carousel.

## What it looks like

### Slide 1 (photo cover)

```
┌──────────────────────────────────────────────────┐
│                                                  │
│                                                  │
│            [USER PHOTO — top 600px]              │ ← center-cropped to
│            (1080 wide × 600 tall)                │   1080×600 cover area
│                                                  │
│                                                  │
│                                                  │
├──────────────────────────────────────────────────┤ ← tan accent stripe (6px)
│                                                  │
│ CHRO                                  │ ← brand tag tracked caps
│ ──                                                │   + tan mini-stripe
│                                                  │
│ Internal                                         │ ← bold sans charcoal title
│ Mobility                                         │   (1-2 lines auto-fit)
│ The retention asset you already own.             │ ← italic serif subtitle
│                                                  │   (muted)
│ — MERCER GLOBAL TALENT TRENDS 2026               │ ← em-dash source
│                                       01 / 05    │ ← counter (stacked)
└──────────────────────────────────────────────────┘
```

### Slides 2-6 (content, photo-free)

```
┌──────────────────────────────────────────────────┐
│ 02                                                │ ← large tan slide #
│ ───                                               │ ← thin charcoal rule
│                                                  │
│ External hiring is                               │ ← bold sans charcoal
│ contracting.                                     │   headline
│                                                  │
│ The career inside                                │ ← muted sans regular lead
│ is the new retention asset.                      │ ← charcoal sans bold payoff
│                                                  │
│ MERCER 2026                          02 / 05     │ ← charcoal source +
└──────────────────────────────────────────────────┘   muted counter
```

## Palette

The default palette is sampled from a warm collaborative office photo.
For a photo with a different dominant mood, the palette should be
re-sampled (see "When the photo's mood is cool / cold" below).

- `BG` warm cream — `(235, 225, 208)` — `#EBE1D0`
- `INK` deep charcoal — `(42, 42, 51)` — `#2A2A33` (title, headline, payoff)
- `TAN` warm tan — `(181, 143, 96)` — `#B58F60` (accent stripes, slide #)
- `MUTED` warm gray-tan — `(138, 123, 102)` — `#8A7B66` (subtitle, lead, counter)

## Fonts

- **Sans bold** (DejaVu Sans Bold) — title, headline, slide #, payoff, source, counter
- **Sans regular** (DejaVu Sans) — body lead (muted)
- **Italic serif** (Liberation Serif Italic) — cover subtitle only

## Renderers

| Slide | Script |
|---|---|
| Slide 1 (photo cover) | `scripts/generate_post_image_photo_cover.py` |
| Slides 2-6 (content) | `scripts/generate_post_image_photo_content.py` |
| Slide 7 (dark conclusion) | `scripts/generate_post_image_photo_dark_conclusion.py` |

### Cover CLI

```bash
python3 scripts/generate_post_image_photo_cover.py \
  --photo    path/to/photo.jpg \
  --tag      "CHRO" \
  --title    "Internal\nMobility" \
  --subtitle "The retention asset you already own." \
  --source   "Mercer Global Talent Trends 2026" \
  --slide    "1/7" \
  --output   posts/sets/<date>/<slug>/slide-01.png
```

| Flag | Required | Use |
|---|---|---|
| `--photo`    | yes | Path to the background photo (jpg/png). Any aspect — will be center-cropped to 1080×600. |
| `--tag`      | no  | Brand tag tracked caps. Default `"CHRO"`. |
| `--title`    | yes | Bold sans title. Supports `\n` for forced breaks. |
| `--subtitle` | no  | Italic serif subtitle. Supports `\n`. |
| `--source`   | no  | Em-dash + tracked small-caps source row. |
| `--slide`    | no  | `N/M` slide indicator. |
| `--output`   | yes | Output PNG path. |

### Content CLI

```bash
python3 scripts/generate_post_image_photo_content.py \
  --headline "External hiring is contracting." \
  --lead     "The career inside" \
  --bold     "is the new retention asset." \
  --source   "Mercer 2026" \
  --slide    "2/7" \
  --output   posts/sets/<date>/<slug>/slide-02.png
```

| Flag | Required | Use |
|---|---|---|
| `--headline` | yes | Bold sans charcoal headline. Supports `\n`. |
| `--lead`     | no  | Muted sans regular lead. Supports `\n` for action lists. |
| `--bold`     | no  | Charcoal sans bold payoff. |
| `--source`   | no  | Charcoal tracked-caps source. |
| `--slide`    | no  | `N/M` slide indicator. |
| `--output`   | yes | Output PNG path. |

## Content-fit rules

Same two-part body shape as `hr-linkedin-option1` and `hr-linkedin-option2`:

1. **Title / Headline** — observation in bold sans charcoal.
2. **Lead** (muted sans regular) — bridge phrase.
3. **Payoff** (charcoal sans bold) — completes the lead.
4. **Source** — short attribution.

### Action-list slide (slide 6 of 7)

Drop `--bold` and pass a multi-line `--lead`.

### Closing slide (slide 7 of 7) — dark background

Use `scripts/generate_post_image_photo_dark_conclusion.py` — the ONLY
dark slide in the carousel. Charcoal background, cream text, large tan
slide # with thin cream rule, same lead + bold body structure.

```bash
python3 scripts/generate_post_image_photo_dark_conclusion.py \
  --headline "Internal mobility is not a perk." \
  --lead     "It is the cheapest, fastest" \
  --bold     "retention strategy you already own." \
  --source   "CHRO Read" \
  --slide    "7/7" \
  --output   posts/sets/<date>/<slug>/slide-07.png
```

CLI mirrors the content CLI minus the photo (`--headline / --lead /
--bold / --source / --slide / --output`).

## Photo guidance

What works best as the cover photo:

- **Subject + space:** a photo with people/action AND a quiet area, so
  the typography below has room to breathe.
- **Warm tones** for the default palette to feel native. For a cool
  photo (ocean, snow, blue interior), re-sample the palette (see below).
- **Wide aspect** (16:9, 4:3, or 3:2). Square is fine — minimal crop.
- **High enough resolution** that 1080×600 cover-crop stays sharp
  (≥1200px on the long edge).

### When the photo's mood is cool / cold

The default palette is tuned to warm photos. For cool photos, override
the constants at the top of both scripts:

```python
# Cool palette example:
BG    = (228, 230, 235)   # cool off-white
INK   = (28, 38, 52)      # deep navy-charcoal
TAN   = (88, 130, 152)    # muted steel blue (replaces tan)
MUTED = (118, 132, 148)   # cool gray-blue
```

Re-sample using a tool like ColorThief or by inspecting the photo's
top dominant clusters; tune `TAN` and `MUTED` to track the photo, keep
`BG` near-cream/off-white and `INK` near-charcoal for readability.

## When to use

- When the user invokes `/hr-linkedin-option3`.
- When the post benefits from a single hero image on the cover
  (case stories, people / culture posts, leadership moments).
- When the user wants the carousel to feel rooted in a specific moment
  or scene rather than abstract typography.

## When NOT to use

- When the post is data-heavy and every slide needs a strong visual
  hook → use `hr-linkedin-option1` (chip icons) or `hr-linkedin-option2`
  (TOC tiles) for that "structured framework" feel.
- When no good photo is available — option3 falls apart without a
  cover image worth the slide.

## Sample output

See `posts/design-tests/option3-v1/` for the locked reference set
(including the source photo at `source-photo.jpeg`).
