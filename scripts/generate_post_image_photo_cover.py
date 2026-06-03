#!/usr/bin/env python3
"""Option 3 cover — photo background, typography band below.

Slide 1 for the photo-driven carousel: a user-supplied photo fills the
top 600px of the canvas (center-cropped to fit); a thin tan accent
stripe separates it from a warm cream typography band underneath that
carries the brand tag, big bold sans title, italic serif subtitle, and
the source + counter footer.

Palette is sampled from a warm office / collaborative photo:
  cream / charcoal / tan / muted gray-tan.

Pass any other photo and the same layout still works, but the palette
is tuned to a warm photo — for a cold/blue photo, override the palette
(future enhancement).
"""
import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("ERROR: Pillow not installed.")

CANVAS = 1080
PHOTO_H = 600  # photo area height

# Sampled from a warm collaborative office photo
BG = (235, 225, 208)
INK = (42, 42, 51)
TAN = (181, 143, 96)
MUTED = (138, 123, 102)

# Cool palette — for photos with cool/blue dominant tones (navy suits,
# steel architecture, ocean, etc). Apply via --palette cool.
_COOL_PALETTE = {
    "BG": (232, 232, 230),
    "INK": (26, 36, 52),
    "TAN": (78, 118, 158),
    "MUTED": (110, 124, 140),
}

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


def cover_crop(photo, target_w, target_h):
    """Resize to cover the target area then center-crop."""
    pw, ph = photo.size
    scale = max(target_w / pw, target_h / ph)
    new_w = max(target_w, int(round(pw * scale)))
    new_h = max(target_h, int(round(ph * scale)))
    photo = photo.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return photo.crop((left, top, left + target_w, top + target_h))


def fit_title(draw, text, max_w, max_h, size_hi=72, size_lo=36, step=2):
    raw_lines = [ln.strip() for ln in text.split("\\n")]
    for size in range(size_hi, size_lo - 1, -step):
        font = load_font(FONT_SANS_BOLD, size)
        if not all(draw.textlength(ln, font=font) <= max_w for ln in raw_lines if ln):
            continue
        bbox = draw.textbbox((0, 0), "Hg", font=font)
        lh = (bbox[3] - bbox[1]) * 1.16
        if lh * len(raw_lines) <= max_h:
            return font, raw_lines, lh
    return font, raw_lines, lh


def fit_subtitle(draw, text, max_w, max_h, size_hi=30, size_lo=18):
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


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--photo", required=True, help="Path to background photo.")
    p.add_argument("--palette", default="warm", choices=["warm", "cool"],
                   help="warm (default) or cool palette.")
    p.add_argument("--tag", default="CHRO")
    p.add_argument("--title", required=True)
    p.add_argument("--subtitle", default="")
    p.add_argument("--source", default="")
    p.add_argument("--slide", default="")
    p.add_argument("--output", required=True)
    args = p.parse_args()

    global BG, INK, TAN, MUTED
    if args.palette == "cool":
        BG = _COOL_PALETTE["BG"]
        INK = _COOL_PALETTE["INK"]
        TAN = _COOL_PALETTE["TAN"]
        MUTED = _COOL_PALETTE["MUTED"]

    canvas = Image.new("RGB", (CANVAS, CANVAS), BG)

    # --- Photo in the top region ---
    photo = Image.open(args.photo).convert("RGB")
    photo = cover_crop(photo, CANVAS, PHOTO_H)
    canvas.paste(photo, (0, 0))

    draw = ImageDraw.Draw(canvas)

    # --- Tan accent stripe separating photo from text band ---
    draw.rectangle([0, PHOTO_H, CANVAS, PHOTO_H + 6], fill=TAN)

    pad = 88
    content_w = CANVAS - 2 * pad
    text_top = PHOTO_H + 6

    # --- Bottom rows: source + counter stacked ---
    bottom_counter_y = CANVAS - pad - 22
    bottom_source_y = bottom_counter_y - 32

    # --- Brand tag tracked caps + tan mini-stripe ---
    tag_font = load_font(FONT_SANS_BOLD, 20)
    tag_y = text_top + 36
    tag_text = tracked(args.tag, 2)
    draw.text((pad, tag_y), tag_text, font=tag_font, fill=INK)
    tbbox = draw.textbbox((pad, tag_y), tag_text, font=tag_font)
    stripe_y = tbbox[3] + 12
    draw.rectangle([pad, stripe_y, pad + 60, stripe_y + 3], fill=TAN)
    top_block_end = stripe_y + 3

    # --- Title region ---
    title_top = top_block_end + 22
    title_avail_h = bottom_source_y - title_top - 90  # leave room for subtitle
    title_font, title_lines, title_lh = fit_title(
        draw, args.title, content_w, title_avail_h,
        size_hi=72, size_lo=40,
    )
    y = title_top
    for ln in title_lines:
        draw.text((pad, y), ln, font=title_font, fill=INK)
        y += title_lh
    title_bottom = y

    # --- Subtitle italic serif muted ---
    if args.subtitle.strip():
        sub_avail_h = bottom_source_y - title_bottom - 16
        sub_font, sub_lines, sub_lh = fit_subtitle(
            draw, args.subtitle, content_w, sub_avail_h,
        )
        ys = title_bottom + 12
        for ln in sub_lines:
            draw.text((pad, ys), ln, font=sub_font, fill=MUTED)
            ys += sub_lh

    # --- Source + counter ---
    bottom_font = load_font(FONT_SANS_BOLD, 16)
    if args.source:
        draw.text((pad, bottom_source_y),
                  "—  " + tracked(args.source, 2),
                  font=bottom_font, fill=MUTED)
    sn, st = parse_slide(args.slide)
    if sn is not None and st is not None:
        sc_text = tracked(f"{sn:02d} / {st:02d}", 2)
        sc_w = draw.textlength(sc_text, font=bottom_font)
        draw.text((CANVAS - pad - sc_w, bottom_counter_y),
                  sc_text, font=bottom_font, fill=MUTED)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, format="PNG", optimize=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
