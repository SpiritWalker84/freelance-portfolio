"""Shared 900×1200 helpers for marketplace layout templates."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
IMG = ROOT / "public" / "images" / "marketplace"
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


def fit_contain(im: Image.Image, box: tuple[int, int], pad: float = 0.9, bg=(245, 242, 236)) -> Image.Image:
    tw, th = box
    canvas = Image.new("RGB", (tw, th), bg)
    src = im.convert("RGBA")
    sw, sh = src.size
    scale = min(tw / sw, th / sh) * pad
    nw, nh = max(1, int(sw * scale)), max(1, int(sh * scale))
    src = src.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas.paste(src, ((tw - nw) // 2, (th - nh) // 2), src)
    return canvas


def paste_rounded(base: Image.Image, src: Image.Image, xy: tuple[int, int], radius: int = 28):
    mask = Image.new("L", src.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, src.size[0] - 1, src.size[1] - 1), radius, fill=255)
    base.paste(src, xy, mask)


def shadow_round(base: Image.Image, box, radius=24, blur=14, alpha=48) -> Image.Image:
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(overlay).rounded_rectangle(box, radius, fill=(0, 0, 0, alpha))
    overlay = overlay.filter(ImageFilter.GaussianBlur(blur))
    return Image.alpha_composite(base.convert("RGBA"), overlay)


def text_center(draw: ImageDraw.ImageDraw, text: str, y: int, font, fill):
    bb = draw.textbbox((0, 0), text, font=font)
    draw.text(((W - (bb[2] - bb[0])) / 2, y), text, font=font, fill=fill)


def wrap(draw: ImageDraw.ImageDraw, text: str, font, max_w: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [text]


def save_jpg(im: Image.Image, path: Path, quality: int = 90):
    path.parent.mkdir(parents=True, exist_ok=True)
    im.convert("RGB").save(path, quality=quality, optimize=True)
    print(f"wrote {path.relative_to(ROOT)}")


def save_png(im: Image.Image, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    im.convert("RGB").save(path, optimize=True)
    print(f"wrote {path.relative_to(ROOT)}")
