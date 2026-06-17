#!/usr/bin/env python3
"""Generate He-man do Sertao source sprites from individual frame images.

Current scope is intentionally small: two idle frames only. Required MUGEN
fallback animations reuse the idle frames in the character builder.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
REFERENCE_DIR = ROOT / "assets" / "he_man_do_sertao" / "reference" / "idle"
OUT_DIR = ROOT / "assets" / "he_man_do_sertao" / "sprites"
PCX_DIR = OUT_DIR / "pcx"

TRANSPARENT = (0, 0, 0, 0)
PREVIEW_BG = (32, 34, 40, 255)
CELL_BG = (48, 51, 58, 255)
GRID = (58, 61, 68, 255)
GROUND = (96, 91, 78, 255)
PCX_TRANSPARENT_RGB = (0, 255, 0)
PCX_ALPHA_CUTOFF = 220
GAMEPLAY_TARGET_HEIGHT = 108
GAMEPLAY_CANVAS_W = 220
GAMEPLAY_CANVAS_H = 170
GAMEPLAY_AXIS_X = 110
GAMEPLAY_AXIS_Y = 158


@dataclass(frozen=True)
class FrameSpec:
    name: str
    title: str
    source: str
    ground_ratio: float = 0.96


FRAMES = [
    FrameSpec("idle_00", "Idle 0", "idle_00.png"),
    FrameSpec("idle_01", "Idle 1", "idle_01.png"),
]


def is_checker_background(rgb: tuple[int, int, int]) -> bool:
    r, g, b = rgb
    is_gray = abs(r - g) < 8 and abs(g - b) < 8
    return is_gray and 95 <= r <= 230


def remove_checker_background(img: Image.Image) -> Image.Image:
    rgb = img.convert("RGB")
    alpha = Image.new("L", rgb.size, 255)
    src = rgb.load()
    alpha_px = alpha.load()
    w, h = rgb.size
    queue: deque[tuple[int, int]] = deque()
    visited: set[tuple[int, int]] = set()

    for x in range(w):
        queue.append((x, 0))
        queue.append((x, h - 1))
    for y in range(h):
        queue.append((0, y))
        queue.append((w - 1, y))

    while queue:
        x, y = queue.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if not is_checker_background(src[x, y]):
            continue

        alpha_px[x, y] = 0
        if x > 0:
            queue.append((x - 1, y))
        if x < w - 1:
            queue.append((x + 1, y))
        if y > 0:
            queue.append((x, y - 1))
        if y < h - 1:
            queue.append((x, y + 1))

    out = img.convert("RGBA")
    out.putalpha(alpha)
    return out


def trim_transparent(img: Image.Image, margin: int = 2) -> Image.Image:
    bbox = img.getbbox()
    if bbox is None:
        return img
    x0, y0, x1, y1 = bbox
    return img.crop((max(0, x0 - margin), max(0, y0 - margin), min(img.width, x1 + margin), min(img.height, y1 + margin)))


def normalize_height(img: Image.Image) -> Image.Image:
    if img.height <= GAMEPLAY_TARGET_HEIGHT:
        return img
    scale = GAMEPLAY_TARGET_HEIGHT / img.height
    return img.resize((max(1, round(img.width * scale)), GAMEPLAY_TARGET_HEIGHT), Image.Resampling.LANCZOS)


def place_on_canvas(img: Image.Image, ground_ratio: float = 0.96) -> Image.Image:
    canvas = Image.new("RGBA", (GAMEPLAY_CANVAS_W, GAMEPLAY_CANVAS_H), TRANSPARENT)
    axis_x = img.width // 2
    axis_y = round(img.height * ground_ratio)
    canvas.alpha_composite(img, (GAMEPLAY_AXIS_X - axis_x, GAMEPLAY_AXIS_Y - axis_y))
    return canvas


def make_frame(spec: FrameSpec) -> Image.Image:
    source = Image.open(REFERENCE_DIR / spec.source).convert("RGBA")
    cleaned = remove_checker_background(source)
    trimmed = trim_transparent(cleaned)
    normalized = normalize_height(trimmed)
    return place_on_canvas(trim_transparent(normalized), spec.ground_ratio)


def make_portrait_small(frame: Image.Image) -> Image.Image:
    bbox = frame.getbbox()
    crop = frame.crop(bbox) if bbox else frame
    crop = crop.crop((0, 0, crop.width, max(1, int(crop.height * 0.55))))
    crop.thumbnail((23, 23), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (25, 25), TRANSPARENT)
    canvas.alpha_composite(crop, ((25 - crop.width) // 2, (25 - crop.height) // 2))
    return canvas


def make_portrait_big(frame: Image.Image) -> Image.Image:
    bbox = frame.getbbox()
    crop = frame.crop(bbox) if bbox else frame
    crop.thumbnail((110, 136), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (120, 140), TRANSPARENT)
    canvas.alpha_composite(crop, ((120 - crop.width) // 2, 140 - crop.height - 2))
    return canvas


def quantized_palette(frames: list[Image.Image]) -> list[int]:
    atlas_w = max(frame.width for frame in frames)
    atlas_h = sum(frame.height for frame in frames)
    atlas = Image.new("RGB", (atlas_w, atlas_h), (0, 0, 0))
    y_offset = 0
    for frame in frames:
        rgba = frame.convert("RGBA")
        rgb = Image.new("RGB", rgba.size, (0, 0, 0))
        src = rgba.load()
        dst = rgb.load()
        for y in range(rgba.height):
            for x in range(rgba.width):
                r, g, b, a = src[x, y]
                if a >= PCX_ALPHA_CUTOFF:
                    dst[x, y] = (r, g, b)
        atlas.paste(rgb, (0, y_offset))
        y_offset += frame.height
    paletted = atlas.quantize(colors=255, method=Image.Quantize.MEDIANCUT)
    palette = paletted.getpalette()[: 255 * 3]
    return [*PCX_TRANSPARENT_RGB] + palette + [0, 0, 0] * (256 - 1 - len(palette) // 3)


def save_indexed_pcx(frame: Image.Image, palette: list[int], name: str) -> None:
    rgba = frame.convert("RGBA")
    rgb = Image.new("RGB", frame.size, PCX_TRANSPARENT_RGB)
    src = rgba.load()
    dst = rgb.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, a = src[x, y]
            if a >= PCX_ALPHA_CUTOFF:
                dst[x, y] = (r, g, b)
    pal = Image.new("P", (1, 1))
    pal.putpalette(palette)
    indexed = rgb.quantize(palette=pal, dither=Image.Dither.NONE)
    pix = indexed.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            if src[x, y][3] < PCX_ALPHA_CUTOFF:
                pix[x, y] = 0
    indexed.save(PCX_DIR / f"{name}.pcx")


def make_preview(items: list[tuple[FrameSpec, Image.Image]]) -> Image.Image:
    cols = 4
    cell_w = 154
    cell_h = 156
    rows = (len(items) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * cell_w, rows * cell_h), PREVIEW_BG)
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 10)
        font_small = ImageFont.truetype("DejaVuSans.ttf", 9)
    except OSError:
        font = ImageFont.load_default()
        font_small = font

    for idx, (spec, frame) in enumerate(items):
        cx = (idx % cols) * cell_w
        cy = (idx // cols) * cell_h
        draw.rectangle((cx + 6, cy + 6, cx + cell_w - 7, cy + cell_h - 7), fill=CELL_BG)
        for gx in range(cx + 14, cx + cell_w - 14, 16):
            draw.line((gx, cy + 14, gx, cy + 126), fill=GRID)
        for gy in range(cy + 14, cy + 126, 16):
            draw.line((cx + 14, gy, cx + cell_w - 14, gy), fill=GRID)
        scale = min(1.0, (cell_w - 30) / frame.width, 110 / frame.height)
        shown = frame if scale == 1.0 else frame.resize((round(frame.width * scale), round(frame.height * scale)), Image.Resampling.NEAREST)
        ground_y = cy + 14 + round(110 * spec.ground_ratio)
        sheet.alpha_composite(shown, (cx + (cell_w - shown.width) // 2, ground_y - round(shown.height * spec.ground_ratio)))
        draw.line((cx + 14, ground_y, cx + cell_w - 14, ground_y), fill=GROUND)
        draw.text((cx + 10, cy + 130), spec.title, fill=(235, 232, 215, 255), font=font)
        draw.text((cx + 10, cy + 142), f"{spec.name}.png", fill=(175, 180, 188, 255), font=font_small)
    return sheet


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PCX_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_DIR.glob("*.png"):
        old.unlink()
    for old in PCX_DIR.glob("*.pcx"):
        old.unlink()

    frames: list[tuple[FrameSpec, Image.Image]] = []
    frame_by_name: dict[str, Image.Image] = {}
    for spec in FRAMES:
        frame = make_frame(spec)
        frame.save(OUT_DIR / f"{spec.name}.png")
        frames.append((spec, frame))
        frame_by_name[spec.name] = frame

    for spec, frame in [
        (FrameSpec("portrait_small", "Small Portrait", "idle_00.png"), make_portrait_small(frame_by_name["idle_00"])),
        (FrameSpec("portrait_big", "Big Portrait", "idle_00.png"), make_portrait_big(frame_by_name["idle_00"])),
    ]:
        frame.save(OUT_DIR / f"{spec.name}.png")
        frames.append((spec, frame))

    palette = quantized_palette(frames=[frame for _, frame in frames])
    for spec, frame in frames:
        save_indexed_pcx(frame, palette, spec.name)
    make_preview(frames).save(OUT_DIR / "he_man_do_sertao_sprite_sheet_preview.png")


if __name__ == "__main__":
    main()
