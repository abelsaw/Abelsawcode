#!/usr/bin/env python3
"""Option 3 content slides — palette matched to the cover's photo.

No photo on content slides — the palette sampled from the cover photo
(cream / charcoal / tan / muted gray-tan) carries the mood through
slides 2-5. Each slide opens with a large tan slide number + thin
charcoal rule, sans bold charcoal headline, and the two-part body
(muted sans regular lead + charcoal sans bold payoff).
"""
import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("ERROR: Pillow not installed.")

CANVAS = 1080

# Same palette as the photo cover
BG = (235, 225, 208)
INK = (42, 42, 51)
TAN = (181, 143, 96)
MUTED = (138, 123, 102)

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


def fit_headline(draw, text, max_w, max_h, size_hi=82, size_lo=38, step=2):
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


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--headline", required=True)
    p.add_argument("--lead", default="")
    p.add_argument("--bold", default="")
    p.add_argument("--source", default="")
    p.add_argument("--slide", default="")
    p.add_argument("--output", required=True)
    args = p.parse_args()

    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    draw = ImageDraw.Draw(img)

    pad = 92
    content_w = CANVAS - 2 * pad

    # --- Top-left: LARGE slide # in tan with thin charcoal rule under it ---
    sn, st = parse_slide(args.slide)
    top_y = pad + 4
    if sn is not None:
        num_font = load_font(FONT_SANS_BOLD, 96)
        num_text = f"{sn:02d}"
        draw.text((pad - 6, top_y), num_text, font=num_font, fill=TAN)
        nbbox = draw.textbbox((pad - 6, top_y), num_text, font=num_font)
        rule_y = nbbox[3] + 12
        draw.rectangle([pad, rule_y, pad + 110, rule_y + 4], fill=INK)
        top_block_end = rule_y + 4
    else:
        top_block_end = top_y

    # --- Bottom rows: source + counter stacked ---
    bottom_counter_y = CANVAS - pad - 24
    bottom_source_y = bottom_counter_y - 32

    # --- Headline ---
    head_top = top_block_end + 70
    head_max_h = int((bottom_source_y - head_top) * 0.48)
    h_font, h_lines, h_lh = fit_headline(
        draw, args.headline, content_w, head_max_h,
    )
    y = head_top
    for ln in h_lines:
        draw.text((pad, y), ln, font=h_font, fill=INK)
        y += h_lh
    head_bottom = y

    # --- Body: muted regular lead + charcoal bold payoff ---
    has_body = bool(args.lead.strip() or args.bold.strip())
    if has_body:
        body_top = head_bottom + 36
        body_avail_h = bottom_source_y - body_top - 30

        body_parts = []
        if args.lead.strip():
            body_parts.append(("lead", args.lead.strip()))
        if args.bold.strip():
            body_parts.append(("bold", args.bold.strip()))

        for body_size in range(52, 22, -2):
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
            color = MUTED if kind == "lead" else INK
            for ln in lines:
                draw.text((pad, yb), ln, font=f, fill=color)
                yb += blh
            if i == 0 and len(blocks) > 1:
                yb += 12

    # --- Source + counter ---
    bottom_font = load_font(FONT_SANS_BOLD, 16)
    if args.source:
        draw.text((pad, bottom_source_y),
                  tracked(args.source, 2),
                  font=bottom_font, fill=INK)
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
