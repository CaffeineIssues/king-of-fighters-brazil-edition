#!/usr/bin/env python3
"""Extract Mestre Thaynan source sprites from the provided reference sheet.

The input sheet is stored at:
  assets/mestre_thaynan/reference/black_tiger_maestro_reference.jpg

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
REFERENCE = ROOT / "assets" / "mestre_thaynan" / "reference" / "black_tiger_maestro_reference.jpg"
OUT_DIR = ROOT / "assets" / "mestre_thaynan" / "sprites"
PCX_DIR = OUT_DIR / "pcx"

TRANSPARENT = (0, 0, 0, 0)
PREVIEW_BG = (32, 34, 40, 255)
CELL_BG = (48, 51, 58, 255)
GRID = (58, 61, 68, 255)
GROUND = (96, 91, 78, 255)


@dataclass(frozen=True)
class CropSpec:
    name: str
    title: str
    box: tuple[int, int, int, int]
    ground_ratio: float = 0.94


# Coordinates are measured against the downloaded 574x1024 reference sheet.
# Crops intentionally include a small margin so the edge flood-fill can remove
# the light-blue cell background without eating into outlines.
FRAMES = [
    # Full-body stance / movement row.
    CropSpec("idle_00", "Idle 0", (12, 209, 81, 326)),
    CropSpec("idle_01", "Idle 1", (83, 209, 149, 326)),
    CropSpec("idle_02", "Idle 2", (153, 209, 219, 326)),
    CropSpec("idle_03", "Idle 3", (222, 209, 287, 326)),
    CropSpec("walk_00", "Walk 0", (12, 209, 81, 326)),
    CropSpec("walk_01", "Walk 1", (83, 209, 149, 326)),
    CropSpec("walk_02", "Walk 2", (153, 209, 219, 326)),
    CropSpec("walk_03", "Walk 3", (222, 209, 287, 326)),
    CropSpec("sidewalk_step", "Sidewalk Step", (356, 209, 424, 326)),
    CropSpec("jacket_alt_idle", "Alt Idle", (496, 209, 562, 326)),
    # Kung fu form attacks.
    CropSpec("prayer_guard", "Prayer Guard", (13, 384, 82, 500)),
    CropSpec("stand_lp", "LP Claw", (83, 384, 151, 500)),
    CropSpec("stand_hp", "HP Tiger Claw", (153, 384, 221, 500)),
    CropSpec("black_tiger_palm", "Black Tiger Palm", (222, 384, 289, 500)),
    CropSpec("jump_neutral", "Jump", (291, 384, 356, 500), 0.88),
    CropSpec("crane_anti_air", "Crane Kick", (358, 384, 425, 500), 0.88),
    CropSpec("stand_hk", "HK Side Kick", (426, 384, 494, 500), 0.88),
    CropSpec("stand_lk", "LK Stance", (496, 384, 562, 500)),
    # Special move row.
    CropSpec("crouch", "Low Stance", (15, 535, 119, 653)),
    CropSpec("tiger_roar_start", "Tiger Roar Start", (120, 535, 223, 653)),
    CropSpec("tiger_roar_charge", "Tiger Roar Charge", (224, 535, 327, 653)),
    CropSpec("prayer_counter", "Tiger Roar", (328, 535, 431, 653)),
    CropSpec("tiger_roar_projectile", "Tiger Projectile", (432, 535, 561, 653)),
    # Hurt / KO row.
    CropSpec("hit_high", "Hit High", (66, 687, 173, 755), 0.90),
    CropSpec("hit_recoil", "Hit Recoil", (174, 687, 280, 755), 0.90),
    CropSpec("knockdown", "Knockdown", (281, 687, 410, 755), 0.94),
    CropSpec("ko", "KO", (411, 687, 509, 755), 0.94),
    # Portrait crops for select/victory references.
    CropSpec("portrait_neutral", "Portrait", (27, 790, 273, 1000), 0.96),
    CropSpec("portrait_tiger_roar", "Tiger Roar Portrait", (302, 790, 549, 1000), 0.96),
]


def color_distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def likely_sheet_background(rgb: tuple[int, int, int]) -> bool:
    r, g, b = rgb
    # The sheet uses light cyan panels and medium blue separators. Restrict the
    # rule to blue-dominant, high-brightness colors so the jacket and shirt stay.
    return b > 145 and g > 135 and r > 80 and b >= r + 20 and g >= r + 5


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


def make_frame(sheet: Image.Image, spec: CropSpec) -> Image.Image:
    crop = sheet.crop(spec.box)
    transparent = remove_edge_background(crop)
    return trim_transparent(transparent)


def quantized_palette(frames: list[Image.Image]) -> list[int]:
    atlas_w = max(frame.width for frame in frames)
    atlas_h = sum(frame.height for frame in frames)
    atlas = Image.new("RGBA", (atlas_w, atlas_h), TRANSPARENT)
    y = 0
    for frame in frames:
        atlas.alpha_composite(frame, (0, y))
        y += frame.height

    opaque = Image.new("RGBA", atlas.size, (0, 255, 0, 255))
    opaque.alpha_composite(atlas)
    paletted = opaque.convert("RGB").quantize(colors=255, method=Image.Quantize.MEDIANCUT)
    palette = paletted.getpalette()[: 255 * 3]
    return [0, 255, 0] + palette + [0, 0, 0] * (256 - 1 - len(palette) // 3)


def save_indexed_pcx(frame: Image.Image, palette: list[int], name: str) -> None:
    base = Image.new("RGBA", frame.size, (0, 255, 0, 255))
    base.alpha_composite(frame)
    rgb = base.convert("RGB")
    pal = Image.new("P", (1, 1))
    pal.putpalette(palette)
    indexed = rgb.quantize(palette=pal, dither=Image.Dither.NONE)

    # Restore transparent key for alpha pixels.
    alpha = frame.getchannel("A")
    pix = indexed.load()
    for y in range(frame.height):
        for x in range(frame.width):
            if alpha.getpixel((x, y)) < 128:
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
    if not REFERENCE.exists():
        raise SystemExit(f"Missing reference sheet: {REFERENCE}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PCX_DIR.mkdir(parents=True, exist_ok=True)

    sheet = Image.open(REFERENCE).convert("RGB")
    frames: list[tuple[CropSpec, Image.Image]] = []
    for spec in FRAMES:
        frame = make_frame(sheet, spec)
        frame.save(OUT_DIR / f"{spec.name}.png")
        frames.append((spec, frame))

    palette = quantized_palette([frame for _, frame in frames])
    for spec, frame in frames:
        save_indexed_pcx(frame, palette, spec.name)

    make_palette_strip(palette).save(OUT_DIR / "palette_strip.png")
    make_preview(frames).save(OUT_DIR / "mestre_thaynan_sprite_sheet_preview.png")


if __name__ == "__main__":
    main()
