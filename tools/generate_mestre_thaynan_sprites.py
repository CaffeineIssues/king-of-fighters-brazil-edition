#!/usr/bin/env python3
"""Extract Mestre Thaynan source sprites from the provided reference sheet.

The input sheet is stored at:
  assets/mestre_thaynan/reference/mestre_thaynan_final_reference.png

The output files are source-art frames for review and MUGEN / IKEMEN import
prep. They are not a finished SFF: a pixel artist should still clean the JPEG
artifacts, normalize axes, add in-betweens, and author CLSN boxes.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
BASE_REFERENCE = ROOT / "assets" / "mestre_thaynan" / "reference" / "mestre_thaynan_final_reference.png"
OUT_DIR = ROOT / "assets" / "mestre_thaynan" / "sprites"
PCX_DIR = OUT_DIR / "pcx"

TRANSPARENT = (0, 0, 0, 0)
PREVIEW_BG = (32, 34, 40, 255)
CELL_BG = (48, 51, 58, 255)
GRID = (58, 61, 68, 255)
GROUND = (96, 91, 78, 255)
GAMEPLAY_MAX_HEIGHT = 108
PCX_TRANSPARENT_RGB = (0, 255, 0)
PCX_ALPHA_CUTOFF = 220


@dataclass(frozen=True)
class CropSpec:
    name: str
    title: str
    box: tuple[int, int, int, int]
    ground_ratio: float = 0.94
    keep_largest: bool = True


# Coordinates are measured against the 640x640 final reference sheet. Every
# generated frame comes from this sheet; no older reference art is mixed in.
def cell(
    name: str,
    title: str,
    x: int,
    y: int,
    w: int,
    h: int,
    ground_ratio: float = 0.94,
    keep_largest: bool = True,
    inset: int = 2,
) -> CropSpec:
    return CropSpec(name, title, (x + inset, y + inset, x + w - inset, y + h - inset), ground_ratio, keep_largest)


def row(
    prefix: str,
    title: str,
    x: int,
    y: int,
    w: int,
    h: int,
    count: int,
    ground_ratio: float = 0.94,
    keep_largest: bool = True,
) -> list[CropSpec]:
    return [
        cell(f"{prefix}_{idx:02d}", f"{title} {idx}", x + idx * w, y, w, h, ground_ratio, keep_largest)
        for idx in range(count)
    ]


FRAMES = [
    *row("idle", "Idle", 0, 14, 80, 88, 4),
    *row("walk", "Walk", 320, 14, 64, 88, 5),
    *row("walk_back", "Walk Back", 0, 122, 64, 82, 5),
    *row("jump", "Jump", 320, 122, 64, 82, 5, 0.88),
    *row("crouch", "Crouch", 0, 224, 64, 83, 5),
    *row("guard", "Guard", 320, 224, 64, 83, 5),
    *row("stand_lp", "Light Punch", 0, 328, 64, 64, 5, keep_largest=False),
    *row("stand_hp", "Strong Punch", 320, 328, 64, 64, 5, keep_largest=False),
    *row("stand_lk", "Light Kick", 0, 430, 64, 62, 5, 0.88, keep_largest=False),
    *row("stand_hk", "Strong Kick", 320, 430, 64, 62, 5, 0.88, keep_largest=False),
    *row("dash", "Dash", 0, 512, 64, 52, 5, keep_largest=False),
    *row("hit", "Hurt", 320, 512, 64, 52, 5, 0.90, keep_largest=False),
    *[cell(f"block_{idx:02d}", f"Block {idx}", idx * 46, 584, 46, 56, 0.94) for idx in range(4)],
    cell("knockdown_00", "Knockdown 0", 184, 584, 80, 56),
    cell("knockdown_01", "Knockdown 1", 264, 584, 80, 56),
    cell("knockdown_02", "Knockdown 2", 344, 584, 59, 56),
    cell("knockdown_03", "Knockdown 3", 403, 584, 59, 56),
    cell("win_00", "Win 0", 462, 584, 59, 56),
    cell("win_01", "Win 1", 521, 584, 59, 56),
    cell("win_02", "Win 2", 580, 584, 60, 56),
    cell("portrait_neutral", "Portrait", 0, 14, 80, 88, 0.96, keep_largest=False),
    cell("portrait_tiger_roar", "Punch Portrait", 0, 328, 128, 82, 0.96, keep_largest=False),
]


def color_distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def likely_sheet_background(rgb: tuple[int, int, int]) -> bool:
    r, g, b = rgb
    # The sheet uses light cyan panels and medium blue separators. Restrict the
    # rule to blue-dominant, high-brightness colors so the jacket and shirt stay.
    blue_panel = b > 145 and g > 135 and r > 80 and b >= r + 20 and g >= r + 5
    green_panel = g > 210 and r < 80 and b < 80
    return blue_panel or green_panel


def likely_fringe(rgb: tuple[int, int, int]) -> bool:
    r, g, b = rgb
    is_cyan_panel = b > 128 and g > 118 and r > 68 and b >= r + 10
    is_white_jpeg_edge = r > 204 and g > 204 and b > 204
    return is_cyan_panel or is_white_jpeg_edge


def remove_edge_background(crop: Image.Image) -> Image.Image:
    rgb = crop.convert("RGB")
    w, h = rgb.size
    alpha = Image.new("L", (w, h), 255)
    alpha_px = alpha.load()
    src = rgb.load()
    visited: set[tuple[int, int]] = set()
    queue: deque[tuple[int, int, tuple[int, int, int]]] = deque()

    for x in range(w):
        queue.append((x, 0, src[x, 0]))
        queue.append((x, h - 1, src[x, h - 1]))
    for y in range(h):
        queue.append((0, y, src[0, y]))
        queue.append((w - 1, y, src[w - 1, y]))

    while queue:
        x, y, seed = queue.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))

        current = src[x, y]
        if not (likely_sheet_background(current) or color_distance(current, seed) < 54):
            continue

        alpha_px[x, y] = 0
        if x > 0:
            queue.append((x - 1, y, seed))
        if x < w - 1:
            queue.append((x + 1, y, seed))
        if y > 0:
            queue.append((x, y - 1, seed))
        if y < h - 1:
            queue.append((x, y + 1, seed))

    out = crop.convert("RGBA")
    out.putalpha(alpha)
    return out


def remove_light_fringe(img: Image.Image, radius: int = 2) -> Image.Image:
    src = img.convert("RGBA")
    px = src.load()
    to_clear: set[tuple[int, int]] = set()
    for y in range(src.height):
        for x in range(src.width):
            r, g, b, a = px[x, y]
            if a == 0 or not likely_fringe((r, g, b)):
                continue
            touches_transparency = False
            for ny in range(max(0, y - radius), min(src.height, y + radius + 1)):
                for nx in range(max(0, x - radius), min(src.width, x + radius + 1)):
                    if px[nx, ny][3] == 0:
                        touches_transparency = True
                        break
                if touches_transparency:
                    break
            if touches_transparency:
                to_clear.add((x, y))
    for x, y in to_clear:
        px[x, y] = (0, 0, 0, 0)
    return src


def green_spill(rgb: tuple[int, int, int]) -> bool:
    r, g, b = rgb
    return g > 110 and g > r + 30 and g > b + 30


def remove_green_spill(img: Image.Image, radius: int = 2) -> Image.Image:
    src = img.convert("RGBA")
    px = src.load()
    changes: dict[tuple[int, int], tuple[int, int, int, int]] = {}
    for y in range(src.height):
        for x in range(src.width):
            r, g, b, a = px[x, y]
            if a == 0 or not green_spill((r, g, b)):
                continue

            touches_transparency = False
            for ny in range(max(0, y - radius), min(src.height, y + radius + 1)):
                for nx in range(max(0, x - radius), min(src.width, x + radius + 1)):
                    if px[nx, ny][3] == 0:
                        touches_transparency = True
                        break
                if touches_transparency:
                    break

            neutral = max(r, b)
            changes[(x, y)] = (neutral, neutral, neutral, a)

    for (x, y), value in changes.items():
        px[x, y] = value
    return src


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
    cleaned = Image.new("RGBA", src.size, TRANSPARENT)
    out = cleaned.load()
    for x, y in largest:
        out[x, y] = px[x, y]
    return cleaned


def trim_transparent(img: Image.Image, margin: int = 2) -> Image.Image:
    bbox = img.getbbox()
    if bbox is None:
        return img
    x0, y0, x1, y1 = bbox
    x0 = max(0, x0 - margin)
    y0 = max(0, y0 - margin)
    x1 = min(img.width, x1 + margin)
    y1 = min(img.height, y1 + margin)
    return img.crop((x0, y0, x1, y1))


def pad_transparent(img: Image.Image, margin: int = 1) -> Image.Image:
    padded = Image.new("RGBA", (img.width + margin * 2, img.height + margin * 2), TRANSPARENT)
    padded.alpha_composite(img, (margin, margin))
    return padded


def scale_gameplay_frame(img: Image.Image, spec: CropSpec) -> Image.Image:
    if spec.name.startswith("portrait_") or img.height <= GAMEPLAY_MAX_HEIGHT:
        return pad_transparent(remove_green_spill(img))

    scale = GAMEPLAY_MAX_HEIGHT / img.height
    new_size = (max(1, round(img.width * scale)), GAMEPLAY_MAX_HEIGHT)
    scaled = img.resize(new_size, Image.Resampling.LANCZOS)
    scaled = remove_light_fringe(scaled, radius=1)
    scaled = remove_green_spill(scaled)
    return pad_transparent(trim_transparent(scaled))


def make_frame(sheet: Image.Image, spec: CropSpec) -> Image.Image:
    crop = sheet.crop(spec.box)
    transparent = remove_edge_background(crop)
    defringed = remove_light_fringe(transparent)
    defringed = remove_green_spill(defringed)
    if spec.keep_largest:
        defringed = keep_largest_component(defringed)
    trimmed = trim_transparent(defringed)
    return scale_gameplay_frame(trimmed, spec)


def make_portrait_small(portrait: Image.Image) -> Image.Image:
    """Create the standard small select icon for sprite 9000,0."""
    bbox = portrait.getbbox()
    crop = portrait.crop(bbox) if bbox else portrait
    # Favor head/torso for the tiny select icon instead of shrinking the whole body.
    crop = crop.crop((0, 0, crop.width, max(1, int(crop.height * 0.58))))
    crop.thumbnail((23, 23), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (25, 25), TRANSPARENT)
    canvas.alpha_composite(crop, ((25 - crop.width) // 2, (25 - crop.height) // 2))
    return canvas


def make_portrait_big(portrait: Image.Image) -> Image.Image:
    """Create a controlled big select portrait for sprite 9000,1."""
    canvas = Image.new("RGBA", (120, 140), TRANSPARENT)
    bbox = portrait.getbbox()
    crop = portrait.crop(bbox) if bbox else portrait
    crop.thumbnail((108, 132), Image.Resampling.LANCZOS)
    canvas.alpha_composite(crop, ((120 - crop.width) // 2, 140 - crop.height - 4))
    return canvas


def quantized_palette(frames: list[Image.Image]) -> list[int]:
    atlas_w = max(frame.width for frame in frames)
    atlas_h = sum(frame.height for frame in frames)
    atlas = Image.new("RGB", (atlas_w, atlas_h), (0, 0, 0))
    y = 0
    for frame in frames:
        rgba = frame.convert("RGBA")
        rgb = Image.new("RGB", rgba.size, (0, 0, 0))
        rgb_px = rgb.load()
        src_px = rgba.load()
        for py in range(rgba.height):
            for px in range(rgba.width):
                r, g, b, a = src_px[px, py]
                if a >= PCX_ALPHA_CUTOFF:
                    rgb_px[px, py] = (r, g, b)
        atlas.paste(rgb, (0, y))
        y += frame.height

    paletted = atlas.quantize(colors=255, method=Image.Quantize.MEDIANCUT)
    palette = paletted.getpalette()[: 255 * 3]
    return [*PCX_TRANSPARENT_RGB] + palette + [0, 0, 0] * (256 - 1 - len(palette) // 3)


def save_indexed_pcx(frame: Image.Image, palette: list[int], name: str) -> None:
    rgba = frame.convert("RGBA")
    rgb = Image.new("RGB", frame.size, PCX_TRANSPARENT_RGB)
    rgb_px = rgb.load()
    src_px = rgba.load()
    for y in range(frame.height):
        for x in range(frame.width):
            r, g, b, a = src_px[x, y]
            if a >= PCX_ALPHA_CUTOFF:
                rgb_px[x, y] = (r, g, b)

    pal = Image.new("P", (1, 1))
    pal.putpalette(palette)
    indexed = rgb.quantize(palette=pal, dither=Image.Dither.NONE)

    # Restore transparent key after quantization. Semi-transparent source pixels
    # are treated as transparent instead of being matted against key green.
    pix = indexed.load()
    for y in range(frame.height):
        for x in range(frame.width):
            if src_px[x, y][3] < PCX_ALPHA_CUTOFF:
                pix[x, y] = 0

    indexed.save(PCX_DIR / f"{name}.pcx")


def make_palette_strip(palette: list[int]) -> Image.Image:
    visible_colors = []
    for idx in range(1, min(33, len(palette) // 3)):
        r, g, b = palette[idx * 3 : idx * 3 + 3]
        visible_colors.append((r, g, b, 255))

    img = Image.new("RGBA", (len(visible_colors) * 14, 26), TRANSPARENT)
    draw = ImageDraw.Draw(img)
    for idx, color in enumerate(visible_colors):
        x = idx * 14
        draw.rectangle((x, 0, x + 13, 17), fill=color)
        draw.rectangle((x, 18, x + 13, 25), fill=(28, 28, 32, 255))
    return img


def make_preview(items: list[tuple[CropSpec, Image.Image]]) -> Image.Image:
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

        max_w = cell_w - 30
        max_h = 110
        scale = min(1.0, max_w / frame.width, max_h / frame.height)
        shown = frame
        if scale < 1.0:
            shown = frame.resize((int(frame.width * scale), int(frame.height * scale)), Image.Resampling.NEAREST)

        x = cx + (cell_w - shown.width) // 2
        ground_y = cy + 14 + int(max_h * spec.ground_ratio)
        y = ground_y - int(shown.height * spec.ground_ratio)
        sheet.alpha_composite(shown, (x, y))
        draw.line((cx + 14, ground_y, cx + cell_w - 14, ground_y), fill=GROUND)
        draw.text((cx + 10, cy + 130), spec.title, fill=(235, 232, 215, 255), font=font)
        draw.text((cx + 10, cy + 142), f"{spec.name}.png", fill=(175, 180, 188, 255), font=font_small)

    return sheet


def main() -> None:
    if not BASE_REFERENCE.exists():
        raise SystemExit(f"Missing base reference sheet: {BASE_REFERENCE}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PCX_DIR.mkdir(parents=True, exist_ok=True)
    for old_png in OUT_DIR.glob("*.png"):
        old_png.unlink()
    for old_pcx in PCX_DIR.glob("*.pcx"):
        old_pcx.unlink()

    sheet = Image.open(BASE_REFERENCE).convert("RGB")
    frames: list[tuple[CropSpec, Image.Image]] = []
    frame_by_name: dict[str, Image.Image] = {}
    for spec in FRAMES:
        frame = make_frame(sheet, spec)
        frame.save(OUT_DIR / f"{spec.name}.png")
        frames.append((spec, frame))
        frame_by_name[spec.name] = frame

    portrait_small = make_portrait_small(frame_by_name["portrait_neutral"])
    portrait_big = make_portrait_big(frame_by_name["portrait_neutral"])
    for spec, frame in [
        (CropSpec("portrait_small", "Small Portrait", (0, 0, 0, 0), 0.96), portrait_small),
        (CropSpec("portrait_big", "Big Portrait", (0, 0, 0, 0), 0.96), portrait_big),
    ]:
        frame.save(OUT_DIR / f"{spec.name}.png")
        frames.append((spec, frame))

    palette = quantized_palette([frame for _, frame in frames])
    for spec, frame in frames:
        save_indexed_pcx(frame, palette, spec.name)

    make_palette_strip(palette).save(OUT_DIR / "palette_strip.png")
    make_preview(frames).save(OUT_DIR / "mestre_thaynan_sprite_sheet_preview.png")


if __name__ == "__main__":
    main()
