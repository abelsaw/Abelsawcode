#!/usr/bin/env python3
"""Option 1 v5: Combined v2 + v4 — immersed editorial pull-quote card.

Fuses v4's pull-quote framing (hairline gold frame + oversized opening
quote glyph + em-dash source attribution) with v2's two-part body
treatment (italic serif setup → thin rule → muted sans lead → bold sans
payoff). Every element has a single role, and they read top-to-bottom
as one unified arc:

  ┌─────────── frame ──────────┐
  │ 02                          │   <- slide #, gold rule
  │ ─                           │
  │                             │
  │     "                       │   <- gold opening quote glyph
  │     setup line in italic    │   <- italic serif setup (muted)
  │     serif, can be 1-3 lines │
  │     ─────────────           │   <- thin gold rule closes setup
  │                             │
  │     muted lead phrase       │   <- sans regular muted
  │     BOLD PAYOFF PHRASE      │   <- sans bold espresso
  │                             │
  │ — MERCER 2026     03 / 12   │   <- source + counter stacked
  └─────────────────────────────┘

Three earth tones:
  cream / espresso / antique gold (muted gray-brown is a tonal
  variant of espresso for the secondary text layer)

Fonts (four roles):
  - Sans tracked caps   (slide #, source, counter)
  - Display serif bold  (opening quote glyph)
  - Italic serif        (setup line)
  - Sans regular + bold (body lead + payoff)

CLI:
  --setup    Italic serif setup line. Supports \\n for forced breaks.
  --lead     Muted sans regular lead phrase below the rule. Supports \\n
             (use for the action-list slide).
  --bold     Bold sans payoff phrase below the lead.
  --source   Em-dash source line at the bottom (e.g. "Mercer 2026").
  --slide    N/M slide indicator.
  --output   Output PNG path.
"""
import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("ERROR: Pillow not installed. Run: pip install Pillow")

CANVAS = 1080

# Earth-tone palette (cream / espresso / antique gold + muted tonal)
BG = (239, 229, 208)
INK = (38, 30, 22)
GOLD = (160, 122, 64)
MUTED = (120, 102, 84)

FONT_SERIF_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
]
FONT_SERIF_ITAL = [
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
]
FONT_SANS_REG = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]
FONT_SANS_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]


def load_font(candidates, size):
    for p in candidates:
        if Path(p).is_file():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], []
    for w in words:
        if draw.textlength(" ".join(cur + [w]), font=font) <= max_w:
            cur.append(w)
        else:
            if cur:
                lines.append(" ".join(cur))
            cur = [w]
            if draw.textlength(w, font=font) > max_w:
                lines.append(w)
                cur = []
    if cur:
        lines.append(" ".join(cur))
    return lines


def wrap_multi(draw, text, font, max_w):
    out = []
    for raw in text.split("\\n"):
        raw = raw.strip()
        if not raw:
            out.append("")
            continue
        out.extend(wrap(draw, raw, font, max_w))
    return out


def tracked(text, spaces=2):
    return (" " * spaces).join(text.upper())


def parse_slide(s):
    if not s:
        return None, None
    parts = s.split("/")
    if len(parts) != 2:
        return None, None
    try:
        return int(parts[0]), int(parts[1])
    except ValueError:
        return None, None


def fit_italic(draw, text, max_w, max_h, size_hi=64, size_lo=30):
    """Honor \\n as hard breaks; shrink until every forced line fits."""
    raw_lines = [ln.strip() for ln in text.split("\\n")]
    for size in range(size_hi, size_lo - 1, -2):
        font = load_font(FONT_SERIF_ITAL, size)
        widths_ok = all(
            draw.textlength(ln, font=font) <= max_w
            for ln in raw_lines if ln
        )
        if not widths_ok:
            continue
        bbox = draw.textbbox((0, 0), "Hg", font=font)
        lh = (bbox[3] - bbox[1]) * 1.28
        total = lh * len(raw_lines)
        if total <= max_h:
            return font, raw_lines, lh
    return font, raw_lines, lh


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--setup", required=True)
    p.add_argument("--lead", default="")
    p.add_argument("--bold", default="")
    p.add_argument("--source", default="")
    p.add_argument("--slide", default="")
    p.add_argument("--output", required=True)
    args = p.parse_args()

    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    draw = ImageDraw.Draw(img)

    # --- Hairline antique-gold frame, inset 44px ---
    inset = 44
    draw.rectangle(
        [inset, inset, CANVAS - inset, CANVAS - inset],
        outline=GOLD, width=2,
    )

    pad = 96  # inside-frame padding
    content_w = CANVAS - 2 * pad

    # --- Top-left: slide number "02" + thin gold rule under it ---
    slide_num, slide_total = parse_slide(args.slide)
    top_y = pad + 6
    if slide_num is not None:
        num_font = load_font(FONT_SANS_BOLD, 26)
        num_text = f"{slide_num:02d}"
        draw.text((pad, top_y), num_text, font=num_font, fill=MUTED)
        nbbox = draw.textbbox((pad, top_y), num_text, font=num_font)
        rule_y = nbbox[3] + 12
        draw.rectangle([pad, rule_y, pad + 50, rule_y + 2], fill=GOLD)
        top_block_bottom = rule_y + 2
    else:
        top_block_bottom = top_y

    # --- Bottom rows: source above counter, stacked ---
    bottom_counter_y = CANVAS - pad - 28
    bottom_source_y = bottom_counter_y - 36

    # --- Decorative opening quote glyph (gold) hangs above the setup ---
    glyph = "“"  # left double quotation mark
    glyph_font = load_font(FONT_SERIF_BOLD, 130)
    g_bbox = draw.textbbox((0, 0), glyph, font=glyph_font)
    g_w = g_bbox[2] - g_bbox[0]
    g_h = g_bbox[3] - g_bbox[1]
    glyph_top = top_block_bottom + 70
    glyph_x = pad - g_bbox[0]  # snap left edge to pad
    glyph_y = glyph_top - g_bbox[1]
    draw.text((glyph_x, glyph_y), glyph, font=glyph_font, fill=GOLD)
    glyph_visual_bottom = glyph_top + int(g_h * 0.55)  # quote sits high in its box

    # --- Setup (italic serif, muted) sits hanging under the glyph ---
    has_body = bool(args.lead.strip() or args.bold.strip())

    # Region for setup + (rule) + body
    region_top = glyph_visual_bottom + 14
    region_bottom = bottom_source_y - 32
    region_h = region_bottom - region_top

    if has_body:
        # Setup ~ 38% of region; rule + body ~ 62%.
        setup_max_h = int(region_h * 0.40)
    else:
        setup_max_h = int(region_h * 0.65)

    setup_font, setup_lines, setup_lh = fit_italic(
        draw, args.setup, content_w, setup_max_h,
        size_hi=64 if has_body else 76,
        size_lo=30,
    )
    y = region_top
    for ln in setup_lines:
        draw.text((pad, y), ln, font=setup_font, fill=MUTED)
        y += setup_lh

    if has_body:
        # Thin gold rule closes the setup, opens the body
        rule_y = int(y + 18)
        draw.rectangle(
            [pad, rule_y, pad + content_w, rule_y + 2],
            fill=GOLD,
        )
        body_top = rule_y + 38

        # Body: lead muted regular + bold espresso
        body_parts = []
        if args.lead.strip():
            body_parts.append(("lead", args.lead.strip()))
        if args.bold.strip():
            body_parts.append(("bold", args.bold.strip()))

        body_avail_h = region_bottom - body_top
        for body_size in range(52, 24, -2):
            reg_font = load_font(FONT_SANS_REG, body_size)
            bold_font = load_font(FONT_SANS_BOLD, body_size)
            blocks = []
            ok = True
            for kind, txt in body_parts:
                f = reg_font if kind == "lead" else bold_font
                lines = wrap_multi(draw, txt, f, content_w)
                bbox = draw.textbbox((0, 0), "Hg", font=f)
                lh = (bbox[3] - bbox[1]) * 1.25
                blocks.append((kind, lines, f, lh))
                if any(draw.textlength(ln, font=f) > content_w for ln in lines):
                    ok = False
            total_h = sum(len(b[1]) * b[3] for b in blocks) + (
                12 if len(blocks) > 1 else 0
            )
            if ok and total_h <= body_avail_h:
                break

        yb = body_top
        for i, (kind, lines, f, lh) in enumerate(blocks):
            color = MUTED if kind == "lead" else INK
            for ln in lines:
                draw.text((pad, yb), ln, font=f, fill=color)
                yb += lh
            if i == 0 and len(blocks) > 1:
                yb += 12

    # --- Bottom-left: em-dash + source small-caps tracked ---
    if args.source:
        src_font = load_font(FONT_SANS_BOLD, 17)
        src_text = "—  " + tracked(args.source, 2)
        draw.text((pad, bottom_source_y), src_text, font=src_font, fill=MUTED)

    # --- Bottom-right: slide counter on its own row ---
    if slide_num is not None and slide_total is not None:
        sc_font = load_font(FONT_SANS_BOLD, 17)
        sc_text = tracked(f"{slide_num:02d} / {slide_total:02d}", 2)
        sc_w = draw.textlength(sc_text, font=sc_font)
        draw.text(
            (CANVAS - pad - sc_w, bottom_counter_y),
            sc_text,
            font=sc_font,
            fill=MUTED,
        )

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
