#!/usr/bin/env python3
"""Build minimal He-man do Sertao WIP character files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PCX_DIR = ROOT / "assets" / "he_man_do_sertao" / "sprites" / "pcx"
CHAR_DIR = ROOT / "chars" / "he_man_do_sertao"
GAMEPLAY_AXIS_X = 110
GAMEPLAY_AXIS_Y = 158


@dataclass(frozen=True)
class SpriteSpec:
    group: int
    image: int
    frame: str
    ground_ratio: float = 0.96


def specs_for(group: int, prefix: str, count: int, ground_ratio: float = 0.96) -> list[SpriteSpec]:
    return [SpriteSpec(group, idx, f"{prefix}_{idx:02d}", ground_ratio) for idx in range(count)]


SPRITES = [
    *specs_for(0, "idle", 2),
    SpriteSpec(5, 0, "idle_00"),
    SpriteSpec(6, 0, "idle_00"),
    *specs_for(10, "idle", 2),
    *specs_for(11, "idle", 2),
    SpriteSpec(12, 0, "idle_00"),
    *specs_for(20, "idle", 2),
    *specs_for(21, "idle", 2),
    SpriteSpec(40, 0, "idle_00"),
    *specs_for(41, "idle", 2),
    *specs_for(42, "idle", 2),
    *specs_for(43, "idle", 2),
    *specs_for(44, "idle", 2),
    SpriteSpec(47, 0, "idle_00"),
    *specs_for(100, "idle", 2),
    SpriteSpec(105, 0, "idle_00"),
    *specs_for(120, "idle", 2),
    *specs_for(130, "idle", 2),
    *specs_for(131, "idle", 2),
    *specs_for(132, "idle", 2),
    *specs_for(140, "idle", 2),
    *specs_for(150, "idle", 2),
    *specs_for(151, "idle", 2),
    *specs_for(152, "idle", 2),
    *specs_for(154, "idle", 2),
    SpriteSpec(170, 0, "idle_00"),
    SpriteSpec(175, 0, "idle_00"),
    SpriteSpec(190, 0, "idle_00"),
    *specs_for(400, "idle", 2),
    *specs_for(430, "idle", 2),
    *specs_for(5000, "idle", 2),
    *specs_for(5001, "idle", 2),
    *specs_for(5002, "idle", 2),
    *specs_for(5010, "idle", 2),
    *specs_for(5011, "idle", 2),
    *specs_for(5012, "idle", 2),
    *specs_for(5020, "idle", 2),
    *specs_for(5021, "idle", 2),
    *specs_for(5022, "idle", 2),
    *specs_for(5030, "idle", 2),
    *specs_for(5035, "idle", 2),
    *specs_for(5040, "idle", 2),
    *specs_for(5050, "idle", 2),
    *specs_for(5060, "idle", 2),
    *specs_for(5070, "idle", 2),
    *specs_for(5080, "idle", 2),
    *specs_for(5100, "idle", 2),
    *specs_for(5101, "idle", 2),
    *specs_for(5110, "idle", 2),
    SpriteSpec(5120, 0, "idle_00"),
    SpriteSpec(5150, 0, "idle_00"),
    SpriteSpec(5200, 0, "idle_00"),
    SpriteSpec(5210, 0, "idle_00"),
    *specs_for(5300, "idle", 2),
    SpriteSpec(9000, 0, "portrait_small", 0.96),
    SpriteSpec(9000, 1, "portrait_big", 0.96),
]


def pcx_dimensions(path: Path) -> tuple[int, int]:
    with Image.open(path) as img:
        return img.size


def action(action_no: int, frames: list[tuple[int, int, int]]) -> str:
    lines = [
        f"[Begin Action {action_no}]",
        "Clsn2Default: 2",
        " Clsn2[0] = -26, 0, 26, -76",
        " Clsn2[1] = -14, -76, 14, -108",
    ]
    for group, image, ticks in frames:
        lines.append(f"{group},{image}, 0,0, {ticks}")
    return "\n".join(lines)


def seq(group: int, count: int, ticks: int) -> list[tuple[int, int, int]]:
    return [(group, idx, ticks) for idx in range(count)]


def write_air(path: Path) -> None:
    chunks = ["; He-man do Sertao WIP animation file"]
    for action_no in [0, 10, 11, 20, 21, 41, 42, 43, 44, 100, 120, 130, 131, 132, 140, 150, 151, 152, 154, 400, 430, 5000, 5001, 5002, 5010, 5011, 5012, 5020, 5021, 5022, 5030, 5035, 5040, 5050, 5060, 5070, 5080, 5100, 5101, 5110, 5300]:
        chunks.append(action(action_no, seq(action_no, 2, 8)))
    for action_no in [5, 6, 12, 40, 47, 105, 170, 175, 190, 5120, 5150, 5200, 5210]:
        group = action_no if action_no in [5, 6, 12, 40, 47, 105, 170, 175, 190, 5120, 5150, 5200, 5210] else 0
        chunks.append(action(action_no, [(group, 0, 12)] if group not in [5120, 5150, 5200, 5210] else [(action_no, 0, 12)]))
    path.write_text("\n\n".join(chunks) + "\n", encoding="utf-8")


DEF = """; Definition file for He-man do Sertao WIP

[Info]
name = "He-man do Sertao"
displayname = "He-man do Sertão"
versiondate = 06,17,2026
mugenversion = 1.0
author = "Brazilian Meme Fighters Team"
pal.defaults = 1
localcoord = 320,240

[Files]
cmd     = he_man_do_sertao.cmd
cns     = he_man_do_sertao.cns
st      = he_man_do_sertao.cns
stcommon = common1.cns
sprite  = he_man_do_sertao.sff
anim    = he_man_do_sertao.air

[Palette Keymap]
x = 1
y = 1
z = 1
a = 1
b = 1
c = 1
"""


CNS = """; He-man do Sertao WIP constants

[Data]
life = 1000
attack = 100
defence = 100
fall.defence_up = 50
liedown.time = 60
airjuggle = 15
sparkno = -1
guard.sparkno = -1
KO.echo = 0
volume = 0
IntPersistIndex = 60
FloatPersistIndex = 40

[Size]
xscale = 1
yscale = 1
ground.back = 18
ground.front = 18
air.back = 14
air.front = 14
height = 70
attack.dist = 160
proj.attack.dist = 90
proj.doscale = 0
head.pos = 0, -105
mid.pos = 0, -62
shadowoffset = 0
draw.offset = 0,0

[Velocity]
walk.fwd = 2.0
walk.back = -1.8
run.fwd = 4.0, 0
run.back = -4.0,-3.5
jump.neu = 0,-8.1
jump.back = -2.3
jump.fwd = 2.4
runjump.back = -2.4,-8.0
runjump.fwd = 3.8,-8.0
airjump.neu = 0,-8.0
airjump.back = -2.4
airjump.fwd = 2.4
air.gethit.groundrecover = -.15,-3.5
air.gethit.airrecover.mul = .5,.2
air.gethit.airrecover.add = 0,-4.5
air.gethit.airrecover.back = -1
air.gethit.airrecover.fwd = 0
air.gethit.airrecover.up = -2
air.gethit.airrecover.down = 1.5

[Movement]
airjump.num = 0
airjump.height = 35
yaccel = .44
stand.friction = .85
crouch.friction = .82
stand.friction.threshold = 2
crouch.friction.threshold = .05
air.gethit.groundlevel = 25
air.gethit.groundrecover.ground.threshold = -20
air.gethit.groundrecover.groundlevel = 10
air.gethit.airrecover.threshold = -1
air.gethit.airrecover.yaccel = .35
air.gethit.trip.groundlevel = 15
down.bounce.offset = 0, 20
down.bounce.yaccel = .4
down.bounce.groundlevel = 12
down.friction.threshold = .05

[Statedef -2]

[State -2, No-op]
type = Null
trigger1 = 1
"""


CMD = """; He-man do Sertao WIP command file

[Command]
name = "recovery"
command = x+y
time = 1

[Command]
name = "holdfwd"
command = /$F
time = 1

[Command]
name = "holdback"
command = /$B
time = 1

[Command]
name = "holdup"
command = /$U
time = 1

[Command]
name = "holddown"
command = /$D
time = 1

[Statedef -1]

[State -1, No-op]
type = Null
trigger1 = 1
"""


README = """He-man do Sertao WIP Test
=========================

This is a minimal idle-only test character.

What works:
- Selection via data/select.def
- Two-frame idle loop
- Required movement/hurt states reuse the idle frames as placeholders

Known limitations:
- No attacks yet.
- No custom sounds yet.
- Rebuild he_man_do_sertao.sff with SprMake2 after sprite changes.

Build:
  sprmake2.exe chars\\he_man_do_sertao\\he_man_do_sertao-sff.def
"""


def write_sprmake2_def(path: Path) -> None:
    lines = [
        "[Output]",
        "filename = chars/he_man_do_sertao/he_man_do_sertao.sff",
        "",
        "[Option]",
        "input.dir = assets/he_man_do_sertao/sprites/pcx",
        "sprite.compress.5 = lz5",
        "sprite.compress.8 = rle8",
        "sprite.compress.24 = none",
        "sprite.decompressonload = 0",
        "sprite.detectduplicates = 0",
        "sprite.autocrop = 0",
        "pal.detectduplicates = 1",
        "pal.discardduplicates = 1",
        "pal.reverseact = 0",
        "pal.reversepng = 0",
        "",
        "[Pal]",
        "1,1, idle_00.pcx, 0,255",
        "",
        "[Option]",
        "sprite.usepal = 1,1",
        "",
        "[Sprite]",
    ]
    for spec in SPRITES:
        width, height = pcx_dimensions(PCX_DIR / f"{spec.frame}.pcx")
        if spec.frame.startswith("portrait_"):
            x_axis = 0
            y_axis = 0
        else:
            x_axis = GAMEPLAY_AXIS_X
            y_axis = GAMEPLAY_AXIS_Y
        lines.append(f"{spec.group}, {spec.image}, {spec.frame}.pcx, {x_axis}, {y_axis}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_text_files() -> None:
    CHAR_DIR.mkdir(parents=True, exist_ok=True)
    (CHAR_DIR / "he_man_do_sertao.def").write_text(DEF, encoding="utf-8")
    (CHAR_DIR / "he_man_do_sertao.cns").write_text(CNS, encoding="utf-8")
    (CHAR_DIR / "he_man_do_sertao.cmd").write_text(CMD, encoding="utf-8")
    (CHAR_DIR / "readme.txt").write_text(README, encoding="utf-8")
    write_air(CHAR_DIR / "he_man_do_sertao.air")
    write_sprmake2_def(CHAR_DIR / "he_man_do_sertao-sff.def")


def main() -> None:
    write_text_files()


if __name__ == "__main__":
    main()
