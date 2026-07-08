#!/usr/bin/env python3
"""blueprint — monospace analyst-brief carousel style (option6).

One script, every slide kind via --kind:
  cover   — // tag, mono title, a drawn trend chart on graph paper
  content — comment-style label, mono headline, a drawn bar/annotation, payoff
  action  — "$ ctro --do" prompt + mono numbered checklist
  dark    — the single dark slide: terminal field, mono, accent close

Visual language: light graph-paper (or dark terminal for the closer),
monospace throughout, one analytic accent, drawn data marks. Reads like a
strategist's working deck, not a designed template.
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
MONO = [DJ + "DejaVuSansMono.ttf"]
MONO_B = [DJ + "DejaVuSansMono-Bold.ttf"]

_PALETTES = {
    # Muji / earth-tone: warm unbleached graph paper, walnut ink, muted natural
    # accent; the closer is a warm dark-walnut terminal, not a cold near-black.
    "kraft-clay": dict(bg=(227, 218, 201), grid=(207, 197, 178), ink=(58, 50, 42), acc=(166, 98, 66), mut=(124, 114, 100),
                       dbg=(40, 34, 28), dink=(230, 222, 208), dacc=(196, 128, 92), dmut=(140, 128, 112)),
    "oat-sage":   dict(bg=(232, 228, 216), grid=(210, 206, 190), ink=(52, 56, 46), acc=(116, 136, 102), mut=(122, 128, 112),
                       dbg=(34, 38, 30), dink=(228, 230, 216), dacc=(150, 172, 128), dmut=(128, 138, 120)),
    "sand-ochre": dict(bg=(231, 222, 203), grid=(212, 202, 182), ink=(60, 50, 40), acc=(172, 134, 74), mut=(128, 118, 100),
                       dbg=(40, 34, 26), dink=(232, 224, 208), dacc=(204, 166, 100), dmut=(138, 128, 108)),
}
BG = GRID = INK = ACC = MUT = None
DBG = DINK = DACC = DMUT = None


def _apply_palette(name):
    global BG, GRID, INK, ACC, MUT, DBG, DINK, DACC, DMUT
    p = _PALETTES.get(name, _PALETTES["kraft-clay"])
    BG, GRID, INK, ACC, MUT = p["bg"], p["grid"], p["ink"], p["acc"], p["mut"]
    DBG, DINK, DACC, DMUT = p["dbg"], p["dink"], p["dacc"], p["dmut"]


def font(cands, size):
    for p in cands:
        if Path(p).is_file():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


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


def fit(draw, text, cands, max_w, max_h, hi, lo, lh_mult=1.16, step=2):
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


PAD = 80


def grid_bg(bg, grid):
    img = Image.new("RGB", (CANVAS, CANVAS), bg)
    d = ImageDraw.Draw(img)
    for g in range(0, CANVAS, 45):
        d.line([(g, 0), (g, CANVAS)], fill=grid, width=1)
        d.line([(0, g), (CANVAS, g)], fill=grid, width=1)
    return img, d


def draw_trend(d, x0, y0, x1, y1, ink, acc, mut, label, xl, xr, pts):
    d.rectangle([x0, y0, x1, y1], outline=ink, width=2)
    xy = [(x0 + px * (x1 - x0), y0 + py * (y1 - y0)) for px, py in pts]
    d.line(xy, fill=acc, width=5)
    for (px, py) in xy:
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=None, outline=acc, width=4)
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=None)
    d.text((x0 + 8, y0 + 8), label, font=font(MONO, 18), fill=mut)
    d.text((x0 + 8, y1 - 30), xl, font=font(MONO, 18), fill=mut)
    rw = d.textlength(xr, font=font(MONO, 18))
    d.text((x1 - rw - 8, y1 - 30), xr, font=font(MONO, 18), fill=mut)


def draw_bars(d, x0, y0, x1, y1, ink, acc, mut, label, bars):
    # bars: list of (name, frac 0..1)
    d.text((x0, y0 - 30), label, font=font(MONO, 18), fill=mut)
    n = len(bars)
    gap = 18
    bh = (y1 - y0 - gap * (n - 1)) / n
    for i, (nm, fr) in enumerate(bars):
        by = y0 + i * (bh + gap)
        d.rectangle([x0, by, x1, by + bh], outline=GRID, width=1)
        d.rectangle([x0, by, x0 + (x1 - x0) * fr, by + bh], fill=acc)
        d.text((x0 + 12, by + bh / 2 - 12), nm, font=font(MONO_B, 20), fill=ink)
    return


def footer(d, source, slide, ink, mut):
    if source:
        d.text((PAD, CANVAS - 104), f"src: {source}", font=font(MONO, 19), fill=mut)
    sn, st = parse_slide(slide)
    if sn is not None:
        sc = f"[{sn:02d}/{st:02d}]"
        sw = d.textlength(sc, font=font(MONO, 19))
        d.text((CANVAS - PAD - sw, CANVAS - 104), sc, font=font(MONO, 19), fill=mut)


def render_cover(a):
    img, d = grid_bg(BG, GRID)
    d.text((PAD, 78), f"// {a.tag}", font=font(MONO_B, 26), fill=ACC)
    d.text((PAD, 116), a.kicker or "transformation_signal[07]", font=font(MONO, 20), fill=MUT)
    ty = 185
    tf, tlines, tlh = fit(d, a.title, MONO_B, CANVAS - 2 * PAD, 200, 54, 34)
    for i, ln in enumerate(tlines):
        d.text((PAD, ty + i * tlh), ln, font=tf, fill=INK)
    yy = ty + len(tlines) * tlh + 8
    if a.subtitle.strip():
        d.text((PAD, yy), a.subtitle, font=font(MONO, 28), fill=MUT)
    pts = [(0.05, 0.75), (0.28, 0.60), (0.5, 0.55), (0.72, 0.32), (0.95, 0.12)]
    draw_trend(d, PAD, 560, CANVAS - PAD, 880, INK, ACC, MUT,
               a.chartlabel or "signal, % of orgs", a.xl or "'22", a.xr or "'27", pts)
    footer(d, a.source, a.slide, INK, MUT)
    return img


def render_content(a):
    img, d = grid_bg(BG, GRID)
    sn, st = parse_slide(a.slide)
    d.text((PAD, 90), f"# {a.kicker or 'finding'}[{sn:02d}]" if sn else f"# {a.kicker or 'finding'}",
           font=font(MONO, 22), fill=ACC)
    ty = 150
    hf, hlines, hlh = fit(d, a.headline, MONO_B, CANVAS - 2 * PAD, 220, 46, 30)
    for i, ln in enumerate(hlines):
        d.text((PAD, ty + i * hlh), ln, font=hf, fill=INK)
    yy = ty + len(hlines) * hlh + 20
    # optional data mark
    if a.bars:
        bars = []
        for seg in a.bars.split(","):
            if ":" in seg:
                nm, fr = seg.split(":", 1)
                try:
                    bars.append((nm.strip(), max(0.0, min(1.0, float(fr)))))
                except ValueError:
                    pass
        if bars:
            draw_bars(d, PAD, 470, CANVAS - PAD, 470 + 70 * len(bars), INK, ACC, MUT,
                      a.chartlabel or "share", bars)
            yy = 470 + 70 * len(bars) + 60
    if a.lead.strip():
        d.text((PAD, yy), a.lead, font=font(MONO, 26), fill=MUT)
        yy += 44
    if a.bold.strip():
        bf, blines, blh = fit(d, a.bold, MONO_B, CANVAS - 2 * PAD, 160, 34, 24)
        for ln in blines:
            d.text((PAD, yy), ln, font=bf, fill=INK)
            yy += blh
    footer(d, a.source, a.slide, INK, MUT)
    return img


def render_action(a):
    img, d = grid_bg(BG, GRID)
    d.text((PAD, 96), "$ ctro --do", font=font(MONO_B, 30), fill=ACC)
    d.text((PAD, 142), (a.kicker or "what CTROs are doing now").lower(), font=font(MONO, 22), fill=MUT)
    items = [ln for ln in lines_of(a.lead) if ln]
    yy = 230
    for it in items[:5]:
        d.text((PAD, yy), "[x]", font=font(MONO_B, 30), fill=ACC)
        d.text((PAD + 78, yy + 2), it, font=font(MONO, 28), fill=INK)
        yy += 84
    footer(d, a.source, a.slide, INK, MUT)
    return img


def render_dark(a):
    img = Image.new("RGB", (CANVAS, CANVAS), DBG)
    d = ImageDraw.Draw(img)
    d.text((PAD, 96), "$ ctro --conclude", font=font(MONO_B, 28), fill=DACC)
    d.text((PAD, 140), "> " + (a.kicker or "the takeaway").lower(), font=font(MONO, 22), fill=DMUT)
    ty = 300
    hf, hlines, hlh = fit(d, a.headline, MONO_B, CANVAS - 2 * PAD, 240, 48, 30)
    for i, ln in enumerate(hlines):
        d.text((PAD, ty + i * hlh), ln, font=hf, fill=DINK)
    yy = ty + len(hlines) * hlh + 26
    if a.lead.strip():
        d.text((PAD, yy), a.lead, font=font(MONO, 26), fill=DMUT)
        yy += 46
    if a.bold.strip():
        bf, blines, blh = fit(d, a.bold, MONO_B, CANVAS - 2 * PAD, 160, 38, 26)
        for ln in blines:
            d.text((PAD, yy), ln, font=bf, fill=DACC)
            yy += blh
    footer(d, a.source, a.slide, DINK, DMUT)
    return img


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--kind", default="content", choices=["cover", "content", "action", "dark"])
    p.add_argument("--palette", default="kraft-clay", choices=list(_PALETTES))
    p.add_argument("--tag", default="CTRO.brief")
    p.add_argument("--kicker", default="")
    p.add_argument("--title", default="")
    p.add_argument("--subtitle", default="")
    p.add_argument("--headline", default="")
    p.add_argument("--lead", default="")
    p.add_argument("--bold", default="")
    p.add_argument("--bars", default="", help="content data mark: 'name:frac,name:frac' (0..1)")
    p.add_argument("--chartlabel", default="")
    p.add_argument("--xl", default="")
    p.add_argument("--xr", default="")
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
