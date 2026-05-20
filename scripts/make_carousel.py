#!/usr/bin/env python3
"""Render a LinkedIn carousel from a JSON spec, in either Muji or Tesla style.

Usage:
    python3 scripts/make_carousel.py --spec <path> --out-dir <dir> [--style tesla|muji]

The spec may include a top-level "style" field ("muji" or "tesla"). The CLI
--style flag overrides it. Default is "tesla".

Spec JSON shape:
{
  "style":  "tesla",                 # optional, default "tesla"
  "source": "ANTHROPIC",
  "url":    "https://...",
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

SIZE = 1080
MARGIN = 90

# Muji theme (warm, light)
M_BG = (245, 242, 236)
M_INK = (38, 38, 38)
M_MUTED = (130, 125, 115)
M_ACCENT = (190, 180, 162)

# Tesla theme (stark, dark)
T_BG = (0, 0, 0)
T_INK = (255, 255, 255)
T_MUTED = (140, 140, 145)
T_ACCENT = (227, 25, 55)

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


def tracked_caps(text):
    return "   ".join(list(text.upper()))


# -------- Muji renderers (warm off-white, centered, accent rules) --------

def _muji_page(draw, page, total):
    if total <= 1:
        return
    font = load_font(20, bold=True)
    text = f"{page:02d}   /   {total:02d}"
    bbox = draw.textbbox((0, 0), text, font=font)
    x = SIZE - MARGIN - (bbox[2] - bbox[0])
    draw.text((x, SIZE - MARGIN + 10), text, fill=M_MUTED, font=font)


def render_cover_muji(slide, source, page, total):
    img = Image.new("RGB", (SIZE, SIZE), M_BG)
    draw = ImageDraw.Draw(img)
    headline = slide.get("headline", "")
    max_w = SIZE - 2 * MARGIN
    font, lines, size = auto_size(headline, max_w, draw, 96, 48, bold=True, max_lines=5)
    line_h = int(size * 1.18)
    y = (SIZE - line_h * len(lines)) // 2 - 50
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        x = (SIZE - (bbox[2] - bbox[0])) // 2
        draw.text((x, y), line, fill=M_INK, font=font)
        y += line_h
    draw.line([(SIZE // 2 - 36, y + 24), (SIZE // 2 + 36, y + 24)], fill=M_ACCENT, width=2)
    if source:
        sf = load_font(22, bold=True)
        spaced = tracked_caps(source)
        bbox = draw.textbbox((0, 0), spaced, font=sf)
        x = (SIZE - (bbox[2] - bbox[0])) // 2
        draw.text((x, SIZE - MARGIN), spaced, fill=M_MUTED, font=sf)
    _muji_page(draw, page, total)
    return img


def render_content_muji(slide, source, page, total):
    img = Image.new("RGB", (SIZE, SIZE), M_BG)
    draw = ImageDraw.Draw(img)
    max_w = SIZE - 2 * MARGIN
    y = MARGIN + 20
    kicker = (slide.get("kicker") or "").strip()
    if kicker:
        kf = load_font(22, bold=True)
        draw.text((MARGIN, y), tracked_caps(kicker), fill=M_MUTED, font=kf)
        y += 36
        draw.line([(MARGIN, y + 4), (MARGIN + 60, y + 4)], fill=M_ACCENT, width=2)
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
            draw.text((MARGIN, y), line, fill=M_INK, font=font)
            y += line_h
        y += 24

    body = slide.get("body", "")
    if body:
        font, lines, _ = auto_size(body, max_w, draw, 32, 22, bold=False, max_lines=6)
        line_h = int(font.size * 1.45)
        for line in lines:
            draw.text((MARGIN, y), line, fill=M_MUTED, font=font)
            y += line_h
    _muji_page(draw, page, total)
    return img


# -------- Tesla renderers (black, left-anchored, no accent rules) --------

def _tesla_page(draw, page, total):
    if total <= 1:
        return
    font = load_font(18, bold=True)
    text = f"{page:02d}   /   {total:02d}"
    bbox = draw.textbbox((0, 0), text, font=font)
    x = SIZE - MARGIN - (bbox[2] - bbox[0])
    draw.text((x, SIZE - MARGIN + 12), text, fill=T_MUTED, font=font)


def render_cover_tesla(slide, source, page, total):
    img = Image.new("RGB", (SIZE, SIZE), T_BG)
    draw = ImageDraw.Draw(img)
    headline = slide.get("headline", "")
    max_w = SIZE - 2 * MARGIN
    font, lines, size = auto_size(headline, max_w, draw, 144, 60, bold=True, max_lines=4)
    line_h = int(size * 1.06)
    block_h = line_h * len(lines)
    y = SIZE - MARGIN - 80 - block_h
    for line in lines:
        draw.text((MARGIN, y), line, fill=T_INK, font=font)
        y += line_h

    if source:
        sf = load_font(20, bold=True)
        draw.text((MARGIN, MARGIN), tracked_caps(source), fill=T_MUTED, font=sf)

    _tesla_page(draw, page, total)
    return img


def render_content_tesla(slide, source, page, total):
    img = Image.new("RGB", (SIZE, SIZE), T_BG)
    draw = ImageDraw.Draw(img)
    max_w = SIZE - 2 * MARGIN

    y = MARGIN + 30
    kicker = (slide.get("kicker") or "").strip()
    if kicker:
        kf = load_font(20, bold=True)
        draw.text((MARGIN, y), tracked_caps(kicker), fill=T_MUTED, font=kf)
        y += 70

    is_stat = slide.get("type") == "stat"

    if is_stat:
        headline = slide.get("headline", "")
        font, lines, size = auto_size(headline, max_w, draw, 280, 110, bold=True, max_lines=2)
        line_h = int(size * 1.02)
        block_h = line_h * len(lines)
        ny = (SIZE - block_h) // 2 - 30
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            x = (SIZE - (bbox[2] - bbox[0])) // 2
            draw.text((x, ny), line, fill=T_INK, font=font)
            ny += line_h

        body = slide.get("body", "")
        if body:
            bf = load_font(22, bold=True)
            bbox = draw.textbbox((0, 0), tracked_caps(body), font=bf)
            if bbox[2] - bbox[0] > max_w:
                bf = load_font(18, bold=True)
                bbox = draw.textbbox((0, 0), tracked_caps(body), font=bf)
            x = (SIZE - (bbox[2] - bbox[0])) // 2
            draw.text((x, ny + 40), tracked_caps(body), fill=T_MUTED, font=bf)
    else:
        headline = slide.get("headline", "")
        if headline:
            font, lines, size = auto_size(headline, max_w, draw, 88, 44, bold=True, max_lines=4)
            line_h = int(size * 1.12)
            for line in lines:
                draw.text((MARGIN, y), line, fill=T_INK, font=font)
                y += line_h
            y += 36

        body = slide.get("body", "")
        if body:
            font, lines, _ = auto_size(body, max_w, draw, 30, 22, bold=False, max_lines=6)
            line_h = int(font.size * 1.50)
            for line in lines:
                draw.text((MARGIN, y), line, fill=T_MUTED, font=font)
                y += line_h

    _tesla_page(draw, page, total)
    return img


def render_slide(slide, source, page, total, style):
    is_cover = slide.get("type") == "cover"
    if style == "tesla":
        return render_cover_tesla(slide, source, page, total) if is_cover \
            else render_content_tesla(slide, source, page, total)
    return render_cover_muji(slide, source, page, total) if is_cover \
        else render_content_muji(slide, source, page, total)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--spec", required=True)
    p.add_argument("--out-dir", required=True)
    p.add_argument("--style", choices=["muji", "tesla"], default=None,
                   help="Override the style declared in the spec.")
    args = p.parse_args()

    with open(args.spec) as f:
        spec = json.load(f)

    style = args.style or spec.get("style") or "tesla"
    if style not in ("muji", "tesla"):
        raise SystemExit(f"unknown style: {style}")

    slides = spec.get("slides", [])
    source = spec.get("source", "")
    total = len(slides)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for i, slide in enumerate(slides, start=1):
        img = render_slide(slide, source, i, total, style)
        path = out_dir / f"slide-{i}.png"
        img.save(path, "PNG", optimize=True)
        print(path)


if __name__ == "__main__":
    main()
