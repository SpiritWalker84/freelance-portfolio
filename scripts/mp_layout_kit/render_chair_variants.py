"""Render chair slides on distinct layout templates (not one pill stack)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
CASE1 = ROOT / "public" / "images" / "marketplace" / "case1"
OUT = CASE1
W, H = 900, 1200

FONT = r"C:\Windows\Fonts\segoeui.ttf"
FONT_B = r"C:\Windows\Fonts\segoeuib.ttf"

BG = (242, 236, 228)
INK = (42, 36, 32)
MUTED = (110, 100, 92)
ACCENT = (58, 48, 40)
WHITE = (255, 255, 255)
OK = (46, 125, 80)
BAD = (160, 70, 60)


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


def fit_contain(im: Image.Image, box: tuple[int, int], pad: float = 0.9, bg=BG) -> Image.Image:
    tw, th = box
    canvas = Image.new("RGB", (tw, th), bg)
    src = im.convert("RGBA")
    sw, sh = src.size
    scale = min(tw / sw, th / sh) * pad
    nw, nh = max(1, int(sw * scale)), max(1, int(sh * scale))
    src = src.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas.paste(src, ((tw - nw) // 2, (th - nh) // 2), src)
    return canvas


def shadow_rect(base: Image.Image, box, radius=24, blur=14, alpha=50):
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.rounded_rectangle(box, radius, fill=(0, 0, 0, alpha))
    overlay = overlay.filter(ImageFilter.GaussianBlur(blur))
    return Image.alpha_composite(base.convert("RGBA"), overlay)


def paste_rounded(base: Image.Image, src: Image.Image, xy: tuple[int, int], radius=28):
    mask = Image.new("L", src.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, src.size[0] - 1, src.size[1] - 1), radius, fill=255)
    base.paste(src, xy, mask)


def text_center(draw, text, y, font, fill=WHITE):
    bb = draw.textbbox((0, 0), text, font=font)
    tw = bb[2] - bb[0]
    draw.text(((W - tw) / 2, y), text, font=font, fill=fill)


# --- template: dims_callouts ---
def render_dims_callouts():
    studio = Image.open(CASE1 / "source_chair_studio.png")
    out = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(out)
    text_center(draw, "РАЗМЕРЫ", 48, fnt(48, True), INK)
    draw.text((W // 2 - 90, 108), "мягкое кресло Сидней", font=fnt(22), fill=MUTED)

    # product panel
    panel = fit_contain(studio, (720, 780), pad=0.88, bg=(250, 247, 242))
    out = shadow_rect(out, (90, 160, 810, 940), radius=32, blur=16, alpha=45).convert("RGB")
    draw = ImageDraw.Draw(out)
    paste_rounded(out, panel, (90, 160), 32)
    draw.rounded_rectangle((90, 160, 810, 940), 32, outline=(220, 210, 200), width=2)

    # dimension ticks around product (visual hierarchy ≠ pill list)
    tick = fnt(26, True)
    # height left
    draw.line((130, 220, 130, 860), fill=ACCENT, width=3)
    draw.line((118, 220, 142, 220), fill=ACCENT, width=3)
    draw.line((118, 860, 142, 860), fill=ACCENT, width=3)
    draw.text((148, 510), "85 см", font=tick, fill=ACCENT)
    draw.text((148, 542), "высота", font=fnt(18), fill=MUTED)

    # width bottom
    draw.line((220, 900, 680, 900), fill=ACCENT, width=3)
    draw.line((220, 888, 220, 912), fill=ACCENT, width=3)
    draw.line((680, 888, 680, 912), fill=ACCENT, width=3)
    wb = draw.textbbox((0, 0), "58 см · ширина", font=tick)
    draw.text((450 - (wb[2] - wb[0]) / 2, 920), "58 см · ширина", font=tick, fill=ACCENT)

    # depth right
    draw.line((770, 280, 770, 720), fill=ACCENT, width=3)
    draw.line((758, 280, 782, 280), fill=ACCENT, width=3)
    draw.line((758, 720, 782, 720), fill=ACCENT, width=3)
    draw.text((640, 470), "60 см", font=tick, fill=ACCENT)
    draw.text((620, 502), "глубина", font=fnt(18), fill=MUTED)

    # corner facts (not another pill stack)
    facts = [("сиденье", "45 см"), ("нагрузка", "до 120 кг")]
    x = 70
    for label, val in facts:
        draw.rounded_rectangle((x, 1040, x + 360, 1140), 20, fill=WHITE)
        draw.text((x + 28, 1058), label, font=fnt(20), fill=MUTED)
        draw.text((x + 28, 1088), val, font=fnt(34, True), fill=INK)
        x += 400

    out.save(OUT / "02_dimensions.png", optimize=True)
    print("dims_callouts -> 02_dimensions.png")


# --- template: usp_side_rail ---
def render_usp_side_rail():
    studio = Image.open(CASE1 / "source_chair_studio.png")
    # warm cream field, product right, rail left
    out = Image.new("RGB", (W, H), (235, 228, 218))
    hero = fit_cover(studio, (620, 980))
    # soft vignette panel
    out.paste(hero, (280, 140))

    # left wash so pills read
    wash = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wash)
    for i in range(420):
        a = int(200 * (1 - i / 420))
        wd.line((i, 0, i, H), fill=(235, 228, 218, a))
    out = Image.alpha_composite(out.convert("RGBA"), wash).convert("RGB")
    draw = ImageDraw.Draw(out)

    draw.text((48, 56), "СИДНЕЙ", font=fnt(44, True), fill=INK)
    draw.text((48, 112), "мягкое кресло · ежедневный комфорт", font=fnt(22), fill=MUTED)

    pills = ["МЯГКОЕ СИДЕНЬЕ", "СКАНДИ-ОБИВКА", "ДО 120 КГ"]
    y = 220
    for p in pills:
        pf = fnt(26, True)
        tw = draw.textlength(p, font=pf)
        draw.rounded_rectangle((48, y, 48 + tw + 48, y + 72), 18, fill=WHITE)
        draw.text((72, y + 20), p, font=pf, fill=INK)
        y += 100

    # bottom caption bar (different from header+list template)
    draw.rounded_rectangle((48, 1040, W - 48, 1145), 24, fill=(35, 30, 28))
    draw.text((80, 1065), "Гостиная · спальня · кабинет", font=fnt(28, True), fill=WHITE)
    draw.text((80, 1105), "Деревянные ножки · светлый букле", font=fnt(22), fill=(210, 205, 200))

    out.save(OUT / "04_benefits.png", optimize=True)
    print("usp_side_rail -> 04_benefits.png")


# --- template: compare_split ---
def render_compare_split():
    studio = Image.open(CASE1 / "source_chair_studio.png")
    out = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(out)
    text_center(draw, "ПОЧЕМУ ЭТОТ", 44, fnt(44, True), INK)
    draw.text((W // 2 - 160, 100), "кресло vs типичный вариант", font=fnt(22), fill=MUTED)

    thumb = fit_contain(studio, (280, 280), pad=0.85, bg=(250, 247, 242))
    paste_rounded(out, thumb, ((W - 280) // 2, 150), 24)

    # two columns
    left = (48, 470, 430, 1120)
    right = (470, 470, 852, 1120)
    draw.rounded_rectangle(left, 28, fill=WHITE)
    draw.rounded_rectangle(right, 28, fill=(252, 245, 242))
    draw.text((90, 500), "Сидней", font=fnt(32, True), fill=OK)
    draw.text((520, 500), "Типичный", font=fnt(32, True), fill=BAD)

    rows = [
        ("нагрузка до 120 кг", "часто до 80–90 кг"),
        ("светлый букле", "гладкая синтетика"),
        ("высота сиденья 45 см", "низкая / без указания"),
        ("ножки дерево", "пластик / скрыты"),
    ]
    y = 570
    for ours, theirs in rows:
        draw.ellipse((80, y + 8, 104, y + 32), fill=OK)
        draw.text((86, y + 8), "✓", font=fnt(16, True), fill=WHITE)
        draw.text((118, y + 6), ours, font=fnt(22), fill=INK)

        draw.ellipse((502, y + 8, 526, y + 32), fill=BAD)
        draw.text((508, y + 6), "×", font=fnt(16, True), fill=WHITE)
        draw.text((540, y + 6), theirs, font=fnt(22), fill=INK)
        y += 110

    out.save(OUT / "07_compare.png", optimize=True)
    print("compare_split -> 07_compare.png")


def main():
    render_dims_callouts()
    render_usp_side_rail()
    render_compare_split()


if __name__ == "__main__":
    main()
