#!/usr/bin/env python3
"""playful-iconic — Option 2 cover slide (slide 1).

Companion to scripts/generate_post_image_playful_content.py for slides 2-5.

Design:
  - Warm cream BG
  - Top-left: brand tag in navy tracked caps
  - A coral short stripe just under the tag (decorative anchor)
  - Big bold sans title (navy), multi-line aware
  - Mustard short rule under the title
  - Italic serif subtitle (muted), multi-line aware
  - Bottom band: 4 geometric "chip icons" (circle, square, triangle, diamond)
    in the palette colors with tracked-caps single-word labels under each
  - Bottom-right: slide counter
"""
import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("ERROR: Pillow not installed. Run: pip install Pillow")

CANVAS = 1080

# Palette
BG = (244, 235, 220)       # warm cream
NAVY = (27, 49, 71)         # deep navy primary
CORAL = (226, 106, 75)      # coral accent
MUSTARD = (212, 154, 56)    # mustard accent
MUTED = (108, 95, 80)       # warm gray-brown for subtitle / supporting text

FONT_SANS_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
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


def fit_title(draw, text, max_w, max_h, size_hi=130, size_lo=60, step=4):
    raw_lines = [ln.strip() for ln in text.split("\\n")]
    for size in range(size_hi, size_lo - 1, -step):
        font = load_font(FONT_SANS_BOLD, size)
        widths_ok = all(
            draw.textlength(ln, font=font) <= max_w
            for ln in raw_lines if ln
        )
        if not widths_ok:
            continue
        bbox = draw.textbbox((0, 0), "Hg", font=font)
        lh = (bbox[3] - bbox[1]) * 1.12
        total = lh * len(raw_lines)
        if total <= max_h:
            return font, raw_lines, lh
    return font, raw_lines, lh


def fit_subtitle(draw, text, max_w, max_h, size_hi=42, size_lo=22):
    for size in range(size_hi, size_lo - 1, -2):
        font = load_font(FONT_SERIF_ITAL, size)
        lines = wrap_multi(draw, text, font, max_w)
        bbox = draw.textbbox((0, 0), "Hg", font=font)
        lh = (bbox[3] - bbox[1]) * 1.30
        total = lh * len(lines)
        if total <= max_h and all(
            draw.textlength(ln, font=font) <= max_w for ln in lines
        ):
            return font, lines, lh
    return font, lines, lh


# --- Chip icon shapes ---

def chip_circle(draw, cx, cy, r, color):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)


def chip_square(draw, cx, cy, r, color):
    draw.rectangle([cx - r, cy - r, cx + r, cy + r], fill=color)


def chip_triangle(draw, cx, cy, r, color):
    draw.polygon([
        (cx, cy - r),
        (cx - r, cy + r * 0.85),
        (cx + r, cy + r * 0.85),
    ], fill=color)


def chip_diamond(draw, cx, cy, r, color):
    draw.polygon([
        (cx, cy - r),
        (cx + r, cy),
        (cx, cy + r),
        (cx - r, cy),
    ], fill=color)



_PALETTES = {
    'warm-classic': dict(bg=(244, 235, 220), primary=(27, 49, 71), a1=(226, 106, 75), a2=(212, 154, 56), da=(175, 75, 55), muted=(108, 95, 80), mi=(188, 178, 158)),
    'cool-steel': dict(bg=(232, 232, 232), primary=(26, 36, 52), a1=(78, 118, 158), a2=(120, 140, 165), da=(44, 62, 86), muted=(110, 124, 140), mi=(170, 180, 195)),
    'earth-editorial': dict(bg=(239, 229, 208), primary=(46, 36, 24), a1=(181, 102, 60), a2=(160, 122, 64), da=(120, 70, 44), muted=(120, 102, 84), mi=(175, 165, 148)),
    'ink-slate': dict(bg=(238, 236, 230), primary=(32, 32, 36), a1=(198, 88, 66), a2=(128, 128, 132), da=(70, 70, 74), muted=(118, 116, 110), mi=(180, 178, 172)),
}

def _apply_palette(name):
    global BG, NAVY, CORAL, MUSTARD, MUTED
    _p = _PALETTES.get(name, _PALETTES['warm-classic'])
    BG=_p['bg']; NAVY=_p['primary']; CORAL=_p['a1']; MUSTARD=_p['a2']; MUTED=_p['muted']

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--palette", default="warm-classic", choices=list(_PALETTES), help="Color palette (design rotation).")
    p.add_argument("--tag", default="CTRO")
    p.add_argument("--title", required=True,
                   help="Bold sans title. Supports \\n.")
    p.add_argument("--subtitle", default="",
                   help="Italic serif subtitle. Supports \\n.")
    p.add_argument("--chips", default="HIRE,KEEP,GROW,MOVE",
                   help="Comma-separated labels for the 4 bottom chips.")
    p.add_argument("--source", default="",
                   help="Bottom-left source row, e.g. 'Mercer 2026'.")
    p.add_argument("--slide", default="")
    p.add_argument("--output", required=True)
    args = p.parse_args()
    _apply_palette(args.palette)

    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    draw = ImageDraw.Draw(img)

    pad = 92
    content_w = CANVAS - 2 * pad

    # --- Top-left: brand tag tracked caps + coral short stripe ---
    tag_y = pad
    tag_font = load_font(FONT_SANS_BOLD, 20)
    tag_text = tracked(args.tag, 2)
    draw.text((pad, tag_y), tag_text, font=tag_font, fill=NAVY)
    tbbox = draw.textbbox((pad, tag_y), tag_text, font=tag_font)
    stripe_y = tbbox[3] + 16
    draw.rectangle([pad, stripe_y, pad + 80, stripe_y + 4], fill=CORAL)
    top_block_bottom = stripe_y + 4

    # --- Reserve bottom region for chip-icon band + source/counter ---
    bottom_counter_y = CANVAS - pad - 26
    bottom_source_y = bottom_counter_y - 32
    chip_label_y = bottom_source_y - 80    # label row above the source line
    chip_row_y = chip_label_y - 60          # icon center row above the labels
    bottom_band_top = chip_row_y - 60       # top of the chip-icon band

    # --- Title region ---
    title_top = top_block_bottom + 110
    title_max_h = int((bottom_band_top - title_top) * 0.55)
    title_font, title_lines, title_lh = fit_title(
        draw, args.title, content_w, title_max_h,
    )
    y = title_top
    for ln in title_lines:
        draw.text((pad, y), ln, font=title_font, fill=NAVY)
        y += title_lh

    # --- Mustard short rule under title ---
    rule_y = int(y + 22)
    draw.rectangle([pad, rule_y, pad + 110, rule_y + 5], fill=MUSTARD)
    rule_bottom = rule_y + 5

    # --- Subtitle (italic serif muted) ---
    sub_top = rule_bottom + 36
    sub_max_h = bottom_band_top - sub_top - 20
    if args.subtitle.strip() and sub_max_h > 30:
        sub_font, sub_lines, sub_lh = fit_subtitle(
            draw, args.subtitle, content_w, sub_max_h,
        )
        yy = sub_top
        for ln in sub_lines:
            draw.text((pad, yy), ln, font=sub_font, fill=MUTED)
            yy += sub_lh

    # --- Bottom band: 4 geometric chip icons + tracked-caps labels ---
    chip_labels = [s.strip() for s in args.chips.split(",")][:4]
    while len(chip_labels) < 4:
        chip_labels.append("")
    chip_colors = [CORAL, NAVY, MUSTARD, CORAL]
    chip_shapes = [chip_circle, chip_square, chip_triangle, chip_diamond]
    chip_r = 38

    # 4 evenly spaced centers across the content width
    col_w = content_w / 4
    label_font = load_font(FONT_SANS_BOLD, 18)
    for i in range(4):
        cx = int(pad + col_w * (i + 0.5))
        chip_shapes[i](draw, cx, chip_row_y, chip_r, chip_colors[i])
        lbl = tracked(chip_labels[i], 2) if chip_labels[i] else ""
        if lbl:
            lw = draw.textlength(lbl, font=label_font)
            draw.text(
                (cx - lw / 2, chip_label_y),
                lbl, font=label_font, fill=NAVY,
            )

    # --- Bottom-left source small caps + Bottom-right counter ---
    bottom_font = load_font(FONT_SANS_BOLD, 17)
    if args.source:
        src_text = "—  " + tracked(args.source, 2)
        draw.text((pad, bottom_source_y), src_text,
                  font=bottom_font, fill=MUTED)

    slide_num, slide_total = parse_slide(args.slide)
    if slide_num is not None and slide_total is not None:
        sc_text = tracked(f"{slide_num:02d} / {slide_total:02d}", 2)
        sc_w = draw.textlength(sc_text, font=bottom_font)
        draw.text(
            (CANVAS - pad - sc_w, bottom_counter_y),
            sc_text, font=bottom_font, fill=MUTED,
        )

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
