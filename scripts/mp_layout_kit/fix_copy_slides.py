"""Fix chair compare, shelf dims, poncho copy — human buyer-facing texts."""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
IMG = ROOT / "public" / "images" / "marketplace"
COPY = json.loads((Path(__file__).with_name("copy.ru.json")).read_text(encoding="utf-8"))

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


def draw_check(draw, x: int, y: int, size: int = 22, color=(46, 125, 80), width: int = 4):
    """Simple green checkmark, geometrically centered on (x,y)."""
    # relative points of a check
    p1 = (x - size * 0.45, y + size * 0.05)
    p2 = (x - size * 0.1, y + size * 0.4)
    p3 = (x + size * 0.5, y - size * 0.4)
    draw.line([p1, p2, p3], fill=color, width=width, joint="curve")


def draw_cross(draw, x: int, y: int, size: int = 18, color=(180, 70, 60), width: int = 4):
    """Simple red X, centered on (x,y)."""
    s = size * 0.55
    draw.line((x - s, y - s, x + s, y + s), fill=color, width=width)
    draw.line((x + s, y - s, x - s, y + s), fill=color, width=width)


def fix_chair_compare():
    # Override title to something natural
    title = "В чём разница"
    sub = "Сидней и обычное кресло"
    ours_label = "Сидней"
    theirs_label = "Часто бывает"
    rows = COPY["case1_chair"]["07_compare"]["rows"]

    studio = Image.open(IMG / "case1" / "source_chair_studio.png")
    bg = (242, 236, 228)
    ink = (42, 36, 32)
    muted = (110, 100, 92)
    out = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(out)

    text_center(draw, title, 48, fnt(44, True), ink)
    text_center(draw, sub, 112, fnt(24), muted)

    thumb = fit_contain(studio, (300, 280), pad=0.88, bg=(250, 247, 242))
    paste_rounded(out, thumb, ((W - 300) // 2, 165), 22)

    draw.rounded_rectangle((40, 490, 440, 1145), 28, fill=(255, 255, 255))
    draw.rounded_rectangle((460, 490, 860, 1145), 28, fill=(252, 245, 242))
    draw.text((80, 520), ours_label, font=fnt(32, True), fill=(46, 125, 80))
    draw.text((500, 520), theirs_label, font=fnt(30, True), fill=(180, 70, 60))

    y = 610
    for ours, theirs in rows:
        draw_check(draw, 78, y + 14)
        draw.text((110, y), ours, font=fnt(22), fill=ink)
        draw_cross(draw, 498, y + 14)
        draw.text((530, y), theirs, font=fnt(22), fill=ink)
        y += 115

    out.save(IMG / "case1" / "07_compare.png", optimize=True)
    print("fixed chair compare")


def heal_region(im: Image.Image, box, color, blur: int = 8):
    """Soft-fill a rectangle with solid color (hide old annotations)."""
    overlay = Image.new("RGB", im.size, color)
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rectangle(box, fill=255)
    if blur:
        mask = mask.filter(ImageFilter.GaussianBlur(blur))
    return Image.composite(overlay, im, mask)


def fix_shelf_dims():
    """Clean shelf photo + only length + depth + material/load. No fake height."""
    c = COPY["case2_shelf"]["03_dims"]
    base_path = IMG / "case2" / "_dims_base.jpg"
    base = Image.open(base_path).convert("RGB")
    # Base already 900x1200-ish; normalize
    base = fit_cover(base, (W, H))

    # Heal old dimension lines / labels (approximate zones on previous slide)
    beige = (245, 240, 232)
    # top title strip — redraw clean
    base = heal_region(base, (0, 0, W, 130), beige, blur=2)
    # vertical 500 mm line area (right)
    base = heal_region(base, (780, 180, 900, 720), (248, 244, 238), blur=10)
    # horizontal 720 label + line under shelf
    base = heal_region(base, (80, 700, 820, 820), (248, 244, 238), blur=8)
    # depth label zone
    base = heal_region(base, (620, 420, 880, 560), (248, 244, 238), blur=8)
    # left material text zone / bottom
    base = heal_region(base, (0, 820, W, H), beige, blur=2)
    # left "Материал" old
    base = heal_region(base, (20, 620, 220, 720), (248, 244, 238), blur=10)

    out = base
    draw = ImageDraw.Draw(out)
    ink = (45, 38, 34)
    muted = (100, 90, 80)
    accent = (35, 35, 35)

    text_center(draw, c["title"].upper(), 42, fnt(40, True), ink)

    # Shelf front edge is slightly tilted: left higher than right on this photo
    # Approximate underside of shelf board
    x0, y0 = 175, 618
    x1, y1 = 720, 638
    draw.line((x0, y0, x1, y1), fill=accent, width=3)
    # end ticks roughly perpendicular to shelf
    draw.line((x0 - 2, y0 - 14, x0 + 4, y0 + 14), fill=accent, width=3)
    draw.line((x1 - 2, y1 - 14, x1 + 4, y1 + 14), fill=accent, width=3)
    lf = fnt(28, True)
    label = c["length"]
    bb = draw.textbbox((0, 0), label, font=lf)
    tw = bb[2] - bb[0]
    mx = (x0 + x1) / 2 - tw / 2
    my = (y0 + y1) / 2 + 22
    draw.text((mx, my), label, font=lf, fill=accent)

    # Depth along top-right of shelf board (into wall)
    # parallel to shelf depth direction
    dx0, dy0 = 690, 500
    dx1, dy1 = 760, 545
    draw.line((dx0, dy0, dx1, dy1), fill=accent, width=3)
    draw.line((dx0 - 6, dy0 + 8, dx0 + 8, dy0 - 4), fill=accent, width=2)
    draw.line((dx1 - 6, dy1 + 8, dx1 + 8, dy1 - 4), fill=accent, width=2)
    draw.text((700, 555), c["depth"], font=fnt(26, True), fill=accent)

    draw.rounded_rectangle((48, 1020, 430, 1145), 22, fill=(255, 255, 255))
    draw.rounded_rectangle((470, 1020, 852, 1145), 22, fill=(255, 255, 255))
    draw.text((78, 1045), "Материал", font=fnt(20), fill=muted)
    draw.text((78, 1080), c["material"], font=fnt(32, True), fill=ink)
    draw.text((500, 1045), "Нагрузка", font=fnt(20), fill=muted)
    draw.text((500, 1080), c["load"], font=fnt(32, True), fill=ink)

    out.save(IMG / "case2" / "03_specs_dims.jpg", quality=92, optimize=True)
    print("fixed shelf dims")


def fix_poncho_benefits():
    c = COPY["case3_poncho"]["03_benefits"]
    # Clean fabric source without baked-in infographic text
    fabric = Image.open(IMG / "case3" / "02_product_reference.png")
    bg = (236, 230, 242)
    ink = (48, 36, 58)
    out = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(out)
    text_center(draw, c["title"].upper(), 44, fnt(42, True), ink)

    photo = fit_cover(fabric, (W - 120, 520))
    paste_rounded(out, photo, (60, 120), 28)

    items = c["items"]
    positions = [(48, 700), (474, 700), (48, 920), (474, 920)]
    for text, (x, y) in zip(items, positions):
        draw.rounded_rectangle((x, y, x + 378, y + 180), 24, fill=(255, 255, 255))
        font = fnt(28, True)
        # Prefer natural break on em dash / hyphen for long lines
        if " — " in text:
            a, b = text.split(" — ", 1)
            lines = [a, "— " + b]
        else:
            lines = [text]
        line_h = 34
        total = line_h * len(lines)
        ty = y + (180 - total) / 2
        for i, line in enumerate(lines):
            bb = draw.textbbox((0, 0), line, font=font)
            tw = bb[2] - bb[0]
            draw.text((x + (378 - tw) / 2, ty + i * line_h), line, font=font, fill=ink)

    out.save(IMG / "case3" / "03_benefits.jpg", quality=92, optimize=True)
    print("fixed poncho benefits")


def fix_poncho_scenarios():
    c = COPY["case3_poncho"]["04_scenarios"]
    base = Image.open(IMG / "case3" / "_scenes_base.jpg").convert("RGB")
    base = fit_cover(base, (W, H))
    out = base
    draw = ImageDraw.Draw(out)

    # Clean title
    draw.rectangle((0, 0, W, 115), fill=(245, 242, 238))
    text_center(draw, c["title"].upper(), 40, fnt(42, True), (50, 45, 42))

    # Cover old caption bars completely (bottom-left of each panel) then write once
    # Panels approx: y 130-400, 420-690, 710-980
    covers = [
        (55, 340, 420, 400),
        (55, 620, 380, 680),
        (55, 900, 450, 960),
    ]
    # sample dark for bar bg from nearby
    for box in covers:
        draw.rounded_rectangle(box, 10, fill=(55, 55, 55))

    captions = [
        (70, 355, c["items"][0]),
        (70, 635, c["items"][1]),
        (70, 915, c["items"][2]),
    ]
    for x, y, text in captions:
        draw.text((x, y), text, font=fnt(26, True), fill=(255, 255, 255))

    out.save(IMG / "case3" / "04_scenarios.jpg", quality=92, optimize=True)
    print("fixed poncho scenarios")


def fix_poncho_care():
    c = COPY["case3_poncho"]["05_care"]
    fabric = Image.open(IMG / "case3" / "02_product_reference.png")
    bg = (236, 230, 242)
    ink = (40, 30, 50)
    header = (70, 50, 95)
    out = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(out)
    draw.rectangle((0, 0, W, 100), fill=header)
    text_center(draw, c["title"].upper(), 28, fnt(40, True), (255, 255, 255))

    photo = fit_cover(fabric, (400, 980))
    paste_rounded(out, photo, (40, 140), 24)

    items = c["items"]
    card_h = 170
    gap = 28
    block = len(items) * card_h + (len(items) - 1) * gap
    y = 140 + max(0, (980 - block) // 2)
    for item in items:
        draw.rounded_rectangle((470, y, W - 40, y + card_h), 22, fill=(255, 255, 255))
        font = fnt(28)
        line = "•  " + item
        bb = draw.textbbox((0, 0), line, font=font)
        th = bb[3] - bb[1]
        draw.text((500, y + (card_h - th) / 2 - 4), line, font=font, fill=ink)
        y += card_h + gap

    out.save(IMG / "case3" / "05_care.jpg", quality=92, optimize=True)
    print("fixed poncho care")


def main():
    # Update locked copy titles to match final
    COPY["case1_chair"]["07_compare"]["title"] = "В чём разница"
    COPY["case1_chair"]["07_compare"]["sub"] = "Сидней и обычное кресло"
    Path(__file__).with_name("copy.ru.json").write_text(
        json.dumps(COPY, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    fix_chair_compare()
    fix_shelf_dims()
    fix_poncho_benefits()
    fix_poncho_scenarios()
    fix_poncho_care()


if __name__ == "__main__":
    main()
