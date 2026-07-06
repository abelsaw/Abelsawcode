#!/usr/bin/env python3
"""playful-iconic v2 cover — numbered TOC tiles.

Slide 1 cover where the 4 substance slides preview as a 2×2 grid of
colored tiles, each containing a number + a topic word. The title sits
above the grid; the brand tag + coral mini-stripe anchors the top.

Palette: cream / navy / coral / mustard (+ deep coral for the 4th tile).
"""
import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("ERROR: Pillow not installed.")

CANVAS = 1080
BG = (244, 235, 220)
NAVY = (27, 49, 71)
CORAL = (226, 106, 75)
MUSTARD = (212, 154, 56)
DARK_CORAL = (175, 75, 55)
MUTED = (108, 95, 80)
TILE_TEXT = BG

FONT_SANS_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]
FONT_SERIF_ITAL = [
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
]


def load_font(cands, size):
    for p in cands:
        if Path(p).is_file():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


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


def fit_lines_bold(draw, text, max_w, max_h, size_hi=110, size_lo=46, step=2):
    raw_lines = [ln.strip() for ln in text.split("\\n")]
    for size in range(size_hi, size_lo - 1, -step):
        font = load_font(FONT_SANS_BOLD, size)
        if not all(draw.textlength(ln, font=font) <= max_w for ln in raw_lines if ln):
            continue
        bbox = draw.textbbox((0, 0), "Hg", font=font)
        lh = (bbox[3] - bbox[1]) * 1.14
        if lh * len(raw_lines) <= max_h:
            return font, raw_lines, lh
    return font, raw_lines, lh


def fit_lines_ital(draw, text, max_w, max_h, size_hi=36, size_lo=18):
    raw_lines = [ln.strip() for ln in text.split("\\n")]
    for size in range(size_hi, size_lo - 1, -2):
        font = load_font(FONT_SERIF_ITAL, size)
        if not all(draw.textlength(ln, font=font) <= max_w for ln in raw_lines if ln):
            continue
        bbox = draw.textbbox((0, 0), "Hg", font=font)
        lh = (bbox[3] - bbox[1]) * 1.3
        if lh * len(raw_lines) <= max_h:
            return font, raw_lines, lh
    return font, raw_lines, lh



_PALETTES = {
    'warm-classic': dict(bg=(244, 235, 220), primary=(27, 49, 71), a1=(226, 106, 75), a2=(212, 154, 56), da=(175, 75, 55), muted=(108, 95, 80), mi=(188, 178, 158)),
    'cool-steel': dict(bg=(232, 232, 232), primary=(26, 36, 52), a1=(78, 118, 158), a2=(120, 140, 165), da=(44, 62, 86), muted=(110, 124, 140), mi=(170, 180, 195)),
    'earth-editorial': dict(bg=(239, 229, 208), primary=(46, 36, 24), a1=(181, 102, 60), a2=(160, 122, 64), da=(120, 70, 44), muted=(120, 102, 84), mi=(175, 165, 148)),
    'ink-slate': dict(bg=(238, 236, 230), primary=(32, 32, 36), a1=(198, 88, 66), a2=(128, 128, 132), da=(70, 70, 74), muted=(118, 116, 110), mi=(180, 178, 172)),
}

def _apply_palette(name):
    global BG, NAVY, CORAL, MUSTARD, DARK_CORAL, MUTED, TILE_TEXT
    _p = _PALETTES.get(name, _PALETTES['warm-classic'])
    BG=_p['bg']; NAVY=_p['primary']; CORAL=_p['a1']; MUSTARD=_p['a2']; DARK_CORAL=_p['da']; MUTED=_p['muted']; TILE_TEXT=_p['bg']

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--palette", default="warm-classic", choices=list(_PALETTES), help="Color palette (design rotation).")
    p.add_argument("--tag", default="CTRO")
    p.add_argument("--title", required=True)
    p.add_argument("--subtitle", default="")
    p.add_argument("--tiles", default="01:HIRE,02:KEEP,03:GROW,04:MOVE")
    p.add_argument("--source", default="")
    p.add_argument("--slide", default="")
    p.add_argument("--output", required=True)
    args = p.parse_args()
    _apply_palette(args.palette)

    tile_data = []
    for t in args.tiles.split(","):
        if ":" in t:
            num, lbl = t.split(":", 1)
            tile_data.append((num.strip(), lbl.strip()))
    while len(tile_data) < 4:
        tile_data.append(("", ""))

    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    draw = ImageDraw.Draw(img)

    pad = 92
    content_w = CANVAS - 2 * pad

    # Brand tag + coral mini-stripe
    tag_font = load_font(FONT_SANS_BOLD, 20)
    tag_text = tracked(args.tag, 2)
    draw.text((pad, pad), tag_text, font=tag_font, fill=NAVY)
    tbbox = draw.textbbox((pad, pad), tag_text, font=tag_font)
    stripe_y = tbbox[3] + 14
    draw.rectangle([pad, stripe_y, pad + 80, stripe_y + 4], fill=CORAL)
    top_block_end = stripe_y + 4

    # Bottom rows
    bottom_counter_y = CANVAS - pad - 26
    bottom_source_y = bottom_counter_y - 32

    # Title
    title_top = top_block_end + 56
    title_font, title_lines, title_lh = fit_lines_bold(
        draw, args.title, content_w, 260, size_hi=104, size_lo=58,
    )
    y = title_top
    for ln in title_lines:
        draw.text((pad, y), ln, font=title_font, fill=NAVY)
        y += title_lh
    title_bottom = y

    # Subtitle
    subtitle_bottom = title_bottom
    if args.subtitle.strip():
        sub_font, sub_lines, sub_lh = fit_lines_ital(
            draw, args.subtitle, content_w, 96, size_hi=34, size_lo=22,
        )
        ys = title_bottom + 14
        for ln in sub_lines:
            draw.text((pad, ys), ln, font=sub_font, fill=MUTED)
            ys += sub_lh
        subtitle_bottom = ys

    # 2×2 tile grid
    grid_top_min = int(subtitle_bottom + 40)
    grid_bottom_max = bottom_source_y - 36
    avail_h = grid_bottom_max - grid_top_min

    GAP = 22
    tile_w = (content_w - GAP) // 2
    tile_h = (avail_h - GAP) // 2
    tile_h = min(tile_h, int(tile_w * 0.62))

    grid_h = tile_h * 2 + GAP
    grid_top = grid_top_min + max(0, (avail_h - grid_h) // 2)

    tile_colors = [CORAL, NAVY, MUSTARD, DARK_CORAL]
    num_font = load_font(FONT_SANS_BOLD, 64)
    lbl_font = load_font(FONT_SANS_BOLD, 26)

    for i, (num, lbl) in enumerate(tile_data[:4]):
        row, col = i // 2, i % 2
        tx = pad + col * (tile_w + GAP)
        ty = grid_top + row * (tile_h + GAP)
        draw.rectangle([tx, ty, tx + tile_w, ty + tile_h], fill=tile_colors[i])
        draw.text((tx + 22, ty + 14), num, font=num_font, fill=TILE_TEXT)
        if lbl:
            lbl_text = tracked(lbl, 2)
            lbb = draw.textbbox((0, 0), lbl_text, font=lbl_font)
            lh = lbb[3] - lbb[1]
            draw.text((tx + 22, ty + tile_h - lh - 20),
                      lbl_text, font=lbl_font, fill=TILE_TEXT)

    # Source + counter
    bottom_font = load_font(FONT_SANS_BOLD, 17)
    if args.source:
        src_text = "—  " + tracked(args.source, 2)
        draw.text((pad, bottom_source_y), src_text,
                  font=bottom_font, fill=MUTED)
    sn, st = parse_slide(args.slide)
    if sn is not None and st is not None:
        sc_text = tracked(f"{sn:02d} / {st:02d}", 2)
        sc_w = draw.textlength(sc_text, font=bottom_font)
        draw.text((CANVAS - pad - sc_w, bottom_counter_y),
                  sc_text, font=bottom_font, fill=MUTED)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
