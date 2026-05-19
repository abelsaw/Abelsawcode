#!/usr/bin/env python3
"""Render a Muji-style LinkedIn carousel from a JSON spec.

Usage:
    python3 scripts/make_carousel.py --spec <path> --out-dir <dir>

Spec JSON shape:
{
  "source": "BBC",
  "url": "https://...",
  "slides": [
    {"type": "cover",    "headline": "..."},
    {"type": "point",    "kicker": "the story",      "headline": "...", "body": "..."},
    {"type": "stat",     "kicker": "the number",     "headline": "73%",  "body": "..."},
    {"type": "point",    "kicker": "why it matters", "headline": "...", "body": "..."},
    {"type": "takeaway", "kicker": "the takeaway",   "headline": "...", "body": "..."}
  ]
}
"""
import argparse
import json
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BG = (245, 242, 236)
INK = (38, 38, 38)
MUTED = (130, 125, 115)
ACCENT = (190, 180, 162)

SIZE = 1080
MARGIN = 90

REGULAR_FONTS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
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
        if bbox[2] - bbox[0] <= max_width or not current:
            current.append(w)
        else:
            lines.append(" ".join(current))
            current = [w]
    if current:
        lines.append(" ".join(current))
    return lines


def auto_size(text, max_width, draw, start, floor, bold, max_lines):
    size = start
    while size >= floor:
        font = load_font(size, bold=bold)
        lines = wrap(text, font, max_width, draw)
        if len(lines) <= max_lines:
            return font, lines, size
        size -= 4
    font = load_font(floor, bold=bold)
    return font, wrap(text, font, max_width, draw)[:max_lines], floor


def draw_page_indicator(draw, page, total):
    if total <= 1:
        return
    font = load_font(20, bold=True)
    text = f"{page:02d}   /   {total:02d}"
    bbox = draw.textbbox((0, 0), text, font=font)
    x = SIZE - MARGIN - (bbox[2] - bbox[0])
    y = SIZE - MARGIN + 10
    draw.text((x, y), text, fill=MUTED, font=font)


def draw_source_centered(draw, source, y):
    if not source:
        return
    font = load_font(22, bold=True)
    spaced = "   ".join(list(source.upper()))
    bbox = draw.textbbox((0, 0), spaced, font=font)
    x = (SIZE - (bbox[2] - bbox[0])) // 2
    draw.text((x, y), spaced, fill=MUTED, font=font)


def render_cover(slide, source, page, total):
    img = Image.new("RGB", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(img)

    headline = slide.get("headline", "")
    max_w = SIZE - 2 * MARGIN
    font, lines, size = auto_size(headline, max_w, draw, 96, 48, bold=True, max_lines=5)
    line_h = int(size * 1.18)
    block_h = line_h * len(lines)
    y = (SIZE - block_h) // 2 - 50

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        x = (SIZE - (bbox[2] - bbox[0])) // 2
        draw.text((x, y), line, fill=INK, font=font)
        y += line_h

    accent_y = y + 24
    draw.line(
        [(SIZE // 2 - 36, accent_y), (SIZE // 2 + 36, accent_y)],
        fill=ACCENT,
        width=2,
    )

    draw_source_centered(draw, source, SIZE - MARGIN)
    draw_page_indicator(draw, page, total)
    return img


def render_content(slide, source, page, total):
    img = Image.new("RGB", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(img)
    max_w = SIZE - 2 * MARGIN

    y = MARGIN + 20
    kicker = (slide.get("kicker") or "").upper()
    if kicker:
        kf = load_font(22, bold=True)
        spaced = "   ".join(list(kicker))
        draw.text((MARGIN, y), spaced, fill=MUTED, font=kf)
        y += 36
        draw.line([(MARGIN, y + 4), (MARGIN + 60, y + 4)], fill=ACCENT, width=2)
        y += 38

    is_stat = slide.get("type") == "stat"
    start = 168 if is_stat else 74
    floor = 84 if is_stat else 40
    max_lines = 2 if is_stat else 5

    headline = slide.get("headline", "")
    if headline:
        font, lines, size = auto_size(headline, max_w, draw, start, floor, bold=True, max_lines=max_lines)
        line_h = int(size * 1.14)
        for line in lines:
            draw.text((MARGIN, y), line, fill=INK, font=font)
            y += line_h
        y += 24

    body = slide.get("body", "")
    if body:
        font, lines, size = auto_size(body, max_w, draw, 32, 22, bold=False, max_lines=6)
        line_h = int(size * 1.45)
        for line in lines:
            draw.text((MARGIN, y), line, fill=MUTED, font=font)
            y += line_h

    draw_page_indicator(draw, page, total)
    return img


def render_slide(slide, source, page, total):
    if slide.get("type") == "cover":
        return render_cover(slide, source, page, total)
    return render_content(slide, source, page, total)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--spec", required=True)
    p.add_argument("--out-dir", required=True)
    args = p.parse_args()

    with open(args.spec) as f:
        spec = json.load(f)

    slides = spec.get("slides", [])
    source = spec.get("source", "")
    total = len(slides)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for i, slide in enumerate(slides, start=1):
        img = render_slide(slide, source, i, total)
        path = out_dir / f"slide-{i}.png"
        img.save(path, "PNG", optimize=True)
        print(path)


if __name__ == "__main__":
    main()
