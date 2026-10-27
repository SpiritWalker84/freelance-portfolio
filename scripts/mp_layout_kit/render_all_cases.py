"""Rebuild case2–5 slides on distinct layout templates."""
from __future__ import annotations

from PIL import Image, ImageDraw

from common import (
    IMG,
    W,
    H,
    fnt,
    fit_cover,
    fit_contain,
    paste_rounded,
    shadow_round,
    text_center,
    wrap,
    save_jpg,
)


# ---------------------------------------------------------------------------
# Case 2 · shelf
# ---------------------------------------------------------------------------
def case2():
    c = IMG / "case2"
    cover = Image.open(c / "01_cover.jpg")
    life = Image.open(c / "02_lifestyle.jpg")
    bg = (244, 238, 230)
    ink = (45, 38, 34)
    muted = (115, 105, 95)
    accent = (70, 58, 48)

    # 04 · benefits_2x2 (was lifestyle+icons top — now photo top, 2×2 tiles)
    out = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(out)
    text_center(draw, "ПОЧЕМУ УДОБНО", 40, fnt(42, True), ink)
    photo = fit_cover(life, (W - 96, 480))
    out = shadow_round(out, (48, 110, W - 48, 110 + 480), 28).convert("RGB")
    draw = ImageDraw.Draw(out)
    paste_rounded(out, photo, (48, 110), 28)

    tiles = [
        ("01", "До 15 кг", "нагрузка на полку"),
        ("02", "Крепёж", "в комплекте"),
        ("03", "Экономит", "место у стены"),
        ("04", "Декор", "книги и растения"),
    ]
    positions = [(48, 640), (474, 640), (48, 900), (474, 900)]
    for (num, t, s), (x, y) in zip(tiles, positions):
        draw.rounded_rectangle((x, y, x + 378, y + 220), 24, fill=(255, 255, 255))
        draw.ellipse((x + 24, y + 28, x + 76, y + 80), fill=accent)
        nb = draw.textbbox((0, 0), num, font=fnt(20, True))
        draw.text((x + 50 - (nb[2] - nb[0]) / 2, y + 40), num, font=fnt(20, True), fill=(255, 255, 255))
        draw.text((x + 96, y + 36), t, font=fnt(30, True), fill=ink)
        draw.text((x + 96, y + 84), s, font=fnt(22), fill=muted)
    save_jpg(out, c / "04_benefits.jpg")

    # 05 · compare_split shelf vs шкаф
    out = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(out)
    text_center(draw, "МЕСТО И ОБЪЁМ", 44, fnt(42, True), ink)
    draw.text((W // 2 - 170, 100), "полка vs типичный шкаф", font=fnt(22), fill=muted)
    thumb = fit_cover(cover, (320, 280))
    paste_rounded(out, thumb, ((W - 320) // 2, 150), 22)

    draw.rounded_rectangle((48, 470, 430, 1120), 28, fill=(255, 255, 255))
    draw.rounded_rectangle((470, 470, 852, 1120), 28, fill=(252, 245, 242))
    draw.text((90, 500), "Полка", font=fnt(32, True), fill=(46, 125, 80))
    draw.text((520, 500), "Шкаф", font=fnt(32, True), fill=(160, 70, 60))
    rows = [
        ("глубина 150 мм", "часто 400–600 мм"),
        ("нагрузка до 15 кг", "тяжёлый корпус"),
        ("крепёж в наборе", "сборка часами"),
        ("стена свободна", "съедает комнату"),
    ]
    y = 580
    for a, b in rows:
        draw.ellipse((80, y + 6, 104, y + 30), fill=(46, 125, 80))
        draw.text((86, y + 6), "✓", font=fnt(15, True), fill=(255, 255, 255))
        draw.text((118, y + 4), a, font=fnt(22), fill=ink)
        draw.ellipse((502, y + 6, 526, y + 30), fill=(160, 70, 60))
        draw.text((508, y + 4), "×", font=fnt(15, True), fill=(255, 255, 255))
        draw.text((540, y + 4), b, font=fnt(22), fill=ink)
        y += 110
    save_jpg(out, c / "05_compare.jpg")

    # 03 · dims_callouts refresh on product crop
    out = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(out)
    text_center(draw, "РАЗМЕРЫ И НАГРУЗКА", 40, fnt(40, True), ink)
    panel = fit_cover(cover, (760, 720))
    out = shadow_round(out, (70, 120, 830, 840), 28).convert("RGB")
    draw = ImageDraw.Draw(out)
    paste_rounded(out, panel, (70, 120), 28)
    # ticks
    draw.line((110, 180, 110, 760), fill=accent, width=3)
    draw.line((98, 180, 122, 180), fill=accent, width=3)
    draw.line((98, 760, 122, 760), fill=accent, width=3)
    draw.text((130, 440), "500 мм", font=fnt(26, True), fill=accent)
    draw.line((160, 800, 740, 800), fill=accent, width=3)
    draw.text((360, 820), "720 мм · длина", font=fnt(26, True), fill=accent)
    draw.line((790, 260, 790, 560), fill=accent, width=3)
    draw.text((680, 380), "150 мм", font=fnt(24, True), fill=accent)

    facts = [("материал", "ЛДСП"), ("нагрузка", "до 15 кг")]
    x = 70
    for label, val in facts:
        draw.rounded_rectangle((x, 900, x + 360, 1120), 24, fill=(255, 255, 255))
        draw.text((x + 28, 940), label, font=fnt(22), fill=muted)
        draw.text((x + 28, 990), val, font=fnt(36, True), fill=ink)
        x += 400
    save_jpg(out, c / "03_specs_dims.jpg")


# ---------------------------------------------------------------------------
# Case 3 · poncho
# ---------------------------------------------------------------------------
def case3():
    c = IMG / "case3"
    cover = Image.open(c / "01_cover.jpg")
    product = Image.open(c / "02_product.jpg")
    bg = (236, 230, 242)
    ink = (48, 36, 58)
    muted = (120, 105, 130)
    accent = (92, 62, 120)

    # 03 · usp_side_rail
    out = fit_cover(cover, (W, H)).convert("RGBA")
    wash = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wash)
    for i in range(460):
        a = int(210 * (1 - i / 460))
        wd.line((i, 0, i, H), fill=(236, 230, 242, a))
    out = Image.alpha_composite(out, wash).convert("RGB")
    draw = ImageDraw.Draw(out)
    draw.text((48, 56), "ПЛЕД-ПОНЧО", font=fnt(40, True), fill=ink)
    draw.text((48, 112), "тепло · руки свободны", font=fnt(22), fill=muted)
    pills = ["МЯГКИЙ ФЛИС", "ONE SIZE", "ДОМА И В ДОРОГЕ"]
    y = 220
    for p in pills:
        tw = draw.textlength(p, font=fnt(24, True))
        draw.rounded_rectangle((48, y, 48 + tw + 48, y + 68), 18, fill=(255, 255, 255))
        draw.text((72, y + 18), p, font=fnt(24, True), fill=ink)
        y += 96
    draw.rounded_rectangle((48, 1040, W - 48, 1145), 24, fill=(40, 30, 50))
    draw.text((80, 1068), "Диван · балкон · поездка", font=fnt(26, True), fill=(255, 255, 255))
    draw.text((80, 1108), "Без рукавов — телефон и чай в руках", font=fnt(20), fill=(210, 200, 220))
    save_jpg(out, c / "03_benefits.jpg")

    # 04 · scenarios as 3 horizontal bands (care_steps rhythm)
    out = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(out)
    text_center(draw, "КОГДА НОСИТЬ", 44, fnt(42, True), ink)
    scenes = [
        (cover, "Дома на диване", "фильм, чай, плед без путаницы"),
        (product, "Прохладно утром", "быстро накинуть one size"),
        (cover, "В дороге", "самолёт, поезд, авто"),
    ]
    y = 130
    for i, (src, title, sub) in enumerate(scenes, 1):
        band = fit_cover(src, (W - 96, 280))
        # darken bottom of band for text
        band_rgba = band.convert("RGBA")
        ov = Image.new("RGBA", band.size, (0, 0, 0, 0))
        ImageDraw.Draw(ov).rectangle((0, 160, band.size[0], band.size[1]), fill=(30, 22, 40, 170))
        band = Image.alpha_composite(band_rgba, ov).convert("RGB")
        paste_rounded(out, band, (48, y), 22)
        draw = ImageDraw.Draw(out)
        draw.ellipse((68, y + 188, 112, y + 232), fill=(255, 255, 255))
        draw.text((80, y + 196), str(i), font=fnt(22, True), fill=accent)
        draw.text((128, y + 188), title, font=fnt(28, True), fill=(255, 255, 255))
        draw.text((128, y + 228), sub, font=fnt(20), fill=(220, 210, 230))
        y += 310
    save_jpg(out, c / "04_scenarios.jpg")

    # 05 · care_steps
    out = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(out)
    text_center(draw, "СОСТАВ И УХОД", 44, fnt(42, True), ink)
    thumb = fit_cover(product, (W - 96, 360))
    paste_rounded(out, thumb, (48, 120), 28)
    steps = [
        ("1", "Стирка", "деликатный режим 30°C"),
        ("2", "Сушка", "на воздухе, без барабана"),
        ("3", "Хранение", "сложить или повесить"),
    ]
    y = 520
    for num, title, sub in steps:
        draw.rounded_rectangle((48, y, W - 48, y + 130), 24, fill=(255, 255, 255))
        draw.ellipse((72, y + 36, 128, y + 92), fill=accent)
        nb = draw.textbbox((0, 0), num, font=fnt(26, True))
        draw.text((100 - (nb[2] - nb[0]) / 2, y + 48), num, font=fnt(26, True), fill=(255, 255, 255))
        draw.text((156, y + 34), title, font=fnt(30, True), fill=ink)
        draw.text((156, y + 78), sub, font=fnt(24), fill=muted)
        y += 150
    draw.text((48, 1000), "Не отбеливать · мягкий флис · one size", font=fnt(22), fill=muted)
    save_jpg(out, c / "05_care.jpg")


# ---------------------------------------------------------------------------
# Case 4 · perfume
# ---------------------------------------------------------------------------
def case4():
    c = IMG / "case4"
    cover = Image.open(c / "01_cover_pyramid.jpg")
    life = Image.open(c / "02_lifestyle.jpg")
    bg = (236, 228, 244)
    ink = (42, 32, 55)
    muted = (115, 100, 130)
    accent = (140, 70, 150)

    # 04 · benefits_2x2 — bottle from cover (no discount badge)
    out = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(out)
    text_center(draw, "AURA LUNE", 36, fnt(40, True), ink)
    text_center(draw, "eau de toilette · 50 мл", 88, fnt(22), muted)
    photo = fit_cover(cover, (W - 96, 420))
    paste_rounded(out, photo, (48, 140), 28)

    tiles = [
        ("01", "До 48 ч", "стойкость на коже*"),
        ("02", "50 мл", "удобный формат"),
        ("03", "Дневной", "лёгкий шлейф"),
        ("04", "Пирамида", "верх · сердце · база"),
    ]
    positions = [(48, 600), (474, 600), (48, 880), (474, 880)]
    for (num, t, s), (x, y) in zip(tiles, positions):
        draw.rounded_rectangle((x, y, x + 378, y + 240), 24, fill=(255, 255, 255))
        draw.ellipse((x + 24, y + 32, x + 76, y + 84), fill=accent)
        nb = draw.textbbox((0, 0), num, font=fnt(20, True))
        draw.text((x + 50 - (nb[2] - nb[0]) / 2, y + 44), num, font=fnt(20, True), fill=(255, 255, 255))
        draw.text((x + 96, y + 40), t, font=fnt(30, True), fill=ink)
        for j, line in enumerate(wrap(draw, s, fnt(22), 240)[:2]):
            draw.text((x + 96, y + 90 + j * 28), line, font=fnt(22), fill=muted)
    draw.text((48, 1155), "*ориентир по отзывам категории; индивидуально", font=fnt(16), fill=muted)
    save_jpg(out, c / "04_benefits.jpg")

    # 05 · for-whom as compare-like two columns (proof)
    out = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(out)
    text_center(draw, "ДЛЯ КОГО", 44, fnt(42, True), ink)
    thumb = fit_cover(life, (W - 96, 360))
    paste_rounded(out, thumb, (48, 120), 28)
    draw.rounded_rectangle((48, 520, 430, 1120), 28, fill=(255, 255, 255))
    draw.rounded_rectangle((470, 520, 852, 1120), 28, fill=(255, 255, 255))
    draw.text((90, 555), "Подойдёт", font=fnt(30, True), fill=(46, 125, 80))
    draw.text((510, 555), "Менее актуально", font=fnt(26, True), fill=(160, 70, 60))
    left = ["офис и день", "лёгкий цветочный", "подарок без риска", "объём 50 мл"]
    right = ["тяжёлый вечерний", "очень сладкий шлейф", "коллекционный нишевый"]
    y = 630
    for t in left:
        draw.ellipse((80, y + 6, 104, y + 30), fill=(46, 125, 80))
        draw.text((86, y + 6), "✓", font=fnt(15, True), fill=(255, 255, 255))
        draw.text((118, y + 4), t, font=fnt(22), fill=ink)
        y += 90
    y = 630
    for t in right:
        draw.ellipse((502, y + 6, 526, y + 30), fill=(160, 70, 60))
        draw.text((508, y + 4), "×", font=fnt(15, True), fill=(255, 255, 255))
        draw.text((540, y + 4), t, font=fnt(22), fill=ink)
        y += 90
    save_jpg(out, c / "05_proof.jpg")

    # 03 · notes as specs_icon_list (pyramid text blocks)
    out = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(out)
    text_center(draw, "ПИРАМИДА НОТ", 44, fnt(42, True), ink)
    photo = fit_contain(cover, (380, 900), pad=0.92, bg=(250, 246, 255))
    out = shadow_round(out, (40, 130, 420, 1030), 28).convert("RGB")
    draw = ImageDraw.Draw(out)
    paste_rounded(out, photo, (40, 130), 28)
    notes = [
        ("Верх", "цитрус · зелень"),
        ("Сердце", "цветы · лёгкость"),
        ("База", "мускус · дерево"),
        ("Формат", "EDT · 50 мл"),
    ]
    y = 160
    for label, value in notes:
        draw.rounded_rectangle((460, y, W - 40, y + 160), 22, fill=(255, 255, 255))
        draw.text((490, y + 28), label, font=fnt(22), fill=muted)
        for j, line in enumerate(wrap(draw, value, fnt(28, True), 340)[:2]):
            draw.text((490, y + 68 + j * 34), line, font=fnt(28, True), fill=ink)
        y += 190
    save_jpg(out, c / "03_notes.jpg")


# ---------------------------------------------------------------------------
# Case 5 · blender
# ---------------------------------------------------------------------------
def case5():
    c = IMG / "case5"
    cover = Image.open(c / "01_cover.jpg")
    life = Image.open(c / "02_lifestyle.jpg")
    kit = Image.open(c / "03_kit.jpg")
    benefits = Image.open(c / "04_benefits.jpg")
    bg = (236, 238, 236)
    ink = (36, 40, 38)
    muted = (100, 110, 105)
    accent = (40, 90, 80)

    # 04 · benefits_2x2 (case already had side rail — switch grid)
    out = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(out)
    text_center(draw, "MIXORA", 36, fnt(42, True), ink)
    text_center(draw, "портативный блендер", 90, fnt(22), muted)
    photo = fit_cover(benefits, (W - 96, 420))
    paste_rounded(out, photo, (48, 140), 28)
    tiles = [
        ("01", "В сумку", "компактный корпус"),
        ("02", "USB", "без розетки рядом"),
        ("03", "Легко мыть", "разборная чаша"),
        ("04", "300 Вт", "смузи за минуты"),
    ]
    positions = [(48, 600), (474, 600), (48, 880), (474, 880)]
    for (num, t, s), (x, y) in zip(tiles, positions):
        draw.rounded_rectangle((x, y, x + 378, y + 240), 24, fill=(255, 255, 255))
        draw.ellipse((x + 24, y + 32, x + 76, y + 84), fill=accent)
        nb = draw.textbbox((0, 0), num, font=fnt(20, True))
        draw.text((x + 50 - (nb[2] - nb[0]) / 2, y + 44), num, font=fnt(20, True), fill=(255, 255, 255))
        draw.text((x + 96, y + 40), t, font=fnt(30, True), fill=ink)
        draw.text((x + 96, y + 90), s, font=fnt(22), fill=muted)
    save_jpg(out, c / "04_benefits.jpg")

    # 05 · care_steps
    out = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(out)
    text_center(draw, "УХОД ЗА БЛЕНДЕРОМ", 40, fnt(38, True), ink)
    thumb = fit_cover(cover, (W - 96, 340))
    paste_rounded(out, thumb, (48, 110), 28)
    steps = [
        ("1", "Разобрать", "чаша и ножи отдельно"),
        ("2", "Промыть", "тёплая вода, без абразива"),
        ("3", "Высушить", "собрать после просушки"),
    ]
    y = 490
    for num, title, sub in steps:
        draw.rounded_rectangle((48, y, W - 48, y + 140), 24, fill=(255, 255, 255))
        draw.ellipse((72, y + 40, 132, y + 100), fill=accent)
        nb = draw.textbbox((0, 0), num, font=fnt(26, True))
        draw.text((102 - (nb[2] - nb[0]) / 2, y + 54), num, font=fnt(26, True), fill=(255, 255, 255))
        draw.text((160, y + 40), title, font=fnt(30, True), fill=ink)
        draw.text((160, y + 86), sub, font=fnt(24), fill=muted)
        y += 160
    draw.text((48, 1010), "Не погружать моторный блок в воду", font=fnt(22), fill=muted)
    save_jpg(out, c / "05_care.jpg")

    # 06 · compare_split
    out = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(out)
    text_center(draw, "ПОРТАТИВНЫЙ VS ОБЫЧНЫЙ", 36, fnt(34, True), ink)
    thumb = fit_cover(life, (320, 260))
    paste_rounded(out, thumb, ((W - 320) // 2, 100), 20)
    draw.rounded_rectangle((48, 400, 430, 1120), 28, fill=(255, 255, 255))
    draw.rounded_rectangle((470, 400, 852, 1120), 28, fill=(252, 248, 245))
    draw.text((78, 430), "MIXORA", font=fnt(30, True), fill=(46, 125, 80))
    draw.text((500, 430), "Обычный", font=fnt(30, True), fill=(160, 70, 60))
    rows = [
        ("USB, без розетки", "нужна розетка"),
        ("в сумку / спортзал", "только кухня"),
        ("чаша 400 мл", "громоздкая чаша"),
        ("мыть за минуту", "много деталей"),
    ]
    y = 520
    for a, b in rows:
        draw.ellipse((78, y + 6, 102, y + 30), fill=(46, 125, 80))
        draw.text((84, y + 6), "✓", font=fnt(15, True), fill=(255, 255, 255))
        draw.text((116, y + 4), a, font=fnt(21), fill=ink)
        draw.ellipse((500, y + 6, 524, y + 30), fill=(160, 70, 60))
        draw.text((506, y + 4), "×", font=fnt(15, True), fill=(255, 255, 255))
        draw.text((538, y + 4), b, font=fnt(21), fill=ink)
        y += 120
    save_jpg(out, c / "06_compare.jpg")

    # 03 · kit as checklist under flatlay crop
    out = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(out)
    text_center(draw, "ЧТО В КОРОБКЕ", 40, fnt(40, True), ink)
    photo = fit_cover(kit, (W - 96, 520))
    paste_rounded(out, photo, (48, 110), 28)
    items = [
        "моторный блок 300 Вт",
        "чаша 400 мл + крышка",
        "ножевой блок",
        "USB-C кабель",
        "щётка для чистки",
    ]
    y = 670
    for item in items:
        draw.rounded_rectangle((48, y, W - 48, y + 78), 18, fill=(255, 255, 255))
        draw.ellipse((72, y + 22, 106, y + 56), fill=accent)
        draw.text((80, y + 26), "✓", font=fnt(18, True), fill=(255, 255, 255))
        draw.text((128, y + 22), item, font=fnt(26), fill=ink)
        y += 92
    save_jpg(out, c / "03_kit.jpg")


def main():
    case2()
    case3()
    case4()
    case5()


if __name__ == "__main__":
    main()
