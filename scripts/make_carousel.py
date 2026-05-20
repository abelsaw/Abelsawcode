#!/usr/bin/env python3
"""Render a LinkedIn carousel from a JSON spec, in Tesla or Muji style.

Usage:
    python3 scripts/make_carousel.py --spec <path> --out-dir <dir> [--style tesla|muji]

The spec may set "style" ("muji" or "tesla"). CLI --style overrides. Default tesla.

Slide types:
    cover     — hook headline
    point     — kicker + headline + body
    stat      — kicker + giant number + tracked-caps label
    list      — kicker + 3-4 numbered items (title + description)
    takeaway  — kicker + headline + body (same layout as point, semantic hint)
    cta       — centered call-to-action (headline + body)
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


def text_height(font, n_lines, line_height_mult=1.4):
    return int(font.size * line_height_mult * n_lines)


# ============================== Muji renderers ==============================

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
    font, lines, size = auto_size(headline, max_w, draw, 92, 44, bold=True, max_lines=6)
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
    start = 168 if is_stat else 70
    floor = 84 if is_stat else 38
    max_lines = 2 if is_stat else 5

    headline = slide.get("headline", "")
    if headline:
        font, lines, size = auto_size(headline, max_w, draw, start, floor, bold=True, max_lines=max_lines)
        line_h = int(size * 1.14)
        for line in lines:
            draw.text((MARGIN, y), line, fill=M_INK, font=font)
            y += line_h
        y += 28

    body = slide.get("body", "")
    if body:
        font, lines, _ = auto_size(body, max_w, draw, 30, 22, bold=False, max_lines=10)
        line_h = int(font.size * 1.45)
        for line in lines:
            draw.text((MARGIN, y), line, fill=M_MUTED, font=font)
            y += line_h
    _muji_page(draw, page, total)
    return img


def render_list_muji(slide, source, page, total):
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
        y += 50

    items = slide.get("items", [])[:4]
    num_x = MARGIN
    text_x = MARGIN + 110
    text_w = SIZE - text_x - MARGIN
    slot = (SIZE - MARGIN - y) // max(len(items), 1)
    for i, item in enumerate(items, start=1):
        nf = load_font(34, bold=True)
        draw.text((num_x, y + 2), f"{i:02d}", fill=M_ACCENT, font=nf)
        tf, tlines, _ = auto_size(item.get("title", ""), text_w, draw, 36, 24, bold=True, max_lines=2)
        ty = y
        for line in tlines:
            draw.text((text_x, ty), line, fill=M_INK, font=tf)
            ty += int(tf.size * 1.18)
        body = item.get("body", "")
        if body:
            bf, blines, _ = auto_size(body, text_w, draw, 24, 18, bold=False, max_lines=3)
            ty += 4
            for line in blines:
                draw.text((text_x, ty), line, fill=M_MUTED, font=bf)
                ty += int(bf.size * 1.4)
        y += slot
    _muji_page(draw, page, total)
    return img


def render_cta_muji(slide, source, page, total):
    img = Image.new("RGB", (SIZE, SIZE), M_BG)
    draw = ImageDraw.Draw(img)
    max_w = SIZE - 2 * MARGIN
    headline = slide.get("headline", "")
    body = slide.get("body", "")

    h_font, h_lines, h_size = auto_size(headline, max_w, draw, 76, 44, bold=True, max_lines=4)
    h_line_h = int(h_size * 1.16)
    block_h = h_line_h * len(h_lines)

    b_font = b_lines = None
    if body:
        b_font, b_lines, _ = auto_size(body, max_w, draw, 28, 20, bold=False, max_lines=5)
        block_h += 40 + int(b_font.size * 1.5 * len(b_lines))

    y = (SIZE - block_h) // 2 - 20
    for line in h_lines:
        bbox = draw.textbbox((0, 0), line, font=h_font)
        x = (SIZE - (bbox[2] - bbox[0])) // 2
        draw.text((x, y), line, fill=M_INK, font=h_font)
        y += h_line_h

    if b_lines:
        y += 30
        draw.line([(SIZE // 2 - 36, y - 6), (SIZE // 2 + 36, y - 6)], fill=M_ACCENT, width=2)
        y += 12
        for line in b_lines:
            bbox = draw.textbbox((0, 0), line, font=b_font)
            x = (SIZE - (bbox[2] - bbox[0])) // 2
            draw.text((x, y), line, fill=M_MUTED, font=b_font)
            y += int(b_font.size * 1.5)

    _muji_page(draw, page, total)
    return img


# ============================= Tesla renderers =============================

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
    body = (slide.get("body") or "").strip()
    max_w = SIZE - 2 * MARGIN

    font, lines, size = auto_size(headline, max_w, draw, 124, 52, bold=True, max_lines=5)
    line_h = int(size * 1.08)
    block_h = line_h * len(lines)

    bf = blines = None
    if body:
        bf, blines, _ = auto_size(body, max_w, draw, 28, 22, bold=False, max_lines=3)
        block_h += 28 + int(bf.size * 1.5 * len(blines))

    y = SIZE - MARGIN - 80 - block_h
    for line in lines:
        draw.text((MARGIN, y), line, fill=T_INK, font=font)
        y += line_h

    if blines:
        y += 28
        for line in blines:
            draw.text((MARGIN, y), line, fill=T_MUTED, font=bf)
            y += int(bf.size * 1.5)

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
            label = tracked_caps(body)
            bbox = draw.textbbox((0, 0), label, font=bf)
            if bbox[2] - bbox[0] > max_w:
                bf = load_font(18, bold=True)
                bbox = draw.textbbox((0, 0), label, font=bf)
            x = (SIZE - (bbox[2] - bbox[0])) // 2
            draw.text((x, ny + 40), label, fill=T_MUTED, font=bf)
    else:
        headline = slide.get("headline", "")
        if headline:
            font, lines, size = auto_size(headline, max_w, draw, 84, 42, bold=True, max_lines=4)
            line_h = int(size * 1.12)
            for line in lines:
                draw.text((MARGIN, y), line, fill=T_INK, font=font)
                y += line_h
            y += 36

        body = slide.get("body", "")
        if body:
            font, lines, _ = auto_size(body, max_w, draw, 28, 20, bold=False, max_lines=10)
            line_h = int(font.size * 1.50)
            for line in lines:
                draw.text((MARGIN, y), line, fill=T_MUTED, font=font)
                y += line_h

    _tesla_page(draw, page, total)
    return img


def render_list_tesla(slide, source, page, total):
    img = Image.new("RGB", (SIZE, SIZE), T_BG)
    draw = ImageDraw.Draw(img)
    y = MARGIN + 30
    kicker = (slide.get("kicker") or "").strip()
    if kicker:
        kf = load_font(20, bold=True)
        draw.text((MARGIN, y), tracked_caps(kicker), fill=T_MUTED, font=kf)
        y += 80

    items = slide.get("items", [])[:4]
    num_x = MARGIN
    text_x = MARGIN + 110
    text_w = SIZE - text_x - MARGIN
    available = SIZE - MARGIN - y
    slot = available // max(len(items), 1)

    for i, item in enumerate(items, start=1):
        nf = load_font(36, bold=True)
        draw.text((num_x, y + 2), f"{i:02d}", fill=T_ACCENT, font=nf)
        tf, tlines, _ = auto_size(item.get("title", ""), text_w, draw, 38, 24, bold=True, max_lines=2)
        ty = y
        for line in tlines:
            draw.text((text_x, ty), line, fill=T_INK, font=tf)
            ty += int(tf.size * 1.18)
        body = item.get("body", "")
        if body:
            bf, blines, _ = auto_size(body, text_w, draw, 24, 18, bold=False, max_lines=3)
            ty += 6
            for line in blines:
                draw.text((text_x, ty), line, fill=T_MUTED, font=bf)
                ty += int(bf.size * 1.45)
        y += slot

    _tesla_page(draw, page, total)
    return img


def render_cta_tesla(slide, source, page, total):
    img = Image.new("RGB", (SIZE, SIZE), T_BG)
    draw = ImageDraw.Draw(img)
    max_w = SIZE - 2 * MARGIN
    headline = slide.get("headline", "")
    body = slide.get("body", "")

    h_font, h_lines, h_size = auto_size(headline, max_w, draw, 84, 44, bold=True, max_lines=4)
    h_line_h = int(h_size * 1.14)
    block_h = h_line_h * len(h_lines)

    b_font = b_lines = None
    if body:
        b_font, b_lines, _ = auto_size(body, max_w, draw, 28, 20, bold=False, max_lines=5)
        block_h += 36 + int(b_font.size * 1.5 * len(b_lines))

    y = (SIZE - block_h) // 2 - 20
    for line in h_lines:
        bbox = draw.textbbox((0, 0), line, font=h_font)
        x = (SIZE - (bbox[2] - bbox[0])) // 2
        draw.text((x, y), line, fill=T_INK, font=h_font)
        y += h_line_h

    if b_lines:
        y += 36
        for line in b_lines:
            bbox = draw.textbbox((0, 0), line, font=b_font)
            x = (SIZE - (bbox[2] - bbox[0])) // 2
            draw.text((x, y), line, fill=T_MUTED, font=b_font)
            y += int(b_font.size * 1.5)

    _tesla_page(draw, page, total)
    return img


# ============================== Dispatch ==============================

TESLA_RENDERERS = {
    "cover": render_cover_tesla,
    "stat": render_content_tesla,
    "point": render_content_tesla,
    "takeaway": render_content_tesla,
    "list": render_list_tesla,
    "cta": render_cta_tesla,
}
MUJI_RENDERERS = {
    "cover": render_cover_muji,
    "stat": render_content_muji,
    "point": render_content_muji,
    "takeaway": render_content_muji,
    "list": render_list_muji,
    "cta": render_cta_muji,
}


def render_slide(slide, source, page, total, style):
    renderers = TESLA_RENDERERS if style == "tesla" else MUJI_RENDERERS
    fn = renderers.get(slide.get("type", "point"), renderers["point"])
    return fn(slide, source, page, total)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--spec", required=True)
    p.add_argument("--out-dir", required=True)
    p.add_argument("--style", choices=["muji", "tesla"], default=None)
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
