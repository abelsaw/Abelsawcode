#!/usr/bin/env python3
"""playful-iconic v3 content slides (2-5) — stat-hero per slide.

Each content slide carries the magazine "by-the-numbers" motif: a big
stat in coral display serif on the left, a bold sans navy headline
beside it on the right, and a two-part muted lead + navy bold payoff
below.

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
FONT_SERIF_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
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


def fit_stat(draw, text, max_w, max_h, size_hi=320, size_lo=130, step=10):
    for size in range(size_hi, size_lo - 1, -step):
        font = load_font(FONT_SERIF_BOLD, size)
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        if w <= max_w and h <= max_h:
            return font, w, h, bbox
    return font, w, h, bbox


def fit_headline(draw, text, max_w, max_h, size_hi=72, size_lo=34, step=2):
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
    p.add_argument("--stat", required=True,
                   help="Big stat (e.g. '2×', '71%', '<25%', '$0').")
    p.add_argument("--headline", required=True,
                   help="Bold sans navy headline. Supports \\n.")
    p.add_argument("--lead", default="")
    p.add_argument("--bold", default="")
    p.add_argument("--source", default="")
    p.add_argument("--slide", default="")
    p.add_argument("--output", required=True)
    args = p.parse_args()

    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    draw = ImageDraw.Draw(img)

    pad = 84
    content_w = CANVAS - 2 * pad

    # --- Top: thin coral rule full width as wayfinder ---
    draw.rectangle([pad, pad + 30, pad + content_w, pad + 33], fill=CORAL)
    top_block_end = pad + 33

    # --- Bottom rows ---
    bottom_counter_y = CANVAS - pad - 24
    bottom_source_y = bottom_counter_y - 30

    # --- Mid block: stat (left) + headline (right) ---
    mid_top = top_block_end + 60
    mid_h_max = int((bottom_source_y - mid_top) * 0.55)

    stat_w_max = int(content_w * 0.42)
    head_w_max = content_w - stat_w_max - 36

    stat_font, sw, sh, s_bbox = fit_stat(
        draw, args.stat, stat_w_max, mid_h_max, size_hi=300, size_lo=140,
    )
    head_font, head_lines, head_lh = fit_headline(
        draw, args.headline, head_w_max, mid_h_max - 20,
        size_hi=68, size_lo=34,
    )

    head_block_h = head_lh * len(head_lines)
    block_h = max(sh, head_block_h)
    block_top = mid_top + max(0, (mid_h_max - block_h) // 4)

    # Stat at left
    stat_x = pad - s_bbox[0]
    stat_y = block_top + (block_h - sh) // 2 - s_bbox[1]
    draw.text((stat_x, stat_y), args.stat, font=stat_font, fill=CORAL)

    # Headline at right
    head_x = pad + stat_w_max + 36
    head_y = block_top + (block_h - head_block_h) // 2
    for ln in head_lines:
        draw.text((head_x, head_y), ln, font=head_font, fill=NAVY)
        head_y += head_lh
    head_block_bottom = head_y

    # --- Mustard short rule under the mid block as separator ---
    block_bottom = max(stat_y + sh + s_bbox[1], head_block_bottom)
    rule_y = int(block_bottom + 36)
    draw.rectangle([pad, rule_y, pad + 90, rule_y + 4], fill=MUSTARD)

    # --- Body: lead muted + bold navy ---
    has_body = bool(args.lead.strip() or args.bold.strip())
    if has_body:
        body_top = rule_y + 34
        body_avail_h = bottom_source_y - body_top - 32

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

    # --- Source + counter ---
    bottom_font = load_font(FONT_SANS_BOLD, 17)
    if args.source:
        draw.text(
            (pad, bottom_source_y),
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
