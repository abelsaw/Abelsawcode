#!/usr/bin/env python3
"""Option 1: Simple vintage. Three colours (cream / espresso / terracotta).

No icons, no frame, no diamond ornaments. Restrained editorial typography:
- Tag at top-left in italic serif, letter-spaced.
- A single thin terracotta rule under the tag.
- Large serif headline, left-aligned, generous whitespace.
- Slide indicator at bottom-right in italic serif, terracotta.
- Mirror rule at bottom-left.

Same CLI as the other generators: --headline, --tag, --slide N/M, --output.
"""
import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("ERROR: Pillow not installed. Run: pip install Pillow")

CANVAS = 1080

# Three earth tones only
BG = (239, 229, 208)         # cream / warm oat
INK = (46, 36, 24)            # espresso brown
ACCENT = (181, 102, 60)       # muted terracotta

FONT_SERIF_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
]
FONT_SERIF_ITAL = [
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
]
FONT_SERIF_REG = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
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


def fit_headline(draw, text, max_w, max_h):
    for size in range(108, 36, -3):
        font = load_font(FONT_SERIF_BOLD, size)
        lines = wrap(draw, text, font, max_w)
        bbox = draw.textbbox((0, 0), "Hg", font=font)
        line_h = (bbox[3] - bbox[1]) * 1.25
        total_h = line_h * len(lines)
        widths_ok = all(draw.textlength(ln, font=font) <= max_w for ln in lines)
        if total_h <= max_h and widths_ok and len(lines) <= 6:
            return font, lines, line_h
    return font, lines, line_h


def parse_slide(slide_arg):
    if not slide_arg:
        return None, None
    parts = slide_arg.split("/")
    if len(parts) != 2:
        return None, None
    try:
        return int(parts[0]), int(parts[1])
    except ValueError:
        return None, None


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--headline", required=True)
    p.add_argument("--tag", default="HR INSIGHTS")
    p.add_argument("--slide", default="")
    p.add_argument("--output", required=True)
    args = p.parse_args()

    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    draw = ImageDraw.Draw(img)

    pad = 110

    # Tag at top-left, italic serif, letter-spaced caps
    tag_font = load_font(FONT_SERIF_ITAL, 28)
    tag_text = "    ".join(args.tag.upper())
    draw.text((pad, pad), tag_text, font=tag_font, fill=INK)
    tag_bbox = draw.textbbox((pad, pad), tag_text, font=tag_font)

    # Thin terracotta rule under tag
    rule_y = tag_bbox[3] + 28
    draw.rectangle([pad, rule_y, pad + 90, rule_y + 2], fill=ACCENT)

    # Headline area
    head_top = rule_y + 110
    bottom_zone = 130
    max_w = CANVAS - 2 * pad
    max_h = CANVAS - head_top - pad - bottom_zone
    font, lines, line_h = fit_headline(draw, args.headline, max_w, max_h)
    y = head_top
    for ln in lines:
        draw.text((pad, y), ln, font=font, fill=INK)
        y += line_h

    # Mirror rule at bottom-left
    bottom_rule_y = CANVAS - pad - 40
    draw.rectangle([pad, bottom_rule_y, pad + 90, bottom_rule_y + 2], fill=ACCENT)

    # Slide indicator at bottom-right in italic serif
    slide_num, slide_total = parse_slide(args.slide)
    if slide_num is not None and slide_total is not None:
        si_font = load_font(FONT_SERIF_ITAL, 24)
        si_text = f"No. {slide_num:02d}  /  {slide_total:02d}"
        si_w = draw.textlength(si_text, font=si_font)
        draw.text(
            (CANVAS - pad - si_w, bottom_rule_y - 22),
            si_text,
            font=si_font,
            fill=ACCENT,
        )

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
