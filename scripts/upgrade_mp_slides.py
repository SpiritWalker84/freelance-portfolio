"""Rebuild sparse marketplace slides (case1) into denser 900x1200 cards."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
CASE1 = ROOT / "public" / "images" / "marketplace" / "case1"
W, H = 900, 1200

FONT = r"C:\Windows\Fonts\segoeui.ttf"
FONT_B = r"C:\Windows\Fonts\segoeuib.ttf"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_B if bold else FONT, size)


def round_rect(draw: ImageDraw.ImageDraw, box, radius: int, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


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


def fit_contain(im: Image.Image, box: tuple[int, int, int, int], bg=(245, 242, 236)) -> Image.Image:
    x0, y0, x1, y1 = box
    tw, th = x1 - x0, y1 - y0
    canvas = Image.new("RGB", (tw, th), bg)
    src = im.convert("RGBA")
    sw, sh = src.size
    scale = min(tw / sw, th / sh) * 0.92
    nw, nh = max(1, int(sw * scale)), max(1, int(sh * scale))
    src = src.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas.paste(src, ((tw - nw) // 2, (th - nh) // 2), src if src.mode == "RGBA" else None)
    return canvas


def wrap(draw, text: str, fnt, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [text]


def draw_header(draw, title: str, bg=(54, 42, 34), y=0, h=92):
    draw.rectangle((0, y, W, y + h), fill=bg)
    f = font(42, bold=True)
    bbox = draw.textbbox((0, 0), title, font=f)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text(((W - tw) / 2, y + (h - th) / 2 - 4), title, font=f, fill=(255, 255, 255))


def pill_rows(draw, items: list[tuple[str, str]] | list[str], y_start: int, *, pair=False):
    f_label = font(28, bold=True)
    f_val = font(28, bold=False)
    f_single = font(30, bold=False)
    gap = 18
    pill_h = 78
    x0, x1 = 48, W - 48
    y = y_start
    for item in items:
        round_rect(draw, (x0, y, x1, y + pill_h), 22, (255, 255, 255))
        if pair:
            label, value = item  # type: ignore[misc]
            draw.text((x0 + 28, y + 22), label, font=f_label, fill=(45, 45, 45))
            vw = draw.textlength(value, font=f_val)
            draw.text((x1 - 28 - vw, y + 22), value, font=f_val, fill=(70, 70, 70))
        else:
            text = item if isinstance(item, str) else item[0]
            lines = wrap(draw, text, f_single, x1 - x0 - 56)
            line_h = 32
            total = line_h * len(lines)
            ty = y + (pill_h - total) / 2 - 2
            for i, line in enumerate(lines[:2]):
                draw.text((x0 + 28, ty + i * line_h), line, font=f_single, fill=(40, 40, 40))
        y += pill_h + gap
    return y


def build_dimensions():
    bg = (236, 230, 220)
    out = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(out)
    draw_header(draw, "ГАБАРИТЫ", bg=(58, 48, 40))

    studio = Image.open(CASE1 / "source_chair_studio.png")
    photo = fit_contain(studio, (0, 0, 420, 520), bg=(248, 245, 240))
    # soft shadow
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((48, 130, 48 + 420, 130 + 520), 28, fill=(0, 0, 0, 55))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    out = Image.alpha_composite(out.convert("RGBA"), shadow).convert("RGB")
    draw = ImageDraw.Draw(out)
    out.paste(photo, (48, 130))
    # frame
    draw.rounded_rectangle((48, 130, 48 + 420, 130 + 520), 28, outline=(210, 200, 188), width=3)

    # dimension callouts on right of photo
    specs = [
        ("Высота", "85 см"),
        ("Ширина", "58 см"),
        ("Глубина", "60 см"),
        ("Сиденье", "45 см"),
        ("Нагрузка", "до 120 кг"),
        ("Модель", "Сидней"),
    ]
    y = 150
    for label, value in specs:
        round_rect(draw, (500, y, W - 48, y + 72), 18, (255, 255, 255))
        draw.text((522, y + 10), label, font=font(22, True), fill=(110, 100, 90))
        draw.text((522, y + 36), value, font=font(30, True), fill=(40, 35, 30))
        y += 84

    # bottom tip
    round_rect(draw, (48, 700, W - 48, 1120), 28, (255, 255, 255))
    draw.text((80, 740), "Что важно покупателю", font=font(34, True), fill=(45, 40, 35))
    tips = [
        "• Компактная глубина — не загромождает гостиную",
        "• Высота сиденья 45 см — удобно вставать",
        "• Нагрузка до 120 кг — ежедневное использование",
        "• Светлая обивка — легко вписать в сканди-интерьер",
    ]
    yy = 810
    for t in tips:
        draw.text((80, yy), t, font=font(28), fill=(55, 50, 45))
        yy += 58

    out.save(CASE1 / "02_dimensions.png", optimize=True)
    print("wrote 02_dimensions.png")


def build_benefits():
    bg = (240, 234, 226)
    out = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(out)
    draw_header(draw, "ПРЕИМУЩЕСТВА", bg=(58, 48, 40))

    studio = Image.open(CASE1 / "source_chair_studio.png")
    # top photo strip
    strip = fit_cover(studio, (W - 96, 420))
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((48, 120, W - 48, 120 + 420), 28, fill=(0, 0, 0, 50))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    out = Image.alpha_composite(out.convert("RGBA"), shadow).convert("RGB")
    draw = ImageDraw.Draw(out)
    # mask rounded paste
    mask = Image.new("L", strip.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, strip.size[0], strip.size[1]), 28, fill=255)
    out.paste(strip, (48, 120), mask)

    benefits = [
        "Мягкое сиденье и спинка — комфорт каждый день",
        "Светлая обивка — легко сочетается со сканди",
        "Деревянные ножки — устойчивость и аккуратный вид",
        "Гостиная, спальня, кабинет, кухня-столовая",
    ]
    y = 580
    for i, text in enumerate(benefits, 1):
        round_rect(draw, (48, y, W - 48, y + 110), 24, (255, 255, 255))
        # number badge
        cx, cy = 98, y + 55
        draw.ellipse((cx - 28, cy - 28, cx + 28, cy + 28), fill=(58, 48, 40))
        n = str(i)
        nf = font(28, True)
        nb = draw.textbbox((0, 0), n, font=nf)
        draw.text((cx - (nb[2] - nb[0]) / 2, cy - (nb[3] - nb[1]) / 2 - 2), n, font=nf, fill=(255, 255, 255))
        lines = wrap(draw, text, font(28), W - 220)
        ty = y + 28 if len(lines) == 1 else y + 22
        for j, line in enumerate(lines[:2]):
            draw.text((150, ty + j * 34), line, font=font(28), fill=(40, 35, 30))
        y += 128

    draw.text(
        (48, 1145),
        "Цвет ткани на фото может незначительно отличаться от партии.",
        font=font(20),
        fill=(120, 110, 100),
    )
    out.save(CASE1 / "04_benefits.png", optimize=True)
    print("wrote 04_benefits.png")


def build_studio():
    studio = Image.open(CASE1 / "source_chair_studio.png")
    photo = fit_cover(studio, (W, H))
    out = photo.convert("RGBA")
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    # bottom panel
    d.rounded_rectangle((36, 920, W - 36, 1160), 28, fill=(35, 30, 28, 210))
    out = Image.alpha_composite(out, overlay)
    draw = ImageDraw.Draw(out)
    draw.text((70, 960), "Мягкое кресло Сидней", font=font(40, True), fill=(255, 255, 255))
    draw.text((70, 1020), "Студийный ракурс · цвет и форма без отвлечений", font=font(26), fill=(230, 225, 220))
    chips = ["букле", "дерево", "до 120 кг"]
    x = 70
    for chip in chips:
        f = font(22, True)
        tw = draw.textlength(chip, font=f)
        draw.rounded_rectangle((x, 1080, x + tw + 36, 1130), 18, fill=(255, 255, 255, 230))
        draw.text((x + 18, 1088), chip, font=f, fill=(40, 35, 30))
        x += tw + 52
    out.convert("RGB").save(CASE1 / "05_studio_product.png", optimize=True)
    print("wrote 05_studio_product.png")


def build_care():
    bg = (236, 230, 220)
    out = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(out)
    draw_header(draw, "КОМПЛЕКТАЦИЯ И УХОД", bg=(58, 48, 40))

    studio = Image.open(CASE1 / "source_chair_studio.png")
    photo = fit_contain(studio, (0, 0, W - 96, 480), bg=(248, 245, 240))
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((48, 120, W - 48, 120 + 480), 28, fill=(0, 0, 0, 50))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    out = Image.alpha_composite(out.convert("RGBA"), shadow).convert("RGB")
    draw = ImageDraw.Draw(out)
    mask = Image.new("L", photo.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, photo.size[0], photo.size[1]), 28, fill=255)
    out.paste(photo, (48, 120), mask)

    items = [
        ("Комплект", "кресло, ножки ×4, крепёж, инструкция"),
        ("Обивка", "износостойкий текстиль, сухая чистка"),
        ("Каркас", "усиленный, ежедневная нагрузка"),
        ("Уход", "не отбеливать; пятна — мягкой салфеткой"),
    ]
    y = 640
    for label, value in items:
        round_rect(draw, (48, y, W - 48, y + 110), 24, (255, 255, 255))
        draw.text((80, y + 18), label, font=font(24, True), fill=(120, 105, 90))
        lines = wrap(draw, value, font(30), W - 160)
        draw.text((80, y + 54), lines[0], font=font(30), fill=(40, 35, 30))
        if len(lines) > 1:
            draw.text((80, y + 88), lines[1], font=font(28), fill=(40, 35, 30))
        y += 128

    out.save(CASE1 / "06_care_structure.png", optimize=True)
    print("wrote 06_care_structure.png")


def main():
    build_dimensions()
    build_benefits()
    build_studio()
    build_care()


if __name__ == "__main__":
    main()
