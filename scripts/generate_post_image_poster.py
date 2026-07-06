#!/usr/bin/env python3
"""poster — brutalist Swiss stat-poster carousel style (option5).

One script, every slide kind via --kind:
  cover   — brand tag, kicker, ONE giant stat, bold statement, thick rule
  content — big accent stat/number, bold cream statement, thin support line
  action  — "What CTROs are doing now" + big numbered bold list
  dark    — the closer: flips to a full ACCENT field with ink text (stands out)

Visual language: near-black field, cream text, one hot accent. Type is the
graphic — oversized numbers, minimal chrome. Maximum scroll-stop.
"""
import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("ERROR: Pillow not installed. Run: pip install Pillow")

CANVAS = 1080
DJ = "/usr/share/fonts/truetype/dejavu/"
LB = "/usr/share/fonts/truetype/liberation/"
SANS_B = [DJ + "DejaVuSans-Bold.ttf", LB + "LiberationSans-Bold.ttf"]

_PALETTES = {
    "coral-dark":   dict(bg=(24, 24, 28), cream=(244, 238, 226), acc=(230, 96, 66), mut=(150, 146, 138)),
    "mustard-dark": dict(bg=(26, 26, 24), cream=(245, 240, 228), acc=(224, 168, 60), mut=(150, 148, 138)),
    "teal-dark":    dict(bg=(20, 26, 28), cream=(236, 242, 240), acc=(64, 176, 160), mut=(138, 150, 148)),
}
BG = CREAM = ACC = MUT = None


def _apply_palette(name):
    global BG, CREAM, ACC, MUT
    p = _PALETTES.get(name, _PALETTES["coral-dark"])
    BG, CREAM, ACC, MUT = p["bg"], p["cream"], p["acc"], p["mut"]


def font(cands, size):
    for p in cands:
        if Path(p).is_file():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def track(t, n=2):
    return (" " * n).join(t.upper())


def parse_slide(s):
    if not s or "/" not in s:
        return None, None
    a, b = s.split("/", 1)
    try:
        return int(a), int(b)
    except ValueError:
        return None, None


def lines_of(text):
    return [ln.strip() for ln in text.split("\\n")]


def fit(draw, text, max_w, max_h, hi, lo, lh_mult=1.06, step=4):
    raw = lines_of(text)
    f = font(SANS_B, lo)
    lh = lo * lh_mult
    for size in range(hi, lo - 1, -step):
        f = font(SANS_B, size)
        if not all(draw.textlength(ln, font=f) <= max_w for ln in raw if ln):
            continue
        bb = draw.textbbox((0, 0), "Hg", font=f)
        lh = (bb[3] - bb[1]) * lh_mult
        if lh * len(raw) <= max_h:
            return f, raw, lh
    return f, raw, lh


PAD = 86


def brand(d, tag, fg):
    d.text((PAD, 80), track(tag, 4), font=font(SANS_B, 24), fill=fg)
    d.rectangle([PAD, 124, PAD + 70, 130], fill=ACC)


def footer(d, source, slide, fg):
    if source:
        d.text((PAD, CANVAS - 108), track(source, 2), font=font(SANS_B, 20), fill=fg)
    sn, st = parse_slide(slide)
    if sn is not None:
        sc = track(f"{sn:02d} / {st:02d}", 2)
        sw = d.textlength(sc, font=font(SANS_B, 20))
        d.text((CANVAS - PAD - sw, CANVAS - 108), sc, font=font(SANS_B, 20), fill=fg)


def render_cover(a):
    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    d = ImageDraw.Draw(img)
    brand(d, a.tag, CREAM)
    if a.kicker:
        d.text((PAD, 190), track(a.kicker, 2), font=font(SANS_B, 26), fill=MUT)
    # giant stat
    stat = a.stat or a.title or "1 in 3"
    sf, slines, slh = fit(d, stat, CANVAS - 2 * PAD, 260, 210, 96)
    d.text((PAD - 8, 250), slines[0], font=sf, fill=ACC)
    # statement
    sy = 520
    tf, tlines, tlh = fit(d, a.subtitle or a.title, CANVAS - 2 * PAD, 200, 62, 40)
    for i, ln in enumerate(tlines):
        d.text((PAD, sy + i * tlh), ln, font=tf, fill=CREAM)
    ry = sy + len(tlines) * tlh + 34
    d.rectangle([PAD, ry, CANVAS - PAD, ry + 12], fill=ACC)
    footer(d, a.source, a.slide, MUT)
    return img


def render_content(a):
    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    d = ImageDraw.Draw(img)
    sn, st = parse_slide(a.slide)
    if sn:
        d.text((PAD, 88), track(f"{sn:02d}", 2), font=font(SANS_B, 30), fill=MUT)
    yy = 180
    stat = a.stat.strip()
    if stat:
        sf, slines, slh = fit(d, stat, CANVAS - 2 * PAD, 220, 168, 90)
        d.text((PAD - 6, yy), slines[0], font=sf, fill=ACC)
        yy += slh + 30
    else:
        yy = 250
    hf, hlines, hlh = fit(d, a.headline, CANVAS - 2 * PAD, 260, 78, 46)
    for i, ln in enumerate(hlines):
        d.text((PAD, yy + i * hlh), ln, font=hf, fill=CREAM)
    yy = yy + len(hlines) * hlh + 26
    if a.bold.strip():
        bf, blines, blh = fit(d, a.bold, CANVAS - 2 * PAD, 160, 50, 32)
        for ln in blines:
            d.text((PAD, yy), ln, font=bf, fill=ACC)
            yy += blh
    footer(d, a.source, a.slide, MUT)
    return img


def render_action(a):
    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    d = ImageDraw.Draw(img)
    d.text((PAD, 100), track(a.kicker or "What CTROs are doing now", 2),
           font=font(SANS_B, 28), fill=ACC)
    d.rectangle([PAD, 152, CANVAS - PAD, 160], fill=ACC)
    items = [ln for ln in lines_of(a.lead) if ln]
    yy = 230
    for i, it in enumerate(items[:5], 1):
        d.text((PAD, yy), str(i), font=font(SANS_B, 54), fill=ACC)
        d.text((PAD + 78, yy + 8), it, font=font(SANS_B, 40), fill=CREAM)
        yy += 110
    footer(d, a.source, a.slide, MUT)
    return img


def render_dark(a):
    # the closer flips to a full accent field with ink text
    img = Image.new("RGB", (CANVAS, CANVAS), ACC)
    d = ImageDraw.Draw(img)
    ink = BG
    d.text((PAD, 100), track(a.kicker or "The takeaway", 3), font=font(SANS_B, 26), fill=ink)
    d.rectangle([PAD, 152, PAD + 90, 160], fill=ink)
    yy = 300
    hf, hlines, hlh = fit(d, a.headline, CANVAS - 2 * PAD, 300, 96, 52)
    for i, ln in enumerate(hlines):
        d.text((PAD, yy + i * hlh), ln, font=hf, fill=ink)
    yy = yy + len(hlines) * hlh + 24
    if a.bold.strip():
        bf, blines, blh = fit(d, a.bold, CANVAS - 2 * PAD, 180, 56, 34)
        for ln in blines:
            d.text((PAD, yy), ln, font=bf, fill=CREAM)
            yy += blh
    footer(d, a.source, a.slide, ink)
    return img


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--kind", default="content", choices=["cover", "content", "action", "dark"])
    p.add_argument("--palette", default="coral-dark", choices=list(_PALETTES))
    p.add_argument("--tag", default="CTRO")
    p.add_argument("--kicker", default="")
    p.add_argument("--stat", default="")
    p.add_argument("--title", default="")
    p.add_argument("--subtitle", default="")
    p.add_argument("--headline", default="")
    p.add_argument("--lead", default="")
    p.add_argument("--bold", default="")
    p.add_argument("--source", default="")
    p.add_argument("--slide", default="")
    p.add_argument("--output", required=True)
    a = p.parse_args()
    _apply_palette(a.palette)
    if a.kind == "cover":
        img = render_cover(a)
    elif a.kind == "action":
        img = render_action(a)
    elif a.kind == "dark":
        img = render_dark(a)
    else:
        img = render_content(a)
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
