#!/usr/bin/env python3
"""broadsheet — serif editorial / newspaper carousel style (option4).

One script renders every slide kind via --kind:
  cover   — masthead rules, big serif headline, italic deck, body teaser
  content — section label + rule, serif headline, italic lead + bold payoff
  action  — section label, "What CTROs are doing now", numbered serif list
  dark    — the single dark slide: ink field, cream serif, red accent close

Visual language: warm off-white, near-black serif, one editorial-red accent.
No icons, no color blocks, no photos — the type and the rules do the work.
"""
import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("ERROR: Pillow not installed. Run: pip install Pillow")

CANVAS = 1080
LB = "/usr/share/fonts/truetype/liberation/"
DJ = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = [LB + "LiberationSerif-Bold.ttf", DJ + "DejaVuSerif-Bold.ttf"]
SERIF_R = [LB + "LiberationSerif-Regular.ttf", DJ + "DejaVuSerif.ttf"]
SERIF_I = [LB + "LiberationSerif-Italic.ttf", DJ + "DejaVuSerif.ttf"]

_PALETTES = {
    "classic-red": dict(bg=(250, 247, 240), ink=(26, 24, 22), acc=(150, 45, 35), mut=(120, 110, 98)),
    "ink-blue":    dict(bg=(247, 247, 243), ink=(22, 26, 34), acc=(38, 74, 120), mut=(110, 116, 128)),
    "forest":      dict(bg=(246, 245, 236), ink=(24, 30, 26), acc=(52, 96, 66), mut=(112, 118, 108)),
}
BG = INK = ACC = MUT = None


def _apply_palette(name):
    global BG, INK, ACC, MUT
    p = _PALETTES.get(name, _PALETTES["classic-red"])
    BG, INK, ACC, MUT = p["bg"], p["ink"], p["acc"], p["mut"]


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


def fit_serif(draw, text, cands, max_w, max_h, hi, lo, lh_mult=1.08, step=3):
    raw = lines_of(text)
    f = font(cands, lo)
    lh = lo * lh_mult
    for size in range(hi, lo - 1, -step):
        f = font(cands, size)
        if not all(draw.textlength(ln, font=f) <= max_w for ln in raw if ln):
            continue
        bb = draw.textbbox((0, 0), "Hg", font=f)
        lh = (bb[3] - bb[1]) * lh_mult
        if lh * len(raw) <= max_h:
            return f, raw, lh
    return f, raw, lh


PAD = 90


def draw_masthead(draw, tag, kicker, no):
    y = 88
    mast = font(SERIF_R, 22)
    t = track(tag, 3)
    w = draw.textlength(t, font=mast)
    draw.line([(PAD, y), (CANVAS - PAD, y)], fill=INK, width=3)
    draw.text(((CANVAS - w) / 2, y + 16), t, font=mast, fill=INK)
    y2 = y + 16 + 34
    draw.line([(PAD, y2), (CANVAS - PAD, y2)], fill=INK, width=1)
    if kicker:
        draw.text((PAD, y2 + 22), kicker, font=font(SERIF_I, 24), fill=ACC)
    if no:
        nt = track(no, 2)
        nw = draw.textlength(nt, font=font(SERIF_R, 20))
        draw.text((CANVAS - PAD - nw, y2 + 26), nt, font=font(SERIF_R, 20), fill=MUT)
    return y2 + 22 + 44


def draw_footer(draw, source, slide, dark=False):
    line_c = (238, 232, 220) if dark else INK
    mut = (150, 142, 128) if dark else MUT
    draw.line([(PAD, CANVAS - 120), (CANVAS - PAD, CANVAS - 120)], fill=line_c, width=1)
    if source:
        draw.text((PAD, CANVAS - 104), track(source, 2), font=font(SERIF_R, 19), fill=mut)
    sn, st = parse_slide(slide)
    if sn is not None:
        sc = track(f"{sn:02d} / {st:02d}", 2)
        sw = draw.textlength(sc, font=font(SERIF_R, 19))
        draw.text((CANVAS - PAD - sw, CANVAS - 104), sc, font=font(SERIF_R, 19), fill=mut)


def render_cover(a):
    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    d = ImageDraw.Draw(img)
    top = draw_masthead(d, a.tag, a.kicker or "Transformation Brief", a.no or "")
    hy = top + 34
    hf, hlines, hlh = fit_serif(d, a.title, SERIF_B, CANVAS - 2 * PAD, 340, 100, 60)
    for i, ln in enumerate(hlines):
        d.text((PAD, hy + i * hlh), ln, font=hf, fill=INK)
    hy2 = hy + len(hlines) * hlh + 8
    d.line([(PAD, hy2), (PAD + 140, hy2)], fill=ACC, width=4)
    yy = hy2 + 30
    if a.subtitle.strip():
        sf, slines, slh = fit_serif(d, a.subtitle, SERIF_I, CANVAS - 2 * PAD, 150, 42, 26, 1.25)
        for ln in slines:
            d.text((PAD, yy), ln, font=sf, fill=MUT)
            yy += slh
        yy += 26
    if a.body.strip():
        bf, blines, blh = fit_serif(d, a.body, SERIF_R, CANVAS - 2 * PAD, 220, 28, 22, 1.4)
        for ln in blines:
            d.text((PAD, yy), ln, font=bf, fill=INK)
            yy += blh
    draw_footer(d, a.source, a.slide)
    return img


def render_content(a, dark=False):
    bg = INK if dark else BG
    ink = BG if dark else INK
    mut = (168, 160, 146) if dark else MUT
    img = Image.new("RGB", (CANVAS, CANVAS), bg)
    d = ImageDraw.Draw(img)
    # section label + rule
    label = a.kicker or ("The Takeaway" if dark else "Section")
    sn, st = parse_slide(a.slide)
    lab = track(label if dark else f"{label}  {sn:02d}" if sn else label, 3)
    d.text((PAD, 118), lab, font=font(SERIF_R, 24), fill=ACC)
    d.line([(PAD, 168), (CANVAS - PAD, 168)], fill=ink, width=2)
    # headline
    hy = 250
    hf, hlines, hlh = fit_serif(d, a.headline, SERIF_B, CANVAS - 2 * PAD, 300, 88, 52)
    for i, ln in enumerate(hlines):
        d.text((PAD, hy + i * hlh), ln, font=hf, fill=ink)
    yy = hy + len(hlines) * hlh + 40
    if a.lead.strip():
        lf, llines, llh = fit_serif(d, a.lead, SERIF_I, CANVAS - 2 * PAD, 180, 40, 26, 1.3)
        for ln in llines:
            d.text((PAD, yy), ln, font=lf, fill=mut)
            yy += llh
        yy += 8
    if a.bold.strip():
        bf, blines, blh = fit_serif(d, a.bold, SERIF_B, CANVAS - 2 * PAD, 200, 46, 30, 1.2)
        for ln in blines:
            d.text((PAD, yy), ln, font=bf, fill=ink)
            yy += blh
    draw_footer(d, a.source, a.slide, dark=dark)
    return img


def render_action(a):
    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    d = ImageDraw.Draw(img)
    lab = track(a.kicker or "What CTROs are doing now", 3)
    d.text((PAD, 118), lab, font=font(SERIF_R, 24), fill=ACC)
    d.line([(PAD, 168), (CANVAS - PAD, 168)], fill=INK, width=2)
    items = [ln for ln in lines_of(a.lead) if ln]
    yy = 250
    numf = font(SERIF_B, 40)
    itf = font(SERIF_R, 38)
    for i, it in enumerate(items[:5], 1):
        d.text((PAD, yy), f"{i}.", font=numf, fill=ACC)
        d.text((PAD + 66, yy + 2), it, font=itf, fill=INK)
        yy += 92
    draw_footer(d, a.source, a.slide)
    return img


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--kind", default="content", choices=["cover", "content", "action", "dark"])
    p.add_argument("--palette", default="classic-red", choices=list(_PALETTES))
    p.add_argument("--tag", default="The CTRO Read")
    p.add_argument("--kicker", default="")
    p.add_argument("--no", default="")
    p.add_argument("--title", default="")
    p.add_argument("--subtitle", default="")
    p.add_argument("--body", default="")
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
        img = render_content(a, dark=True)
    else:
        img = render_content(a, dark=False)
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
