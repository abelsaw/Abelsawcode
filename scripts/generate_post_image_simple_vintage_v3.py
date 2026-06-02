#!/usr/bin/env python3
"""Option 1 v3: Editorial big-number (FT / Economist data card).

Each slide is built around ONE giant figure — a stat, a multiple, a
percentage — set in display serif and rendered in a rich rust accent.
A small kicker tag sits above; an italic serif caption explains
underneath; a muted small-caps source line closes the slide. The
result is a typographic data card that stops scroll on LinkedIn.

Three earth tones:
  cream / espresso / rust

Fonts:
  - Sans tracked caps for kicker + source (DejaVu Sans Bold tracked)
  - Display serif bold for the big stat (DejaVu Serif Bold)
  - Italic serif for the caption (Liberation Serif Italic)

CLI:
  --kicker   Top tracked-caps tag (e.g. "INTERNAL MOBILITY").
  --stat     The big number / glyph (e.g. "2x", "71%", "<25%", "$0").
             Optional — if omitted, the caption takes center stage in
             italic serif (useful for action-list and closing slides).
  --caption  Italic serif caption explaining the stat. Supports \\n.
  --source   Muted small-caps source line at the bottom.
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

# Three earth tones (rust replaces tan-gold for impact)
BG = (239, 229, 208)          # cream
INK = (38, 30, 22)             # espresso
RUST = (176, 76, 42)           # rich rust — the stat color
MUTED = (120, 102, 84)         # warm gray-brown for support text

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


def fit_stat(draw, text, max_w, max_h, size_hi=420, size_lo=140):
    """Find the largest display-serif size that fits the stat in one line."""
    for size in range(size_hi, size_lo - 1, -10):
        font = load_font(FONT_SERIF_BOLD, size)
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        if w <= max_w and h <= max_h:
            return font, w, h
    return font, w, h


def fit_caption(draw, text, max_w, max_h, size_hi=56, size_lo=26):
    """Honor \\n as hard breaks; shrink until every forced line fits one display line."""
    raw_lines = [ln.strip() for ln in text.split("\\n")]
    for size in range(size_hi, size_lo - 1, -2):
        font = load_font(FONT_SERIF_ITAL, size)
        widths_ok = all(draw.textlength(ln, font=font) <= max_w for ln in raw_lines if ln)
        if not widths_ok:
            continue
        bbox = draw.textbbox((0, 0), "Hg", font=font)
        lh = (bbox[3] - bbox[1]) * 1.28
        total = lh * len(raw_lines)
        if total <= max_h:
            return font, raw_lines, lh
    return font, raw_lines, lh


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--kicker", default="")
    p.add_argument("--stat", default="")
    p.add_argument("--caption", default="")
    p.add_argument("--source", default="")
    p.add_argument("--slide", default="")
    p.add_argument("--output", required=True)
    args = p.parse_args()

    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    draw = ImageDraw.Draw(img)

    pad = 96
    content_w = CANVAS - 2 * pad

    # --- Top: kicker tracked-caps + thin rust rule ---
    y = pad + 8
    if args.kicker:
        k_font = load_font(FONT_SANS_BOLD, 24)
        k_text = tracked(args.kicker, 2)
        draw.text((pad, y), k_text, font=k_font, fill=MUTED)
        kbbox = draw.textbbox((pad, y), k_text, font=k_font)
        rule_y = kbbox[3] + 16
        draw.rectangle([pad, rule_y, pad + 64, rule_y + 2], fill=RUST)
        top_block_bottom = rule_y + 2
    else:
        top_block_bottom = pad

    # --- Bottom: source line (top row) + slide counter (bottom row), stacked ---
    bottom_counter_y = CANVAS - pad - 30
    bottom_source_y = bottom_counter_y - 36

    # --- Middle region for stat + caption ---
    region_top = top_block_bottom + 60
    region_bottom = bottom_source_y - 40
    region_h = region_bottom - region_top

    if args.stat.strip():
        # Stat dominates: ~62% of region, caption ~30%, gap 8%.
        stat_max_h = int(region_h * 0.62)
        cap_max_h = int(region_h * 0.30)
        stat_font, sw, sh = fit_stat(draw, args.stat, content_w, stat_max_h)
        # Draw stat left-aligned at region_top
        # Use bbox offset so the visible top of glyph sits at region_top
        s_bbox = draw.textbbox((0, 0), args.stat, font=stat_font)
        draw.text((pad - s_bbox[0], region_top - s_bbox[1]),
                  args.stat, font=stat_font, fill=RUST)
        stat_drawn_bottom = region_top + (s_bbox[3] - s_bbox[1])

        # Caption below stat
        cap_top = stat_drawn_bottom + 36
        cap_avail_h = region_bottom - cap_top
        if args.caption.strip() and cap_avail_h > 30:
            cap_font, cap_lines, cap_lh = fit_caption(
                draw, args.caption, content_w, cap_avail_h
            )
            yy = cap_top
            for ln in cap_lines:
                draw.text((pad, yy), ln, font=cap_font, fill=INK)
                yy += cap_lh
    else:
        # No stat: caption fills the region in italic serif, vertically centered.
        if args.caption.strip():
            cap_font, cap_lines, cap_lh = fit_caption(
                draw, args.caption, content_w, region_h,
                size_hi=60, size_lo=32,
            )
            total_h = cap_lh * len(cap_lines)
            yy = region_top + max(0, (region_h - total_h) // 2)
            for ln in cap_lines:
                draw.text((pad, yy), ln, font=cap_font, fill=INK)
                yy += cap_lh

    # --- Bottom-left: source small-caps tracked, muted ---
    if args.source:
        src_font = load_font(FONT_SANS_BOLD, 18)
        src_text = tracked(args.source, 2)
        draw.text((pad, bottom_source_y), src_text, font=src_font, fill=MUTED)

    # --- Bottom-right: slide counter on its own row beneath the source ---
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
