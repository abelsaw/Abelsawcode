#!/usr/bin/env python3
"""Option 1 v4: Pull-quote / magazine spread (HBR / New Yorker).

Each slide is a single typographic pull-quote. A large opening curly
quote mark in antique gold anchors the top-left; the body sits as
italic serif filling the canvas; an em-dash + small-caps source line
closes at the bottom-left. A hairline gold frame inset from the canvas
edge gives the whole thing an editorial-spread feel.

Three earth tones:
  cream / espresso / antique gold

Fonts:
  - Display serif bold for the opening glyph (DejaVu Serif Bold)
  - Italic serif for the body (Liberation Serif Italic)
  - Sans tracked caps for the source (DejaVu Sans Bold tracked)

CLI:
  --quote    The pull-quote body in italic serif. Supports \\n.
  --source   Source line (e.g. "Mercer Global Talent Trends 2026").
  --slide    N/M slide indicator.
  --output   Output PNG.
"""
import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("ERROR: Pillow not installed. Run: pip install Pillow")

CANVAS = 1080

# Three earth tones
BG = (239, 229, 208)          # cream
INK = (38, 30, 22)             # espresso
GOLD = (160, 122, 64)          # antique gold
MUTED = (120, 102, 84)         # warm gray-brown for source

FONT_SERIF_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
]
FONT_SERIF_ITAL = [
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
]
FONT_SANS_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
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


def wrap_multi(draw, text, font, max_w):
    out = []
    for raw in text.split("\\n"):
        raw = raw.strip()
        if not raw:
            out.append("")
            continue
        out.extend(wrap(draw, raw, font, max_w))
    return out


def tracked(text, spaces=2):
    return (" " * spaces).join(text.upper())


def parse_slide(s):
    if not s:
        return None, None
    parts = s.split("/")
    if len(parts) != 2:
        return None, None
    try:
        return int(parts[0]), int(parts[1])
    except ValueError:
        return None, None


def fit_quote(draw, text, max_w, max_h, size_hi=80, size_lo=32):
    for size in range(size_hi, size_lo - 1, -2):
        font = load_font(FONT_SERIF_ITAL, size)
        lines = wrap_multi(draw, text, font, max_w)
        bbox = draw.textbbox((0, 0), "Hg", font=font)
        lh = (bbox[3] - bbox[1]) * 1.32
        total = lh * len(lines)
        widths_ok = all(draw.textlength(ln, font=font) <= max_w for ln in lines)
        if widths_ok and total <= max_h:
            return font, lines, lh
    return font, lines, lh


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--quote", required=True)
    p.add_argument("--source", default="")
    p.add_argument("--slide", default="")
    p.add_argument("--output", required=True)
    args = p.parse_args()

    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    draw = ImageDraw.Draw(img)

    # --- Hairline antique gold frame, inset 44px ---
    inset = 44
    draw.rectangle(
        [inset, inset, CANVAS - inset, CANVAS - inset],
        outline=GOLD, width=2,
    )

    pad = 110  # inside-frame padding
    content_w = CANVAS - 2 * pad

    # --- Top-left: oversized opening curly quote glyph in gold ---
    glyph = "“"  # left double quotation mark
    glyph_font = load_font(FONT_SERIF_BOLD, 220)
    # Position so the glyph hugs the top-left of the content area.
    g_bbox = draw.textbbox((0, 0), glyph, font=glyph_font)
    gx = pad - g_bbox[0]
    gy = pad - g_bbox[1] - 24  # nudge up so it overlaps text region naturally
    draw.text((gx, gy), glyph, font=glyph_font, fill=GOLD)
    glyph_h = g_bbox[3] - g_bbox[1]
    glyph_bottom = pad + glyph_h - 80  # account for the upward nudge

    # --- Reserve bottom region: source row + counter row, stacked ---
    bottom_counter_y = CANVAS - pad - 30
    bottom_source_y = bottom_counter_y - 36

    # --- Quote body region ---
    body_top = glyph_bottom + 24
    body_bottom = bottom_source_y - 40
    body_h = body_bottom - body_top

    q_font, q_lines, q_lh = fit_quote(draw, args.quote, content_w, body_h)
    y = body_top
    for ln in q_lines:
        draw.text((pad, y), ln, font=q_font, fill=INK)
        y += q_lh

    # --- Bottom-left: em-dash + source small-caps tracked (upper row) ---
    if args.source:
        src_font = load_font(FONT_SANS_BOLD, 18)
        src_text = "—  " + tracked(args.source, 2)
        draw.text((pad, bottom_source_y), src_text, font=src_font, fill=MUTED)

    # --- Bottom-right: slide counter (lower row) ---
    slide_num, slide_total = parse_slide(args.slide)
    if slide_num is not None and slide_total is not None:
        sc_font = load_font(FONT_SANS_BOLD, 18)
        sc_text = tracked(f"{slide_num:02d} / {slide_total:02d}", 2)
        sc_w = draw.textlength(sc_text, font=sc_font)
        draw.text(
            (CANVAS - pad - sc_w, bottom_counter_y),
            sc_text,
            font=sc_font,
            fill=MUTED,
        )

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
