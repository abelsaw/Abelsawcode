#!/usr/bin/env python3
"""playful-iconic v4 content slides (2-5) — corner accent shape.

Each content slide carries the cover's motif as a SMALLER coral
quarter-circle anchored in the top-right corner (radius ~180 instead
of the cover's 560). Below: brand tag, big sans bold navy headline, a
mustard short rule, two-part body (muted lead + navy bold payoff), and
three rhythm dots in the palette colors at the bottom-left.

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


def fit_headline(draw, text, max_w, max_h, size_hi=86, size_lo=40, step=2):
    raw_lines = [ln.strip() for ln in text.split("\\n")]
    for size in range(size_hi, size_lo - 1, -step):
        font = load_font(FONT_SANS_BOLD, size)
        if len(raw_lines) > 1:
            lines = raw_lines
            ok = all(draw.textlength(ln, font=font) <= max_w for ln in lines if ln)
        else:
            lines = wrap(draw, raw_lines[0], font, max_w)
            ok = all(draw.textlength(ln, font=font) <= max_w for ln in lines)
        if not ok:
            continue
        bbox = draw.textbbox((0, 0), "Hg", font=font)
        lh = (bbox[3] - bbox[1]) * 1.18
        if lh * len(lines) <= max_h:
            return font, lines, lh
    return font, lines, lh


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tag", default="CTRO")
    p.add_argument("--headline", required=True)
    p.add_argument("--lead", default="")
    p.add_argument("--bold", default="")
    p.add_argument("--source", default="")
    p.add_argument("--slide", default="")
    p.add_argument("--output", required=True)
    args = p.parse_args()

    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    draw = ImageDraw.Draw(img)

    # --- Small coral quarter-circle top-right (echoes the cover) ---
    R = 200
    draw.ellipse([CANVAS - R, -R, CANVAS + R, R], fill=CORAL)
    # Tiny mustard nested arc for accent
    R2 = 80
    draw.ellipse([CANVAS - R2, -R2, CANVAS + R2, R2], fill=MUSTARD)

    pad = 92
    content_w = CANVAS - 2 * pad

    # --- Brand tag tracked caps top-left (navy) + thin navy rule ---
    tag_font = load_font(FONT_SANS_BOLD, 20)
    tag_text = tracked(args.tag, 2)
    draw.text((pad, pad), tag_text, font=tag_font, fill=NAVY)
    tbbox = draw.textbbox((pad, pad), tag_text, font=tag_font)
    rule_y = tbbox[3] + 14
    draw.rectangle([pad, rule_y, pad + 60, rule_y + 3], fill=NAVY)
    top_block_end = rule_y + 3

    # --- Bottom rows ---
    bottom_counter_y = CANVAS - pad - 26
    bottom_source_y = bottom_counter_y - 32

    # --- Headline region (starts comfortably below the coral arc) ---
    head_top = max(top_block_end + 110, R + 60)
    head_max_h = int((bottom_source_y - head_top) * 0.45)
    h_font, h_lines, h_lh = fit_headline(
        draw, args.headline, content_w, head_max_h,
    )
    y = head_top
    for ln in h_lines:
        draw.text((pad, y), ln, font=h_font, fill=NAVY)
        y += h_lh
    head_bottom = y

    # --- Mustard short rule under headline ---
    rule_y2 = int(head_bottom + 22)
    draw.rectangle([pad, rule_y2, pad + 110, rule_y2 + 5], fill=MUSTARD)
    rule_bottom = rule_y2 + 5

    # --- Body region ---
    has_body = bool(args.lead.strip() or args.bold.strip())
    if has_body:
        body_top = rule_bottom + 34
        body_avail_h = bottom_source_y - body_top - 70  # leave room for dots

        body_parts = []
        if args.lead.strip():
            body_parts.append(("lead", args.lead.strip()))
        if args.bold.strip():
            body_parts.append(("bold", args.bold.strip()))

        for body_size in range(48, 22, -2):
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

    # --- Three rhythm dots bottom-left ---
    dot_r = 12
    dot_y = bottom_source_y - 32
    dot_gap = 38
    for i, col in enumerate([NAVY, MUSTARD, CORAL]):
        dx = pad + i * dot_gap
        draw.ellipse([dx, dot_y, dx + dot_r * 2, dot_y + dot_r * 2], fill=col)

    # --- Source + counter ---
    bottom_font = load_font(FONT_SANS_BOLD, 17)
    if args.source:
        draw.text(
            (pad + 150, bottom_source_y),
            "—  " + tracked(args.source, 2),
            font=bottom_font, fill=MUTED,
        )
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
