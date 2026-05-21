#!/usr/bin/env python3
"""Generate LinkedIn-native humour visuals (1080x1080 PNG).

Three styles, each a polished UI / data-viz mockup where the joke IS the
content. No copyrighted images, no Reddit-meme aesthetic. Designed for a
professional LinkedIn feed.

  calendar  Outlook/Google Calendar single-day view with absurd entries.
            One event can be highlighted as the punchline.

  chat      Slack/Teams-style chat thread. Messages, a "typing..."
            indicator, and an emoji reaction on the last message.

  chart     Sarah-Cooper-style horizontal bar chart where the data
            labels carry the joke (e.g. word counts, time spent).
"""
import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("ERROR: Pillow not installed. Run: pip install Pillow")

CANVAS = 1080
PADDING = 64

BG = (250, 250, 251)
SURFACE = (255, 255, 255)
INK = (15, 23, 42)
MUTED = (100, 116, 139)
LINE = (226, 232, 240)
ACCENT_BLUE = (37, 99, 235)
ACCENT_RED = (220, 38, 38)
ACCENT_YELLOW = (250, 204, 21)
ACCENT_GREEN = (34, 197, 94)
EVENT_FILL = (219, 234, 254)
EVENT_INK = (30, 58, 138)

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
EMOJI_FONT_PATH = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

# Regex matches the unicode ranges Noto Color Emoji can render.
import re
EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001F6FF"
    "\U0001F900-\U0001F9FF"
    "\U0001FA70-\U0001FAFF"
    "☀-➿"
    "]"
)


def render_emoji(text, target_h):
    """Render an emoji-only string to a transparent PNG at target_h px tall.

    Noto Color Emoji is a fixed-size bitmap font (only loads at size=109),
    so we render at native size and scale down.
    """
    if not Path(EMOJI_FONT_PATH).is_file():
        return None
    try:
        font = ImageFont.truetype(EMOJI_FONT_PATH, size=109)
    except OSError:
        return None
    tmp = Image.new("RGBA", (140 * len(text), 140), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    d.text((0, 0), text, font=font, embedded_color=True)
    bbox = tmp.getbbox()
    if not bbox:
        return None
    cropped = tmp.crop(bbox)
    scale = target_h / cropped.height
    new_w = max(1, int(cropped.width * scale))
    return cropped.resize((new_w, target_h), Image.LANCZOS)


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
    if cur:
        lines.append(" ".join(cur))
    return lines


def rounded_rect(draw, box, radius, fill=None, outline=None, width=1):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle((x0, y0, x1, y1), radius=radius,
                           fill=fill, outline=outline, width=width)


def render_calendar(args):
    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    draw = ImageDraw.Draw(img)

    rounded_rect(draw, (PADDING, PADDING, CANVAS - PADDING, CANVAS - PADDING),
                 radius=18, fill=SURFACE)

    day_label = args.day or "Today"
    title_font = load_font(FONT_BOLD_CANDIDATES, 36)
    sub_font = load_font(FONT_REG_CANDIDATES, 22)
    draw.text((PADDING + 32, PADDING + 28), day_label, font=title_font, fill=INK)
    if args.subtitle:
        draw.text((PADDING + 32, PADDING + 76), args.subtitle,
                  font=sub_font, fill=MUTED)

    header_bottom = PADDING + 130
    draw.line([(PADDING + 24, header_bottom),
               (CANVAS - PADDING - 24, header_bottom)],
              fill=LINE, width=2)

    events = args.event or []
    if not events:
        sys.exit("ERROR: calendar style needs --event entries.")

    time_col_x = PADDING + 32
    event_col_x = PADDING + 160
    event_col_w = CANVAS - PADDING - 32 - event_col_x

    body_top = header_bottom + 28
    body_bottom = CANVAS - PADDING - 32
    body_h = body_bottom - body_top
    row_h = body_h / len(events)

    time_font = load_font(FONT_BOLD_CANDIDATES, 22)
    event_font = load_font(FONT_BOLD_CANDIDATES, 26)
    event_sub_font = load_font(FONT_REG_CANDIDATES, 20)

    for i, ev in enumerate(events):
        if "|" not in ev:
            sys.exit(f"ERROR: --event must be 'TIME|TITLE' (got {ev!r}).")
        time_part, title_part = ev.split("|", 1)
        y_top = body_top + i * row_h
        y_bot = body_top + (i + 1) * row_h - 8

        if i + 1 < len(events):
            draw.line([(time_col_x, y_bot + 4),
                       (CANVAS - PADDING - 32, y_bot + 4)],
                      fill=LINE, width=1)

        draw.text((time_col_x, y_top + 14), time_part.strip(),
                  font=time_font, fill=MUTED)

        is_highlight = (args.highlight is not None
                        and (i + 1) == args.highlight)
        if is_highlight:
            fill = (254, 240, 138)
            outline = (202, 138, 4)
            text_ink = (113, 63, 18)
        else:
            fill = EVENT_FILL
            outline = None
            text_ink = EVENT_INK

        rounded_rect(draw,
                     (event_col_x, y_top + 6,
                      event_col_x + event_col_w, y_bot - 4),
                     radius=10, fill=fill,
                     outline=outline, width=3 if outline else 1)

        title_text = title_part.strip()
        title_lines = wrap(draw, title_text, event_font,
                           event_col_w - 28)
        ty = y_top + 18
        for ln in title_lines[:2]:
            draw.text((event_col_x + 16, ty), ln,
                      font=event_font, fill=text_ink)
            ty += 32

    if args.footer:
        f_font = load_font(FONT_REG_CANDIDATES, 18)
        f_w = draw.textlength(args.footer, font=f_font)
        draw.text(((CANVAS - f_w) / 2, CANVAS - PADDING + 24),
                  args.footer, font=f_font, fill=MUTED)

    return img


def render_chat(args):
    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    draw = ImageDraw.Draw(img)

    rounded_rect(draw, (PADDING, PADDING, CANVAS - PADDING, CANVAS - PADDING),
                 radius=18, fill=SURFACE)

    channel = args.channel or "#general"
    title_font = load_font(FONT_BOLD_CANDIDATES, 30)
    draw.text((PADDING + 32, PADDING + 28), channel,
              font=title_font, fill=INK)
    header_bottom = PADDING + 90
    draw.line([(PADDING + 24, header_bottom),
               (CANVAS - PADDING - 24, header_bottom)],
              fill=LINE, width=2)

    messages = args.message or []
    if not messages:
        sys.exit("ERROR: chat style needs --message entries.")

    name_font = load_font(FONT_BOLD_CANDIDATES, 22)
    time_font = load_font(FONT_REG_CANDIDATES, 18)
    body_font = load_font(FONT_REG_CANDIDATES, 26)
    typing_font = load_font(FONT_REG_CANDIDATES, 22)
    reaction_font = load_font(FONT_REG_CANDIDATES, 22)

    y = header_bottom + 28
    x_left = PADDING + 32
    max_w = CANVAS - 2 * PADDING - 64

    avatar_colors = [
        (37, 99, 235), (220, 38, 38), (34, 197, 94),
        (250, 204, 21), (147, 51, 234),
    ]

    for i, msg in enumerate(messages):
        parts = msg.split("|", 2)
        if len(parts) < 3:
            sys.exit(f"ERROR: --message must be 'NAME|TIME|BODY' (got {msg!r}).")
        name, ts, body = parts[0].strip(), parts[1].strip(), parts[2].strip()

        avatar_color = avatar_colors[i % len(avatar_colors)]
        draw.rounded_rectangle(
            (x_left, y, x_left + 40, y + 40), radius=6, fill=avatar_color)
        initial_font = load_font(FONT_BOLD_CANDIDATES, 22)
        initial = name[:1].upper() or "?"
        iw = draw.textlength(initial, font=initial_font)
        draw.text((x_left + (40 - iw) / 2, y + 6),
                  initial, font=initial_font, fill=SURFACE)

        text_x = x_left + 56
        draw.text((text_x, y - 2), name, font=name_font, fill=INK)
        name_w = draw.textlength(name, font=name_font)
        draw.text((text_x + name_w + 12, y + 4), ts,
                  font=time_font, fill=MUTED)

        emoji_only = EMOJI_RE.fullmatch(body) is not None
        if emoji_only:
            emoji_img = render_emoji(body, target_h=64)
            if emoji_img is not None:
                img.paste(emoji_img, (text_x, y + 28), emoji_img)
                by = y + 28 + 64
            else:
                draw.text((text_x, y + 30), body, font=body_font, fill=INK)
                by = y + 30 + 34
        else:
            body_lines = wrap(draw, body, body_font, max_w - 56)
            by = y + 30
            for ln in body_lines:
                draw.text((text_x, by), ln, font=body_font, fill=INK)
                by += 34

        if (args.reaction_on is not None
                and (i + 1) == args.reaction_on
                and args.reaction):
            r_pad = 8
            r_w = draw.textlength(args.reaction, font=reaction_font) + 2 * r_pad + 16
            r_h = 32
            r_x = text_x
            r_y = by + 4
            rounded_rect(draw,
                         (r_x, r_y, r_x + r_w, r_y + r_h),
                         radius=14,
                         fill=(241, 245, 249),
                         outline=LINE, width=1)
            draw.text((r_x + r_pad, r_y + 4),
                      args.reaction, font=reaction_font, fill=INK)
            by += r_h + 8

        y = by + 18

    if args.typing:
        t_x = x_left + 56
        draw.ellipse((t_x - 28, y + 6, t_x - 12, y + 22), fill=MUTED)
        draw.ellipse((t_x - 6, y + 6, t_x + 10, y + 22), fill=MUTED)
        draw.ellipse((t_x + 16, y + 6, t_x + 32, y + 22), fill=MUTED)
        draw.text((t_x + 56, y + 4), args.typing,
                  font=typing_font, fill=MUTED)

    composer_top = CANVAS - PADDING - 100
    composer_left = PADDING + 32
    composer_right = CANVAS - PADDING - 32
    rounded_rect(draw,
                 (composer_left, composer_top,
                  composer_right, composer_top + 64),
                 radius=12, fill=SURFACE, outline=LINE, width=2)
    placeholder = args.composer_placeholder or f"Message {channel}"
    p_font = load_font(FONT_REG_CANDIDATES, 22)
    draw.text((composer_left + 18, composer_top + 18),
              placeholder, font=p_font, fill=MUTED)
    btn_r = 18
    btn_cx = composer_right - 32
    btn_cy = composer_top + 32
    draw.ellipse((btn_cx - btn_r, btn_cy - btn_r,
                  btn_cx + btn_r, btn_cy + btn_r),
                 fill=ACCENT_BLUE)
    draw.polygon([(btn_cx - 8, btn_cy - 8),
                  (btn_cx + 10, btn_cy),
                  (btn_cx - 8, btn_cy + 8)],
                 fill=SURFACE)

    return img


def render_chart(args):
    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    draw = ImageDraw.Draw(img)

    rounded_rect(draw, (PADDING, PADDING, CANVAS - PADDING, CANVAS - PADDING),
                 radius=18, fill=SURFACE)

    title = args.chart_title or ""
    sub = args.subtitle or ""
    title_font = load_font(FONT_BOLD_CANDIDATES, 38)
    sub_font = load_font(FONT_REG_CANDIDATES, 22)

    inner_left = PADDING + 40
    inner_right = CANVAS - PADDING - 40
    inner_w = inner_right - inner_left

    title_lines = wrap(draw, title, title_font, inner_w)
    ty = PADDING + 36
    for ln in title_lines[:3]:
        draw.text((inner_left, ty), ln, font=title_font, fill=INK)
        ty += 46

    if sub:
        ty += 6
        sub_lines = wrap(draw, sub, sub_font, inner_w)
        for ln in sub_lines[:2]:
            draw.text((inner_left, ty), ln, font=sub_font, fill=MUTED)
            ty += 28

    bars = args.bar or []
    if not bars:
        sys.exit("ERROR: chart style needs --bar entries.")

    parsed = []
    for b in bars:
        if "|" not in b:
            sys.exit(f"ERROR: --bar must be 'LABEL|VALUE' (got {b!r}).")
        label, val = b.split("|", 1)
        try:
            num = float(val.strip().replace(",", ""))
        except ValueError:
            sys.exit(f"ERROR: --bar value must be numeric (got {val!r}).")
        parsed.append((label.strip(), num, val.strip()))

    max_val = max(p[1] for p in parsed) or 1
    label_font = load_font(FONT_BOLD_CANDIDATES, 26)
    value_font = load_font(FONT_BOLD_CANDIDATES, 30)

    chart_top = ty + 30
    chart_bottom = CANVAS - PADDING - 60
    chart_h = chart_bottom - chart_top
    row_h = chart_h / len(parsed)
    bar_h = min(row_h - 40, 60)

    label_col_w = max(draw.textlength(p[0], font=label_font) for p in parsed) + 20
    label_col_w = min(label_col_w, inner_w * 0.32)
    bar_x = inner_left + label_col_w + 16
    bar_max_w = inner_right - bar_x - 100

    highlight_idx = args.highlight
    for i, (label, num, val_str) in enumerate(parsed):
        cy = chart_top + i * row_h + (row_h - bar_h) / 2
        draw.text((inner_left, cy + (bar_h - 30) / 2), label,
                  font=label_font, fill=INK)

        w = max(8, bar_max_w * (num / max_val))
        is_hl = (highlight_idx is not None and (i + 1) == highlight_idx)
        fill = ACCENT_RED if is_hl else ACCENT_BLUE
        rounded_rect(draw, (bar_x, cy, bar_x + w, cy + bar_h),
                     radius=6, fill=fill)
        draw.text((bar_x + w + 12, cy + (bar_h - 34) / 2),
                  val_str, font=value_font, fill=INK)

    if args.footer:
        f_font = load_font(FONT_REG_CANDIDATES, 18)
        f_w = draw.textlength(args.footer, font=f_font)
        draw.text(((CANVAS - f_w) / 2, CANVAS - PADDING - 36),
                  args.footer, font=f_font, fill=MUTED)

    return img


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--style", required=True,
                   choices=["calendar", "chat", "chart"])
    p.add_argument("--day", default="", help="calendar: day header text.")
    p.add_argument("--subtitle", default="",
                   help="calendar/chart: small subtitle line.")
    p.add_argument("--event", action="append",
                   help="calendar: event row, 'TIME|TITLE'. Repeatable.")
    p.add_argument("--highlight", type=int, default=None,
                   help="calendar/chart: 1-based index of the event/bar to highlight.")
    p.add_argument("--channel", default="",
                   help="chat: channel or DM header.")
    p.add_argument("--message", action="append",
                   help="chat: message row, 'NAME|TIME|BODY'. Repeatable.")
    p.add_argument("--typing", default="",
                   help="chat: 'typing...' indicator text (e.g. 'Alex is typing... (4 min)').")
    p.add_argument("--reaction", default="",
                   help="chat: reaction text (e.g. '👍 1').")
    p.add_argument("--reaction-on", type=int, default=None,
                   help="chat: 1-based index of the message the reaction attaches to.")
    p.add_argument("--composer-placeholder", default="",
                   help="chat: placeholder text in the composer at the bottom.")
    p.add_argument("--chart-title", default="",
                   help="chart: title text.")
    p.add_argument("--bar", action="append",
                   help="chart: 'LABEL|VALUE'. Repeatable.")
    p.add_argument("--footer", default="",
                   help="optional small footer line.")
    p.add_argument("--output", required=True)
    args = p.parse_args()

    if args.style == "calendar":
        img = render_calendar(args)
    elif args.style == "chat":
        img = render_chat(args)
    else:
        img = render_chart(args)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({CANVAS}x{CANVAS}, style={args.style})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
