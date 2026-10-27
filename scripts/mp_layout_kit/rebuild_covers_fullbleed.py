"""Rebuild marketplace covers: full-bleed photo + soft 15–18% bottom gradient (no heavy plates)."""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

from common import IMG, W, H, fnt, fit_cover, save_jpg, save_png, text_center

COPY = json.loads(Path(__file__).with_name("copy.ru.json").read_text(encoding="utf-8"))

# Bottom gradient height as fraction of canvas (10–20% target)
GRAD_H = int(H * 0.17)


def soft_bottom_gradient(base: Image.Image, strength: int = 200) -> Image.Image:
    """Darken only the lower strip — photo stays full-bleed."""
    out = base.convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    y0 = H - GRAD_H
    draw = ImageDraw.Draw(ov)
    for i in range(GRAD_H):
        t = i / max(1, GRAD_H - 1)
        # ease-in: mostly transparent until last half
        a = int(strength * (t ** 1.35))
        draw.line((0, y0 + i, W, y0 + i), fill=(18, 16, 20, a))
    return Image.alpha_composite(out, ov)


def soft_top_scrim(base: Image.Image, height: int = 160, strength: int = 140) -> Image.Image:
    """Lighten/darken top for title readability on busy photos."""
    out = base.convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(ov)
    for i in range(height):
        t = 1 - i / max(1, height - 1)
        a = int(strength * (t ** 1.2))
        draw.line((0, i, W, i), fill=(255, 255, 255, a))
    return Image.alpha_composite(out, ov)


def draw_bottom_copy(im: Image.Image, title: str, sub: str, title_size=42, sub_size=24):
    draw = ImageDraw.Draw(im)
    ft = fnt(title_size, True)
    fs = fnt(sub_size, False)
    tb = draw.textbbox((0, 0), title, font=ft)
    sb = draw.textbbox((0, 0), sub, font=fs)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    sw, sh = sb[2] - sb[0], sb[3] - sb[1]
    gap = 12
    block = th + gap + sh
    y0 = H - GRAD_H
    ty = y0 + int(GRAD_H * 0.28)
    if ty + block > H - 28:
        ty = H - 28 - block
    draw.text(((W - tw) / 2, ty), title, font=ft, fill=(255, 255, 255))
    draw.text(((W - sw) / 2, ty + th + gap), sub, font=fs, fill=(236, 232, 238))
    return im


def draw_top_copy(im: Image.Image, title: str, sub: str, title_size=40, sub_size=22, fill=(42, 36, 32), sub_fill=(90, 85, 80)):
    draw = ImageDraw.Draw(im)
    ft = fnt(title_size, True)
    fs = fnt(sub_size, False)
    tb = draw.textbbox((0, 0), title, font=ft)
    sb = draw.textbbox((0, 0), sub, font=fs)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    sw = sb[2] - sb[0]
    draw.text(((W - tw) / 2, 36), title, font=ft, fill=fill)
    draw.text(((W - sw) / 2, 36 + th + 10), sub, font=fs, fill=sub_fill)
    return im


def crop_above_dark_bar(im: Image.Image, dark_thresh: float = 95.0, min_y_frac: float = 0.55) -> Image.Image:
    """Cut off a dark footer plate; return upper photo content."""
    import numpy as np

    arr = np.asarray(im.convert("RGB"))
    h = arr.shape[0]
    means = arr.mean(axis=(1, 2))
    cut = h
    for y in range(int(h * min_y_frac), h):
        if means[y] < dark_thresh and means[min(y + 15, h - 1)] < dark_thresh:
            cut = y
            break
    if cut >= h - 40:
        cut = int(h * 0.78)
    return im.crop((0, 0, im.size[0], cut))


def crop_between_white_bars(im: Image.Image) -> Image.Image:
    """Shelf-style: white header + footer → keep middle lifestyle."""
    import numpy as np

    arr = np.asarray(im.convert("RGB"))
    h, w = arr.shape[:2]
    means = arr.mean(axis=(1, 2))
    std = arr.std(axis=(1, 2))
    # photo rows have higher std
    photo_ys = [y for y in range(h) if std[y] > 18 and means[y] < 235]
    if not photo_ys:
        return im
    y0, y1 = photo_ys[0], photo_ys[-1]
    # pad a little
    y0 = max(0, y0 - 5)
    y1 = min(h, y1 + 5)
    return im.crop((0, y0, w, y1))


def rebuild_poncho():
    c = COPY["case3_poncho"]["01_cover"]
    # Prefer clean lifestyle trial; strip its footer if present
    src = Image.open(IMG / "case3" / "01_lifestyle_trial.png").convert("RGB")
    src = crop_above_dark_bar(src, dark_thresh=110, min_y_frac=0.62)
    base = fit_cover(src, (W, H))
    base = soft_bottom_gradient(base, strength=195).convert("RGB")
    draw_bottom_copy(base, c["title"].upper(), c["sub"], title_size=44, sub_size=25)
    save_jpg(base, IMG / "case3" / "01_cover.jpg", quality=93)
    print("poncho cover")


def rebuild_shelf():
    c = COPY["case2_shelf"]["01_cover"]
    # Prefer pre-text lifestyle band from git-era cover if present; else crop current
    src = Image.open(IMG / "case2" / "01_cover.jpg").convert("RGB")
    # Tight crop: exclude top/bottom letterboxing + any baked captions
    sw, sh = src.size
    mid = src.crop((int(sw * 0.02), int(sh * 0.18), int(sw * 0.98), int(sh * 0.82)))
    base = fit_cover(mid, (W, H))
    base = soft_top_scrim(base, height=170, strength=175)
    base = soft_bottom_gradient(base, strength=175).convert("RGB")
    draw_top_copy(base, c["title"].upper(), c["sub"], title_size=40, sub_size=23)
    draw = ImageDraw.Draw(base)
    dims = c["dims"]
    fd = fnt(26, True)
    bb = draw.textbbox((0, 0), dims, font=fd)
    dw = bb[2] - bb[0]
    dy = H - int(GRAD_H * 0.42)
    draw.text(((W - dw) / 2, dy), dims, font=fd, fill=(255, 255, 255))
    save_jpg(base, IMG / "case2" / "01_cover.jpg", quality=93)
    print("shelf cover")


def rebuild_chair():
    c = COPY["case1_chair"]["01_cover"]
    src = Image.open(IMG / "case1" / "01_cover_interior.png").convert("RGB")
    src = crop_above_dark_bar(src, dark_thresh=100, min_y_frac=0.68)
    base = fit_cover(src, (W, H))
    base = soft_bottom_gradient(base, strength=200).convert("RGB")
    # title + sub from locked copy (not the long baked line)
    draw_bottom_copy(base, c["title"], c["sub"], title_size=36, sub_size=23)
    save_png(base, IMG / "case1" / "01_cover_interior.png")
    print("chair cover")


def rebuild_blender():
    # Restore clean product plate from git before our redraw, then rebuild once
    import subprocess, io

    try:
        raw = subprocess.check_output(
            ["git", "show", "420890e:public/images/marketplace/case5/01_cover.jpg"],
            cwd=str(IMG.parents[2]),
        )
        src = Image.open(io.BytesIO(raw)).convert("RGB")
    except Exception:
        src = Image.open(IMG / "case5" / "01_cover.jpg").convert("RGB")
    src = crop_above_dark_bar(src, dark_thresh=80, min_y_frac=0.72)
    # Cover old badge zone with bg sample, then redraw once
    sw, sh = src.size
    bg = src.getpixel((sw // 2, 40))
    d0 = ImageDraw.Draw(src)
    d0.ellipse((20, 20, 200, 200), fill=bg)
    base = fit_cover(src, (W, H))
    base = soft_bottom_gradient(base, strength=185).convert("RGB")
    draw = ImageDraw.Draw(base)
    cx, cy, r = 90, 90, 58
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(70, 60, 50), width=3)
    draw.ellipse((cx - r + 6, cy - r + 6, cx + r - 6, cy + r - 6), outline=(70, 60, 50), width=2)
    lab = "400 мл"
    fb = fnt(22, True)
    bb = draw.textbbox((0, 0), lab, font=fb)
    draw.text((cx - (bb[2] - bb[0]) / 2, cy - (bb[3] - bb[1]) / 2 - 2), lab, font=fb, fill=(50, 42, 36))
    draw_bottom_copy(base, "СМУЗИ ЗА 30 СЕК", "MIXORA · портативный блендер", title_size=36, sub_size=22)
    save_jpg(base, IMG / "case5" / "01_cover.jpg", quality=93)
    print("blender cover")


def rebuild_perfume():
    """Already photo-led; only soften if a hard plate exists — leave pyramid layout intact."""
    print("perfume cover: skip (already full-bleed product)")


def main():
    rebuild_poncho()
    rebuild_shelf()
    rebuild_chair()
    rebuild_blender()
    rebuild_perfume()


if __name__ == "__main__":
    main()
