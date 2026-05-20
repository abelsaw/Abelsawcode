#!/usr/bin/env python3
"""Render a LinkedIn carousel from a JSON spec.

Styles:
  terminal  — dev/AI engineer aesthetic: deep blue-black, neon-green mono accents.
  aurora    — premium gradient (indigo->black), cyan accents, frosted glass cards.
  editorial — modern tech editorial: warm off-white, electric-blue mono accents.
  tesla     — legacy: stark black, white type, source wordmark top-left.
  muji      — legacy: warm off-white, centered ink type, taupe accent rules.

Slide types:
  cover, point, stat, list, takeaway, cta

Usage:
    python3 scripts/make_carousel.py --spec <path> --out-dir <dir> [--style <name>]
"""
import argparse
import json
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIZE = 1080
MARGIN = 90

# ---------------- themes ----------------
M  = dict(bg=(245, 242, 236), ink=(38, 38, 38),  muted=(130, 125, 115), accent=(190, 180, 162))
T  = dict(bg=(0, 0, 0),       ink=(255, 255, 255), muted=(140, 140, 145), accent=(227, 25, 55))
TR = dict(bg=(10, 14, 19),    ink=(240, 244, 248), muted=(100, 116, 139), accent=(74, 222, 128))
AU = dict(bg_top=(30, 27, 75), bg_bot=(2, 6, 23), ink=(255, 255, 255), muted=(148, 163, 184),
          accent=(34, 211, 238), accent2=(217, 70, 239))
ED = dict(bg=(247, 247, 245), ink=(15, 23, 42),  muted=(100, 116, 139), accent=(37, 99, 235))

# ---------------- fonts ----------------
SANS_REG = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial.ttf",
    "C:/Windows/Fonts/arial.ttf",
]
SANS_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]
MONO_REG = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
    "/System/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/Monaco.ttf",
    "C:/Windows/Fonts/consola.ttf",
]
MONO_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
    "C:/Windows/Fonts/consolab.ttf",
]


def _font(paths, size):
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size=size)
            except OSError:
                continue
    return ImageFont.load_default()


def sans(size, bold=False):
    return _font(SANS_BOLD if bold else SANS_REG, size)


def mono(size, bold=False):
    return _font(MONO_BOLD if bold else MONO_REG, size)


# ---------------- helpers ----------------
def wrap(text, font, max_w, draw):
    words, lines, current = text.split(), [], []
    for w in words:
        trial = " ".join(current + [w])
        bb = draw.textbbox((0, 0), trial, font=font)
        if bb[2] - bb[0] <= max_w or not current:
            current.append(w)
        else:
            lines.append(" ".join(current))
            current = [w]
    if current:
        lines.append(" ".join(current))
    return lines


def auto_size(text, max_w, draw, start, floor, bold, max_lines, font_fn=sans):
    size = start
    while size >= floor:
        f = font_fn(size, bold=bold)
        ls = wrap(text, f, max_w, draw)
        if len(ls) <= max_lines:
            return f, ls, size
        size -= 4
    f = font_fn(floor, bold=bold)
    return f, wrap(text, f, max_w, draw)[:max_lines], floor


def tracked_caps(s):
    return "   ".join(list(s.upper()))


def gradient_bg(top, bot):
    img = Image.new("RGB", (SIZE, SIZE), top)
    d = ImageDraw.Draw(img)
    for y in range(SIZE):
        t = y / SIZE
        r = int(top[0] + (bot[0] - top[0]) * t)
        g = int(top[1] + (bot[1] - top[1]) * t)
        b = int(top[2] + (bot[2] - top[2]) * t)
        d.line([(0, y), (SIZE, y)], fill=(r, g, b))
    return img


def overlay_card(img, rect, fill_rgba, border_rgba=None, radius=24, border_w=1):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(layer)
    x, y, w, h = rect
    od.rounded_rectangle(
        [(x, y), (x + w, y + h)], radius=radius,
        fill=fill_rgba,
        outline=border_rgba if border_rgba else None,
        width=border_w if border_rgba else 0,
    )
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


# ============================== Muji ==============================
def _muji_page(draw, page, total):
    if total <= 1:
        return
    f = sans(20, bold=True)
    text = f"{page:02d}   /   {total:02d}"
    bb = draw.textbbox((0, 0), text, font=f)
    draw.text((SIZE - MARGIN - (bb[2] - bb[0]), SIZE - MARGIN + 10), text, fill=M["muted"], font=f)


def render_cover_muji(slide, source, page, total):
    img = Image.new("RGB", (SIZE, SIZE), M["bg"])
    draw = ImageDraw.Draw(img)
    headline = slide.get("headline", "")
    max_w = SIZE - 2 * MARGIN
    f, lines, size = auto_size(headline, max_w, draw, 92, 44, bold=True, max_lines=6)
    line_h = int(size * 1.18)
    y = (SIZE - line_h * len(lines)) // 2 - 50
    for line in lines:
        bb = draw.textbbox((0, 0), line, font=f)
        draw.text(((SIZE - (bb[2] - bb[0])) // 2, y), line, fill=M["ink"], font=f)
        y += line_h
    draw.line([(SIZE // 2 - 36, y + 24), (SIZE // 2 + 36, y + 24)], fill=M["accent"], width=2)
    if source:
        sf = sans(22, bold=True)
        spaced = tracked_caps(source)
        bb = draw.textbbox((0, 0), spaced, font=sf)
        draw.text(((SIZE - (bb[2] - bb[0])) // 2, SIZE - MARGIN), spaced, fill=M["muted"], font=sf)
    _muji_page(draw, page, total)
    return img


def render_content_muji(slide, source, page, total):
    img = Image.new("RGB", (SIZE, SIZE), M["bg"])
    draw = ImageDraw.Draw(img)
    max_w = SIZE - 2 * MARGIN
    y = MARGIN + 20
    kicker = (slide.get("kicker") or "").strip()
    if kicker:
        kf = sans(22, bold=True)
        draw.text((MARGIN, y), tracked_caps(kicker), fill=M["muted"], font=kf)
        y += 36
        draw.line([(MARGIN, y + 4), (MARGIN + 60, y + 4)], fill=M["accent"], width=2)
        y += 38
    is_stat = slide.get("type") == "stat"
    start = 168 if is_stat else 70
    floor = 84 if is_stat else 38
    max_lines = 2 if is_stat else 5
    headline = slide.get("headline", "")
    if headline:
        f, lines, size = auto_size(headline, max_w, draw, start, floor, bold=True, max_lines=max_lines)
        line_h = int(size * 1.14)
        for line in lines:
            draw.text((MARGIN, y), line, fill=M["ink"], font=f)
            y += line_h
        y += 28
    body = slide.get("body", "")
    if body:
        f, lines, _ = auto_size(body, max_w, draw, 30, 22, bold=False, max_lines=10)
        lh = int(f.size * 1.45)
        for line in lines:
            draw.text((MARGIN, y), line, fill=M["muted"], font=f)
            y += lh
    _muji_page(draw, page, total)
    return img


def render_list_muji(slide, source, page, total):
    img = Image.new("RGB", (SIZE, SIZE), M["bg"])
    draw = ImageDraw.Draw(img)
    y = MARGIN + 20
    kicker = (slide.get("kicker") or "").strip()
    if kicker:
        kf = sans(22, bold=True)
        draw.text((MARGIN, y), tracked_caps(kicker), fill=M["muted"], font=kf)
        y += 36
        draw.line([(MARGIN, y + 4), (MARGIN + 60, y + 4)], fill=M["accent"], width=2)
        y += 50
    items = slide.get("items", [])[:4]
    num_x, text_x = MARGIN, MARGIN + 110
    text_w = SIZE - text_x - MARGIN
    slot = (SIZE - MARGIN - y) // max(len(items), 1)
    for i, item in enumerate(items, start=1):
        nf = sans(34, bold=True)
        draw.text((num_x, y + 2), f"{i:02d}", fill=M["accent"], font=nf)
        tf, tlines, _ = auto_size(item.get("title", ""), text_w, draw, 36, 24, bold=True, max_lines=2)
        ty = y
        for line in tlines:
            draw.text((text_x, ty), line, fill=M["ink"], font=tf)
            ty += int(tf.size * 1.18)
        body = item.get("body", "")
        if body:
            bf, blines, _ = auto_size(body, text_w, draw, 24, 18, bold=False, max_lines=3)
            ty += 4
            for line in blines:
                draw.text((text_x, ty), line, fill=M["muted"], font=bf)
                ty += int(bf.size * 1.4)
        y += slot
    _muji_page(draw, page, total)
    return img


def render_cta_muji(slide, source, page, total):
    img = Image.new("RGB", (SIZE, SIZE), M["bg"])
    draw = ImageDraw.Draw(img)
    max_w = SIZE - 2 * MARGIN
    headline = slide.get("headline", "")
    body = slide.get("body", "")
    hf, hlines, hsize = auto_size(headline, max_w, draw, 76, 44, bold=True, max_lines=4)
    h_line_h = int(hsize * 1.16)
    block_h = h_line_h * len(hlines)
    bf = blines = None
    if body:
        bf, blines, _ = auto_size(body, max_w, draw, 28, 20, bold=False, max_lines=5)
        block_h += 40 + int(bf.size * 1.5 * len(blines))
    y = (SIZE - block_h) // 2 - 20
    for line in hlines:
        bb = draw.textbbox((0, 0), line, font=hf)
        draw.text(((SIZE - (bb[2] - bb[0])) // 2, y), line, fill=M["ink"], font=hf)
        y += h_line_h
    if blines:
        y += 30
        draw.line([(SIZE // 2 - 36, y - 6), (SIZE // 2 + 36, y - 6)], fill=M["accent"], width=2)
        y += 12
        for line in blines:
            bb = draw.textbbox((0, 0), line, font=bf)
            draw.text(((SIZE - (bb[2] - bb[0])) // 2, y), line, fill=M["muted"], font=bf)
            y += int(bf.size * 1.5)
    _muji_page(draw, page, total)
    return img


# ============================== Tesla ==============================
def _tesla_page(draw, page, total):
    if total <= 1:
        return
    f = sans(18, bold=True)
    text = f"{page:02d}   /   {total:02d}"
    bb = draw.textbbox((0, 0), text, font=f)
    draw.text((SIZE - MARGIN - (bb[2] - bb[0]), SIZE - MARGIN + 12), text, fill=T["muted"], font=f)


def render_cover_tesla(slide, source, page, total):
    img = Image.new("RGB", (SIZE, SIZE), T["bg"])
    draw = ImageDraw.Draw(img)
    headline = slide.get("headline", "")
    body = (slide.get("body") or "").strip()
    max_w = SIZE - 2 * MARGIN
    f, lines, size = auto_size(headline, max_w, draw, 124, 52, bold=True, max_lines=5)
    line_h = int(size * 1.08)
    block_h = line_h * len(lines)
    bf = blines = None
    if body:
        bf, blines, _ = auto_size(body, max_w, draw, 28, 22, bold=False, max_lines=3)
        block_h += 28 + int(bf.size * 1.5 * len(blines))
    y = SIZE - MARGIN - 80 - block_h
    for line in lines:
        draw.text((MARGIN, y), line, fill=T["ink"], font=f)
        y += line_h
    if blines:
        y += 28
        for line in blines:
            draw.text((MARGIN, y), line, fill=T["muted"], font=bf)
            y += int(bf.size * 1.5)
    if source:
        sf = sans(20, bold=True)
        draw.text((MARGIN, MARGIN), tracked_caps(source), fill=T["muted"], font=sf)
    _tesla_page(draw, page, total)
    return img


def render_content_tesla(slide, source, page, total):
    img = Image.new("RGB", (SIZE, SIZE), T["bg"])
    draw = ImageDraw.Draw(img)
    max_w = SIZE - 2 * MARGIN
    y = MARGIN + 30
    kicker = (slide.get("kicker") or "").strip()
    if kicker:
        kf = sans(20, bold=True)
        draw.text((MARGIN, y), tracked_caps(kicker), fill=T["muted"], font=kf)
        y += 70
    is_stat = slide.get("type") == "stat"
    if is_stat:
        headline = slide.get("headline", "")
        f, lines, size = auto_size(headline, max_w, draw, 280, 110, bold=True, max_lines=2)
        line_h = int(size * 1.02)
        block_h = line_h * len(lines)
        ny = (SIZE - block_h) // 2 - 30
        for line in lines:
            bb = draw.textbbox((0, 0), line, font=f)
            draw.text(((SIZE - (bb[2] - bb[0])) // 2, ny), line, fill=T["ink"], font=f)
            ny += line_h
        body = slide.get("body", "")
        if body:
            bf = sans(22, bold=True)
            label = tracked_caps(body)
            bb = draw.textbbox((0, 0), label, font=bf)
            if bb[2] - bb[0] > max_w:
                bf = sans(18, bold=True)
                bb = draw.textbbox((0, 0), label, font=bf)
            draw.text(((SIZE - (bb[2] - bb[0])) // 2, ny + 40), label, fill=T["muted"], font=bf)
    else:
        headline = slide.get("headline", "")
        if headline:
            f, lines, size = auto_size(headline, max_w, draw, 84, 42, bold=True, max_lines=4)
            line_h = int(size * 1.12)
            for line in lines:
                draw.text((MARGIN, y), line, fill=T["ink"], font=f)
                y += line_h
            y += 36
        body = slide.get("body", "")
        if body:
            f, lines, _ = auto_size(body, max_w, draw, 28, 20, bold=False, max_lines=10)
            lh = int(f.size * 1.50)
            for line in lines:
                draw.text((MARGIN, y), line, fill=T["muted"], font=f)
                y += lh
    _tesla_page(draw, page, total)
    return img


def render_list_tesla(slide, source, page, total):
    img = Image.new("RGB", (SIZE, SIZE), T["bg"])
    draw = ImageDraw.Draw(img)
    y = MARGIN + 30
    kicker = (slide.get("kicker") or "").strip()
    if kicker:
        kf = sans(20, bold=True)
        draw.text((MARGIN, y), tracked_caps(kicker), fill=T["muted"], font=kf)
        y += 80
    items = slide.get("items", [])[:4]
    num_x, text_x = MARGIN, MARGIN + 110
    text_w = SIZE - text_x - MARGIN
    slot = (SIZE - MARGIN - y) // max(len(items), 1)
    for i, item in enumerate(items, start=1):
        nf = sans(36, bold=True)
        draw.text((num_x, y + 2), f"{i:02d}", fill=T["accent"], font=nf)
        tf, tlines, _ = auto_size(item.get("title", ""), text_w, draw, 38, 24, bold=True, max_lines=2)
        ty = y
        for line in tlines:
            draw.text((text_x, ty), line, fill=T["ink"], font=tf)
            ty += int(tf.size * 1.18)
        body = item.get("body", "")
        if body:
            bf, blines, _ = auto_size(body, text_w, draw, 24, 18, bold=False, max_lines=3)
            ty += 6
            for line in blines:
                draw.text((text_x, ty), line, fill=T["muted"], font=bf)
                ty += int(bf.size * 1.45)
        y += slot
    _tesla_page(draw, page, total)
    return img


def render_cta_tesla(slide, source, page, total):
    img = Image.new("RGB", (SIZE, SIZE), T["bg"])
    draw = ImageDraw.Draw(img)
    max_w = SIZE - 2 * MARGIN
    headline = slide.get("headline", "")
    body = slide.get("body", "")
    hf, hlines, hsize = auto_size(headline, max_w, draw, 84, 44, bold=True, max_lines=4)
    h_line_h = int(hsize * 1.14)
    block_h = h_line_h * len(hlines)
    bf = blines = None
    if body:
        bf, blines, _ = auto_size(body, max_w, draw, 28, 20, bold=False, max_lines=5)
        block_h += 36 + int(bf.size * 1.5 * len(blines))
    y = (SIZE - block_h) // 2 - 20
    for line in hlines:
        bb = draw.textbbox((0, 0), line, font=hf)
        draw.text(((SIZE - (bb[2] - bb[0])) // 2, y), line, fill=T["ink"], font=hf)
        y += h_line_h
    if blines:
        y += 36
        for line in blines:
            bb = draw.textbbox((0, 0), line, font=bf)
            draw.text(((SIZE - (bb[2] - bb[0])) // 2, y), line, fill=T["muted"], font=bf)
            y += int(bf.size * 1.5)
    _tesla_page(draw, page, total)
    return img


# ============================== Terminal ==============================
def _term_page(draw, page, total):
    if total <= 1:
        return
    f = mono(20, bold=True)
    text = f"[{page:02d}/{total:02d}]"
    bb = draw.textbbox((0, 0), text, font=f)
    draw.text((SIZE - MARGIN - (bb[2] - bb[0]), SIZE - MARGIN + 12), text, fill=TR["accent"], font=f)


def _term_kicker(draw, kicker, x, y):
    if not kicker:
        return y
    kf = mono(20, bold=True)
    draw.text((x, y), f"> {kicker.upper()}", fill=TR["accent"], font=kf)
    y += 34
    draw.line([(x, y + 4), (x + 90, y + 4)], fill=TR["accent"], width=1)
    return y + 40


def render_cover_terminal(slide, source, page, total):
    img = Image.new("RGB", (SIZE, SIZE), TR["bg"])
    draw = ImageDraw.Draw(img)
    if source:
        sf = mono(18, bold=True)
        draw.text((MARGIN, MARGIN), f"> {source.upper()}", fill=TR["accent"], font=sf)
    draw.line([(MARGIN - 30, MARGIN + 70), (MARGIN - 30, SIZE - MARGIN - 70)], fill=TR["accent"], width=1)
    headline = slide.get("headline", "")
    body = (slide.get("body") or "").strip()
    max_w = SIZE - 2 * MARGIN
    f, lines, size = auto_size(headline, max_w, draw, 116, 52, bold=True, max_lines=5)
    line_h = int(size * 1.10)
    block_h = line_h * len(lines)
    bf = blines = None
    if body:
        bf, blines, _ = auto_size(body, max_w, draw, 26, 20, bold=False, max_lines=3, font_fn=mono)
        block_h += 30 + int(bf.size * 1.5 * len(blines))
    y = SIZE - MARGIN - 100 - block_h
    for line in lines:
        draw.text((MARGIN, y), line, fill=TR["ink"], font=f)
        y += line_h
    if blines:
        y += 30
        for line in blines:
            draw.text((MARGIN, y), line, fill=TR["muted"], font=bf)
            y += int(bf.size * 1.5)
    _term_page(draw, page, total)
    return img


def render_content_terminal(slide, source, page, total):
    img = Image.new("RGB", (SIZE, SIZE), TR["bg"])
    draw = ImageDraw.Draw(img)
    max_w = SIZE - 2 * MARGIN
    y = _term_kicker(draw, (slide.get("kicker") or "").strip(), MARGIN, MARGIN + 30)
    is_stat = slide.get("type") == "stat"
    if is_stat:
        headline = slide.get("headline", "")
        f, lines, size = auto_size(headline, max_w, draw, 280, 110, bold=True, max_lines=2)
        line_h = int(size * 1.02)
        block_h = line_h * len(lines)
        ny = (SIZE - block_h) // 2
        for line in lines:
            bb = draw.textbbox((0, 0), line, font=f)
            draw.text(((SIZE - (bb[2] - bb[0])) // 2, ny), line, fill=TR["ink"], font=f)
            ny += line_h
        body = slide.get("body", "")
        if body:
            bf = mono(22, bold=True)
            label = tracked_caps(body)
            bb = draw.textbbox((0, 0), label, font=bf)
            if bb[2] - bb[0] > max_w:
                bf = mono(18, bold=True)
                bb = draw.textbbox((0, 0), label, font=bf)
            draw.text(((SIZE - (bb[2] - bb[0])) // 2, ny + 40), label, fill=TR["accent"], font=bf)
    else:
        headline = slide.get("headline", "")
        if headline:
            f, lines, size = auto_size(headline, max_w, draw, 84, 42, bold=True, max_lines=4)
            line_h = int(size * 1.12)
            for line in lines:
                draw.text((MARGIN, y), line, fill=TR["ink"], font=f)
                y += line_h
            y += 32
        body = slide.get("body", "")
        if body:
            f, lines, _ = auto_size(body, max_w, draw, 26, 20, bold=False, max_lines=10, font_fn=mono)
            lh = int(f.size * 1.55)
            for line in lines:
                draw.text((MARGIN, y), line, fill=TR["muted"], font=f)
                y += lh
    _term_page(draw, page, total)
    return img


def render_list_terminal(slide, source, page, total):
    img = Image.new("RGB", (SIZE, SIZE), TR["bg"])
    draw = ImageDraw.Draw(img)
    y = _term_kicker(draw, (slide.get("kicker") or "").strip(), MARGIN, MARGIN + 30)
    items = slide.get("items", [])[:4]
    num_x, text_x = MARGIN, MARGIN + 100
    text_w = SIZE - text_x - MARGIN
    slot = (SIZE - MARGIN - y) // max(len(items), 1)
    for i, item in enumerate(items, start=1):
        nf = mono(32, bold=True)
        draw.text((num_x, y + 4), f"{i:02d}", fill=TR["accent"], font=nf)
        tf, tlines, _ = auto_size(item.get("title", ""), text_w, draw, 36, 24, bold=True, max_lines=2)
        ty = y
        for line in tlines:
            draw.text((text_x, ty), line, fill=TR["ink"], font=tf)
            ty += int(tf.size * 1.18)
        body = item.get("body", "")
        if body:
            bf, blines, _ = auto_size(body, text_w, draw, 22, 18, bold=False, max_lines=3, font_fn=mono)
            ty += 6
            for line in blines:
                draw.text((text_x, ty), line, fill=TR["muted"], font=bf)
                ty += int(bf.size * 1.45)
        y += slot
    _term_page(draw, page, total)
    return img


def render_cta_terminal(slide, source, page, total):
    img = Image.new("RGB", (SIZE, SIZE), TR["bg"])
    draw = ImageDraw.Draw(img)
    max_w = SIZE - 2 * MARGIN
    headline = slide.get("headline", "")
    body = slide.get("body", "")
    hf, hlines, hsize = auto_size(headline, max_w, draw, 80, 44, bold=True, max_lines=4)
    h_line_h = int(hsize * 1.14)
    block_h = h_line_h * len(hlines)
    bf = blines = None
    if body:
        bf, blines, _ = auto_size(body, max_w, draw, 24, 18, bold=False, max_lines=5, font_fn=mono)
        block_h += 36 + int(bf.size * 1.5 * len(blines))
    y = (SIZE - block_h) // 2 - 20
    for line in hlines:
        bb = draw.textbbox((0, 0), line, font=hf)
        draw.text(((SIZE - (bb[2] - bb[0])) // 2, y), line, fill=TR["ink"], font=hf)
        y += h_line_h
    if blines:
        y += 36
        for line in blines:
            bb = draw.textbbox((0, 0), line, font=bf)
            draw.text(((SIZE - (bb[2] - bb[0])) // 2, y), line, fill=TR["muted"], font=bf)
            y += int(bf.size * 1.5)
    cf = mono(44, bold=True)
    draw.text((SIZE // 2 - 12, y + 16), "_", fill=TR["accent"], font=cf)
    _term_page(draw, page, total)
    return img


# ============================== Aurora ==============================
def _aurora_page(draw, page, total):
    if total <= 1:
        return
    f = sans(18, bold=True)
    text = f"{page:02d} / {total:02d}"
    bb = draw.textbbox((0, 0), text, font=f)
    draw.text((SIZE - MARGIN - (bb[2] - bb[0]), SIZE - MARGIN + 12), text, fill=AU["muted"], font=f)


def _aurora_bg():
    return gradient_bg(AU["bg_top"], AU["bg_bot"])


def render_cover_aurora(slide, source, page, total):
    img = _aurora_bg()
    draw = ImageDraw.Draw(img)
    if source:
        sf = sans(20, bold=True)
        draw.text((MARGIN, MARGIN), tracked_caps(source), fill=AU["accent"], font=sf)
    headline = slide.get("headline", "")
    body = (slide.get("body") or "").strip()
    max_w = SIZE - 2 * MARGIN
    f, lines, size = auto_size(headline, max_w, draw, 124, 52, bold=True, max_lines=5)
    line_h = int(size * 1.08)
    block_h = line_h * len(lines)
    bf = blines = None
    if body:
        bf, blines, _ = auto_size(body, max_w, draw, 28, 22, bold=False, max_lines=3)
        block_h += 28 + int(bf.size * 1.5 * len(blines))
    y = SIZE - MARGIN - 100 - block_h
    for line in lines:
        draw.text((MARGIN, y), line, fill=AU["ink"], font=f)
        y += line_h
    if blines:
        y += 28
        for line in blines:
            draw.text((MARGIN, y), line, fill=AU["muted"], font=bf)
            y += int(bf.size * 1.5)
    _aurora_page(draw, page, total)
    return img


def render_content_aurora(slide, source, page, total):
    img = _aurora_bg()
    draw = ImageDraw.Draw(img)
    max_w = SIZE - 2 * MARGIN
    y = MARGIN + 30
    kicker = (slide.get("kicker") or "").strip()
    if kicker:
        kf = sans(20, bold=True)
        draw.text((MARGIN, y), tracked_caps(kicker), fill=AU["accent"], font=kf)
        y += 70
    is_stat = slide.get("type") == "stat"
    if is_stat:
        headline = slide.get("headline", "")
        f, lines, size = auto_size(headline, max_w, draw, 280, 110, bold=True, max_lines=2)
        line_h = int(size * 1.02)
        block_h = line_h * len(lines)
        ny = (SIZE - block_h) // 2 - 20
        for line in lines:
            bb = draw.textbbox((0, 0), line, font=f)
            draw.text(((SIZE - (bb[2] - bb[0])) // 2, ny), line, fill=AU["ink"], font=f)
            ny += line_h
        body = slide.get("body", "")
        if body:
            bf = sans(22, bold=True)
            label = tracked_caps(body)
            bb = draw.textbbox((0, 0), label, font=bf)
            if bb[2] - bb[0] > max_w:
                bf = sans(18, bold=True)
                bb = draw.textbbox((0, 0), label, font=bf)
            draw.text(((SIZE - (bb[2] - bb[0])) // 2, ny + 40), label, fill=AU["accent"], font=bf)
    else:
        headline = slide.get("headline", "")
        if headline:
            f, lines, size = auto_size(headline, max_w, draw, 84, 42, bold=True, max_lines=4)
            line_h = int(size * 1.12)
            for line in lines:
                draw.text((MARGIN, y), line, fill=AU["ink"], font=f)
                y += line_h
            y += 36
        body = slide.get("body", "")
        if body:
            f, lines, _ = auto_size(body, max_w, draw, 28, 20, bold=False, max_lines=10)
            lh = int(f.size * 1.50)
            for line in lines:
                draw.text((MARGIN, y), line, fill=AU["muted"], font=f)
                y += lh
    _aurora_page(draw, page, total)
    return img


def render_list_aurora(slide, source, page, total):
    img = _aurora_bg()
    draw = ImageDraw.Draw(img)
    y = MARGIN + 30
    kicker = (slide.get("kicker") or "").strip()
    if kicker:
        kf = sans(20, bold=True)
        draw.text((MARGIN, y), tracked_caps(kicker), fill=AU["accent"], font=kf)
        y += 70
    items = slide.get("items", [])[:4]
    # render glass cards
    card_x, card_w = MARGIN - 10, SIZE - 2 * (MARGIN - 10)
    available = SIZE - MARGIN - y
    card_h = (available - 20 * (len(items) - 1)) // max(len(items), 1)
    for i, item in enumerate(items, start=1):
        rect = (card_x, y, card_w, card_h - 10)
        img = overlay_card(img, rect, fill_rgba=(255, 255, 255, 18),
                           border_rgba=(255, 255, 255, 40), radius=22)
        draw = ImageDraw.Draw(img)
        nf = sans(34, bold=True)
        draw.text((card_x + 26, y + 22), f"{i:02d}", fill=AU["accent"], font=nf)
        text_x = card_x + 110
        text_w = card_w - 130
        tf, tlines, _ = auto_size(item.get("title", ""), text_w, draw, 36, 24, bold=True, max_lines=2)
        ty = y + 18
        for line in tlines:
            draw.text((text_x, ty), line, fill=AU["ink"], font=tf)
            ty += int(tf.size * 1.18)
        body = item.get("body", "")
        if body:
            bf, blines, _ = auto_size(body, text_w, draw, 22, 18, bold=False, max_lines=2)
            ty += 6
            for line in blines:
                draw.text((text_x, ty), line, fill=AU["muted"], font=bf)
                ty += int(bf.size * 1.4)
        y += card_h + 10
    _aurora_page(draw, page, total)
    return img


def render_cta_aurora(slide, source, page, total):
    img = _aurora_bg()
    draw = ImageDraw.Draw(img)
    max_w = SIZE - 2 * MARGIN
    headline = slide.get("headline", "")
    body = slide.get("body", "")
    hf, hlines, hsize = auto_size(headline, max_w, draw, 84, 44, bold=True, max_lines=4)
    h_line_h = int(hsize * 1.14)
    block_h = h_line_h * len(hlines)
    bf = blines = None
    if body:
        bf, blines, _ = auto_size(body, max_w, draw, 28, 20, bold=False, max_lines=5)
        block_h += 36 + int(bf.size * 1.5 * len(blines))
    y = (SIZE - block_h) // 2 - 20
    for line in hlines:
        bb = draw.textbbox((0, 0), line, font=hf)
        draw.text(((SIZE - (bb[2] - bb[0])) // 2, y), line, fill=AU["ink"], font=hf)
        y += h_line_h
    if blines:
        y += 36
        for line in blines:
            bb = draw.textbbox((0, 0), line, font=bf)
            draw.text(((SIZE - (bb[2] - bb[0])) // 2, y), line, fill=AU["muted"], font=bf)
            y += int(bf.size * 1.5)
    _aurora_page(draw, page, total)
    return img


# ============================== Editorial ==============================
def _ed_page(draw, page, total):
    if total <= 1:
        return
    f = mono(20, bold=True)
    text = f"{page:02d} / {total:02d}"
    bb = draw.textbbox((0, 0), text, font=f)
    draw.text((SIZE - MARGIN - (bb[2] - bb[0]), SIZE - MARGIN + 12), text, fill=ED["muted"], font=f)


def _ed_kicker(draw, kicker, x, y):
    if not kicker:
        return y
    kf = mono(22, bold=True)
    draw.text((x, y), kicker.upper(), fill=ED["accent"], font=kf)
    y += 34
    draw.line([(x, y + 4), (SIZE - MARGIN, y + 4)], fill=ED["accent"], width=2)
    return y + 38


def render_cover_editorial(slide, source, page, total):
    img = Image.new("RGB", (SIZE, SIZE), ED["bg"])
    draw = ImageDraw.Draw(img)
    # left accent bar
    draw.rectangle([(MARGIN - 28, MARGIN + 40), (MARGIN - 18, SIZE - MARGIN - 40)], fill=ED["accent"])
    if source:
        sf = mono(18, bold=True)
        bb = draw.textbbox((0, 0), source.upper(), font=sf)
        draw.text((SIZE - MARGIN - (bb[2] - bb[0]), MARGIN), source.upper(), fill=ED["muted"], font=sf)
    headline = slide.get("headline", "")
    body = (slide.get("body") or "").strip()
    max_w = SIZE - 2 * MARGIN
    f, lines, size = auto_size(headline, max_w, draw, 120, 50, bold=True, max_lines=5)
    line_h = int(size * 1.10)
    block_h = line_h * len(lines)
    bf = blines = None
    if body:
        bf, blines, _ = auto_size(body, max_w, draw, 28, 22, bold=False, max_lines=3)
        block_h += 28 + int(bf.size * 1.5 * len(blines))
    y = (SIZE - block_h) // 2 - 30
    for line in lines:
        draw.text((MARGIN, y), line, fill=ED["ink"], font=f)
        y += line_h
    if blines:
        y += 28
        for line in blines:
            draw.text((MARGIN, y), line, fill=ED["muted"], font=bf)
            y += int(bf.size * 1.5)
    _ed_page(draw, page, total)
    return img


def render_content_editorial(slide, source, page, total):
    img = Image.new("RGB", (SIZE, SIZE), ED["bg"])
    draw = ImageDraw.Draw(img)
    max_w = SIZE - 2 * MARGIN
    y = _ed_kicker(draw, (slide.get("kicker") or "").strip(), MARGIN, MARGIN + 30)
    is_stat = slide.get("type") == "stat"
    if is_stat:
        headline = slide.get("headline", "")
        f, lines, size = auto_size(headline, max_w, draw, 280, 110, bold=True, max_lines=2)
        line_h = int(size * 1.02)
        block_h = line_h * len(lines)
        ny = (SIZE - block_h) // 2
        for line in lines:
            bb = draw.textbbox((0, 0), line, font=f)
            draw.text(((SIZE - (bb[2] - bb[0])) // 2, ny), line, fill=ED["ink"], font=f)
            ny += line_h
        body = slide.get("body", "")
        if body:
            bf = mono(22, bold=True)
            label = body.upper()
            bb = draw.textbbox((0, 0), label, font=bf)
            if bb[2] - bb[0] > max_w:
                bf = mono(18, bold=True)
                bb = draw.textbbox((0, 0), label, font=bf)
            draw.text(((SIZE - (bb[2] - bb[0])) // 2, ny + 40), label, fill=ED["accent"], font=bf)
    else:
        headline = slide.get("headline", "")
        if headline:
            f, lines, size = auto_size(headline, max_w, draw, 84, 42, bold=True, max_lines=4)
            line_h = int(size * 1.12)
            for line in lines:
                draw.text((MARGIN, y), line, fill=ED["ink"], font=f)
                y += line_h
            y += 36
        body = slide.get("body", "")
        if body:
            f, lines, _ = auto_size(body, max_w, draw, 28, 20, bold=False, max_lines=10)
            lh = int(f.size * 1.50)
            for line in lines:
                draw.text((MARGIN, y), line, fill=ED["muted"], font=f)
                y += lh
    _ed_page(draw, page, total)
    return img


def render_list_editorial(slide, source, page, total):
    img = Image.new("RGB", (SIZE, SIZE), ED["bg"])
    draw = ImageDraw.Draw(img)
    y = _ed_kicker(draw, (slide.get("kicker") or "").strip(), MARGIN, MARGIN + 30)
    items = slide.get("items", [])[:4]
    num_x, text_x = MARGIN, MARGIN + 100
    text_w = SIZE - text_x - MARGIN
    slot = (SIZE - MARGIN - y) // max(len(items), 1)
    for i, item in enumerate(items, start=1):
        nf = mono(34, bold=True)
        draw.text((num_x, y + 4), f"{i:02d}", fill=ED["accent"], font=nf)
        tf, tlines, _ = auto_size(item.get("title", ""), text_w, draw, 36, 24, bold=True, max_lines=2)
        ty = y
        for line in tlines:
            draw.text((text_x, ty), line, fill=ED["ink"], font=tf)
            ty += int(tf.size * 1.18)
        body = item.get("body", "")
        if body:
            bf, blines, _ = auto_size(body, text_w, draw, 22, 18, bold=False, max_lines=3)
            ty += 6
            for line in blines:
                draw.text((text_x, ty), line, fill=ED["muted"], font=bf)
                ty += int(bf.size * 1.45)
        # subtle divider
        if i < len(items):
            draw.line([(MARGIN, y + slot - 16), (SIZE - MARGIN, y + slot - 16)],
                      fill=(220, 220, 215), width=1)
        y += slot
    _ed_page(draw, page, total)
    return img


def render_cta_editorial(slide, source, page, total):
    img = Image.new("RGB", (SIZE, SIZE), ED["bg"])
    draw = ImageDraw.Draw(img)
    max_w = SIZE - 2 * MARGIN
    headline = slide.get("headline", "")
    body = slide.get("body", "")
    hf, hlines, hsize = auto_size(headline, max_w, draw, 84, 44, bold=True, max_lines=4)
    h_line_h = int(hsize * 1.14)
    block_h = h_line_h * len(hlines)
    bf = blines = None
    if body:
        bf, blines, _ = auto_size(body, max_w, draw, 28, 20, bold=False, max_lines=5)
        block_h += 36 + int(bf.size * 1.5 * len(blines))
    y = (SIZE - block_h) // 2 - 20
    for line in hlines:
        bb = draw.textbbox((0, 0), line, font=hf)
        draw.text(((SIZE - (bb[2] - bb[0])) // 2, y), line, fill=ED["ink"], font=hf)
        y += h_line_h
    if blines:
        y += 36
        for line in blines:
            bb = draw.textbbox((0, 0), line, font=bf)
            draw.text(((SIZE - (bb[2] - bb[0])) // 2, y), line, fill=ED["muted"], font=bf)
            y += int(bf.size * 1.5)
    _ed_page(draw, page, total)
    return img


# ============================== Dispatch ==============================
STYLE_RENDERERS = {
    "muji":     {"cover": render_cover_muji,     "point": render_content_muji,     "stat": render_content_muji,     "takeaway": render_content_muji,     "list": render_list_muji,     "cta": render_cta_muji},
    "tesla":    {"cover": render_cover_tesla,    "point": render_content_tesla,    "stat": render_content_tesla,    "takeaway": render_content_tesla,    "list": render_list_tesla,    "cta": render_cta_tesla},
    "terminal": {"cover": render_cover_terminal, "point": render_content_terminal, "stat": render_content_terminal, "takeaway": render_content_terminal, "list": render_list_terminal, "cta": render_cta_terminal},
    "aurora":   {"cover": render_cover_aurora,   "point": render_content_aurora,   "stat": render_content_aurora,   "takeaway": render_content_aurora,   "list": render_list_aurora,   "cta": render_cta_aurora},
    "editorial":{"cover": render_cover_editorial,"point": render_content_editorial,"stat": render_content_editorial,"takeaway": render_content_editorial,"list": render_list_editorial,"cta": render_cta_editorial},
}


def render_slide(slide, source, page, total, style):
    renderers = STYLE_RENDERERS[style]
    fn = renderers.get(slide.get("type", "point"), renderers["point"])
    return fn(slide, source, page, total)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--spec", required=True)
    p.add_argument("--out-dir", required=True)
    p.add_argument("--style", choices=list(STYLE_RENDERERS.keys()), default=None)
    args = p.parse_args()
    with open(args.spec) as f:
        spec = json.load(f)
    style = args.style or spec.get("style") or "tesla"
    if style not in STYLE_RENDERERS:
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
