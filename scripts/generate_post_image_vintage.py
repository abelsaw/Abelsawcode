#!/usr/bin/env python3
"""Generate a 1080x1080 LinkedIn carousel slide in vintage editorial style.

Warm parchment background, sepia/brown ink, serif typography, restrained
decorative ornaments. Inspired by classic financial-document and editorial
infographic aesthetics — feels considered and editorial rather than
modern-bold. Single accent color (no rotation) lets the carousel read as
one coherent piece.

Same CLI as the bold-editorial generator: --headline, --tag, --accent,
--slide N/M, --output. Accent values are warm tones that all harmonize
with the cream background.
"""
import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("ERROR: Pillow not installed. Run: pip install Pillow")

CANVAS = 1080

# Warm vintage palette
BG = (245, 237, 216)         # parchment / warm cream
INK = (42, 31, 21)           # very dark brown (near black)
MUTED = (122, 107, 90)       # warm slate brown
BORDER = (170, 138, 100)     # tan border

ACCENTS = {
    "sepia": (139, 100, 56),
    "rust":  (160, 82, 45),
    "olive": (110, 99, 53),
    "navy":  (60, 73, 90),
    "brown": (101, 67, 33),
}

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
        trial = " ".join(cur + [w])
        if draw.textlength(trial, font=font) <= max_w:
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
    for size in range(108, 36, -4):
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


def draw_diamond(draw, cx, cy, size, fill):
    draw.polygon([(cx, cy - size), (cx + size, cy), (cx, cy + size), (cx - size, cy)], fill=fill)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--headline", required=True)
    p.add_argument("--tag", default="HR INSIGHTS")
    p.add_argument("--accent", default="sepia", choices=sorted(ACCENTS.keys()))
    p.add_argument("--slide", default="")
    p.add_argument("--output", required=True)
    args = p.parse_args()

    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    draw = ImageDraw.Draw(img)
    accent = ACCENTS[args.accent]

    # Outer decorative frame (double-rule)
    frame_outer = 30
    frame_inner = 42
    draw.rectangle(
        [frame_outer, frame_outer, CANVAS - frame_outer, CANVAS - frame_outer],
        outline=BORDER, width=2,
    )
    draw.rectangle(
        [frame_inner, frame_inner, CANVAS - frame_inner, CANVAS - frame_inner],
        outline=BORDER, width=1,
    )

    content_pad = 96

    # Top: tag in italic serif, all-caps, letter-spaced feel
    tag_font = load_font(FONT_SERIF_ITAL, 28)
    tag_text = args.tag.upper()
    # Add spaces between chars for letter-spacing
    spaced_tag = "  ".join(tag_text)
    draw.text((content_pad, content_pad), spaced_tag, font=tag_font, fill=MUTED)
    tag_bbox = draw.textbbox((content_pad, content_pad), spaced_tag, font=tag_font)

    # Decorative rule + diamond ornament below tag
    rule_y = tag_bbox[3] + 30
    rule_left = content_pad
    rule_right = content_pad + 100
    draw.rectangle([rule_left, rule_y, rule_right, rule_y + 3], fill=accent)
    # Diamond ornament after the rule
    draw_diamond(draw, rule_right + 18, rule_y + 1, 6, accent)
    draw.rectangle([rule_right + 30, rule_y, rule_right + 60, rule_y + 3], fill=accent)

    # Headline area
    head_top = rule_y + 90
    footer_zone = 110
    max_w = CANVAS - 2 * content_pad
    max_h = CANVAS - head_top - content_pad - footer_zone

    font, lines, line_h = fit_headline(draw, args.headline, max_w, max_h)
    y = head_top
    for ln in lines:
        draw.text((content_pad, y), ln, font=font, fill=INK)
        y += line_h

    # Bottom decorative line + diamond + slide indicator
    bottom_zone_y = CANVAS - content_pad - 30
    # Decorative bar bottom-left
    draw.rectangle([content_pad, bottom_zone_y, content_pad + 80, bottom_zone_y + 3], fill=accent)
    draw_diamond(draw, content_pad + 98, bottom_zone_y + 1, 5, accent)

    # Slide indicator bottom-right (serif bold, ornament-framed)
    slide_num, slide_total = parse_slide(args.slide)
    if slide_num is not None and slide_total is not None:
        si_font = load_font(FONT_SERIF_BOLD, 22)
        si_text = f"{slide_num:02d}  ·  {slide_total:02d}"
        si_w = draw.textlength(si_text, font=si_font)
        right = CANVAS - content_pad
        draw.text((right - si_w, bottom_zone_y - 10), si_text, font=si_font, fill=accent)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
