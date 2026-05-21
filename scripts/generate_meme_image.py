#!/usr/bin/env python3
"""Generate a 1080x1080 viral-humour meme card for LinkedIn.

Two layouts, picked via --style:

  caption    Single-panel card. Big bold punchline center-stage,
             optional small setup line above it, optional tiny tag
             at top-left. Use for one-liners and observational jokes.

  two-panel  Stacked A/B card ("Expectations vs Reality",
             "Me / My calendar", "Slack / Email"). Each panel has
             a short label and a short body line.

Style is bright, flat, high-contrast — designed to stop the scroll
in a professional LinkedIn feed without being childish or crude.
"""
import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("ERROR: Pillow not installed. Run: pip install Pillow")

CANVAS = 1080
PADDING = 80

PALETTES = {
    "lemon":   {"bg": (253, 224, 71),  "ink": (15, 15, 15),    "accent": (15, 15, 15)},
    "electric":{"bg": (37, 99, 235),   "ink": (255, 255, 255), "accent": (253, 224, 71)},
    "coral":   {"bg": (251, 113, 133), "ink": (15, 15, 15),    "accent": (15, 15, 15)},
    "mint":    {"bg": (167, 243, 208), "ink": (15, 15, 15),    "accent": (6, 95, 70)},
    "paper":   {"bg": (250, 248, 244), "ink": (15, 15, 15),    "accent": (37, 99, 235)},
    "ink":     {"bg": (15, 15, 15),    "ink": (255, 255, 255), "accent": (253, 224, 71)},
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


def load_font(candidates, size):
    for p in candidates:
        if Path(p).is_file():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def wrap(draw, text, font, max_width):
    words = text.split()
    lines, cur = [], []
    for w in words:
        if draw.textlength(" ".join(cur + [w]), font=font) <= max_width:
            cur.append(w)
        else:
            if cur:
                lines.append(" ".join(cur))
            cur = [w]
            if draw.textlength(w, font=font) > max_width:
                lines.append(w)
                cur = []
    if cur:
        lines.append(" ".join(cur))
    return lines


def fit_text(draw, text, font_candidates, max_w, max_h, size_range):
    for size in size_range:
        font = load_font(font_candidates, size)
        lines = wrap(draw, text, font, max_w)
        bbox = draw.textbbox((0, 0), "Hg", font=font)
        line_h = (bbox[3] - bbox[1]) * 1.22
        total_h = line_h * len(lines)
        widths_ok = all(draw.textlength(ln, font=font) <= max_w for ln in lines)
        if total_h <= max_h and widths_ok:
            return font, lines, line_h
    return font, lines, line_h


def draw_block(draw, lines, font, line_h, x, y_top, max_w, color, align="center"):
    y = y_top
    for ln in lines:
        if align == "center":
            w = draw.textlength(ln, font=font)
            draw.text((x + (max_w - w) // 2, y), ln, font=font, fill=color)
        else:
            draw.text((x, y), ln, font=font, fill=color)
        y += line_h
    return y


def render_caption(args, palette):
    img = Image.new("RGB", (CANVAS, CANVAS), palette["bg"])
    draw = ImageDraw.Draw(img)

    if args.tag:
        tag_font = load_font(FONT_BOLD_CANDIDATES, 28)
        draw.text((PADDING, PADDING), args.tag.upper().strip(),
                  font=tag_font, fill=palette["accent"])

    max_w = CANVAS - 2 * PADDING

    setup_block = None
    setup_h = 0
    if args.setup:
        setup_font, setup_lines, setup_lh = fit_text(
            draw, args.setup, FONT_REG_CANDIDATES,
            max_w, 260, range(48, 26, -2),
        )
        setup_h = int(setup_lh * len(setup_lines))
        setup_block = (setup_lines, setup_font, setup_lh)

    punch_max_h = CANVAS - 2 * PADDING - setup_h - (80 if setup_block else 0)
    punch_font, punch_lines, punch_lh = fit_text(
        draw, args.headline, FONT_BOLD_CANDIDATES,
        max_w, punch_max_h, range(160, 48, -4),
    )
    punch_h = punch_lh * len(punch_lines)

    total = setup_h + (60 if setup_block else 0) + punch_h
    y_top = (CANVAS - total) // 2

    if setup_block:
        lines, font, lh = setup_block
        y_top = draw_block(draw, lines, font, lh, PADDING, y_top, max_w,
                           palette["ink"], align="center")
        y_top += 60

    draw_block(draw, punch_lines, punch_font, punch_lh, PADDING, y_top,
               max_w, palette["ink"], align="center")

    draw.rectangle(
        [PADDING, CANVAS - PADDING - 6, PADDING + 120, CANVAS - PADDING],
        fill=palette["accent"],
    )
    if args.footer:
        f_font = load_font(FONT_REG_CANDIDATES, 22)
        draw.text((PADDING + 140, CANVAS - PADDING - 16),
                  args.footer, font=f_font, fill=palette["ink"])
    return img


def render_two_panel(args, palette):
    if not args.panel_a or not args.panel_b:
        sys.exit("ERROR: --panel-a and --panel-b are required for --style two-panel.")

    img = Image.new("RGB", (CANVAS, CANVAS), palette["bg"])
    draw = ImageDraw.Draw(img)

    divider_y = CANVAS // 2
    draw.rectangle([0, divider_y - 3, CANVAS, divider_y + 3], fill=palette["accent"])

    label_font = load_font(FONT_BOLD_CANDIDATES, 30)
    max_w = CANVAS - 2 * PADDING

    def render_panel(label, body, y_top, y_bottom):
        draw.text((PADDING, y_top + 32), label.upper().strip(),
                  font=label_font, fill=palette["accent"])
        body_top = y_top + 32 + 50
        body_h = y_bottom - body_top - 40
        font, lines, lh = fit_text(
            draw, body, FONT_BOLD_CANDIDATES,
            max_w, body_h, range(110, 36, -4),
        )
        total_h = lh * len(lines)
        y = body_top + (body_h - total_h) // 2
        draw_block(draw, lines, font, lh, PADDING, y, max_w,
                   palette["ink"], align="center")

    render_panel(args.label_a or "A", args.panel_a, 0, divider_y)
    render_panel(args.label_b or "B", args.panel_b, divider_y, CANVAS)

    if args.tag:
        tag_font = load_font(FONT_BOLD_CANDIDATES, 22)
        tag_w = draw.textlength(args.tag.upper(), font=tag_font)
        draw.text((CANVAS - PADDING - tag_w, PADDING - 32),
                  args.tag.upper().strip(),
                  font=tag_font, fill=palette["accent"])
    return img


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--style", choices=["caption", "two-panel"], default="caption")
    p.add_argument("--palette", default="lemon", choices=sorted(PALETTES.keys()))
    p.add_argument("--headline", default="",
                   help="Caption-style: the punchline. Big bold text in the center.")
    p.add_argument("--setup", default="",
                   help="Caption-style: optional smaller setup line above the punchline.")
    p.add_argument("--label-a", default="",
                   help="Two-panel: short label for the top panel (e.g. 'My calendar').")
    p.add_argument("--panel-a", default="",
                   help="Two-panel: body line for the top panel.")
    p.add_argument("--label-b", default="",
                   help="Two-panel: short label for the bottom panel (e.g. 'Reality').")
    p.add_argument("--panel-b", default="",
                   help="Two-panel: body line for the bottom panel.")
    p.add_argument("--tag", default="",
                   help="Optional small uppercase tag (e.g. 'MEETINGS', 'INBOX LIFE').")
    p.add_argument("--footer", default="",
                   help="Optional small text near the bottom (caption-style only).")
    p.add_argument("--output", required=True)
    args = p.parse_args()

    palette = PALETTES[args.palette]

    if args.style == "caption":
        if not args.headline:
            sys.exit("ERROR: --headline is required for --style caption.")
        img = render_caption(args, palette)
    else:
        img = render_two_panel(args, palette)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({CANVAS}x{CANVAS}, style={args.style}, palette={args.palette})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
