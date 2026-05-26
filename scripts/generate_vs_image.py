#!/usr/bin/env python3
"""Generate a 1080x1080 side-by-side competitor comparison LinkedIn image.

Layout (top -> bottom):
  - Accent band carrying the industry tag (white, uppercase) and an
    optional option label on the right.
  - Two logo cells, side by side, with a small "vs" divider between.
  - Company names under each logo.
  - 5-7 labelled comparison rows. Each row shows a dimension label
    (e.g. "Revenue") with company A's value on the left and company B's
    value on the right. Subtle row separators between rows.
  - Bottom accent rule + a short tagline / hook line.

Logos are fetched at runtime from Clearbit's free logo API
(https://logo.clearbit.com/{domain}) and cached under ./.cache/logos/.
On fetch failure or 404, the cell falls back to a flat accent-colored
disc with the company's first letter in white.

Accents are reused from generate_post_image.py so comparison cards can
sit alongside carousel slides without color drift. Option 1 = navy,
option 2 = rust, option 3 = moss.
"""
import argparse
import sys
import urllib.request
import urllib.error
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("ERROR: Pillow not installed. Run: pip install Pillow")

CANVAS = 1080
PADDING = 72
BAND_H = 200

BG = (250, 248, 244)
INK = (15, 15, 15)
WHITE = (255, 255, 255)
MUTED = (108, 116, 124)
RULE = (210, 205, 195)

ACCENTS = {
    "navy": (30, 58, 138),
    "rust": (180, 83, 9),
    "moss": (22, 101, 52),
    "plum": (107, 33, 168),
    "slate": (51, 65, 85),
}

FONT_BOLD_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
]
FONT_REG_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/Library/Fonts/Arial.ttf",
]

CACHE_DIR = Path(".cache/logos")
LOGO_SIZE = 168


def load_font(candidates, size):
    for p in candidates:
        if Path(p).is_file():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def fit_text(draw, text, candidates, max_w, start=72, floor=24, step=2):
    for size in range(start, floor, -step):
        font = load_font(candidates, size)
        if draw.textlength(text, font=font) <= max_w:
            return font
    return load_font(candidates, floor)


def fetch_logo(domain: str) -> Path | None:
    """Fetch a logo from Clearbit's free logo API, cache to disk, return path.

    Returns None on any failure — caller falls back to a letter disc.
    """
    if not domain:
        return None
    domain = domain.strip().lower()
    for prefix in ("https://", "http://"):
        if domain.startswith(prefix):
            domain = domain[len(prefix):]
            break
    domain = domain.rstrip("/")
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cached = CACHE_DIR / f"{domain}.png"
    if cached.is_file() and cached.stat().st_size > 0:
        return cached
    url = f"https://logo.clearbit.com/{domain}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "competitor-comparison/1.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = resp.read()
        if not data:
            return None
        cached.write_bytes(data)
        return cached
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError) as e:
        print(f"  logo fetch failed for {domain}: {e}", file=sys.stderr)
        return None


def paste_logo(canvas: Image.Image, logo_path: Path | None, cx: int, cy: int, accent, fallback_letter: str):
    """Paste a logo centered at (cx, cy), scaled to LOGO_SIZE box.

    On any failure, draws a flat accent-colored disc with the fallback letter.
    """
    if logo_path is not None:
        try:
            logo = Image.open(logo_path).convert("RGBA")
            # Scale to fit LOGO_SIZE x LOGO_SIZE preserving aspect ratio.
            logo.thumbnail((LOGO_SIZE, LOGO_SIZE), Image.LANCZOS)
            lx = cx - logo.width // 2
            ly = cy - logo.height // 2
            canvas.paste(logo, (lx, ly), logo)
            return
        except Exception as e:
            print(f"  logo paste failed: {e}", file=sys.stderr)

    # Fallback: solid disc with letter
    draw = ImageDraw.Draw(canvas)
    r = LOGO_SIZE // 2
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=accent)
    letter_font = load_font(FONT_BOLD_CANDIDATES, 108)
    letter = (fallback_letter or "?")[0].upper()
    lw = draw.textlength(letter, font=letter_font)
    lbbox = draw.textbbox((0, 0), letter, font=letter_font)
    lh = lbbox[3] - lbbox[1]
    draw.text((cx - lw // 2, cy - lh // 2 - 12), letter, font=letter_font, fill=WHITE)


def parse_row(spec: str):
    parts = [p.strip() for p in spec.split("|")]
    if len(parts) != 3:
        raise ValueError(f"--row expects 'Label|Value A|Value B', got: {spec!r}")
    label, a, b = parts
    if not label:
        raise ValueError(f"--row label must not be empty: {spec!r}")
    return label, a, b


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--left", required=True, help="Left-side competitor name (e.g. 'Apple').")
    p.add_argument("--right", required=True, help="Right-side competitor name (e.g. 'Microsoft').")
    p.add_argument("--left-domain", default="", help="Left company's primary domain for logo fetch, e.g. apple.com")
    p.add_argument("--right-domain", default="", help="Right company's primary domain for logo fetch, e.g. microsoft.com")
    p.add_argument("--row", action="append", default=[], help="Comparison row: 'Label|Value A|Value B'. Repeat 5-7 times.")
    p.add_argument("--tag", required=True, help="Industry / category tag in the top band, e.g. 'Big Tech 2026'.")
    p.add_argument("--option", default="", help="Optional option label rendered top-right, e.g. 'Option 1'.")
    p.add_argument("--tagline", default="", help="Short hook line anchored at the bottom (≤80 chars).")
    p.add_argument("--accent", default="navy", choices=sorted(ACCENTS.keys()))
    p.add_argument("--output", required=True)
    args = p.parse_args()

    rows = [parse_row(r) for r in args.row]
    if len(rows) < 3:
        sys.exit("ERROR: provide at least 3 --row entries (5-9 recommended).")
    if len(rows) > 9:
        sys.exit("ERROR: at most 9 --row entries supported.")

    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    draw = ImageDraw.Draw(img)
    accent = ACCENTS[args.accent]

    # Top accent band
    draw.rectangle([0, 0, CANVAS, BAND_H], fill=accent)
    tag_font = load_font(FONT_BOLD_CANDIDATES, 32)
    draw.text((PADDING, PADDING - 6), args.tag.upper().strip(), font=tag_font, fill=WHITE)
    if args.option:
        opt_font = load_font(FONT_BOLD_CANDIDATES, 22)
        opt_text = args.option.upper().strip()
        opt_w = draw.textlength(opt_text, font=opt_font)
        draw.text((CANVAS - PADDING - opt_w, PADDING + 2), opt_text, font=opt_font, fill=WHITE)

    # Logos row
    logo_band_top = BAND_H + 40
    logo_y = logo_band_top + LOGO_SIZE // 2 + 8
    left_logo_cx = CANVAS // 4
    right_logo_cx = CANVAS - CANVAS // 4

    left_logo = fetch_logo(args.left_domain) if args.left_domain else None
    right_logo = fetch_logo(args.right_domain) if args.right_domain else None
    paste_logo(img, left_logo, left_logo_cx, logo_y, accent, args.left)
    paste_logo(img, right_logo, right_logo_cx, logo_y, accent, args.right)

    # Small "vs" divider between logos
    vs_font = load_font(FONT_BOLD_CANDIDATES, 44)
    vs_text = "vs"
    vs_w = draw.textlength(vs_text, font=vs_font)
    vs_bbox = draw.textbbox((0, 0), vs_text, font=vs_font)
    vs_h = vs_bbox[3] - vs_bbox[1]
    draw.text(
        ((CANVAS - vs_w) // 2, logo_y - vs_h // 2 - 8),
        vs_text,
        font=vs_font,
        fill=MUTED,
    )

    # Company names under logos
    name_y = logo_y + LOGO_SIZE // 2 + 16
    name_max_w = (CANVAS // 2) - PADDING - 40
    left_name_font = fit_text(draw, args.left, FONT_BOLD_CANDIDATES, name_max_w, start=44, floor=24)
    lname_w = draw.textlength(args.left, font=left_name_font)
    draw.text((left_logo_cx - lname_w // 2, name_y), args.left, font=left_name_font, fill=INK)

    right_name_font = fit_text(draw, args.right, FONT_BOLD_CANDIDATES, name_max_w, start=44, floor=24)
    rname_w = draw.textlength(args.right, font=right_name_font)
    draw.text((right_logo_cx - rname_w // 2, name_y), args.right, font=right_name_font, fill=INK)

    # Comparison rows
    rows_top = name_y + 80
    rows_bottom_max = CANVAS - PADDING - 110  # reserve space for tagline+rule
    row_area_h = rows_bottom_max - rows_top
    row_h = row_area_h // len(rows)

    # Column geometry
    label_col_x = PADDING
    label_col_w = 250
    value_a_x = label_col_x + label_col_w + 20
    value_a_w = (CANVAS - 2 * PADDING - label_col_w - 60) // 2
    value_b_x = value_a_x + value_a_w + 20
    value_b_w = value_a_w

    # Tighten row typography as the row count grows so 8-9 rows still fit cleanly.
    label_pt = 22 if len(rows) <= 7 else 18
    value_start = 34 if len(rows) <= 7 else 28
    value_floor = 18 if len(rows) <= 7 else 16
    label_font = load_font(FONT_REG_CANDIDATES, label_pt)
    for i, (label, val_a, val_b) in enumerate(rows):
        y = rows_top + i * row_h
        # Row separator (top of each row except the first)
        if i > 0:
            draw.line([(PADDING, y), (CANVAS - PADDING, y)], fill=RULE, width=1)
        # Vertical center for content
        cy = y + row_h // 2
        # Label
        lbbox = draw.textbbox((0, 0), label.upper(), font=label_font)
        lh = lbbox[3] - lbbox[1]
        draw.text((label_col_x, cy - lh // 2 - 4), label.upper(), font=label_font, fill=MUTED)
        # Value A
        a_font = fit_text(draw, val_a, FONT_BOLD_CANDIDATES, value_a_w, start=value_start, floor=value_floor)
        abbox = draw.textbbox((0, 0), val_a, font=a_font)
        ah = abbox[3] - abbox[1]
        draw.text((value_a_x, cy - ah // 2 - 4), val_a, font=a_font, fill=INK)
        # Value B
        b_font = fit_text(draw, val_b, FONT_BOLD_CANDIDATES, value_b_w, start=value_start, floor=value_floor)
        bbbox = draw.textbbox((0, 0), val_b, font=b_font)
        bh = bbbox[3] - bbbox[1]
        draw.text((value_b_x, cy - bh // 2 - 4), val_b, font=b_font, fill=INK)

    # Bottom accent rule + tagline
    rule_y = CANVAS - PADDING - 90
    draw.rectangle([PADDING, rule_y, PADDING + 120, rule_y + 5], fill=accent)
    if args.tagline:
        tg_font = fit_text(draw, args.tagline, FONT_BOLD_CANDIDATES, CANVAS - 2 * PADDING, start=34, floor=20)
        draw.text((PADDING, rule_y + 22), args.tagline, font=tg_font, fill=INK)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({CANVAS}x{CANVAS}, accent={args.accent}, {args.left} vs {args.right}, {len(rows)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
