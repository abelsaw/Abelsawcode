#!/usr/bin/env python3
"""Generate a 1080x1080 LinkedIn carousel slide in vintage editorial style.

Warm parchment background, sepia/brown ink, serif typography, restrained
decorative ornaments + a small infographic-style icon centered above the
headline. Inspired by classic financial-document and editorial infographic
aesthetics — feels considered and editorial rather than modern-bold.

Same CLI as before: --headline, --tag, --accent, --slide N/M, --output.
Plus --icon (briefcase | chart-up | chart-bars | lightbulb | target |
seal | book | clock). Each icon is drawn programmatically from Pillow
primitives — no external assets.
"""
import argparse
import math
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("ERROR: Pillow not installed. Run: pip install Pillow")

CANVAS = 1080

# Warm vintage palette
BG = (245, 237, 216)         # parchment / warm cream
INK = (42, 31, 21)           # very dark brown
MUTED = (122, 107, 90)       # warm slate brown
BORDER = (170, 138, 100)     # tan border

ACCENTS = {
    "sepia": (139, 100, 56),
    "rust":  (160, 82, 45),
    "olive": (110, 99, 53),
    "navy":  (60, 73, 90),
    "brown": (101, 67, 33),
}

FONT_SERIF_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
]
FONT_SERIF_ITAL = [
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
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


def fit_headline(draw, text, max_w, max_h):
    for size in range(100, 32, -3):
        font = load_font(FONT_SERIF_BOLD, size)
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


def draw_diamond(draw, cx, cy, size, fill):
    draw.polygon([(cx, cy - size), (cx + size, cy), (cx, cy + size), (cx - size, cy)], fill=fill)


# ---------- Icon library (programmatic, no external assets) ----------

def icon_briefcase(draw, cx, cy, s, color):
    """Briefcase: rounded body + handle on top."""
    body_top = cy - s * 0.25
    body_bot = cy + s * 0.45
    body_left = cx - s * 0.5
    body_right = cx + s * 0.5
    draw.rounded_rectangle([body_left, body_top, body_right, body_bot], radius=8, outline=color, width=5)
    hw, hh = s * 0.27, s * 0.18
    draw.rounded_rectangle([cx - hw, body_top - hh, cx + hw, body_top + 4], radius=10, outline=color, width=4)
    # Center seam + lock
    draw.line([(body_left + 8, cy + 6), (body_right - 8, cy + 6)], fill=color, width=2)
    lock = s * 0.08
    draw.rectangle([cx - lock, cy - 4, cx + lock, cy + 14], outline=color, width=3)


def icon_chart_up(draw, cx, cy, s, color):
    """Line chart trending up with arrow head."""
    ax_left = cx - s * 0.48
    ax_bot = cy + s * 0.42
    ax_right = cx + s * 0.48
    ax_top = cy - s * 0.42
    # Axes
    draw.line([(ax_left, ax_top), (ax_left, ax_bot), (ax_right, ax_bot)], fill=color, width=4)
    # Trending line
    pts = [
        (ax_left + s * 0.10, ax_bot - s * 0.08),
        (ax_left + s * 0.30, ax_bot - s * 0.22),
        (ax_left + s * 0.52, ax_bot - s * 0.45),
        (ax_left + s * 0.78, ax_bot - s * 0.70),
    ]
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i + 1]], fill=color, width=5)
    # Dots at points
    for x, y in pts:
        r = 5
        draw.ellipse([x - r, y - r, x + r, y + r], fill=color)
    # Arrow head at end
    ex, ey = pts[-1]
    head = 14
    draw.polygon([(ex, ey - head), (ex + head * 0.9, ey + head * 0.4), (ex - head * 0.9, ey + head * 0.4)], fill=color)


def icon_chart_bars(draw, cx, cy, s, color):
    """Bar chart with bars of increasing height."""
    bar_w = s * 0.14
    gap = s * 0.06
    n = 4
    total_w = n * bar_w + (n - 1) * gap
    start_x = cx - total_w / 2
    base_y = cy + s * 0.42
    heights = [0.22, 0.38, 0.55, 0.78]
    for i, h in enumerate(heights):
        bl = start_x + i * (bar_w + gap)
        br = bl + bar_w
        bt = base_y - s * h
        draw.rectangle([bl, bt, br, base_y], fill=color)
    # Base line
    draw.line([(start_x - 4, base_y), (start_x + total_w + 4, base_y)], fill=color, width=4)


def icon_lightbulb(draw, cx, cy, s, color):
    """Lightbulb with rays around the top."""
    bulb_r = s * 0.28
    bulb_cy = cy - s * 0.12
    draw.ellipse([cx - bulb_r, bulb_cy - bulb_r, cx + bulb_r, bulb_cy + bulb_r], outline=color, width=5)
    # Base
    base_w = s * 0.17
    base_top = bulb_cy + bulb_r - 2
    draw.rectangle([cx - base_w, base_top, cx + base_w, base_top + s * 0.13], outline=color, width=4)
    draw.rectangle([cx - base_w * 0.65, base_top + s * 0.13, cx + base_w * 0.65, base_top + s * 0.22], fill=color)
    # Rays
    for angle_deg in (-130, -100, -80, -50):
        a = math.radians(angle_deg)
        inner = bulb_r + 14
        outer = bulb_r + 34
        x1, y1 = cx + inner * math.cos(a), bulb_cy + inner * math.sin(a)
        x2, y2 = cx + outer * math.cos(a), bulb_cy + outer * math.sin(a)
        draw.line([(x1, y1), (x2, y2)], fill=color, width=4)


def icon_target(draw, cx, cy, s, color):
    """Concentric circles target with bullseye."""
    radii_outline = [s * 0.5, s * 0.34, s * 0.20]
    for r in radii_outline:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=4)
    # Bullseye
    rb = s * 0.08
    draw.ellipse([cx - rb, cy - rb, cx + rb, cy + rb], fill=color)
    # Crosshair tick marks
    tick_inner = s * 0.55
    tick_outer = s * 0.62
    for angle_deg in (0, 90, 180, 270):
        a = math.radians(angle_deg)
        x1, y1 = cx + tick_inner * math.cos(a), cy + tick_inner * math.sin(a)
        x2, y2 = cx + tick_outer * math.cos(a), cy + tick_outer * math.sin(a)
        draw.line([(x1, y1), (x2, y2)], fill=color, width=4)


def icon_seal(draw, cx, cy, s, color):
    """Vintage seal: outer notched circle with inner ornament."""
    r_outer = s * 0.5
    r_inner = s * 0.38
    draw.ellipse([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer], outline=color, width=4)
    draw.ellipse([cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner], outline=color, width=2)
    # Star inside
    pts = []
    for i in range(10):
        a = math.radians(-90 + i * 36)
        r = s * 0.24 if i % 2 == 0 else s * 0.10
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=color)


def icon_book(draw, cx, cy, s, color):
    """Open book — two pages with center binding."""
    half = s * 0.45
    h = s * 0.55
    top = cy - h / 2
    bot = cy + h / 2
    # Left page
    draw.polygon([(cx - half, top + 6), (cx - 4, top), (cx - 4, bot), (cx - half, bot - 4)], outline=color, width=4)
    # Right page
    draw.polygon([(cx + 4, top), (cx + half, top + 6), (cx + half, bot - 4), (cx + 4, bot)], outline=color, width=4)
    # Page lines
    for off in (s * 0.12, s * 0.06, 0.0, -s * 0.06, -s * 0.12):
        ly = cy + off
        draw.line([(cx - half + 16, ly), (cx - 10, ly)], fill=color, width=2)
        draw.line([(cx + 10, ly), (cx + half - 16, ly)], fill=color, width=2)


def icon_clock(draw, cx, cy, s, color):
    """Clock face with hands."""
    r = s * 0.45
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=5)
    # Tick marks at 12, 3, 6, 9
    for angle_deg in (-90, 0, 90, 180):
        a = math.radians(angle_deg)
        x1, y1 = cx + (r - 14) * math.cos(a), cy + (r - 14) * math.sin(a)
        x2, y2 = cx + (r - 4) * math.cos(a), cy + (r - 4) * math.sin(a)
        draw.line([(x1, y1), (x2, y2)], fill=color, width=4)
    # Hour hand (pointing to 10)
    a = math.radians(-120)
    draw.line([(cx, cy), (cx + r * 0.5 * math.cos(a), cy + r * 0.5 * math.sin(a))], fill=color, width=5)
    # Minute hand (pointing to 2)
    a = math.radians(-60)
    draw.line([(cx, cy), (cx + r * 0.75 * math.cos(a), cy + r * 0.75 * math.sin(a))], fill=color, width=4)
    # Center dot
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=color)


ICONS = {
    "briefcase":  icon_briefcase,
    "chart-up":   icon_chart_up,
    "chart-bars": icon_chart_bars,
    "lightbulb":  icon_lightbulb,
    "target":     icon_target,
    "seal":       icon_seal,
    "book":       icon_book,
    "clock":      icon_clock,
}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--headline", required=True)
    p.add_argument("--tag", default="HR INSIGHTS")
    p.add_argument("--accent", default="sepia", choices=sorted(ACCENTS.keys()))
    p.add_argument("--slide", default="")
    p.add_argument("--icon", default="", choices=[""] + list(ICONS.keys()),
                   help="Decorative icon centered above the headline.")
    p.add_argument("--output", required=True)
    args = p.parse_args()

    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    draw = ImageDraw.Draw(img)
    accent = ACCENTS[args.accent]

    # Outer double-rule frame
    draw.rectangle([30, 30, CANVAS - 30, CANVAS - 30], outline=BORDER, width=2)
    draw.rectangle([42, 42, CANVAS - 42, CANVAS - 42], outline=BORDER, width=1)

    content_pad = 96

    # Top: tag in italic serif, letter-spaced
    tag_font = load_font(FONT_SERIF_ITAL, 28)
    tag_text = "  ".join(args.tag.upper())
    draw.text((content_pad, content_pad), tag_text, font=tag_font, fill=MUTED)
    tag_bbox = draw.textbbox((content_pad, content_pad), tag_text, font=tag_font)

    # Decorative rule + diamond ornaments below tag
    rule_y = tag_bbox[3] + 30
    draw.rectangle([content_pad, rule_y, content_pad + 100, rule_y + 3], fill=accent)
    draw_diamond(draw, content_pad + 118, rule_y + 1, 6, accent)
    draw.rectangle([content_pad + 130, rule_y, content_pad + 160, rule_y + 3], fill=accent)

    # Icon (if provided), centered horizontally
    icon_size = 168
    icon_top = rule_y + 60
    icon_cy = icon_top + icon_size // 2
    if args.icon:
        ICONS[args.icon](draw, CANVAS // 2, icon_cy, icon_size, accent)
        head_top = icon_top + icon_size + 50
    else:
        head_top = rule_y + 80

    # Headline
    footer_zone = 110
    max_w = CANVAS - 2 * content_pad
    max_h = CANVAS - head_top - content_pad - footer_zone
    font, lines, line_h = fit_headline(draw, args.headline, max_w, max_h)
    y = head_top
    for ln in lines:
        draw.text((content_pad, y), ln, font=font, fill=INK)
        y += line_h

    # Bottom decorative bar + slide indicator
    bottom_y = CANVAS - content_pad - 30
    draw.rectangle([content_pad, bottom_y, content_pad + 80, bottom_y + 3], fill=accent)
    draw_diamond(draw, content_pad + 98, bottom_y + 1, 5, accent)

    slide_num, slide_total = parse_slide(args.slide)
    if slide_num is not None and slide_total is not None:
        si_font = load_font(FONT_SERIF_BOLD, 22)
        si_text = f"{slide_num:02d}  ·  {slide_total:02d}"
        si_w = draw.textlength(si_text, font=si_font)
        right = CANVAS - content_pad
        draw.text((right - si_w, bottom_y - 10), si_text, font=si_font, fill=accent)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
