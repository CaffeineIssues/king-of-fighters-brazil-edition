#!/usr/bin/env python3
"""Generate first-pass pixel sprite source frames for Mestre Thaynan.

The output is intentionally source-art, not a finished SFF. Frames are
transparent PNGs that can be touched up by a pixel artist, indexed, cropped,
and imported into MUGEN / IKEMEN once the full animation set exists.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "assets" / "mestre_thaynan" / "sprites"
PCX_DIR = OUT_DIR / "pcx"
FRAME_W = 96
FRAME_H = 128
GROUND_Y = 112

TRANSPARENT = (0, 0, 0, 0)
OUTLINE = (24, 20, 18, 255)
BLACK = (34, 31, 33, 255)
BLACK_2 = (15, 15, 18, 255)
NAVY = (24, 44, 76, 255)
PANTS = (25, 28, 34, 255)
PANTS_HI = (45, 48, 58, 255)
SKIN = (190, 132, 94, 255)
SKIN_DARK = (124, 78, 58, 255)
SKIN_LIGHT = (225, 169, 123, 255)
HAIR = (58, 52, 50, 255)
HAIR_HI = (119, 112, 103, 255)
WHITE = (224, 220, 200, 255)
GLASS = (145, 188, 194, 255)
CREAM = (216, 205, 168, 255)
GOLD = (185, 145, 62, 255)
DUST = (114, 94, 73, 255)
FX = (225, 205, 126, 255)
FX_DARK = (154, 112, 48, 255)
SHADOW = (0, 0, 0, 72)
INDEXED_COLORS = [
    (0, 255, 0),  # index 0: transparent key for MUGEN import
    OUTLINE[:3],
    BLACK[:3],
    BLACK_2[:3],
    NAVY[:3],
    PANTS[:3],
    PANTS_HI[:3],
    SKIN[:3],
    SKIN_DARK[:3],
    SKIN_LIGHT[:3],
    HAIR[:3],
    HAIR_HI[:3],
    WHITE[:3],
    GLASS[:3],
    CREAM[:3],
    GOLD[:3],
    DUST[:3],
    FX[:3],
    FX_DARK[:3],
    (18, 18, 22),  # baked source-art shadow for PCX previews
]


@dataclass(frozen=True)
class FrameSpec:
    name: str
    pose: str
    title: str


FRAMES = [
    FrameSpec("idle_00", "idle0", "Idle 0"),
    FrameSpec("idle_01", "idle1", "Idle 1"),
    FrameSpec("idle_02", "idle2", "Idle 2"),
    FrameSpec("idle_03", "idle1", "Idle 3"),
    FrameSpec("prayer_guard", "prayer", "Prayer Guard"),
    FrameSpec("walk_00", "walk0", "Walk 0"),
    FrameSpec("walk_01", "walk1", "Walk 1"),
    FrameSpec("walk_02", "walk2", "Walk 2"),
    FrameSpec("walk_03", "walk3", "Walk 3"),
    FrameSpec("crouch", "crouch", "Crouch"),
    FrameSpec("jump_neutral", "jump", "Jump"),
    FrameSpec("stand_lp", "lp", "LP Palm"),
    FrameSpec("stand_hp", "hp", "HP Claw"),
    FrameSpec("stand_lk", "lk", "LK Tap"),
    FrameSpec("stand_hk", "hk", "HK Side Kick"),
    FrameSpec("black_tiger_palm", "palm", "Black Tiger Palm"),
    FrameSpec("crane_anti_air", "crane", "Crane Anti-Air"),
    FrameSpec("prayer_counter", "counter", "Prayer Counter"),
    FrameSpec("sidewalk_step", "step", "Sidewalk Step"),
    FrameSpec("hit_high", "hit", "Hit High"),
    FrameSpec("win_bow", "bow", "Win Bow"),
    FrameSpec("jacket_alt_idle", "jacket", "Alt Costume"),
]


def line(draw: ImageDraw.ImageDraw, pts: Iterable[tuple[int, int]], fill, width: int = 3) -> None:
    draw.line(list(pts), fill=OUTLINE, width=width + 2, joint="curve")
    draw.line(list(pts), fill=fill, width=width, joint="curve")


def rect(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill) -> None:
    draw.rectangle(box, fill=OUTLINE)
    x0, y0, x1, y1 = box
    draw.rectangle((x0 + 1, y0 + 1, x1 - 1, y1 - 1), fill=fill)


def poly(draw: ImageDraw.ImageDraw, pts: list[tuple[int, int]], fill) -> None:
    draw.polygon(pts, fill=OUTLINE)
    if len(pts) >= 3:
        cx = sum(p[0] for p in pts) // len(pts)
        cy = sum(p[1] for p in pts) // len(pts)
        inner = []
        for x, y in pts:
            ix = x + (1 if x < cx else -1 if x > cx else 0)
            iy = y + (1 if y < cy else -1 if y > cy else 0)
            inner.append((ix, iy))
        draw.polygon(inner, fill=fill)


def ellipse(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill) -> None:
    draw.ellipse(box, fill=OUTLINE)
    x0, y0, x1, y1 = box
    draw.ellipse((x0 + 1, y0 + 1, x1 - 1, y1 - 1), fill=fill)


def draw_head(draw: ImageDraw.ImageDraw, x: int, y: int, glasses_shift: int = 0) -> None:
    # Hair mass behind the thin face, matching the long center-parted reference.
    ellipse(draw, (x - 12, y - 11, x + 12, y + 21), HAIR)
    rect(draw, (x - 14, y + 3, x - 8, y + 27), HAIR)
    rect(draw, (x + 8, y + 3, x + 14, y + 27), HAIR)
    ellipse(draw, (x - 9, y - 7, x + 9, y + 16), SKIN)
    draw.rectangle((x - 2, y - 8, x + 2, y - 5), fill=HAIR_HI)
    draw.rectangle((x - 7, y - 1, x - 2, y + 3), fill=GLASS)
    draw.rectangle((x + 2, y - 1 + glasses_shift, x + 7, y + 3 + glasses_shift), fill=GLASS)
    draw.rectangle((x - 2, y + 1, x + 2, y + 2), fill=OUTLINE)
    draw.point((x - 4, y + 1), fill=OUTLINE)
    draw.point((x + 4, y + 1 + glasses_shift), fill=OUTLINE)
    draw.rectangle((x - 1, y + 4, x + 1, y + 7), fill=SKIN_DARK)
    draw.rectangle((x - 4, y + 10, x + 4, y + 11), fill=SKIN_DARK)
    draw.rectangle((x - 6, y - 5, x + 6, y - 4), fill=HAIR)


def draw_torso(draw: ImageDraw.ImageDraw, x: int, y: int, jacket: bool = False) -> None:
    shirt = NAVY if jacket else BLACK
    poly(draw, [(x - 14, y), (x + 13, y), (x + 17, y + 39), (x - 17, y + 39)], shirt)
    poly(draw, [(x - 5, y + 1), (x + 4, y + 1), (x + 1, y + 16), (x - 2, y + 16)], SKIN)
    draw.rectangle((x - 3, y + 4, x + 3, y + 27), fill=BLACK_2 if jacket else WHITE)
    if jacket:
        draw.rectangle((x - 13, y + 6, x - 9, y + 35), fill=GOLD)
        draw.rectangle((x + 9, y + 6, x + 13, y + 35), fill=GOLD)
        draw.rectangle((x - 7, y + 8, x + 7, y + 13), fill=BLACK_2)
    else:
        draw.rectangle((x - 10, y + 8, x - 8, y + 25), fill=WHITE)
        draw.rectangle((x + 8, y + 8, x + 10, y + 25), fill=WHITE)
    # Neck cord / towel.
    draw.arc((x - 13, y - 7, x + 13, y + 12), 20, 160, fill=CREAM, width=3)
    draw.line((x - 11, y + 4, x - 7, y + 21), fill=CREAM, width=2)
    draw.line((x + 11, y + 4, x + 7, y + 21), fill=CREAM, width=2)


def draw_legs(draw: ImageDraw.ImageDraw, hip: tuple[int, int], pose: str) -> None:
    x, y = hip
    if pose in {"hk", "crane"}:
        line(draw, [(x - 7, y), (x - 12, y + 28), (x - 13, GROUND_Y)], PANTS_HI, 7)
        line(draw, [(x + 7, y), (x + 28, y + 22), (x + 48, y + 22)], PANTS, 7)
        rect(draw, (x + 44, y + 17, x + 59, y + 25), BLACK_2)
    elif pose == "crouch":
        line(draw, [(x - 7, y - 5), (x - 25, y + 14), (x - 31, GROUND_Y)], PANTS, 7)
        line(draw, [(x + 8, y - 4), (x + 19, y + 18), (x + 32, GROUND_Y)], PANTS_HI, 7)
        rect(draw, (x - 38, GROUND_Y - 4, x - 24, GROUND_Y + 2), BLACK_2)
        rect(draw, (x + 26, GROUND_Y - 4, x + 41, GROUND_Y + 2), BLACK_2)
    elif pose == "jump":
        line(draw, [(x - 7, y), (x - 18, y + 24), (x - 32, y + 46)], PANTS, 7)
        line(draw, [(x + 7, y), (x + 17, y + 22), (x + 9, y + 48)], PANTS_HI, 7)
        rect(draw, (x - 39, y + 42, x - 27, y + 49), BLACK_2)
        rect(draw, (x + 3, y + 45, x + 15, y + 52), BLACK_2)
    elif pose == "step":
        line(draw, [(x - 8, y), (x - 18, y + 30), (x - 37, GROUND_Y)], PANTS, 7)
        line(draw, [(x + 8, y), (x + 21, y + 22), (x + 46, GROUND_Y - 6)], PANTS_HI, 7)
        rect(draw, (x - 45, GROUND_Y - 4, x - 30, GROUND_Y + 2), BLACK_2)
        rect(draw, (x + 39, GROUND_Y - 11, x + 54, GROUND_Y - 4), BLACK_2)
    else:
        step = {"walk0": -4, "walk1": 4, "walk2": 8, "walk3": -8, "lk": 16}.get(pose, 0)
        line(draw, [(x - 7, y), (x - 12 + step // 2, y + 30), (x - 16 + step, GROUND_Y)], PANTS, 7)
        line(draw, [(x + 7, y), (x + 9 - step // 2, y + 30), (x + 14 - step, GROUND_Y)], PANTS_HI, 7)
        rect(draw, (x - 23 + step, GROUND_Y - 4, x - 8 + step, GROUND_Y + 2), BLACK_2)
        rect(draw, (x + 7 - step, GROUND_Y - 4, x + 22 - step, GROUND_Y + 2), BLACK_2)


def draw_arms(draw: ImageDraw.ImageDraw, shoulder: tuple[int, int], pose: str) -> None:
    x, y = shoulder
    if pose in {"idle0", "idle1", "idle2", "prayer", "counter"}:
        dy = {"idle0": 0, "idle1": 1, "idle2": -1, "prayer": 0, "counter": -2}[pose]
        line(draw, [(x - 13, y + 5), (x - 2, y + 22 + dy), (x + 7, y + 22 + dy)], SKIN, 5)
        line(draw, [(x + 13, y + 5), (x + 5, y + 22 + dy), (x - 8, y + 22 + dy)], SKIN_LIGHT, 5)
        rect(draw, (x - 1, y + 18 + dy, x + 2, y + 26 + dy), CREAM)
    elif pose == "lp":
        line(draw, [(x - 12, y + 8), (x - 1, y + 20), (x + 12, y + 18)], SKIN, 5)
        line(draw, [(x + 12, y + 7), (x + 31, y + 9), (x + 43, y + 10)], SKIN_LIGHT, 5)
        rect(draw, (x + 40, y + 6, x + 48, y + 13), SKIN_LIGHT)
    elif pose in {"hp", "palm"}:
        line(draw, [(x - 12, y + 7), (x - 1, y + 17), (x + 14, y + 18)], SKIN, 5)
        line(draw, [(x + 12, y + 6), (x + 32, y - 1), (x + 51, y - 4)], SKIN_LIGHT, 5)
        poly(draw, [(x + 51, y - 9), (x + 62, y - 5), (x + 52, y + 1)], SKIN_LIGHT)
        if pose == "palm":
            draw.rectangle((x + 54, y - 12, x + 71, y - 9), fill=FX)
            draw.rectangle((x + 60, y - 5, x + 78, y - 2), fill=FX_DARK)
    elif pose == "lk":
        line(draw, [(x - 12, y + 6), (x - 5, y + 21), (x + 4, y + 21)], SKIN, 5)
        line(draw, [(x + 12, y + 7), (x + 3, y + 22), (x - 5, y + 22)], SKIN_LIGHT, 5)
    elif pose == "hk":
        line(draw, [(x - 12, y + 6), (x - 24, y + 20), (x - 34, y + 28)], SKIN, 5)
        line(draw, [(x + 12, y + 7), (x + 2, y + 24), (x - 11, y + 31)], SKIN_LIGHT, 5)
    elif pose == "crane":
        line(draw, [(x - 12, y + 6), (x - 21, y - 12), (x - 18, y - 27)], SKIN, 5)
        line(draw, [(x + 12, y + 6), (x + 23, y - 16), (x + 22, y - 31)], SKIN_LIGHT, 5)
        draw.rectangle((x + 16, y - 36, x + 27, y - 30), fill=FX)
    elif pose == "hit":
        line(draw, [(x - 12, y + 8), (x - 28, y + 20), (x - 35, y + 31)], SKIN, 5)
        line(draw, [(x + 12, y + 8), (x + 1, y + 29), (x - 8, y + 38)], SKIN_LIGHT, 5)
    elif pose == "bow":
        line(draw, [(x - 12, y + 8), (x - 4, y + 29), (x + 5, y + 36)], SKIN, 5)
        line(draw, [(x + 12, y + 8), (x + 4, y + 29), (x - 5, y + 36)], SKIN_LIGHT, 5)
    else:
        line(draw, [(x - 12, y + 8), (x - 4, y + 24), (x + 4, y + 26)], SKIN, 5)
        line(draw, [(x + 12, y + 8), (x + 4, y + 24), (x - 4, y + 26)], SKIN_LIGHT, 5)


def draw_fx(draw: ImageDraw.ImageDraw, pose: str) -> None:
    if pose == "counter":
        draw.rectangle((20, 53, 75, 55), fill=FX)
        draw.rectangle((28, 47, 67, 49), fill=FX_DARK)
        draw.rectangle((32, 61, 63, 63), fill=FX_DARK)
    elif pose == "step":
        draw.rectangle((18, GROUND_Y + 3, 65, GROUND_Y + 4), fill=DUST)
        draw.rectangle((25, GROUND_Y + 6, 48, GROUND_Y + 7), fill=DUST)


def draw_character(spec: FrameSpec) -> Image.Image:
    img = Image.new("RGBA", (FRAME_W, FRAME_H), TRANSPARENT)
    draw = ImageDraw.Draw(img)
    pose = spec.pose

    y_offset = {"idle1": 1, "idle2": -1, "jump": -18, "crouch": 16, "bow": 8}.get(pose, 0)
    x = {"hp": 37, "palm": 35, "hk": 27, "step": 37, "hit": 54}.get(pose, 48)
    head_y = 24 + y_offset
    torso_y = 44 + y_offset
    hip = (x, 80 + y_offset)
    shoulder = (x, 49 + y_offset)

    draw.ellipse((23, GROUND_Y - 3, 73, GROUND_Y + 7), fill=SHADOW)
    if pose == "jump":
        draw.ellipse((27, GROUND_Y + 1, 70, GROUND_Y + 7), fill=(0, 0, 0, 38))

    draw_legs(draw, hip, pose)
    draw_torso(draw, x, torso_y, jacket=pose == "jacket")
    draw_arms(draw, shoulder, pose)
    if pose == "bow":
        draw_head(draw, x, head_y + 10)
    elif pose == "hit":
        draw_head(draw, x + 3, head_y + 3, glasses_shift=2)
    else:
        draw_head(draw, x, head_y)
    draw_fx(draw, pose)

    return img


def make_preview(frames: list[tuple[FrameSpec, Image.Image]]) -> Image.Image:
    cols = 4
    cell_w = 140
    cell_h = 164
    rows = (len(frames) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * cell_w, rows * cell_h), (32, 34, 40, 255))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 10)
        font_small = ImageFont.truetype("DejaVuSans.ttf", 9)
    except OSError:
        font = ImageFont.load_default()
        font_small = font

    for idx, (spec, img) in enumerate(frames):
        cx = (idx % cols) * cell_w
        cy = (idx // cols) * cell_h
        draw.rectangle((cx + 6, cy + 6, cx + cell_w - 7, cy + cell_h - 7), fill=(48, 51, 58, 255))
        for gx in range(cx + 14, cx + cell_w - 14, 16):
            draw.line((gx, cy + 16, gx, cy + 134), fill=(57, 60, 67, 255))
        for gy in range(cy + 16, cy + 134, 16):
            draw.line((cx + 14, gy, cx + cell_w - 14, gy), fill=(57, 60, 67, 255))
        sheet.alpha_composite(img, (cx + 22, cy + 11))
        draw.line((cx + 14, cy + 11 + GROUND_Y, cx + cell_w - 14, cy + 11 + GROUND_Y), fill=(96, 91, 78, 255))
        draw.text((cx + 10, cy + 140), spec.title, fill=(235, 232, 215, 255), font=font)
        draw.text((cx + 10, cy + 152), f"{spec.name}.png", fill=(175, 180, 188, 255), font=font_small)
    return sheet


def save_palette_strip() -> None:
    colors = [(r, g, b, 255) for r, g, b in INDEXED_COLORS[1:]]
    img = Image.new("RGBA", (len(colors) * 16, 24), TRANSPARENT)
    draw = ImageDraw.Draw(img)
    for i, color in enumerate(colors):
        draw.rectangle((i * 16, 0, i * 16 + 15, 15), fill=color)
        draw.rectangle((i * 16, 16, i * 16 + 15, 23), fill=(28, 28, 32, 255))
    img.save(OUT_DIR / "palette_strip.png")


def save_indexed_pcx(frame: Image.Image, name: str) -> None:
    palette = []
    for color in INDEXED_COLORS:
        palette.extend(color)
    palette.extend([0, 0, 0] * (256 - len(INDEXED_COLORS)))

    color_to_index = {color: idx for idx, color in enumerate(INDEXED_COLORS)}
    indexed = Image.new("P", frame.size, 0)
    indexed.putpalette(palette)
    src = frame.convert("RGBA")
    pix = indexed.load()
    for y in range(frame.height):
        for x in range(frame.width):
            r, g, b, a = src.getpixel((x, y))
            if a < 128:
                pix[x, y] = 0
            elif a < 255:
                pix[x, y] = color_to_index[(18, 18, 22)]
            else:
                pix[x, y] = color_to_index.get((r, g, b), 1)
    indexed.save(PCX_DIR / f"{name}.pcx")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PCX_DIR.mkdir(parents=True, exist_ok=True)
    rendered: list[tuple[FrameSpec, Image.Image]] = []
    for spec in FRAMES:
        frame = draw_character(spec)
        frame.save(OUT_DIR / f"{spec.name}.png")
        save_indexed_pcx(frame, spec.name)
        rendered.append((spec, frame))

    make_preview(rendered).save(OUT_DIR / "mestre_thaynan_sprite_sheet_preview.png")
    save_palette_strip()


if __name__ == "__main__":
    main()
