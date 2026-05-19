#!/usr/bin/env python3
"""Generate a minimalist 1080x1080 LinkedIn post image.

Style: off-white background, small uppercase category tag, short accent
bar, then a single bold headline that auto-fits the canvas. Designed
for HR best-practices posts — no stock photos, no decoration, just
type. Outputs PNG (the format LinkedIn accepts for image attachments).
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

BG = (250, 250, 247)        # warm off-white
INK = (15, 23, 42)          # near-black navy
MUTED = (100, 116, 139)     # slate

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
    "/System/Library/Fonts/Helvetica.ttc",
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
        trial = " ".join(cur + [w])
        if draw.textlength(trial, font=font) <= max_width:
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
    for size in range(112, 40, -4):
        font = load_font(FONT_BOLD_CANDIDATES, size)
        lines = wrap(draw, text, font, max_w)
        bbox = draw.textbbox((0, 0), "Hg", font=font)
        line_h = (bbox[3] - bbox[1]) * 1.2
        total_h = line_h * len(lines)
        widths_ok = all(draw.textlength(ln, font=font) <= max_w for ln in lines)
        if total_h <= max_h and widths_ok and len(lines) <= 6:
            return font, lines, line_h
    return font, lines, line_h


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--headline", required=True, help="The main line of type. Will auto-wrap and auto-size.")
    p.add_argument("--tag", default="HR INSIGHTS", help="Small uppercase tag at the top.")
    p.add_argument("--accent", default="navy", choices=sorted(ACCENTS.keys()))
    p.add_argument("--footer", default="", help="Optional small text bottom-right (e.g. a brand mark).")
    p.add_argument("--output", required=True)
    args = p.parse_args()

    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    draw = ImageDraw.Draw(img)
    accent = ACCENTS[args.accent]

    tag_font = load_font(FONT_BOLD_CANDIDATES, 26)
    tag = args.tag.upper().strip()
    spaced = " ".join(list(tag.replace(" ", "  ")))
    draw.text((PADDING, PADDING), spaced, font=tag_font, fill=MUTED)
    tag_bbox = draw.textbbox((PADDING, PADDING), spaced, font=tag_font)

    line_y = tag_bbox[3] + 32
    draw.rectangle([PADDING, line_y, PADDING + 80, line_y + 5], fill=accent)

    headline_top = line_y + 90
    footer_h = 80 if args.footer else 0
    max_w = CANVAS - 2 * PADDING
    max_h = CANVAS - headline_top - PADDING - footer_h

    font, lines, line_h = fit_headline(draw, args.headline, max_w, max_h)
    y = headline_top
    for ln in lines:
        draw.text((PADDING, y), ln, font=font, fill=INK)
        y += line_h

    if args.footer:
        f_font = load_font(FONT_REG_CANDIDATES, 22)
        fw = draw.textlength(args.footer, font=f_font)
        draw.text(
            (CANVAS - PADDING - fw, CANVAS - PADDING - 14),
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
