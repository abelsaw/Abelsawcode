#!/usr/bin/env python3
"""playful-iconic v3 cover — magazine cover with stat hero.

A magazine-style cover where a giant stat in coral display serif acts
as the lede visual. The title sits beside it in bold sans navy, with
an italic serif subtitle and 3 small "cover line" teasers in tracked
caps below — like a research issue cover.

Palette: cream / navy / coral / mustard.
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
MUTED = (108, 95, 80)

FONT_SANS_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]
FONT_SERIF_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
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


def fit_stat(draw, text, max_w, max_h, size_hi=380, size_lo=160, step=10):
    for size in range(size_hi, size_lo - 1, -step):
        font = load_font(FONT_SERIF_BOLD, size)
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        if w <= max_w and h <= max_h:
            return font, w, h, bbox
    return font, w, h, bbox


def fit_title(draw, text, max_w, max_h, size_hi=86, size_lo=40):
    raw_lines = [ln.strip() for ln in text.split("\\n")]
    for size in range(size_hi, size_lo - 1, -2):
        font = load_font(FONT_SANS_BOLD, size)
        if not all(draw.textlength(ln, font=font) <= max_w for ln in raw_lines if ln):
            continue
        bbox = draw.textbbox((0, 0), "Hg", font=font)
        lh = (bbox[3] - bbox[1]) * 1.14
        if lh * len(raw_lines) <= max_h:
            return font, raw_lines, lh
    return font, raw_lines, lh


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tag", default="CHRO READS · VOL 01")
    p.add_argument("--stat", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--subtitle", default="")
    p.add_argument("--teasers", default="",
                   help="Up to 3 comma-separated cover-line teasers.")
    p.add_argument("--source", default="")
    p.add_argument("--slide", default="")
    p.add_argument("--output", required=True)
    args = p.parse_args()

    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    draw = ImageDraw.Draw(img)

    pad = 84
    content_w = CANVAS - 2 * pad

    # Top: brand tag tracked caps + coral mini-stripe full width
    tag_font = load_font(FONT_SANS_BOLD, 18)
    tag_text = tracked(args.tag, 2)
    draw.text((pad, pad), tag_text, font=tag_font, fill=NAVY)
    tbbox = draw.textbbox((pad, pad), tag_text, font=tag_font)
    stripe_y = tbbox[3] + 12
    draw.rectangle([pad, stripe_y, pad + content_w, stripe_y + 3], fill=CORAL)
    top_block_end = stripe_y + 3

    # Bottom rows
    bottom_counter_y = CANVAS - pad - 24
    bottom_source_y = bottom_counter_y - 30

    # Teaser region at the bottom: up to 3 lines tracked caps tracked
    teasers = [t.strip() for t in args.teasers.split(",") if t.strip()][:3]
    teaser_font = load_font(FONT_SANS_BOLD, 18)
    teaser_lh = 36
    teaser_block_h = teaser_lh * len(teasers) + (14 if teasers else 0)
    teaser_top = bottom_source_y - teaser_block_h - 32

    # Mid block: stat on left, title block on right
    mid_top = top_block_end + 70
    mid_bottom = teaser_top - 40
    mid_h = mid_bottom - mid_top

    stat_w_max = int(content_w * 0.42)
    title_w_max = content_w - stat_w_max - 36

    stat_font, sw, sh, s_bbox = fit_stat(
        draw, args.stat, stat_w_max, mid_h, size_hi=360, size_lo=160,
    )

    title_h_max = mid_h - 20
    title_font, title_lines, title_lh = fit_title(
        draw, args.title, title_w_max, title_h_max,
        size_hi=92, size_lo=44,
    )

    # Vertical centering: align stat and title block midlines.
    title_block_h = title_lh * len(title_lines)
    stat_block_h = sh
    block_h = max(title_block_h, stat_block_h)
    block_top = mid_top + (mid_h - block_h) // 2

    # Stat at left
    stat_x = pad - s_bbox[0]
    stat_y = block_top + (block_h - stat_block_h) // 2 - s_bbox[1]
    draw.text((stat_x, stat_y), args.stat, font=stat_font, fill=CORAL)

    # Title at right (starts at pad + stat_w_max + 36)
    title_x = pad + stat_w_max + 36
    title_y = block_top + (block_h - title_block_h) // 2
    for ln in title_lines:
        draw.text((title_x, title_y), ln, font=title_font, fill=NAVY)
        title_y += title_lh
    title_block_bottom = title_y

    # Subtitle below the title block, in italic serif muted
    if args.subtitle.strip():
        sub_font = load_font(FONT_SERIF_ITAL, 32)
        ys = title_block_bottom + 6
        for raw_line in args.subtitle.split("\\n"):
            raw_line = raw_line.strip()
            if not raw_line:
                continue
            if ys + 40 > mid_bottom:
                break
            draw.text((title_x, ys), raw_line, font=sub_font, fill=MUTED)
            ys += 40

    # Teasers — 3 tracked-caps cover lines, each prefixed with mustard tick
    if teasers:
        ty = teaser_top + 14
        for t in teasers:
            # Mustard short tick
            draw.rectangle(
                [pad, ty + 10, pad + 22, ty + 14],
                fill=MUSTARD,
            )
            draw.text(
                (pad + 36, ty),
                tracked(t, 2),
                font=teaser_font, fill=NAVY,
            )
            ty += teaser_lh

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
