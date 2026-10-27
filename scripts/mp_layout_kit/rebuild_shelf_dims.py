"""Shelf dims: big lifestyle proof + dense stacked drawings (no centered dead air)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from common import IMG, W, H, fnt, fit_cover, paste_rounded, save_jpg, text_center

BG = (246, 242, 236)
INK = (42, 36, 30)
MUTED = (120, 110, 100)
ACCENT = (92, 72, 54)
LINE = (55, 48, 40)
SHELF = (252, 250, 246)
SHELF_EDGE = (198, 190, 180)
SHELF_LIP = (222, 216, 208)
SHADOW = (204, 194, 182)


def dim_h(draw, x0, x1, y, label, font):
    for x in (x0, x1):
        draw.line((x, y - 10, x, y + 10), fill=LINE, width=3)
    for x, s in ((x0, 1), (x1, -1)):
        draw.polygon([(x, y), (x + s * 12, y - 6), (x + s * 12, y + 6)], fill=LINE)
    bb = draw.textbbox((0, 0), label, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    cx = (x0 + x1) / 2
    pad_x, pad_y = 13, 7
    box = (cx - tw / 2 - pad_x, y - th / 2 - pad_y, cx + tw / 2 + pad_x, y + th / 2 + pad_y)
    draw.rounded_rectangle(box, 11, fill=(255, 255, 255), outline=(230, 224, 216), width=1)
    draw.line((x0 + 12, y, box[0] - 2, y), fill=LINE, width=3)
    draw.line((box[2] + 2, y, x1 - 12, y), fill=LINE, width=3)
    draw.text((cx - tw / 2, y - th / 2), label, font=font, fill=ACCENT)


def dim_v(draw, y0, y1, x, label, font, gap=12):
    for y in (y0, y1):
        draw.line((x - 10, y, x + 10, y), fill=LINE, width=3)
    for y, s in ((y0, 1), (y1, -1)):
        draw.polygon([(x, y), (x - 6, y + s * 12), (x + 6, y + s * 12)], fill=LINE)
    bb = draw.textbbox((0, 0), label, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    cy = (y0 + y1) / 2
    pad_x, pad_y = 11, 6
    box = (x + gap, cy - th / 2 - pad_y, x + gap + tw + 2 * pad_x, cy + th / 2 + pad_y)
    draw.rounded_rectangle(box, 11, fill=(255, 255, 255), outline=(230, 224, 216), width=1)
    draw.line((x, y0 + 12, x, box[1] - 2), fill=LINE, width=3)
    draw.line((x, box[3] + 2, x, y1 - 12), fill=LINE, width=3)
    draw.text((box[0] + pad_x, cy - th / 2), label, font=font, fill=ACCENT)


def chip(draw, xy, w, h, label, value):
    x, y = xy
    draw.rounded_rectangle((x, y, x + w, y + h), 16, fill=(255, 255, 255), outline=(230, 224, 216), width=1)
    draw.text((x + 22, y + 14), label, font=fnt(17), fill=MUTED)
    draw.text((x + 22, y + 42), value, font=fnt(32, True), fill=INK)


def build() -> Path:
    out = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(out)
    text_center(draw, "Размеры и нагрузка", 18, fnt(36, True), INK)

    # Large lifestyle — fills top, kills empty mid
    src = IMG / "case2" / "01_cover.jpg"
    if (IMG / "case2" / "_dims_base.jpg").exists():
        src = IMG / "case2" / "_dims_base.jpg"
    photo = Image.open(src).convert("RGB")
    sw, sh = photo.size
    crop = photo.crop((int(sw * 0.04), int(sh * 0.26), int(sw * 0.96), int(sh * 0.60)))
    panel_w, panel_h = 852, 500
    panel = fit_cover(crop, (panel_w, panel_h))
    px, py = (W - panel_w) // 2, 52
    shad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shad).rounded_rectangle(
        (px + 2, py + 6, px + panel_w + 2, py + panel_h + 6), 20, fill=(0, 0, 0, 30)
    )
    out = Image.alpha_composite(out.convert("RGBA"), shad.filter(ImageFilter.GaussianBlur(9))).convert("RGB")
    draw = ImageDraw.Draw(out)
    paste_rounded(out, panel, (px, py), 20)
    draw = ImageDraw.Draw(out)

    chip_h = 96
    chip_y = H - 22 - chip_h

    label_font = fnt(28, True)
    cap = fnt(19)

    # Dense stack directly under photo — no vertical centering
    y = py + panel_h + 18

    # FRONT
    draw.text((36, y), "вид спереди · длина", font=cap, fill=MUTED)
    y += 30
    fl, ft = 828, 100
    fx0 = (W - fl) // 2
    fx1 = fx0 + fl
    ftop, fbot = y, y + ft
    draw.rounded_rectangle((fx0 + 6, fbot, fx1 + 6, fbot + 12), 5, fill=SHADOW)
    draw.rounded_rectangle((fx0, ftop, fx1, fbot), 10, fill=SHELF, outline=SHELF_EDGE, width=3)
    draw.line((fx0 + 16, ftop + 8, fx1 - 16, ftop + 8), fill=(255, 255, 255), width=3)
    draw.rectangle((fx0 + 4, fbot - 14, fx1 - 4, fbot - 3), fill=SHELF_LIP)
    dim_y = fbot + 38
    draw.line((fx0, fbot + 3, fx0, dim_y - 10), fill=LINE, width=2)
    draw.line((fx1, fbot + 3, fx1, dim_y - 10), fill=LINE, width=2)
    dim_h(draw, fx0, fx1, dim_y, "720 мм", label_font)

    # SIDE — same visual weight as front, true 3:1 (150:50)
    y = dim_y + 30
    draw.text((36, y), "вид сбоку · глубина и высота", font=cap, fill=MUTED)
    y += 28

    thick_s = 120
    depth_s = 360  # 3:1
    # Align under front board left edge — less “floating in empty mid”
    wall_x = fx0 + 8
    bx0, bx1 = wall_x, wall_x + depth_s
    top, bot = y, y + thick_s

    draw.line((wall_x, top - 14, wall_x, bot + 18), fill=(194, 184, 174), width=5)
    draw.rounded_rectangle((bx0 + 5, bot, bx1 + 5, bot + 11), 5, fill=SHADOW)
    draw.rounded_rectangle((bx0, top, bx1, bot), 10, fill=SHELF, outline=SHELF_EDGE, width=3)
    draw.line((bx0 + 12, top + 9, bx1 - 14, top + 9), fill=(255, 255, 255), width=3)
    draw.rectangle((bx1 - 12, top + 3, bx1 - 3, bot - 3), fill=SHELF_LIP)

    dim_y2 = bot + 38
    draw.line((bx0, bot + 3, bx0, dim_y2 - 10), fill=LINE, width=2)
    draw.line((bx1, bot + 3, bx1, dim_y2 - 10), fill=LINE, width=2)
    dim_h(draw, bx0, bx1, dim_y2, "150 мм", label_font)
    draw.text((bx0, dim_y2 + 14), "глубина", font=fnt(17), fill=MUTED)

    dim_x = bx1 + 34
    draw.line((bx1 + 3, top, dim_x - 10, top), fill=LINE, width=2)
    draw.line((bx1 + 3, bot, dim_x - 10, bot), fill=LINE, width=2)
    dim_v(draw, top, bot, dim_x, "50 мм", label_font, gap=10)
    draw.text((dim_x + 8, bot + 12), "высота", font=fnt(17), fill=MUTED)

    # Chips snug under last dim (keeps bottom from looking half-empty)
    chip_y = min(chip_y, dim_y2 + 48)
    chip(draw, (36, chip_y), 404, chip_h, "Материал", "ЛДСП")
    chip(draw, (460, chip_y), 404, chip_h, "Нагрузка", "до 15 кг")

    path = IMG / "case2" / "03_specs_dims.jpg"
    save_jpg(out, path, quality=93)
    return path


if __name__ == "__main__":
    build()
