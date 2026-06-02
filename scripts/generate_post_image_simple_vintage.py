#!/usr/bin/env python3
"""Option 1 (v2): Simple vintage, multi-font editorial.

Inspired by the IMG_2027 / IMG_2028 reference: cream background, small slide
number top-left with a thin gold rule under it, italic serif "setup" line
(the lead-in observation), a thin horizontal rule that closes the setup,
then sans-serif body text in two weights — a muted regular phrase followed
by a BOLD black payoff phrase. Slide counter "NN / NN" sits small and muted
at bottom-right.

Three earth tones only:
  cream / espresso / tan-gold (no terracotta in this iteration)

Fonts used (multiple types as requested):
  - Italic serif (Liberation Serif Italic) for the setup line
  - Sans regular (DejaVu Sans) muted gray-brown for the body lead
  - Sans bold (DejaVu Sans Bold) espresso for the body payoff

CLI:
  --setup    The italic serif headline / setup line. Can include literal "\\n"
             for explicit line breaks (e.g. for the "No flashy cars / No giant
             houses / No crazy luxury watches" rhythm).
  --lead     The muted sans-serif lead-in below the rule (optional).
  --bold     The bold sans-serif payoff below the lead (optional).
  --slide    "N/M" slide indicator (e.g. "2/12").
  --output   Output PNG path.
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
BG = (239, 229, 208)          # cream / warm oat
INK = (38, 30, 22)             # near-black espresso for bold payoff
MUTED = (120, 102, 84)         # warm gray-brown for lead/setup body
GOLD = (176, 138, 78)          # muted tan-gold for rules + slide marks

FONT_SERIF_ITAL = [
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
]
FONT_SANS_REG = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
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
        trial = " ".join(cur + [w])
        if draw.textlength(trial, font=font) <= max_w:
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
    """Wrap text honoring literal '\\n' as forced line breaks."""
    out = []
    for raw_line in text.split("\\n"):
        raw_line = raw_line.strip()
        if not raw_line:
            out.append("")
            continue
        out.extend(wrap(draw, raw_line, font, max_w))
    return out


def fit_block(draw, text, font_candidates, max_w, max_h, size_hi, size_lo, step=2):
    """Find the largest font size in [size_lo, size_hi] that fits text in max_w x max_h."""
    for size in range(size_hi, size_lo - 1, -step):
        font = load_font(font_candidates, size)
        lines = wrap_multi(draw, text, font, max_w)
        bbox = draw.textbbox((0, 0), "Hg", font=font)
        line_h = (bbox[3] - bbox[1]) * 1.28
        total_h = line_h * len(lines)
        widths_ok = all(draw.textlength(ln, font=font) <= max_w for ln in lines)
        if total_h <= max_h and widths_ok:
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


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--setup", required=True,
                   help="Italic serif setup line. Use \\n for line breaks.")
    p.add_argument("--lead", default="",
                   help="Muted sans regular lead phrase below the rule.")
    p.add_argument("--bold", default="",
                   help="Bold sans payoff phrase below the lead.")
    p.add_argument("--slide", default="",
                   help="Slide indicator as N/M (e.g. 2/12).")
    p.add_argument("--output", required=True)
    args = p.parse_args()

    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    draw = ImageDraw.Draw(img)

    pad = 96
    content_w = CANVAS - 2 * pad

    # --- Top-left: small slide number "02" + thin gold rule under it ---
    slide_num, slide_total = parse_slide(args.slide)
    top_y = pad
    if slide_num is not None:
        num_font = load_font(FONT_SANS_REG, 30)
        num_text = f"{slide_num:02d}"
        draw.text((pad, top_y), num_text, font=num_font, fill=MUTED)
        nbbox = draw.textbbox((pad, top_y), num_text, font=num_font)
        rule_y = nbbox[3] + 14
        draw.rectangle([pad, rule_y, pad + 56, rule_y + 2], fill=GOLD)
        top_block_bottom = rule_y + 2
    else:
        top_block_bottom = top_y

    # --- Reserve space for bottom slide counter "NN / NN" ---
    bottom_zone = 90  # space reserved at the bottom for slide counter

    # --- Layout: setup (italic serif) -> thin rule -> lead (muted) -> bold payoff ---
    # The setup line is the dominant element; lead+bold are smaller body below.
    has_body = bool(args.lead.strip() or args.bold.strip())

    # Vertical region available for setup + (rule) + body
    region_top = top_block_bottom + 130
    region_bottom = CANVAS - pad - bottom_zone
    region_h = region_bottom - region_top

    if has_body:
        # Setup gets roughly the top 55-60% of the region; body gets the rest.
        setup_max_h = int(region_h * 0.58)
        body_max_h = region_h - setup_max_h - 60  # 60px gap incl rule
        setup_font, setup_lines, setup_lh = fit_block(
            draw, args.setup, FONT_SERIF_ITAL, content_w, setup_max_h,
            size_hi=72, size_lo=36,
        )
    else:
        setup_font, setup_lines, setup_lh = fit_block(
            draw, args.setup, FONT_SERIF_ITAL, content_w, region_h,
            size_hi=88, size_lo=40,
        )

    # Draw setup (italic serif, muted brown)
    y = region_top
    for ln in setup_lines:
        draw.text((pad, y), ln, font=setup_font, fill=MUTED)
        y += setup_lh

    if has_body:
        # Thin horizontal rule under the setup (closes the setup, opens the body)
        rule_y = int(y + 18)
        draw.rectangle([pad, rule_y, pad + content_w, rule_y + 2], fill=GOLD)
        body_top = rule_y + 38

        # Body: lead in muted sans regular, then bold sans in espresso.
        # Stack them: lead first, then bold below.
        body_text_parts = []
        if args.lead.strip():
            body_text_parts.append(("lead", args.lead.strip()))
        if args.bold.strip():
            body_text_parts.append(("bold", args.bold.strip()))

        # Find a body size that fits both blocks within body_max_h.
        # We pick a single size and apply it to lead (regular) and bold.
        body_avail_h = (CANVAS - pad - bottom_zone) - body_top
        for body_size in range(56, 26, -2):
            reg_font = load_font(FONT_SANS_REG, body_size)
            bold_font = load_font(FONT_SANS_BOLD, body_size)
            blocks = []
            ok = True
            for kind, txt in body_text_parts:
                f = reg_font if kind == "lead" else bold_font
                lines = wrap_multi(draw, txt, f, content_w)
                bbox = draw.textbbox((0, 0), "Hg", font=f)
                lh = (bbox[3] - bbox[1]) * 1.25
                blocks.append((kind, lines, f, lh))
                if any(draw.textlength(ln, font=f) > content_w for ln in lines):
                    ok = False
            total_h = sum(len(b[1]) * b[3] for b in blocks) + (10 if len(blocks) > 1 else 0)
            if ok and total_h <= body_avail_h:
                break

        # Draw body blocks
        yb = body_top
        for i, (kind, lines, f, lh) in enumerate(blocks):
            color = MUTED if kind == "lead" else INK
            for ln in lines:
                draw.text((pad, yb), ln, font=f, fill=color)
                yb += lh
            if i == 0 and len(blocks) > 1:
                yb += 10

    # --- Bottom-right slide counter "NN / NN" muted sans ---
    if slide_num is not None and slide_total is not None:
        sc_font = load_font(FONT_SANS_REG, 22)
        sc_text = f"{slide_num:02d} / {slide_total:02d}"
        sc_w = draw.textlength(sc_text, font=sc_font)
        draw.text(
            (CANVAS - pad - sc_w, CANVAS - pad - 30),
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
