#!/usr/bin/env python3
"""Generate a 1080x1080 head-to-head VS LinkedIn image.

Layout (top -> bottom):
  - Accent band carrying the industry tag (uppercase, white) and a small
    option label on the right.
  - Body split into two halves: company A name (big bold) on the left,
    oversized "VS" centered, company B name on the right. A one-line
    stat/descriptor sits under each name.
  - A short tagline / hook anchors the bottom, with a colored accent rule.

Accents are reused from generate_post_image.py so VS cards can sit
alongside carousel slides without color drift. Option 1 = navy, option
2 = rust, option 3 = moss.
"""
import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("ERROR: Pillow not installed. Run: pip install Pillow")

CANVAS = 1080
PADDING = 80
BAND_H = 240

BG = (250, 248, 244)
INK = (15, 15, 15)
WHITE = (255, 255, 255)
MUTED = (108, 116, 124)

ACCENTS = {
    "navy": (30, 58, 138),
    "rust": (180, 83, 9),
    "moss": (22, 101, 52),
    "plum": (107, 33, 168),
    "slate": (51, 65, 85),
}

FONT_BOLD_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
]
FONT_REG_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/Library/Fonts/Arial.ttf",
]


def load_font(candidates, size):
    for p in candidates:
        if Path(p).is_file():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def fit_text(draw, text, candidates, max_w, start=120, floor=40, step=4):
    for size in range(start, floor, -step):
        font = load_font(candidates, size)
        if draw.textlength(text, font=font) <= max_w:
            return font
    return load_font(candidates, floor)


def wrap(draw, text, font, max_width):
    words = text.split()
    lines, cur = [], []
    for w in words:
        if draw.textlength(" ".join(cur + [w]), font=font) <= max_width:
            cur.append(w)
        else:
            if cur:
                lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    return lines


def fit_wrapped(draw, text, candidates, max_w, max_h, start=56, floor=22, step=2):
    for size in range(start, floor, -step):
        font = load_font(candidates, size)
        lines = wrap(draw, text, font, max_w)
        bbox = draw.textbbox((0, 0), "Hg", font=font)
        line_h = (bbox[3] - bbox[1]) * 1.3
        if line_h * len(lines) <= max_h and len(lines) <= 4:
            return font, lines, line_h
    return font, lines, line_h


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--left", required=True, help="Left-side competitor name (e.g. 'Apple').")
    p.add_argument("--right", required=True, help="Right-side competitor name (e.g. 'Microsoft').")
    p.add_argument("--left-stat", default="", help="One-line stat or descriptor under the left name.")
    p.add_argument("--right-stat", default="", help="One-line stat or descriptor under the right name.")
    p.add_argument("--tag", required=True, help="Industry / category tag in the top band, e.g. 'Big Tech 2026'.")
    p.add_argument("--option", default="", help="Optional option label rendered top-right, e.g. 'Option 1'.")
    p.add_argument("--tagline", default="", help="Short hook line anchored at the bottom (≤80 chars).")
    p.add_argument("--accent", default="navy", choices=sorted(ACCENTS.keys()))
    p.add_argument("--output", required=True)
    args = p.parse_args()

    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    draw = ImageDraw.Draw(img)
    accent = ACCENTS[args.accent]

    # Top accent band with industry tag + option label
    draw.rectangle([0, 0, CANVAS, BAND_H], fill=accent)
    tag_font = load_font(FONT_BOLD_CANDIDATES, 36)
    draw.text((PADDING, PADDING), args.tag.upper().strip(), font=tag_font, fill=WHITE)

    if args.option:
        opt_font = load_font(FONT_BOLD_CANDIDATES, 24)
        opt_text = args.option.upper().strip()
        opt_w = draw.textlength(opt_text, font=opt_font)
        draw.text((CANVAS - PADDING - opt_w, PADDING + 8), opt_text, font=opt_font, fill=WHITE)

    # VS band geometry — render VS first so we can size the columns to its bounds.
    body_top = BAND_H + 60
    vs_center_y = body_top + 280
    vs_font = load_font(FONT_BOLD_CANDIDATES, 200)
    vs_text = "VS"
    vs_w = draw.textlength(vs_text, font=vs_font)
    vs_bbox = draw.textbbox((0, 0), vs_text, font=vs_font)
    vs_h = vs_bbox[3] - vs_bbox[1]
    vs_x = (CANVAS - vs_w) // 2
    vs_y = vs_center_y - vs_h // 2
    draw.text((vs_x, vs_y), vs_text, font=vs_font, fill=accent)

    # Columns flank the VS with a guaranteed gap on each side.
    gap = 40
    left_col_x = PADDING
    left_col_right = vs_x - gap
    right_col_x = vs_x + vs_w + gap
    right_col_right = CANVAS - PADDING
    col_w = left_col_right - left_col_x

    # Left competitor name — fit to column width
    left_font = fit_text(draw, args.left, FONT_BOLD_CANDIDATES, col_w, start=96, floor=36)
    left_bbox = draw.textbbox((0, 0), args.left, font=left_font)
    left_h = left_bbox[3] - left_bbox[1]
    left_w = draw.textlength(args.left, font=left_font)
    left_x = left_col_x + (col_w - left_w) // 2
    left_y = vs_center_y - left_h // 2 - 20
    draw.text((left_x, left_y), args.left, font=left_font, fill=INK)

    if args.left_stat:
        ls_font, ls_lines, ls_lh = fit_wrapped(
            draw, args.left_stat, FONT_REG_CANDIDATES, col_w, 120, start=30, floor=18
        )
        sy = left_y + left_h + 24
        for ln in ls_lines:
            lw = draw.textlength(ln, font=ls_font)
            draw.text((left_col_x + (col_w - lw) // 2, sy), ln, font=ls_font, fill=MUTED)
            sy += ls_lh

    # Right competitor name
    right_col_w = right_col_right - right_col_x
    right_font = fit_text(draw, args.right, FONT_BOLD_CANDIDATES, right_col_w, start=96, floor=36)
    right_bbox = draw.textbbox((0, 0), args.right, font=right_font)
    right_h = right_bbox[3] - right_bbox[1]
    right_w = draw.textlength(args.right, font=right_font)
    right_x = right_col_x + (right_col_w - right_w) // 2
    right_y = vs_center_y - right_h // 2 - 20
    draw.text((right_x, right_y), args.right, font=right_font, fill=INK)

    if args.right_stat:
        rs_font, rs_lines, rs_lh = fit_wrapped(
            draw, args.right_stat, FONT_REG_CANDIDATES, right_col_w, 120, start=30, floor=18
        )
        sy = right_y + right_h + 24
        for ln in rs_lines:
            lw = draw.textlength(ln, font=rs_font)
            draw.text((right_col_x + (right_col_w - lw) // 2, sy), ln, font=rs_font, fill=MUTED)
            sy += rs_lh

    # Bottom accent rule + tagline
    rule_y = CANVAS - PADDING - 110
    draw.rectangle([PADDING, rule_y, PADDING + 140, rule_y + 5], fill=accent)

    if args.tagline:
        tg_font, tg_lines, tg_lh = fit_wrapped(
            draw,
            args.tagline,
            FONT_BOLD_CANDIDATES,
            CANVAS - 2 * PADDING,
            90,
            start=44,
            floor=24,
        )
        ty = rule_y + 28
        for ln in tg_lines:
            draw.text((PADDING, ty), ln, font=tg_font, fill=INK)
            ty += tg_lh

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({CANVAS}x{CANVAS}, accent={args.accent}, {args.left} vs {args.right})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
