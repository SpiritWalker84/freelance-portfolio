"""Shelf dims slide: photo + orthographic callouts (marketplace gold pattern).

Research basis (wild-card / fotofactor / Target floating-shelf cards):
- Lines from real product edges; no crossing; large numbers + units
- Volumetric goods need front + side (or a clear schematic)
- Do NOT measure decor (frames, plants)
- Lifestyle photo alone + freehand perspective lines = weak / wrong
"""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from common import IMG, W, H, fnt, fit_cover, paste_rounded, save_jpg, text_center

BG = (246, 242, 236)
INK = (42, 36, 30)
MUTED = (120, 110, 100)
ACCENT = (92, 72, 54)
LINE = (55, 48, 40)
SHELF = (248, 246, 242)
SHELF_EDGE = (220, 214, 206)
WALL = (238, 232, 224)


def dim_h(draw: ImageDraw.ImageDraw, x0: float, x1: float, y: float, label: str, font, gap=10):
    """Horizontal dimension between x0..x1 at y, with end ticks + centered label pill."""
    # extension ticks
    for x in (x0, x1):
        draw.line((x, y - 8, x, y + 8), fill=LINE, width=2)
    draw.line((x0, y, x1, y), fill=LINE, width=2)
    # arrowheads
    for x, s in ((x0, 1), (x1, -1)):
        draw.polygon([(x, y), (x + s * 10, y - 5), (x + s * 10, y + 5)], fill=LINE)
    bb = draw.textbbox((0, 0), label, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    cx = (x0 + x1) / 2
    pad_x, pad_y = 12, 6
    box = (cx - tw / 2 - pad_x, y - th / 2 - pad_y - gap, cx + tw / 2 + pad_x, y + th / 2 + pad_y - gap)
    # white pill so line doesn't cut through digits
    draw.rounded_rectangle(box, 10, fill=BG)
    # break the dim line under the pill
    draw.line((x0 + 10, y, box[0] - 2, y), fill=LINE, width=2)
    draw.line((box[2] + 2, y, x1 - 10, y), fill=LINE, width=2)
    draw.text((cx - tw / 2, y - th / 2 - gap), label, font=font, fill=ACCENT)


def dim_v(draw: ImageDraw.ImageDraw, y0: float, y1: float, x: float, label: str, font, gap=14):
    """Vertical dimension between y0..y1 at x."""
    for y in (y0, y1):
        draw.line((x - 8, y, x + 8, y), fill=LINE, width=2)
    draw.line((x, y0, x, y1), fill=LINE, width=2)
    for y, s in ((y0, 1), (y1, -1)):
        draw.polygon([(x, y), (x - 5, y + s * 10), (x + 5, y + s * 10)], fill=LINE)
    bb = draw.textbbox((0, 0), label, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    cy = (y0 + y1) / 2
    pad_x, pad_y = 10, 5
    box = (x + gap, cy - th / 2 - pad_y, x + gap + tw + 2 * pad_x, cy + th / 2 + pad_y)
    draw.rounded_rectangle(box, 10, fill=BG)
    draw.text((box[0] + pad_x, cy - th / 2), label, font=font, fill=ACCENT)


def draw_front_shelf(draw: ImageDraw.ImageDraw, box, thickness_ratio=0.32):
    """Orthographic front: thick floating shelf board."""
    x0, y0, x1, y1 = box
    th = y1 - y0
    board_h = int(th * thickness_ratio)
    top = y0 + (th - board_h) // 2
    # soft wall strip behind
    draw.rounded_rectangle((x0 - 18, y0, x1 + 18, y1), 16, fill=WALL)
    # shadow under board
    draw.rounded_rectangle((x0 + 6, top + board_h - 2, x1 + 6, top + board_h + 14), 5, fill=(208, 198, 186))
    # board body
    draw.rounded_rectangle((x0, top, x1, top + board_h), 7, fill=SHELF, outline=SHELF_EDGE, width=2)
    # top highlight + bottom lip (reads as thickness)
    draw.line((x0 + 10, top + 5, x1 - 10, top + 5), fill=(255, 255, 255), width=2)
    draw.rectangle((x0 + 2, top + board_h - 10, x1 - 2, top + board_h - 2), fill=(232, 226, 218))
    return x0, top, x1, top + board_h


def draw_side_shelf(draw: ImageDraw.ImageDraw, box, depth_ratio=0.70, thickness_ratio=0.34):
    """Orthographic side: depth into wall (left=wall, right=front)."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle((x0, y0, x1, y1), 16, fill=WALL)
    wall_x = x0 + 28
    draw.line((wall_x, y0 + 14, wall_x, y1 - 14), fill=(205, 195, 185), width=3)
    depth = int((x1 - x0 - 50) * depth_ratio)
    board_h = int((y1 - y0) * thickness_ratio)
    top = y0 + (y1 - y0 - board_h) // 2
    bx0, bx1 = wall_x, wall_x + depth
    draw.rounded_rectangle((bx0, top, bx1, top + board_h), 6, fill=SHELF, outline=SHELF_EDGE, width=2)
    draw.line((bx0 + 6, top + 5, bx1 - 8, top + 5), fill=(255, 255, 255), width=2)
    # front face (end of board)
    draw.rectangle((bx1 - 8, top + 1, bx1 - 1, top + board_h - 1), fill=(228, 222, 214))
    return bx0, top, bx1, top + board_h, wall_x


def chip(draw, xy, w, h, label, value, font_l, font_v):
    x, y = xy
    draw.rounded_rectangle((x, y, x + w, y + h), 18, fill=(255, 255, 255), outline=(230, 224, 216), width=1)
    draw.text((x + 22, y + 18), label, font=font_l, fill=MUTED)
    draw.text((x + 22, y + 48), value, font=font_v, fill=INK)


def build() -> Path:
    out = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(out)

    # Title
    text_center(draw, "Размеры и нагрузка", 42, fnt(40, True), INK)

    # --- Photo proof (real product) ---
    # Prefer old clean lifestyle product crop from cover / archived dims base
    src_candidates = [
        IMG / "case2" / "_dims_base.jpg",
        IMG / "case2" / "01_cover.jpg",
        IMG / "case2" / "03_specs_dims.jpg",
    ]
    src = next((p for p in src_candidates if p.exists()), IMG / "case2" / "01_cover.jpg")
    photo = Image.open(src).convert("RGB")
    # crop around the shelf band (upper-mid of cover-style shots)
    sw, sh = photo.size
    crop = photo.crop((int(sw * 0.06), int(sh * 0.28), int(sw * 0.94), int(sh * 0.62)))
    panel_w, panel_h = 820, 320
    panel = fit_cover(crop, (panel_w, panel_h))
    # soft vignette so decor is quieter; product stays readable
    vignette = Image.new("RGB", panel.size, (248, 244, 238))
    panel = Image.blend(panel, vignette, 0.08)
    px, py = (W - panel_w) // 2, 110
    # soft shadow
    sh_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh_img).rounded_rectangle((px + 4, py + 8, px + panel_w + 4, py + panel_h + 8), 22, fill=(0, 0, 0, 36))
    sh_img = sh_img.filter(ImageFilter.GaussianBlur(12))
    out = Image.alpha_composite(out.convert("RGBA"), sh_img).convert("RGB")
    draw = ImageDraw.Draw(out)
    paste_rounded(out, panel, (px, py), 22)
    draw = ImageDraw.Draw(out)

    # caption under photo
    text_center(draw, "как выглядит в жизни", py + panel_h + 14, fnt(20), MUTED)

    # --- Orthographic diagrams (the accurate measurements) ---
    diagram_top = py + panel_h + 48
    label_font = fnt(26, True)
    caption_font = fnt(18)

    # Front view — length
    front_box = (70, diagram_top, 520, diagram_top + 160)
    draw.text((70, diagram_top - 28), "вид спереди", font=caption_font, fill=MUTED)
    fx0, ftop, fx1, fbot = draw_front_shelf(draw, front_box)
    # extension lines from board ends down to dim line
    dim_y = fbot + 36
    draw.line((fx0, fbot + 2, fx0, dim_y - 8), fill=LINE, width=1)
    draw.line((fx1, fbot + 2, fx1, dim_y - 8), fill=LINE, width=1)
    dim_h(draw, fx0, fx1, dim_y, "720 мм", label_font, gap=0)

    # Side view — depth
    side_box = (560, diagram_top, 830, diagram_top + 160)
    draw.text((560, diagram_top - 28), "вид сбоку", font=caption_font, fill=MUTED)
    bx0, top, bx1, bot, wall_x = draw_side_shelf(draw, side_box)
    # depth dim BELOW the board, measuring wall→front (actual depth of shelf)
    dim_y2 = bot + 36
    draw.line((bx0, bot + 2, bx0, dim_y2 - 8), fill=LINE, width=1)
    draw.line((bx1, bot + 2, bx1, dim_y2 - 8), fill=LINE, width=1)
    dim_h(draw, bx0, bx1, dim_y2, "150 мм", label_font, gap=0)

    # helper labels under diagrams
    draw.text((70, dim_y + 28), "длина", font=caption_font, fill=MUTED)
    draw.text((560, dim_y2 + 28), "глубина", font=caption_font, fill=MUTED)

    # --- Spec chips (tight under diagrams — avoid empty mid band) ---
    chip_y = max(dim_y, dim_y2) + 78
    chip(draw, (70, chip_y), 360, 100, "Материал", "ЛДСП", fnt(18), fnt(32, True))
    chip(draw, (470, chip_y), 360, 100, "Нагрузка", "до 15 кг", fnt(18), fnt(32, True))

    path = IMG / "case2" / "03_specs_dims.jpg"
    save_jpg(out, path, quality=93)
    return path


if __name__ == "__main__":
    build()
