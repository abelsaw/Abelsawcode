#!/usr/bin/env python3
"""Generate a bold editorial 1080x1080 LinkedIn carousel slide.

Style: top color band carrying the topic tag (white) and an oversized
slide number (white), with a generous cream body area below holding a
big sans-serif headline. A short accent rule anchors the bottom.

This is the locked default style for the daily best-practices flow —
chosen for scroll-stopping presence in the LinkedIn feed and strong
visual hierarchy across a 5-slide swipe.
"""
import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("ERROR: Pillow not installed. Run: pip install Pillow")

CANVAS = 1080
PADDING = 96
BAND_H = 360

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
            if draw.textlength(w, font=font) > max_width:
                lines.append(w)
                cur = []
    if cur:
        lines.append(" ".join(cur))
    return lines


def fit_headline(draw, text, max_w, max_h):
    for size in range(124, 44, -4):
        font = load_font(FONT_BOLD_CANDIDATES, size)
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
    p.add_argument("--headline", required=True, help="The main line of type. Auto-wraps and auto-sizes.")
    p.add_argument("--tag", default="HR INSIGHTS", help="Topic tag, rendered uppercase in the top band.")
    p.add_argument("--accent", default="navy", choices=sorted(ACCENTS.keys()))
    p.add_argument("--slide", default="", help="Optional slide indicator like '1/5'. Renders as a large white number in the band.")
    p.add_argument("--footer", default="", help="Optional small text bottom-left in the body area.")
    p.add_argument("--output", required=True)
    args = p.parse_args()

    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    draw = ImageDraw.Draw(img)
    accent = ACCENTS[args.accent]

    draw.rectangle([0, 0, CANVAS, BAND_H], fill=accent)

    tag_font = load_font(FONT_BOLD_CANDIDATES, 32)
    draw.text((PADDING, PADDING), args.tag.upper().strip(), font=tag_font, fill=WHITE)

    slide_num, slide_total = parse_slide(args.slide)
    if slide_num is not None and slide_total is not None:
        sn_font = load_font(FONT_BOLD_CANDIDATES, 220)
        sn_text = f"{slide_num:02d}"
        sn_w = draw.textlength(sn_text, font=sn_font)
        sn_bbox = draw.textbbox((0, 0), sn_text, font=sn_font)
        sn_h = sn_bbox[3] - sn_bbox[1]
        draw.text(
            (CANVAS - PADDING - sn_w, (BAND_H - sn_h) // 2 - 40),
            sn_text,
            font=sn_font,
            fill=WHITE,
        )
        of_font = load_font(FONT_BOLD_CANDIDATES, 22)
        of_text = f"OF {slide_total:02d}"
        of_w = draw.textlength(of_text, font=of_font)
        draw.text(
            (CANVAS - PADDING - of_w, BAND_H - 64),
            of_text,
            font=of_font,
            fill=WHITE,
        )

    head_top = BAND_H + 80
    footer_h = 60 if args.footer else 40
    max_w = CANVAS - 2 * PADDING
    max_h = CANVAS - head_top - PADDING - footer_h

    font, lines, line_h = fit_headline(draw, args.headline, max_w, max_h)
    y = head_top
    for ln in lines:
        draw.text((PADDING, y), ln, font=font, fill=INK)
        y += line_h

    draw.rectangle(
        [PADDING, CANVAS - PADDING - 5, PADDING + 140, CANVAS - PADDING],
        fill=accent,
    )

    if args.footer:
        f_font = load_font(FONT_REG_CANDIDATES, 22)
        draw.text(
            (PADDING + 160, CANVAS - PADDING - 14),
            args.footer,
            font=f_font,
            fill=MUTED,
        )

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({CANVAS}x{CANVAS}, accent={args.accent})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
