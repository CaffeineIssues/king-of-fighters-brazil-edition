#!/usr/bin/env python3
"""Extract Mestre Thaynan source sprites from the provided reference sheet.

The input sheet is stored at:
  assets/mestre_thaynan/reference/black_tiger_maestro_reference_v2.png

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
REFERENCE = ROOT / "assets" / "mestre_thaynan" / "reference" / "black_tiger_maestro_reference_v2.png"
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
    keep_largest: bool = True


# Coordinates are measured against the downloaded 768x1370 v2 reference sheet.
# Crops intentionally include a small margin so the edge flood-fill can remove
# the light-blue cell background without eating into outlines.
FRAMES = [
    # Full-body stance / movement row.
    CropSpec("idle_00", "Idle 0", (16, 280, 108, 436)),
    CropSpec("idle_01", "Idle 1", (111, 280, 199, 436)),
    CropSpec("idle_02", "Idle 2", (205, 280, 293, 436)),
    CropSpec("idle_03", "Idle 3", (297, 280, 384, 436)),
    CropSpec("walk_00", "Walk 0", (16, 280, 108, 436)),
    CropSpec("walk_01", "Walk 1", (111, 280, 199, 436)),
    CropSpec("walk_02", "Walk 2", (205, 280, 293, 436)),
    CropSpec("walk_03", "Walk 3", (297, 280, 384, 436)),
    CropSpec("sidewalk_step", "Sidewalk Step", (476, 280, 567, 436)),
    CropSpec("jacket_alt_idle", "Alt Idle", (664, 280, 752, 436)),
    # Punching Combos & Techniques / new moves row.
    CropSpec("prayer_guard", "Prayer Guard", (17, 514, 110, 669)),
    CropSpec("stand_lp", "Rapid Punch 1", (111, 514, 202, 669), keep_largest=False),
    CropSpec("stand_hp", "Rapid Punch 2", (205, 514, 296, 669), keep_largest=False),
    CropSpec("black_tiger_palm", "Rapid Punch 3", (297, 514, 387, 669), keep_largest=False),
    CropSpec("jump_neutral", "Jump", (389, 514, 476, 669), 0.88),
    CropSpec("crane_anti_air", "Crane Kick", (479, 514, 569, 669), 0.88, keep_largest=False),
    CropSpec("stand_hk", "HK Crane Kick", (570, 514, 661, 669), 0.88, keep_largest=False),
    CropSpec("stand_lk", "LK Stance", (664, 514, 752, 669)),
    # Special move row.
    CropSpec("crouch", "Low Stance", (20, 716, 159, 874)),
    CropSpec("tiger_roar_start", "Tiger Roar Start", (161, 716, 298, 874), keep_largest=False),
    CropSpec("tiger_roar_charge", "Tiger Roar Charge", (300, 716, 438, 874), keep_largest=False),
    CropSpec("prayer_counter", "Tiger Roar", (439, 716, 577, 874), keep_largest=False),
    CropSpec("tiger_roar_projectile", "Tiger Projectile", (578, 716, 751, 874), keep_largest=False),
    # Hurt / KO row.
    CropSpec("hit_high", "Hit High", (88, 919, 231, 1010), 0.90),
    CropSpec("hit_recoil", "Hit Recoil", (233, 919, 375, 1010), 0.90),
    CropSpec("knockdown", "Knockdown", (376, 919, 549, 1010), 0.94),
    CropSpec("ko", "KO", (550, 919, 681, 1010), 0.94),
    # Portrait crops for select/victory references.
    CropSpec("portrait_neutral", "Portrait", (36, 1057, 365, 1338), 0.96, keep_largest=False),
    CropSpec("portrait_tiger_roar", "Tiger Roar Portrait", (404, 1057, 735, 1338), 0.96, keep_largest=False),
]


def color_distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def likely_sheet_background(rgb: tuple[int, int, int]) -> bool:
    r, g, b = rgb
    # The sheet uses light cyan panels and medium blue separators. Restrict the
    # rule to blue-dominant, high-brightness colors so the jacket and shirt stay.
    return b > 145 and g > 135 and r > 80 and b >= r + 20 and g >= r + 5


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


def make_frame(sheet: Image.Image, spec: CropSpec) -> Image.Image:
    crop = sheet.crop(spec.box)
    transparent = remove_edge_background(crop)
    defringed = remove_light_fringe(transparent)
    if spec.keep_largest:
        defringed = keep_largest_component(defringed)
    return trim_transparent(defringed)


def make_portrait_small(portrait: Image.Image) -> Image.Image:
    """Create the standard small select icon for sprite 9000,0."""
    crop = portrait.crop((45, 0, 175, 130))
    return crop.resize((25, 25), Image.Resampling.LANCZOS)


def make_portrait_big(portrait: Image.Image) -> Image.Image:
    """Create a controlled big select portrait for sprite 9000,1."""
    canvas = Image.new("RGBA", (120, 140), TRANSPARENT)
    crop = portrait.crop((20, 0, 210, 210))
    crop.thumbnail((120, 140), Image.Resampling.LANCZOS)
    canvas.alpha_composite(crop, ((120 - crop.width) // 2, 140 - crop.height))
    return canvas


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
