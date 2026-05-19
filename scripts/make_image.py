#!/usr/bin/env python3
"""Generate a Muji-style minimalist 1080x1080 image card for a LinkedIn post.

Design: warm off-white background, dark ink text, generous whitespace,
a thin centered accent line, source label in tracked-out small caps.
"""
import argparse
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BG = (245, 242, 236)        # warm off-white
INK = (38, 38, 38)          # near-black
MUTED = (130, 125, 115)     # warm gray
ACCENT = (190, 180, 162)    # taupe

SIZE = 1080
MARGIN = 100

REGULAR_FONTS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/Library/Fonts/Arial.ttf",
    "C:/Windows/Fonts/arial.ttf",
]
BOLD_FONTS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/Library/Fonts/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]


def load_font(size, bold=False):
    paths = BOLD_FONTS if bold else REGULAR_FONTS
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size=size)
            except OSError:
                continue
    return ImageFont.load_default()


def wrap(text, font, max_width, draw):
    words = text.split()
    lines, current = [], []
    for w in words:
        trial = " ".join(current + [w])
        bbox = draw.textbbox((0, 0), trial, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current.append(w)
        else:
            if current:
                lines.append(" ".join(current))
            current = [w]
    if current:
        lines.append(" ".join(current))
    return lines


def render(title, subtitle, source, out_path):
    img = Image.new("RGB", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(img)

    max_w = SIZE - 2 * MARGIN
    title_size = 78
    while title_size >= 36:
        title_font = load_font(title_size, bold=True)
        lines = wrap(title, title_font, max_w, draw)
        if len(lines) <= 5:
            break
        title_size -= 4
    else:
        title_font = load_font(36, bold=True)
        lines = wrap(title, title_font, max_w, draw)[:5]

    line_h = int(title_size * 1.22)
    block_h = line_h * len(lines)

    sub_lines = []
    if subtitle:
        sub_font = load_font(30)
        sub_lines = wrap(subtitle, sub_font, max_w, draw)
        block_h += 50 + 38 * len(sub_lines)

    y = (SIZE - block_h) // 2 - 30
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        x = (SIZE - (bbox[2] - bbox[0])) // 2
        draw.text((x, y), line, fill=INK, font=title_font)
        y += line_h

    accent_y = y + 18
    draw.line(
        [(SIZE // 2 - 36, accent_y), (SIZE // 2 + 36, accent_y)],
        fill=ACCENT,
        width=2,
    )

    if sub_lines:
        sy = accent_y + 32
        for line in sub_lines:
            bbox = draw.textbbox((0, 0), line, font=sub_font)
            sx = (SIZE - (bbox[2] - bbox[0])) // 2
            draw.text((sx, sy), line, fill=MUTED, font=sub_font)
            sy += 38

    if source:
        src_font = load_font(22, bold=True)
        spaced = "   ".join(list(source.upper()))
        bbox = draw.textbbox((0, 0), spaced, font=src_font)
        sx = (SIZE - (bbox[2] - bbox[0])) // 2
        draw.text((sx, SIZE - MARGIN + 10), spaced, fill=MUTED, font=src_font)

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, "PNG", optimize=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--title", required=True)
    p.add_argument("--subtitle", default="")
    p.add_argument("--source", default="")
    p.add_argument("--out", required=True)
    a = p.parse_args()
    render(a.title, a.subtitle, a.source, a.out)
    print(a.out)


if __name__ == "__main__":
    main()
