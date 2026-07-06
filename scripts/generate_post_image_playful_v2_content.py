#!/usr/bin/env python3
"""playful-iconic v2 content slides (2-5) — colored wayfinder tile.

Each content slide opens with a full-width colored wayfinder tile at
the top — the same tile that appeared in the cover's 2×2 grid for that
slide's position. The tile carries the slide number on the left and the
topic label tracked-caps on the right. Below the tile: sans bold navy
headline + two-part body (muted lead + navy bold payoff).

Palette: cream / navy / coral / mustard (+ deep coral).
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

COLOR_MAP = {
    "coral": CORAL,
    "navy": NAVY,
    "mustard": MUSTARD,
    "dark_coral": DARK_CORAL,
}

FONT_SANS_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]
FONT_SANS_REG = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]


def load_font(cands, size):
    for p in cands:
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


def fit_headline(draw, text, max_w, max_h, size_hi=82, size_lo=40, step=2):
    raw_lines = [ln.strip() for ln in text.split("\\n")]
    if len(raw_lines) > 1:
        for size in range(size_hi, size_lo - 1, -step):
            font = load_font(FONT_SANS_BOLD, size)
            if not all(draw.textlength(ln, font=font) <= max_w for ln in raw_lines if ln):
                continue
            bbox = draw.textbbox((0, 0), "Hg", font=font)
            lh = (bbox[3] - bbox[1]) * 1.18
            if lh * len(raw_lines) <= max_h:
                return font, raw_lines, lh
        return font, raw_lines, lh
    for size in range(size_hi, size_lo - 1, -step):
        font = load_font(FONT_SANS_BOLD, size)
        lines = wrap(draw, raw_lines[0], font, max_w)
        if not all(draw.textlength(ln, font=font) <= max_w for ln in lines):
            continue
        bbox = draw.textbbox((0, 0), "Hg", font=font)
        lh = (bbox[3] - bbox[1]) * 1.18
        if lh * len(lines) <= max_h:
            return font, lines, lh
    return font, lines, lh



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
    p.add_argument("--tile-num", required=True)
    p.add_argument("--tile-label", required=True)
    p.add_argument("--tile-color", default="coral",
                   choices=list(COLOR_MAP))
    p.add_argument("--headline", required=True)
    p.add_argument("--lead", default="")
    p.add_argument("--bold", default="")
    p.add_argument("--source", default="")
    p.add_argument("--slide", default="")
    p.add_argument("--output", required=True)
    args = p.parse_args()
    _apply_palette(args.palette)

    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    draw = ImageDraw.Draw(img)

    pad = 92
    content_w = CANVAS - 2 * pad
    tile_color = COLOR_MAP[args.tile_color]

    # --- Wayfinder tile (full content width) at the top ---
    tile_y = pad
    tile_h = 140
    draw.rectangle([pad, tile_y, pad + content_w, tile_y + tile_h],
                   fill=tile_color)

    # Slide # large sans bold cream at left
    num_font = load_font(FONT_SANS_BOLD, 78)
    nbbox = draw.textbbox((0, 0), args.tile_num, font=num_font)
    nh = nbbox[3] - nbbox[1]
    draw.text(
        (pad + 26, tile_y + (tile_h - nh) // 2 - nbbox[1]),
        args.tile_num, font=num_font, fill=TILE_TEXT,
    )

    # Topic label tracked caps cream at right, vertically centered
    lbl_font = load_font(FONT_SANS_BOLD, 26)
    lbl_text = tracked(args.tile_label, 2)
    lw = draw.textlength(lbl_text, font=lbl_font)
    lbb = draw.textbbox((0, 0), lbl_text, font=lbl_font)
    lh = lbb[3] - lbb[1]
    draw.text(
        (pad + content_w - 26 - lw, tile_y + (tile_h - lh) // 2 - lbb[1]),
        lbl_text, font=lbl_font, fill=TILE_TEXT,
    )

    # --- Bottom rows: source above counter, stacked ---
    bottom_counter_y = CANVAS - pad - 26
    bottom_source_y = bottom_counter_y - 32

    # --- Headline region ---
    head_top = tile_y + tile_h + 70
    head_max_h = int((bottom_source_y - head_top) * 0.48)
    h_font, h_lines, h_lh = fit_headline(
        draw, args.headline, content_w, head_max_h,
    )
    y = head_top
    for ln in h_lines:
        draw.text((pad, y), ln, font=h_font, fill=NAVY)
        y += h_lh
    head_bottom = y

    # --- Body region: muted lead + navy bold payoff ---
    has_body = bool(args.lead.strip() or args.bold.strip())
    if has_body:
        body_top = head_bottom + 38
        body_avail_h = bottom_source_y - body_top - 32

        body_parts = []
        if args.lead.strip():
            body_parts.append(("lead", args.lead.strip()))
        if args.bold.strip():
            body_parts.append(("bold", args.bold.strip()))

        for body_size in range(50, 22, -2):
            reg_font = load_font(FONT_SANS_REG, body_size)
            bold_font = load_font(FONT_SANS_BOLD, body_size)
            blocks = []
            ok = True
            for kind, txt in body_parts:
                f = reg_font if kind == "lead" else bold_font
                lines = wrap_multi(draw, txt, f, content_w)
                bbox = draw.textbbox((0, 0), "Hg", font=f)
                blh = (bbox[3] - bbox[1]) * 1.25
                blocks.append((kind, lines, f, blh))
                if any(draw.textlength(ln, font=f) > content_w for ln in lines):
                    ok = False
            total_h = sum(len(b[1]) * b[3] for b in blocks) + (
                12 if len(blocks) > 1 else 0
            )
            if ok and total_h <= body_avail_h:
                break

        yb = body_top
        for i, (kind, lines, f, blh) in enumerate(blocks):
            color = MUTED if kind == "lead" else NAVY
            for ln in lines:
                draw.text((pad, yb), ln, font=f, fill=color)
                yb += blh
            if i == 0 and len(blocks) > 1:
                yb += 12

    # --- Source + counter ---
    bottom_font = load_font(FONT_SANS_BOLD, 17)
    if args.source:
        draw.text((pad, bottom_source_y),
                  tracked(args.source, 2),
                  font=bottom_font, fill=NAVY)
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
