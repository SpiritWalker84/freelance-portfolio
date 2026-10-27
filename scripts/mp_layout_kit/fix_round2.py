"""Round 2 fixes: chair 04–07 layout/copy, shelf 02–03, poncho 05."""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
IMG = ROOT / "public" / "images" / "marketplace"
COPY_PATH = Path(__file__).with_name("copy.ru.json")

W, H = 900, 1200
FONT = r"C:\Windows\Fonts\segoeui.ttf"
FONT_B = r"C:\Windows\Fonts\segoeuib.ttf"


def fnt(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_B if bold else FONT, size)


def fit_cover(im: Image.Image, size: tuple[int, int]) -> Image.Image:
    tw, th = size
    src = im.convert("RGB")
    sw, sh = src.size
    scale = max(tw / sw, th / sh)
    nw, nh = int(sw * scale), int(sh * scale)
    src = src.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return src.crop((left, top, left + tw, top + th))


def fit_contain(im: Image.Image, box: tuple[int, int], pad: float = 0.9, bg=(250, 247, 242)) -> Image.Image:
    tw, th = box
    canvas = Image.new("RGB", (tw, th), bg)
    src = im.convert("RGBA")
    sw, sh = src.size
    scale = min(tw / sw, th / sh) * pad
    nw, nh = max(1, int(sw * scale)), max(1, int(sh * scale))
    src = src.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas.paste(src, ((tw - nw) // 2, (th - nh) // 2), src)
    return canvas


def paste_rounded(base: Image.Image, src: Image.Image, xy: tuple[int, int], radius: int = 24):
    mask = Image.new("L", src.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, src.size[0] - 1, src.size[1] - 1), radius, fill=255)
    base.paste(src, xy, mask)


def text_center(draw, text, y, font, fill):
    bb = draw.textbbox((0, 0), text, font=font)
    draw.text(((W - (bb[2] - bb[0])) / 2, y), text, font=font, fill=fill)


def draw_check(draw, x, y, size=22, color=(46, 125, 80), width=4):
    p1 = (x - size * 0.45, y + size * 0.05)
    p2 = (x - size * 0.1, y + size * 0.4)
    p3 = (x + size * 0.5, y - size * 0.4)
    draw.line([p1, p2, p3], fill=color, width=width, joint="curve")


def draw_cross(draw, x, y, size=18, color=(180, 70, 60), width=4):
    s = size * 0.55
    draw.line((x - s, y - s, x + s, y + s), fill=color, width=width)
    draw.line((x + s, y - s, x - s, y + s), fill=color, width=width)


# ---------------------------------------------------------------------------
# Chair 04 — side rail + compact bottom bar (text fits bar)
# ---------------------------------------------------------------------------
def chair_04():
    studio = Image.open(IMG / "case1" / "source_chair_studio.png")
    out = Image.new("RGB", (W, H), (235, 228, 218))
    hero = fit_cover(studio, (620, 980))
    out.paste(hero, (280, 140))
    wash = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wash)
    for i in range(420):
        a = int(210 * (1 - i / 420))
        wd.line((i, 0, i, H), fill=(235, 228, 218, a))
    out = Image.alpha_composite(out.convert("RGBA"), wash).convert("RGB")
    draw = ImageDraw.Draw(out)
    ink = (42, 36, 32)
    muted = (110, 100, 92)

    draw.text((48, 56), "СИДНЕЙ", font=fnt(44, True), fill=ink)
    draw.text((48, 112), "мягкое кресло для дома", font=fnt(22), fill=muted)

    pills = ["Мягкое сиденье", "Светлая обивка", "До 120 кг"]
    y = 220
    for p in pills:
        pf = fnt(26, True)
        tw = draw.textlength(p, font=pf)
        draw.rounded_rectangle((48, y, 48 + tw + 48, y + 68), 18, fill=(255, 255, 255))
        draw.text((72, y + 18), p, font=pf, fill=ink)
        y += 96

    # Compact bottom bar — width from content, centered
    line1 = "Гостиная · спальня · кабинет"
    line2 = "Деревянные ножки · светлый букле"
    f1, f2 = fnt(26, True), fnt(20)
    w1 = draw.textlength(line1, font=f1)
    w2 = draw.textlength(line2, font=f2)
    bar_w = int(max(w1, w2) + 64)
    bar_h = 110
    bx0 = (W - bar_w) // 2
    by0 = 1045
    draw.rounded_rectangle((bx0, by0, bx0 + bar_w, by0 + bar_h), 22, fill=(35, 30, 28))
    draw.text((bx0 + (bar_w - w1) / 2, by0 + 22), line1, font=f1, fill=(255, 255, 255))
    draw.text((bx0 + (bar_w - w2) / 2, by0 + 62), line2, font=f2, fill=(210, 205, 200))

    out.save(IMG / "case1" / "04_benefits.png", optimize=True)
    print("chair 04")


# ---------------------------------------------------------------------------
# Chair 05 — studio with centered panel content
# ---------------------------------------------------------------------------
def chair_05():
    studio = Image.open(IMG / "case1" / "source_chair_studio.png")
    photo = fit_cover(studio, (W, H))
    out = photo.convert("RGBA")
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    title = "Мягкое кресло Сидней"
    sub = "Цвет и форма без лишнего"
    chips = ["букле", "дерево", "до 120 кг"]
    f_title, f_sub, f_chip = fnt(36, True), fnt(22), fnt(22, True)

    # measure content width for compact centered panel
    tw = d.textlength(title, font=f_title)
    sw = d.textlength(sub, font=f_sub)
    chip_ws = [d.textlength(c, font=f_chip) + 36 for c in chips]
    chips_total = sum(chip_ws) + 16 * (len(chips) - 1)
    content_w = max(tw, sw, chips_total)
    pad_x, pad_y = 40, 28
    panel_w = int(content_w + pad_x * 2)
    panel_h = 200
    px0 = (W - panel_w) // 2
    py0 = 960
    d.rounded_rectangle((px0, py0, px0 + panel_w, py0 + panel_h), 24, fill=(35, 30, 28, 215))
    out = Image.alpha_composite(out, overlay)
    draw = ImageDraw.Draw(out)

    draw.text((px0 + (panel_w - tw) / 2, py0 + 24), title, font=f_title, fill=(255, 255, 255))
    draw.text((px0 + (panel_w - sw) / 2, py0 + 72), sub, font=f_sub, fill=(230, 225, 220))

    x = px0 + (panel_w - chips_total) / 2
    cy = py0 + 120
    for chip, cw in zip(chips, chip_ws):
        draw.rounded_rectangle((x, cy, x + cw, cy + 44), 16, fill=(255, 255, 255))
        draw.text((x + 18, cy + 10), chip, font=f_chip, fill=(40, 35, 30))
        x += cw + 16

    out.convert("RGB").save(IMG / "case1" / "05_studio_product.png", optimize=True)
    print("chair 05")


# ---------------------------------------------------------------------------
# Chair 06 — care copy
# ---------------------------------------------------------------------------
def chair_06():
    studio = Image.open(IMG / "case1" / "source_chair_studio.png")
    bg = (236, 230, 220)
    out = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(out)
    draw.rectangle((0, 0, W, 92), fill=(58, 48, 40))
    text_center(draw, "КОМПЛЕКТАЦИЯ И УХОД", 22, fnt(36, True), (255, 255, 255))

    photo = fit_contain(studio, (W - 96, 420), pad=0.9, bg=(248, 245, 240))
    paste_rounded(out, photo, (48, 120), 28)

    items = [
        ("В комплекте", "кресло, 4 ножки, крепёж и инструкция"),
        ("Обивка", "плотная ткань · пятна — сухой салфеткой"),
        ("Каркас", "прочный, рассчитан на каждый день"),
        ("Уход", "без отбеливателя · мягкая салфетка"),
    ]
    # "без отбеливателя" still a bit label-like — user said не отбеливать is bad
    # Better: "пятна убирать мягкой тканью"
    items[3] = ("Уход", "пятна — мягкой салфеткой, без жёсткой химии")

    y = 580
    ink, muted = (40, 35, 30), (120, 105, 90)
    for label, value in items:
        draw.rounded_rectangle((48, y, W - 48, y + 120), 24, fill=(255, 255, 255))
        draw.text((80, y + 22), label, font=fnt(22, True), fill=muted)
        draw.text((80, y + 58), value, font=fnt(28), fill=ink)
        y += 140

    out.save(IMG / "case1" / "06_care_structure.png", optimize=True)
    print("chair 06")


# ---------------------------------------------------------------------------
# Chair 07 — compare, clear columns + better rows
# ---------------------------------------------------------------------------
def chair_07():
    studio = Image.open(IMG / "case1" / "source_chair_studio.png")
    bg = (242, 236, 228)
    ink = (42, 36, 32)
    muted = (110, 100, 92)
    out = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(out)

    text_center(draw, "В чём разница", 48, fnt(44, True), ink)
    text_center(draw, "это кресло и типичный вариант", 112, fnt(24), muted)

    thumb = fit_contain(studio, (300, 280), pad=0.88, bg=(250, 247, 242))
    paste_rounded(out, thumb, ((W - 300) // 2, 165), 22)

    draw.rounded_rectangle((40, 490, 440, 1145), 28, fill=(255, 255, 255))
    draw.rounded_rectangle((460, 490, 860, 1145), 28, fill=(252, 245, 242))
    draw.text((80, 520), "Это кресло", font=fnt(30, True), fill=(46, 125, 80))
    draw.text((500, 520), "Типичный вариант", font=fnt(26, True), fill=(180, 70, 60))

    rows = [
        ("выдерживает до 120 кг", "часто до 80–90 кг"),
        ("мягкая ткань букле", "гладкая синтетика"),
        ("высота сиденья 45 см", "часто ниже или не пишут"),
        ("ножки из дерева", "часто пластик"),
    ]
    y = 610
    for ours, theirs in rows:
        draw_check(draw, 78, y + 14)
        draw.text((110, y), ours, font=fnt(22), fill=ink)
        draw_cross(draw, 498, y + 14)
        draw.text((530, y), theirs, font=fnt(22), fill=ink)
        y += 115

    out.save(IMG / "case1" / "07_compare.png", optimize=True)
    print("chair 07")


# ---------------------------------------------------------------------------
# Shelf 02 — rewrite scandi line
# ---------------------------------------------------------------------------
def shelf_02():
    src = Image.open(IMG / "case2" / "02_lifestyle.jpg").convert("RGB")
    # normalize size
    src = fit_cover(src, (W, H)) if src.size != (W, H) else src
    out = src.copy()
    draw = ImageDraw.Draw(out)
    # wipe top text area (white bar) and rewrite
    # detect approximate top white band — paint clean white strip
    draw.rectangle((0, 0, W, 150), fill=(255, 255, 255))
    draw.text((48, 40), "В ИНТЕРЬЕРЕ", font=fnt(36, True), fill=(40, 35, 30))
    draw.text((48, 92), "Над кроватью или диваном — место свободно", font=fnt(22), fill=(90, 85, 80))
    # keep bottom "крепёж в комплекте" if present — rewrite clean
    draw.rectangle((0, 1120, W, H), fill=(255, 255, 255))
    foot = "крепёж в комплекте"
    bb = draw.textbbox((0, 0), foot, font=fnt(22))
    draw.text(((W - (bb[2] - bb[0])) / 2, 1145), foot, font=fnt(22), fill=(100, 95, 90))
    out.save(IMG / "case2" / "02_lifestyle.jpg", quality=92, optimize=True)
    print("shelf 02")


# ---------------------------------------------------------------------------
# Shelf 03 — dimensions from scratch on clean lifestyle crop
# ---------------------------------------------------------------------------
def shelf_03():
    """Build dims slide: shelf board only — length + depth parallel to edges."""
    cover = Image.open(IMG / "case2" / "01_cover.jpg").convert("RGB")
    # Use middle band of cover (shelf) without baked title/footer
    cover = fit_cover(cover, (W, H))
    # Extract shelf scene
    scene = cover.crop((0, 180, W, 980)).resize((820, 700), Image.Resampling.LANCZOS)

    # Soft-heal any leftover title text at top of scene
    sd = ImageDraw.Draw(scene)
    # sample wall near top
    wall = scene.getpixel((400, 40))
    for y in range(0, 50):
        for x in range(scene.size[0]):
            scene.putpixel((x, y), wall)

    canvas = Image.new("RGB", (W, H), (245, 240, 232))
    draw = ImageDraw.Draw(canvas)
    text_center(draw, "РАЗМЕРЫ И НАГРУЗКА", 42, fnt(40, True), (45, 38, 34))

    mask = Image.new("L", scene.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, scene.size[0] - 1, scene.size[1] - 1), 22, fill=255)
    canvas.paste(scene, (40, 120), mask)

    # Shelf front edge on this crop (approx): slightly tilted
    # Tune to sit under shelf board front
    # After crop from cover lifestyle, shelf is mid-frame
    x0, y0 = 115, 120 + 355  # left underside
    x1, y1 = 755, 120 + 372  # right underside — parallel to shelf
    accent = (35, 35, 35)
    draw.line((x0, y0, x1, y1), fill=accent, width=3)
    # end ticks roughly perpendicular to shelf slope
    draw.line((x0 - 3, y0 - 12, x0 + 5, y0 + 12), fill=accent, width=3)
    draw.line((x1 - 3, y1 - 12, x1 + 5, y1 + 12), fill=accent, width=3)
    lab = "720 мм"
    bb = draw.textbbox((0, 0), lab, font=fnt(28, True))
    draw.text(
        ((x0 + x1) / 2 - (bb[2] - bb[0]) / 2, (y0 + y1) / 2 + 18),
        lab,
        font=fnt(28, True),
        fill=accent,
    )

    # Depth along right end of shelf (into wall), parallel to depth edge
    dx0, dy0 = 730, 120 + 270
    dx1, dy1 = 795, 120 + 318
    draw.line((dx0, dy0, dx1, dy1), fill=accent, width=3)
    draw.line((dx0 - 6, dy0 + 8, dx0 + 8, dy0 - 4), fill=accent, width=2)
    draw.line((dx1 - 6, dy1 + 8, dx1 + 8, dy1 - 4), fill=accent, width=2)
    draw.text((720, 120 + 330), "150 мм", font=fnt(26, True), fill=accent)

    # No height-to-picture. Bottom facts only.
    draw.rounded_rectangle((48, 1020, 430, 1145), 22, fill=(255, 255, 255))
    draw.rounded_rectangle((470, 1020, 852, 1145), 22, fill=(255, 255, 255))
    draw.text((78, 1045), "Материал", font=fnt(20), fill=(100, 90, 80))
    draw.text((78, 1080), "ЛДСП", font=fnt(32, True), fill=(45, 38, 34))
    draw.text((500, 1045), "Нагрузка", font=fnt(20), fill=(100, 90, 80))
    draw.text((500, 1080), "до 15 кг", font=fnt(32, True), fill=(45, 38, 34))

    canvas.save(IMG / "case2" / "03_specs_dims.jpg", quality=92, optimize=True)
    print("shelf 03")


# ---------------------------------------------------------------------------
# Poncho 05 — clearer size + dry phrasing
# ---------------------------------------------------------------------------
def poncho_05():
    fabric = Image.open(IMG / "case3" / "02_product_reference.png")
    bg = (236, 230, 242)
    ink = (40, 30, 50)
    header = (70, 50, 95)
    out = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(out)
    draw.rectangle((0, 0, W, 100), fill=header)
    text_center(draw, "СОСТАВ И УХОД", 28, fnt(40, True), (255, 255, 255))

    photo = fit_cover(fabric, (400, 980))
    paste_rounded(out, photo, (40, 140), 24)

    items = [
        "мягкий флис",
        "свободный крой — один размер",
        "стирать при 30°C",
        "без агрессивной химии",
        "не сушить в барабане",
    ]
    y = 160
    for item in items:
        draw.rounded_rectangle((470, y, W - 40, y + 150), 22, fill=(255, 255, 255))
        # wrap if needed
        font = fnt(26)
        words = item.split()
        lines: list[str] = []
        cur = ""
        for w in words:
            trial = f"{cur} {w}".strip()
            if draw.textlength(trial, font=font) <= 340:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        total = 32 * len(lines)
        ty = y + (150 - total) / 2
        for i, line in enumerate(lines):
            prefix = "•  " if i == 0 else "   "
            draw.text((500, ty + i * 32), prefix + line if i == 0 else "   " + line, font=font, fill=ink)
        y += 175

    out.save(IMG / "case3" / "05_care.jpg", quality=92, optimize=True)
    print("poncho 05")


def update_copy():
    data = json.loads(COPY_PATH.read_text(encoding="utf-8"))
    data["case1_chair"]["04_benefits"] = {
        "brand": "СИДНЕЙ",
        "sub": "мягкое кресло для дома",
        "pills": ["Мягкое сиденье", "Светлая обивка", "До 120 кг"],
        "footer": "Гостиная · спальня · кабинет",
        "footer2": "Деревянные ножки · светлый букле",
    }
    data["case1_chair"]["06_care"] = {
        "title": "Комплектация и уход",
        "items": [
            ["В комплекте", "кресло, 4 ножки, крепёж и инструкция"],
            ["Обивка", "плотная ткань · пятна — сухой салфеткой"],
            ["Каркас", "прочный, рассчитан на каждый день"],
            ["Уход", "пятна — мягкой салфеткой, без жёсткой химии"],
        ],
    }
    data["case1_chair"]["07_compare"] = {
        "title": "В чём разница",
        "sub": "это кресло и типичный вариант",
        "ours_label": "Это кресло",
        "theirs_label": "Типичный вариант",
        "rows": [
            ["выдерживает до 120 кг", "часто до 80–90 кг"],
            ["мягкая ткань букле", "гладкая синтетика"],
            ["высота сиденья 45 см", "часто ниже или не пишут"],
            ["ножки из дерева", "часто пластик"],
        ],
    }
    data["case2_shelf"]["02_lifestyle"] = {
        "title": "В интерьере",
        "sub": "Над кроватью или диваном — место свободно",
        "footer": "крепёж в комплекте",
    }
    data["case2_shelf"]["03_dims"] = {
        "title": "Размеры и нагрузка",
        "length": "720 мм",
        "depth": "150 мм",
        "material": "ЛДСП",
        "load": "до 15 кг",
    }
    data["case3_poncho"]["05_care"]["items"] = [
        "мягкий флис",
        "свободный крой — один размер",
        "стирать при 30°C",
        "без агрессивной химии",
        "не сушить в барабане",
    ]
    COPY_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("copy.ru.json updated")


def main():
    chair_04()
    chair_05()
    chair_06()
    chair_07()
    shelf_02()
    shelf_03()
    poncho_05()
    update_copy()


if __name__ == "__main__":
    main()
