#!/usr/bin/env python3
"""playful-iconic — Option 2 content slides (2-5).

Companion to scripts/generate_post_image_playful_cover.py for slide 1.

Design (deliberate contrast with vintage-editorial):
  - Warm cream BG, no frame (modern, open)
  - Top-left: LARGE slide number in coral with a mustard rule under it
    (the signature "wayfinder" element)
  - Bold sans headline (navy)
  - Body: muted sans regular lead + navy sans bold payoff
  - Bottom-left: source line in navy tracked caps
  - Bottom-right: tracked-caps slide counter

Palette (matches the cover):
  cream / navy / coral / mustard
"""
import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("ERROR: Pillow not installed. Run: pip install Pillow")

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
FONT_SANS_REG = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
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


def fit_headline(draw, text, max_w, max_h, size_hi=86, size_lo=40, step=2):
    raw_lines = [ln.strip() for ln in text.split("\\n")]
    multi = any("\\n" in raw_lines for _ in [0])
    for size in range(size_hi, size_lo - 1, -step):
        font = load_font(FONT_SANS_BOLD, size)
        # When \n present, no further wrapping
        if len(raw_lines) > 1:
            widths_ok = all(
                draw.textlength(ln, font=font) <= max_w
                for ln in raw_lines if ln
            )
            lines = raw_lines
        else:
            lines = wrap(draw, raw_lines[0], font, max_w)
            widths_ok = all(
                draw.textlength(ln, font=font) <= max_w for ln in lines
            )
        if not widths_ok:
            continue
        bbox = draw.textbbox((0, 0), "Hg", font=font)
        lh = (bbox[3] - bbox[1]) * 1.18
        if lh * len(lines) <= max_h:
            return font, lines, lh
    return font, lines, lh


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--headline", required=True,
                   help="Bold sans headline. Supports \\n.")
    p.add_argument("--lead", default="",
                   help="Muted sans regular lead. Supports \\n (for lists).")
    p.add_argument("--bold", default="",
                   help="Sans bold payoff in navy.")
    p.add_argument("--source", default="")
    p.add_argument("--slide", default="")
    p.add_argument("--output", required=True)
    args = p.parse_args()

    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    draw = ImageDraw.Draw(img)

    pad = 92
    content_w = CANVAS - 2 * pad

    # --- Top-left: LARGE slide # in coral with mustard rule under it ---
    slide_num, slide_total = parse_slide(args.slide)
    top_y = pad + 4
    if slide_num is not None:
        num_font = load_font(FONT_SANS_BOLD, 96)
        num_text = f"{slide_num:02d}"
        draw.text((pad - 6, top_y), num_text, font=num_font, fill=CORAL)
        nbbox = draw.textbbox((pad - 6, top_y), num_text, font=num_font)
        rule_y = nbbox[3] + 14
        draw.rectangle([pad, rule_y, pad + 120, rule_y + 5], fill=MUSTARD)
        top_block_bottom = rule_y + 5
    else:
        top_block_bottom = top_y

    # --- Bottom rows: source above counter, stacked ---
    bottom_counter_y = CANVAS - pad - 26
    bottom_source_y = bottom_counter_y - 32

    # --- Headline region ---
    headline_top = top_block_bottom + 70
    headline_max_h = int((bottom_source_y - headline_top) * 0.48)
    h_font, h_lines, h_lh = fit_headline(
        draw, args.headline, content_w, headline_max_h,
    )
    y = headline_top
    for ln in h_lines:
        draw.text((pad, y), ln, font=h_font, fill=NAVY)
        y += h_lh
    headline_bottom = y

    # --- Body region: lead muted regular + bold navy ---
    has_body = bool(args.lead.strip() or args.bold.strip())
    if has_body:
        body_top = headline_bottom + 42
        body_avail_h = bottom_source_y - body_top - 32

        body_parts = []
        if args.lead.strip():
            body_parts.append(("lead", args.lead.strip()))
        if args.bold.strip():
            body_parts.append(("bold", args.bold.strip()))

        for body_size in range(54, 24, -2):
            reg_font = load_font(FONT_SANS_REG, body_size)
            bold_font = load_font(FONT_SANS_BOLD, body_size)
            blocks = []
            ok = True
            for kind, txt in body_parts:
                f = reg_font if kind == "lead" else bold_font
                lines = wrap_multi(draw, txt, f, content_w)
                bbox = draw.textbbox((0, 0), "Hg", font=f)
                lh = (bbox[3] - bbox[1]) * 1.25
                blocks.append((kind, lines, f, lh))
                if any(draw.textlength(ln, font=f) > content_w for ln in lines):
                    ok = False
            total_h = sum(len(b[1]) * b[3] for b in blocks) + (
                12 if len(blocks) > 1 else 0
            )
            if ok and total_h <= body_avail_h:
                break

        yb = body_top
        for i, (kind, lines, f, lh) in enumerate(blocks):
            color = MUTED if kind == "lead" else NAVY
            for ln in lines:
                draw.text((pad, yb), ln, font=f, fill=color)
                yb += lh
            if i == 0 and len(blocks) > 1:
                yb += 12

    # --- Bottom-left source navy tracked caps + Bottom-right counter ---
    bottom_font = load_font(FONT_SANS_BOLD, 17)
    if args.source:
        src_text = tracked(args.source, 2)
        draw.text((pad, bottom_source_y), src_text,
                  font=bottom_font, fill=NAVY)

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
