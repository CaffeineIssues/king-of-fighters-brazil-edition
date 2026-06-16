#!/usr/bin/env python3
"""Extract Mestre Thaynan sprites from the restart reference sheet.

This pass intentionally uses only the simpler 1024x1024 sheet requested by the
user. Exported gameplay frames are limited to the moves present in that sheet:
idle, walk forward, light punch, and high kick. Required MUGEN fallback states
reuse standing frames in the character builder instead of inventing extra art.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "assets" / "mestre_thaynan" / "reference" / "mestre_thaynan_restart_reference.png"
IDLE_REFERENCE_DIR = ROOT / "assets" / "mestre_thaynan" / "reference" / "idle"
PORTRAIT_REFERENCE_DIR = ROOT / "assets" / "mestre_thaynan" / "reference" / "portraits"
OUT_DIR = ROOT / "assets" / "mestre_thaynan" / "sprites"
PCX_DIR = OUT_DIR / "pcx"

TRANSPARENT = (0, 0, 0, 0)
PREVIEW_BG = (32, 34, 40, 255)
CELL_BG = (48, 51, 58, 255)
GRID = (58, 61, 68, 255)
GROUND = (96, 91, 78, 255)
PCX_TRANSPARENT_RGB = (0, 255, 0)
PCX_ALPHA_CUTOFF = 220
GAMEPLAY_TARGET_HEIGHT = 82
GAMEPLAY_CANVAS_W = 260
GAMEPLAY_CANVAS_H = 190
GAMEPLAY_AXIS_X = 130
GAMEPLAY_AXIS_Y = 158
IDLE_SOURCE_MAP = {
    "idle_00": "idle_01.png",
    "idle_01": "idle_02.png",
    "idle_02": "idle_03.png",
}


@dataclass(frozen=True)
class FrameSpec:
    name: str
    title: str
    box: tuple[int, int, int, int]
    ground_ratio: float = 0.94
    normalize: bool = True
    keep_largest: bool = False
    x_offset: int = 0


# Explicit one-by-one frame crops from the 1024x1024 restart sheet.
# These boxes avoid row titles and grid dividers.
FRAMES = [
    FrameSpec("idle_00", "Idle 0", (214, 40, 337, 252)),
    FrameSpec("idle_01", "Idle 1", (400, 40, 540, 252), keep_largest=True),
    FrameSpec("idle_02", "Idle 2", (604, 40, 748, 252), keep_largest=True),
    FrameSpec("walk_00", "Walk 0", (16, 294, 163, 508)),
    FrameSpec("walk_01", "Walk 1", (178, 294, 320, 508)),
    FrameSpec("walk_02", "Walk 2", (346, 294, 500, 508)),
    FrameSpec("walk_03", "Walk 3", (520, 294, 668, 508)),
    FrameSpec("walk_04", "Walk 4", (690, 294, 835, 508)),
    FrameSpec("walk_05", "Walk 5", (860, 294, 1005, 508)),
    FrameSpec("stand_lp_00", "Light Punch 0", (18, 552, 247, 765)),
    FrameSpec("stand_lp_01", "Light Punch 1", (266, 552, 502, 765)),
    FrameSpec("stand_lp_02", "Light Punch 2", (522, 552, 756, 765)),
    FrameSpec("stand_lp_03", "Light Punch 3", (778, 552, 1008, 765)),
    FrameSpec("stand_hk_00", "High Kick 0", (18, 812, 196, 1020), 0.98),
    FrameSpec("stand_hk_01", "High Kick 1", (214, 812, 390, 1020), 0.98),
    FrameSpec("stand_hk_02", "High Kick 2", (414, 812, 584, 1020), 0.98),
    FrameSpec("stand_hk_03", "High Kick 3", (618, 812, 778, 1020), 0.98),
    FrameSpec("stand_hk_04", "High Kick 4", (828, 812, 1008, 1020)),
    FrameSpec("portrait_neutral", "Portrait Source", (18, 40, 145, 252), normalize=False),
]


def is_green_background(rgb: tuple[int, int, int]) -> bool:
    r, g, b = rgb
    return g > 135 and g > r + 30 and g > b + 30


def remove_edge_green(crop: Image.Image) -> Image.Image:
    rgb = crop.convert("RGB")
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
        if not is_green_background(src[x, y]):
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

    out = crop.convert("RGBA")
    out.putalpha(alpha)
    return out


def neutralize_green_spill(img: Image.Image) -> Image.Image:
    out = img.convert("RGBA")
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            if g > 95 and g > r + 18 and g > b + 18:
                neutral = max(r, b)
                px[x, y] = (neutral, neutral, neutral, a)
    return out


def trim_transparent(img: Image.Image, margin: int = 2) -> Image.Image:
    bbox = img.getbbox()
    if bbox is None:
        return img
    x0, y0, x1, y1 = bbox
    return img.crop((max(0, x0 - margin), max(0, y0 - margin), min(img.width, x1 + margin), min(img.height, y1 + margin)))


def keep_largest_component(img: Image.Image) -> Image.Image:
    src = img.convert("RGBA")
    px = src.load()
    visited: set[tuple[int, int]] = set()
    components: list[list[tuple[int, int]]] = []

    for y in range(src.height):
        for x in range(src.width):
            if (x, y) in visited or px[x, y][3] == 0:
                continue
            component: list[tuple[int, int]] = []
            queue: deque[tuple[int, int]] = deque([(x, y)])
            visited.add((x, y))
            while queue:
                cx, cy = queue.popleft()
                component.append((cx, cy))
                for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
                    if nx < 0 or ny < 0 or nx >= src.width or ny >= src.height:
                        continue
                    if (nx, ny) in visited or px[nx, ny][3] == 0:
                        continue
                    visited.add((nx, ny))
                    queue.append((nx, ny))

            components.append(component)

    if not components:
        return src

    largest = set(max(components, key=len))
    out = Image.new("RGBA", src.size, TRANSPARENT)
    out_px = out.load()
    for x, y in largest:
        out_px[x, y] = px[x, y]
    return out


def normalize_height(img: Image.Image, spec: FrameSpec) -> Image.Image:
    if not spec.normalize or img.height <= GAMEPLAY_TARGET_HEIGHT:
        return img
    scale = GAMEPLAY_TARGET_HEIGHT / img.height
    size = (max(1, round(img.width * scale)), GAMEPLAY_TARGET_HEIGHT)
    return img.resize(size, Image.Resampling.LANCZOS)


def pad(img: Image.Image, margin: int = 2) -> Image.Image:
    padded = Image.new("RGBA", (img.width + margin * 2, img.height + margin * 2), TRANSPARENT)
    padded.alpha_composite(img, (margin, margin))
    return padded


def place_on_gameplay_canvas(img: Image.Image, spec: FrameSpec) -> Image.Image:
    if spec.name.startswith("portrait_"):
        return pad(img)

    canvas = Image.new("RGBA", (GAMEPLAY_CANVAS_W, GAMEPLAY_CANVAS_H), TRANSPARENT)
    axis_x = img.width // 2
    axis_y = round(img.height * spec.ground_ratio)
    paste_x = GAMEPLAY_AXIS_X - axis_x + spec.x_offset
    paste_y = GAMEPLAY_AXIS_Y - axis_y
    canvas.alpha_composite(img, (paste_x, paste_y))
    return canvas


def make_frame(sheet: Image.Image, spec: FrameSpec) -> Image.Image:
    crop = sheet.crop(spec.box)
    cleaned = neutralize_green_spill(remove_edge_green(crop))
    if spec.keep_largest:
        cleaned = keep_largest_component(cleaned)
    trimmed = trim_transparent(cleaned)
    normalized = normalize_height(trimmed, spec)
    final = neutralize_green_spill(trim_transparent(normalized))
    return place_on_gameplay_canvas(final, spec)


def make_external_idle_frame(spec: FrameSpec) -> Image.Image:
    source_path = IDLE_REFERENCE_DIR / IDLE_SOURCE_MAP[spec.name]
    if not source_path.exists():
        raise FileNotFoundError(source_path)
    source = Image.open(source_path).convert("RGB")
    idle_spec = FrameSpec(spec.name, spec.title, (0, 0, source.width, source.height), spec.ground_ratio, spec.normalize, False, spec.x_offset)
    return make_frame(source, idle_spec)


def make_portrait_small() -> Image.Image:
    source = Image.open(PORTRAIT_REFERENCE_DIR / "portrait_small_source.png").convert("RGBA")
    bbox = source.getbbox()
    crop = source.crop(bbox) if bbox else source
    crop.thumbnail((23, 23), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (25, 25), TRANSPARENT)
    canvas.alpha_composite(crop, ((25 - crop.width) // 2, (25 - crop.height) // 2))
    return canvas


def make_portrait_big() -> Image.Image:
    source = Image.open(PORTRAIT_REFERENCE_DIR / "portrait_big_source.png").convert("RGBA")
    # MUGEN's 9000,1 portrait slot is low-resolution. Use a clean bust crop
    # instead of the full stat card so it reads like KFM's portrait in-menu.
    crop = source.crop((250, 0, 930, 840))
    crop.thumbnail((120, 140), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (120, 140), TRANSPARENT)
    canvas.alpha_composite(crop, ((120 - crop.width) // 2, (140 - crop.height) // 2))
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
    rgb = Image.new("RGB", rgba.size, PCX_TRANSPARENT_RGB)
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


def make_palette_strip(palette: list[int]) -> Image.Image:
    colors = []
    for idx in range(1, min(33, len(palette) // 3)):
        r, g, b = palette[idx * 3 : idx * 3 + 3]
        colors.append((r, g, b, 255))
    img = Image.new("RGBA", (len(colors) * 14, 26), TRANSPARENT)
    draw = ImageDraw.Draw(img)
    for idx, color in enumerate(colors):
        x = idx * 14
        draw.rectangle((x, 0, x + 13, 17), fill=color)
        draw.rectangle((x, 18, x + 13, 25), fill=(28, 28, 32, 255))
    return img


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
    if not REFERENCE.exists():
        raise SystemExit(f"Missing reference sheet: {REFERENCE}")
    for source_name in IDLE_SOURCE_MAP.values():
        idle_path = IDLE_REFERENCE_DIR / source_name
        if not idle_path.exists():
            raise SystemExit(f"Missing idle reference frame: {idle_path}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PCX_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_DIR.glob("*.png"):
        old.unlink()
    for old in PCX_DIR.glob("*.pcx"):
        old.unlink()

    sheet = Image.open(REFERENCE).convert("RGB")
    frames: list[tuple[FrameSpec, Image.Image]] = []
    frame_by_name: dict[str, Image.Image] = {}
    for spec in FRAMES:
        frame = make_external_idle_frame(spec) if spec.name.startswith("idle_") else make_frame(sheet, spec)
        frame.save(OUT_DIR / f"{spec.name}.png")
        frames.append((spec, frame))
        frame_by_name[spec.name] = frame

    for spec, frame in [
        (FrameSpec("portrait_small", "Small Portrait", (0, 0, 0, 0), 0.96, False), make_portrait_small()),
        (FrameSpec("portrait_big", "Big Portrait", (0, 0, 0, 0), 0.96, False), make_portrait_big()),
    ]:
        frame.save(OUT_DIR / f"{spec.name}.png")
        frames.append((spec, frame))

    palette = quantized_palette([frame for spec, frame in frames if not spec.name.startswith("portrait_")])
    for spec, frame in frames:
        frame_palette = quantized_palette([frame]) if spec.name.startswith("portrait_") else palette
        save_indexed_pcx(frame, frame_palette, spec.name)
    make_palette_strip(palette).save(OUT_DIR / "palette_strip.png")
    make_preview(frames).save(OUT_DIR / "mestre_thaynan_sprite_sheet_preview.png")


if __name__ == "__main__":
    main()
