#!/usr/bin/env python3
"""playful-iconic v4 cover — dominant accent shape.

A modern-minimalist cover anchored by ONE large coral quarter-circle in
the upper-right corner. The title sits below/left of it in bold sans
navy, with an italic serif subtitle and three small rhythm dots in the
palette colors at the bottom.

Palette: cream / navy / coral / mustard.
"""
import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("ERROR: Pillow not installed.")

CANVAS = 1080
BG = (244, 235, 220)
NAVY = (27, 49, 71)
CORAL = (226, 106, 75)
MUSTARD = (212, 154, 56)
MUTED = (108, 95, 80)

FONT_SANS_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]
FONT_SERIF_ITAL = [
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
]


def load_font(cands, size):
    for p in cands:
        if Path(p).is_file():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


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


def fit_lines_bold(draw, text, max_w, max_h, size_hi=130, size_lo=54, step=2):
    raw_lines = [ln.strip() for ln in text.split("\\n")]
    for size in range(size_hi, size_lo - 1, -step):
        font = load_font(FONT_SANS_BOLD, size)
        if not all(draw.textlength(ln, font=font) <= max_w for ln in raw_lines if ln):
            continue
        bbox = draw.textbbox((0, 0), "Hg", font=font)
        lh = (bbox[3] - bbox[1]) * 1.14
        if lh * len(raw_lines) <= max_h:
            return font, raw_lines, lh
    return font, raw_lines, lh


def fit_lines_ital(draw, text, max_w, max_h, size_hi=38, size_lo=20):
    raw_lines = [ln.strip() for ln in text.split("\\n")]
    for size in range(size_hi, size_lo - 1, -2):
        font = load_font(FONT_SERIF_ITAL, size)
        if not all(draw.textlength(ln, font=font) <= max_w for ln in raw_lines if ln):
            continue
        bbox = draw.textbbox((0, 0), "Hg", font=font)
        lh = (bbox[3] - bbox[1]) * 1.3
        if lh * len(raw_lines) <= max_h:
            return font, raw_lines, lh
    return font, raw_lines, lh


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tag", default="CTRO")
    p.add_argument("--title", required=True)
    p.add_argument("--subtitle", default="")
    p.add_argument("--source", default="")
    p.add_argument("--slide", default="")
    p.add_argument("--output", required=True)
    args = p.parse_args()

    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    draw = ImageDraw.Draw(img)

    # --- Dominant coral quarter-circle anchored top-right ---
    R = 560
    draw.ellipse(
        [CANVAS - R, -R, CANVAS + R, R],
        fill=CORAL,
    )
    # Small mustard quarter-circle nested inside as a depth accent
    R2 = 200
    draw.ellipse(
        [CANVAS - R2, -R2, CANVAS + R2, R2],
        fill=MUSTARD,
    )

    pad = 92
    content_w = CANVAS - 2 * pad

    # --- Brand tag tracked caps top-left (navy on cream) ---
    tag_font = load_font(FONT_SANS_BOLD, 20)
    tag_text = tracked(args.tag, 2)
    draw.text((pad, pad), tag_text, font=tag_font, fill=NAVY)
    tbbox = draw.textbbox((pad, pad), tag_text, font=tag_font)
    # Coral stripe replaced by the giant shape above — use a thin navy rule here
    stripe_y = tbbox[3] + 14
    draw.rectangle([pad, stripe_y, pad + 60, stripe_y + 3], fill=NAVY)
    top_block_end = stripe_y + 3

    # Bottom rows
    bottom_counter_y = CANVAS - pad - 26
    bottom_source_y = bottom_counter_y - 32

    # --- Title sits in the lower-half left area, below the coral shape ---
    # The shape ends roughly at y = R, so title can start at ~y=R+60
    title_top = max(top_block_end + 280, R + 40)
    title_max_h = bottom_source_y - title_top - 220

    title_font, title_lines, title_lh = fit_lines_bold(
        draw, args.title, content_w, title_max_h,
        size_hi=130, size_lo=54,
    )
    y = title_top
    for ln in title_lines:
        draw.text((pad, y), ln, font=title_font, fill=NAVY)
        y += title_lh
    title_bottom = y

    # Mustard short rule under title (anchor)
    rule_y = int(title_bottom + 18)
    draw.rectangle([pad, rule_y, pad + 110, rule_y + 5], fill=MUSTARD)
    rule_bottom = rule_y + 5

    # Subtitle italic serif muted
    if args.subtitle.strip():
        sub_max_h = bottom_source_y - rule_bottom - 120
        sub_font, sub_lines, sub_lh = fit_lines_ital(
            draw, args.subtitle, content_w, sub_max_h,
            size_hi=36, size_lo=22,
        )
        ys = rule_bottom + 30
        for ln in sub_lines:
            draw.text((pad, ys), ln, font=sub_font, fill=MUTED)
            ys += sub_lh

    # Decorative rhythm dots at the bottom-left (3 small palette dots)
    dot_r = 16
    dot_y = bottom_source_y - 38
    dot_gap = 50
    for i, col in enumerate([NAVY, MUSTARD, CORAL]):
        dx = pad + i * dot_gap
        draw.ellipse([dx, dot_y, dx + dot_r * 2, dot_y + dot_r * 2], fill=col)

    # Source + counter
    bottom_font = load_font(FONT_SANS_BOLD, 17)
    if args.source:
        src_text = "—  " + tracked(args.source, 2)
        draw.text((pad + 180, bottom_source_y), src_text,
                  font=bottom_font, fill=MUTED)
    sn, st = parse_slide(args.slide)
    if sn is not None and st is not None:
        sc_text = tracked(f"{sn:02d} / {st:02d}", 2)
        sc_w = draw.textlength(sc_text, font=bottom_font)
        draw.text((CANVAS - pad - sc_w, bottom_counter_y),
                  sc_text, font=bottom_font, fill=MUTED)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
