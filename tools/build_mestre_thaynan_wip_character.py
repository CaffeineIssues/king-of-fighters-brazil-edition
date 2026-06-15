#!/usr/bin/env python3
"""Build a WIP playable Mestre Thaynan character.

This creates a minimal test character definition and SprMake2 input file from
the extracted source PCX frames:

  chars/mestre_thaynan/
    mestre_thaynan.def
    mestre_thaynan.cmd
    mestre_thaynan.cns
    mestre_thaynan.air
    mestre_thaynan-sff.def
    readme.txt

The reference-extracted Mestre frames remain in assets/mestre_thaynan/. Use the
generated SprMake2 definition to build the SFF on Windows with the official
Elecbyte tool. The resulting character is a local testing placeholder, not a
finished competitive release.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PCX_DIR = ROOT / "assets" / "mestre_thaynan" / "sprites" / "pcx"
CHAR_DIR = ROOT / "chars" / "mestre_thaynan"


@dataclass(frozen=True)
class SpriteSpec:
    group: int
    image: int
    frame: str
    ground_ratio: float = 0.94


SPRITES = [
    SpriteSpec(0, 0, "idle_00"),
    SpriteSpec(0, 1, "idle_01"),
    SpriteSpec(0, 2, "idle_02"),
    SpriteSpec(0, 3, "idle_03"),
    SpriteSpec(5, 0, "idle_00"),
    SpriteSpec(6, 0, "crouch_00"),
    SpriteSpec(10, 0, "crouch_00"),
    SpriteSpec(10, 1, "crouch_01"),
    SpriteSpec(10, 2, "crouch_02"),
    SpriteSpec(10, 3, "crouch_03"),
    SpriteSpec(10, 4, "crouch_04"),
    SpriteSpec(11, 0, "crouch_00"),
    SpriteSpec(11, 1, "crouch_01"),
    SpriteSpec(11, 2, "crouch_02"),
    SpriteSpec(11, 3, "crouch_03"),
    SpriteSpec(11, 4, "crouch_04"),
    SpriteSpec(12, 0, "idle_00"),
    SpriteSpec(20, 0, "walk_00"),
    SpriteSpec(20, 1, "walk_01"),
    SpriteSpec(20, 2, "walk_02"),
    SpriteSpec(20, 3, "walk_03"),
    SpriteSpec(20, 4, "walk_04"),
    SpriteSpec(21, 0, "walk_back_00"),
    SpriteSpec(21, 1, "walk_back_01"),
    SpriteSpec(21, 2, "walk_back_02"),
    SpriteSpec(21, 3, "walk_back_03"),
    SpriteSpec(21, 4, "walk_back_04"),
    SpriteSpec(40, 0, "crouch_00"),
    SpriteSpec(41, 0, "jump_00", 0.88),
    SpriteSpec(41, 1, "jump_01", 0.88),
    SpriteSpec(41, 2, "jump_02", 0.88),
    SpriteSpec(41, 3, "jump_03", 0.88),
    SpriteSpec(41, 4, "jump_04", 0.88),
    SpriteSpec(42, 0, "jump_00", 0.88),
    SpriteSpec(42, 1, "jump_01", 0.88),
    SpriteSpec(42, 2, "jump_02", 0.88),
    SpriteSpec(42, 3, "jump_03", 0.88),
    SpriteSpec(42, 4, "jump_04", 0.88),
    SpriteSpec(43, 0, "jump_00", 0.88),
    SpriteSpec(43, 1, "jump_01", 0.88),
    SpriteSpec(43, 2, "jump_02", 0.88),
    SpriteSpec(43, 3, "jump_03", 0.88),
    SpriteSpec(43, 4, "jump_04", 0.88),
    SpriteSpec(44, 0, "jump_00", 0.88),
    SpriteSpec(44, 1, "jump_01", 0.88),
    SpriteSpec(44, 2, "jump_02", 0.88),
    SpriteSpec(44, 3, "jump_03", 0.88),
    SpriteSpec(44, 4, "jump_04", 0.88),
    SpriteSpec(47, 0, "idle_00"),
    SpriteSpec(100, 0, "dash_00"),
    SpriteSpec(100, 1, "dash_01"),
    SpriteSpec(100, 2, "dash_02"),
    SpriteSpec(100, 3, "dash_03"),
    SpriteSpec(100, 4, "dash_04"),
    SpriteSpec(105, 0, "dash_00"),
    SpriteSpec(120, 0, "guard_00"),
    SpriteSpec(120, 1, "guard_01"),
    SpriteSpec(120, 2, "guard_02"),
    SpriteSpec(120, 3, "guard_03"),
    SpriteSpec(120, 4, "guard_04"),
    SpriteSpec(130, 0, "guard_00"),
    SpriteSpec(130, 1, "guard_01"),
    SpriteSpec(130, 2, "guard_02"),
    SpriteSpec(130, 3, "guard_03"),
    SpriteSpec(130, 4, "guard_04"),
    SpriteSpec(131, 0, "block_00"),
    SpriteSpec(131, 1, "block_01"),
    SpriteSpec(131, 2, "block_02"),
    SpriteSpec(131, 3, "block_03"),
    SpriteSpec(132, 0, "guard_00"),
    SpriteSpec(132, 1, "guard_01"),
    SpriteSpec(132, 2, "guard_02"),
    SpriteSpec(132, 3, "guard_03"),
    SpriteSpec(132, 4, "guard_04"),
    SpriteSpec(140, 0, "crouch_00"),
    SpriteSpec(140, 1, "crouch_01"),
    SpriteSpec(140, 2, "crouch_02"),
    SpriteSpec(140, 3, "crouch_03"),
    SpriteSpec(140, 4, "crouch_04"),
    SpriteSpec(150, 0, "hit_00", 0.9),
    SpriteSpec(150, 1, "hit_01", 0.9),
    SpriteSpec(150, 2, "hit_02", 0.9),
    SpriteSpec(150, 3, "hit_03", 0.9),
    SpriteSpec(150, 4, "hit_04", 0.9),
    SpriteSpec(151, 0, "hit_00", 0.9),
    SpriteSpec(151, 1, "hit_01", 0.9),
    SpriteSpec(151, 2, "hit_02", 0.9),
    SpriteSpec(151, 3, "hit_03", 0.9),
    SpriteSpec(151, 4, "hit_04", 0.9),
    SpriteSpec(152, 0, "hit_00", 0.9),
    SpriteSpec(152, 1, "hit_01", 0.9),
    SpriteSpec(152, 2, "hit_02", 0.9),
    SpriteSpec(152, 3, "hit_03", 0.9),
    SpriteSpec(152, 4, "hit_04", 0.9),
    SpriteSpec(154, 0, "hit_00", 0.9),
    SpriteSpec(154, 1, "hit_01", 0.9),
    SpriteSpec(154, 2, "hit_02", 0.9),
    SpriteSpec(154, 3, "hit_03", 0.9),
    SpriteSpec(154, 4, "hit_04", 0.9),
    SpriteSpec(170, 0, "knockdown_00"),
    SpriteSpec(175, 0, "win_00"),
    SpriteSpec(190, 0, "win_00"),
    SpriteSpec(200, 0, "stand_lp_00"),
    SpriteSpec(200, 1, "stand_lp_01"),
    SpriteSpec(200, 2, "stand_lp_02"),
    SpriteSpec(200, 3, "stand_lp_03"),
    SpriteSpec(200, 4, "stand_lp_04"),
    SpriteSpec(210, 0, "stand_hp_00"),
    SpriteSpec(210, 1, "stand_hp_01"),
    SpriteSpec(210, 2, "stand_hp_02"),
    SpriteSpec(210, 3, "stand_hp_03"),
    SpriteSpec(210, 4, "stand_hp_04"),
    SpriteSpec(230, 0, "stand_lk_00"),
    SpriteSpec(230, 1, "stand_lk_01"),
    SpriteSpec(230, 2, "stand_lk_02"),
    SpriteSpec(230, 3, "stand_lk_03"),
    SpriteSpec(230, 4, "stand_lk_04"),
    SpriteSpec(240, 0, "stand_hk_00", 0.88),
    SpriteSpec(240, 1, "stand_hk_01", 0.88),
    SpriteSpec(240, 2, "stand_hk_02", 0.88),
    SpriteSpec(240, 3, "stand_hk_03", 0.88),
    SpriteSpec(240, 4, "stand_hk_04", 0.88),
    SpriteSpec(400, 0, "crouch_00"),
    SpriteSpec(400, 1, "crouch_01"),
    SpriteSpec(400, 2, "crouch_02"),
    SpriteSpec(400, 3, "crouch_03"),
    SpriteSpec(400, 4, "crouch_04"),
    SpriteSpec(410, 0, "stand_hp_00"),
    SpriteSpec(410, 1, "stand_hp_01"),
    SpriteSpec(410, 2, "stand_hp_02"),
    SpriteSpec(410, 3, "stand_hp_03"),
    SpriteSpec(410, 4, "stand_hp_04"),
    SpriteSpec(430, 0, "crouch_00"),
    SpriteSpec(430, 1, "crouch_01"),
    SpriteSpec(430, 2, "crouch_02"),
    SpriteSpec(430, 3, "crouch_03"),
    SpriteSpec(430, 4, "crouch_04"),
    SpriteSpec(440, 0, "stand_hk_00", 0.88),
    SpriteSpec(440, 1, "stand_hk_01", 0.88),
    SpriteSpec(440, 2, "stand_hk_02", 0.88),
    SpriteSpec(440, 3, "stand_hk_03", 0.88),
    SpriteSpec(440, 4, "stand_hk_04", 0.88),
    SpriteSpec(600, 0, "jump_00", 0.88),
    SpriteSpec(600, 1, "jump_01", 0.88),
    SpriteSpec(600, 2, "jump_02", 0.88),
    SpriteSpec(600, 3, "jump_03", 0.88),
    SpriteSpec(600, 4, "jump_04", 0.88),
    SpriteSpec(610, 0, "stand_hk_00", 0.88),
    SpriteSpec(610, 1, "stand_hk_01", 0.88),
    SpriteSpec(610, 2, "stand_hk_02", 0.88),
    SpriteSpec(610, 3, "stand_hk_03", 0.88),
    SpriteSpec(610, 4, "stand_hk_04", 0.88),
    SpriteSpec(630, 0, "jump_00", 0.88),
    SpriteSpec(630, 1, "jump_01", 0.88),
    SpriteSpec(630, 2, "jump_02", 0.88),
    SpriteSpec(630, 3, "jump_03", 0.88),
    SpriteSpec(630, 4, "jump_04", 0.88),
    SpriteSpec(640, 0, "stand_hk_00", 0.88),
    SpriteSpec(640, 1, "stand_hk_01", 0.88),
    SpriteSpec(640, 2, "stand_hk_02", 0.88),
    SpriteSpec(640, 3, "stand_hk_03", 0.88),
    SpriteSpec(640, 4, "stand_hk_04", 0.88),
    SpriteSpec(900, 0, "win_00"),
    SpriteSpec(900, 1, "win_01"),
    SpriteSpec(900, 2, "win_02"),
    SpriteSpec(5000, 0, "hit_00", 0.9),
    SpriteSpec(5000, 1, "hit_01", 0.9),
    SpriteSpec(5000, 2, "hit_02", 0.9),
    SpriteSpec(5000, 3, "hit_03", 0.9),
    SpriteSpec(5000, 4, "hit_04", 0.9),
    SpriteSpec(5001, 0, "hit_00", 0.9),
    SpriteSpec(5001, 1, "hit_01", 0.9),
    SpriteSpec(5001, 2, "hit_02", 0.9),
    SpriteSpec(5001, 3, "hit_03", 0.9),
    SpriteSpec(5001, 4, "hit_04", 0.9),
    SpriteSpec(5002, 0, "hit_00", 0.9),
    SpriteSpec(5002, 1, "hit_01", 0.9),
    SpriteSpec(5002, 2, "hit_02", 0.9),
    SpriteSpec(5002, 3, "hit_03", 0.9),
    SpriteSpec(5002, 4, "hit_04", 0.9),
    SpriteSpec(5010, 0, "hit_00", 0.9),
    SpriteSpec(5010, 1, "hit_01", 0.9),
    SpriteSpec(5010, 2, "hit_02", 0.9),
    SpriteSpec(5010, 3, "hit_03", 0.9),
    SpriteSpec(5010, 4, "hit_04", 0.9),
    SpriteSpec(5011, 0, "hit_00", 0.9),
    SpriteSpec(5011, 1, "hit_01", 0.9),
    SpriteSpec(5011, 2, "hit_02", 0.9),
    SpriteSpec(5011, 3, "hit_03", 0.9),
    SpriteSpec(5011, 4, "hit_04", 0.9),
    SpriteSpec(5012, 0, "hit_00", 0.9),
    SpriteSpec(5012, 1, "hit_01", 0.9),
    SpriteSpec(5012, 2, "hit_02", 0.9),
    SpriteSpec(5012, 3, "hit_03", 0.9),
    SpriteSpec(5012, 4, "hit_04", 0.9),
    SpriteSpec(5020, 0, "hit_00", 0.9),
    SpriteSpec(5020, 1, "hit_01", 0.9),
    SpriteSpec(5020, 2, "hit_02", 0.9),
    SpriteSpec(5020, 3, "hit_03", 0.9),
    SpriteSpec(5020, 4, "hit_04", 0.9),
    SpriteSpec(5021, 0, "hit_00", 0.9),
    SpriteSpec(5021, 1, "hit_01", 0.9),
    SpriteSpec(5021, 2, "hit_02", 0.9),
    SpriteSpec(5021, 3, "hit_03", 0.9),
    SpriteSpec(5021, 4, "hit_04", 0.9),
    SpriteSpec(5022, 0, "hit_00", 0.9),
    SpriteSpec(5022, 1, "hit_01", 0.9),
    SpriteSpec(5022, 2, "hit_02", 0.9),
    SpriteSpec(5022, 3, "hit_03", 0.9),
    SpriteSpec(5022, 4, "hit_04", 0.9),
    SpriteSpec(5030, 0, "hit_00", 0.9),
    SpriteSpec(5030, 1, "hit_01", 0.9),
    SpriteSpec(5030, 2, "hit_02", 0.9),
    SpriteSpec(5030, 3, "hit_03", 0.9),
    SpriteSpec(5030, 4, "hit_04", 0.9),
    SpriteSpec(5050, 0, "hit_00", 0.9),
    SpriteSpec(5050, 1, "hit_01", 0.9),
    SpriteSpec(5050, 2, "hit_02", 0.9),
    SpriteSpec(5050, 3, "hit_03", 0.9),
    SpriteSpec(5050, 4, "hit_04", 0.9),
    SpriteSpec(5035, 0, "knockdown_00"),
    SpriteSpec(5035, 1, "knockdown_01"),
    SpriteSpec(5035, 2, "knockdown_02"),
    SpriteSpec(5035, 3, "knockdown_03"),
    SpriteSpec(5040, 0, "knockdown_00"),
    SpriteSpec(5040, 1, "knockdown_01"),
    SpriteSpec(5040, 2, "knockdown_02"),
    SpriteSpec(5040, 3, "knockdown_03"),
    SpriteSpec(5060, 0, "knockdown_00"),
    SpriteSpec(5060, 1, "knockdown_01"),
    SpriteSpec(5060, 2, "knockdown_02"),
    SpriteSpec(5060, 3, "knockdown_03"),
    SpriteSpec(5070, 0, "knockdown_00"),
    SpriteSpec(5070, 1, "knockdown_01"),
    SpriteSpec(5070, 2, "knockdown_02"),
    SpriteSpec(5070, 3, "knockdown_03"),
    SpriteSpec(5080, 0, "knockdown_00"),
    SpriteSpec(5080, 1, "knockdown_01"),
    SpriteSpec(5080, 2, "knockdown_02"),
    SpriteSpec(5080, 3, "knockdown_03"),
    SpriteSpec(5100, 0, "knockdown_00"),
    SpriteSpec(5100, 1, "knockdown_01"),
    SpriteSpec(5100, 2, "knockdown_02"),
    SpriteSpec(5100, 3, "knockdown_03"),
    SpriteSpec(5101, 0, "knockdown_00"),
    SpriteSpec(5101, 1, "knockdown_01"),
    SpriteSpec(5101, 2, "knockdown_02"),
    SpriteSpec(5101, 3, "knockdown_03"),
    SpriteSpec(5110, 0, "knockdown_00"),
    SpriteSpec(5110, 1, "knockdown_01"),
    SpriteSpec(5110, 2, "knockdown_02"),
    SpriteSpec(5110, 3, "knockdown_03"),
    SpriteSpec(5120, 0, "idle_00"),
    SpriteSpec(5150, 0, "knockdown_01"),
    SpriteSpec(5200, 0, "idle_00"),
    SpriteSpec(5210, 0, "idle_00"),
    SpriteSpec(5300, 0, "win_00"),
    SpriteSpec(5300, 1, "win_01"),
    SpriteSpec(5300, 2, "win_02"),
    SpriteSpec(9000, 0, "portrait_small", 0.96),
    SpriteSpec(9000, 1, "portrait_big", 0.96),
]

def pcx_dimensions(path: Path) -> tuple[int, int]:
    with Image.open(path) as img:
        return img.size


def action(action_no: int, frames: list[tuple[int, int, int]], clsn1: str | None = None) -> str:
    lines = [f"[Begin Action {action_no}]"]
    lines.extend(
        [
            "Clsn2Default: 2",
            " Clsn2[0] = -18, 0, 20, -58",
            " Clsn2[1] = -10, -58, 10, -92",
        ]
    )
    if clsn1:
        lines.extend(["Clsn1: 1", f" Clsn1[0] = {clsn1}"])
    for group, image, ticks in frames:
        lines.append(f"{group},{image}, 0,0, {ticks}")
    return "\n".join(lines)


def seq(group: int, count: int, ticks: int) -> list[tuple[int, int, int]]:
    return [(group, idx, ticks) for idx in range(count)]


def write_air(path: Path) -> None:
    chunks = [
        "; Mestre Thaynan WIP animation file",
        action(0, seq(0, 4, 8)),
        action(5, [(5, 0, 4)]),
        action(6, [(6, 0, 4)]),
        action(10, seq(10, 5, 3)),
        action(11, seq(11, 5, 4)),
        action(12, [(12, 0, 4)]),
        action(20, seq(20, 5, 5)),
        action(21, seq(21, 5, 5)),
        action(40, [(40, 0, 4)]),
        action(41, seq(41, 5, 5)),
        action(42, seq(42, 5, 5)),
        action(43, seq(43, 5, 5)),
        action(44, seq(44, 5, 5)),
        action(47, [(47, 0, 3)]),
        action(100, seq(100, 5, 3)),
        action(105, [(105, 0, 8)]),
        action(120, seq(120, 5, 5)),
        action(130, seq(130, 5, 5)),
        action(131, seq(131, 4, 5)),
        action(132, seq(132, 5, 5)),
        action(140, seq(140, 5, 4)),
        action(150, seq(150, 5, 4)),
        action(151, seq(151, 5, 4)),
        action(152, seq(152, 5, 4)),
        action(154, seq(154, 5, 4)),
        action(170, [(170, 0, 60)]),
        action(175, [(175, 0, 60)]),
        action(190, [(190, 0, 60)]),
        action(200, seq(200, 5, 3), "8,-60, 54,-30"),
        action(210, seq(210, 5, 4), "10,-64, 58,-30"),
        action(230, seq(230, 5, 4), "8,-45, 56,-10"),
        action(240, seq(240, 5, 4), "8,-72, 62,-12"),
        action(400, seq(400, 5, 4), "8,-42, 48,-8"),
        action(410, seq(410, 5, 4), "8,-62, 58,-28"),
        action(430, seq(430, 5, 4), "8,-24, 48,-4"),
        action(440, seq(440, 5, 4), "8,-58, 62,-12"),
        action(600, seq(600, 5, 4), "8,-70, 42,-35"),
        action(610, seq(610, 5, 4), "8,-78, 62,-12"),
        action(630, seq(630, 5, 4), "8,-60, 42,-20"),
        action(640, seq(640, 5, 4), "8,-78, 62,-12"),
        action(900, seq(900, 3, 12)),
    ]
    for anim in [5000, 5001, 5002, 5010, 5011, 5012, 5020, 5021, 5022, 5030, 5050]:
        chunks.append(action(anim, seq(anim, 5, 4)))
    for anim in [5035, 5040, 5060, 5070, 5080, 5100, 5101, 5110]:
        chunks.append(action(anim, seq(anim, 4, 8)))
    chunks.extend(
        [
            action(5120, [(5120, 0, 12)]),
            action(5150, [(5150, 0, 60)]),
            action(5200, [(5200, 0, 12)]),
            action(5210, [(5210, 0, 12)]),
            action(5300, seq(5300, 3, 12)),
        ]
    )
    path.write_text("\n\n".join(chunks) + "\n", encoding="utf-8")


DEF = """; Definition file for Mestre Thaynan WIP
; Based on the stock KFM .def layout so MUGEN loads it like a normal character.
; Contains all the filenames needed for the character.

; Player information
[Info]
name = "Mestre Thaynan"
displayname = "Mestre Thaynan"
versiondate = 06,15,2026
mugenversion = 1.0
author = "Brazilian Meme Fighters Team"
pal.defaults = 1          ;Default palettes in order of preference
localcoord = 320,240      ;Local coordinate space width and height

; Files for the player
[Files]
cmd     = mestre_thaynan.cmd
cns     = mestre_thaynan.cns
st      = mestre_thaynan.cns
stcommon = common1.cns
sprite  = mestre_thaynan.sff
anim    = mestre_thaynan.air

; Maps character selection buttons to palette numbers.
[Palette Keymap]
x = 1 ;Press button X to select palette 1, etc.
y = 1
z = 1
a = 1
b = 1
c = 1
"""


CNS = """; Mestre Thaynan WIP constants and states

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
xscale = 0.82
yscale = 0.82
ground.back = 16
ground.front = 20
air.back = 14
air.front = 18
height = 82
attack.dist = 120
proj.attack.dist = 90
proj.doscale = 0
head.pos = -6, -82
mid.pos = -4, -50
shadowoffset = 0
draw.offset = 0,0

[Velocity]
walk.fwd = 2.1
walk.back = -1.8
run.fwd = 4.2, 0
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

[Quotes]
victory1 = "Form first. Power follows."
victory2 = "The tiger waits before it strikes."

; ---------------------------------------------------------------------------
; Basic normals

[Statedef 200]
type = S
movetype = A
physics = S
anim = 200
ctrl = 0
sprpriority = 2

[State 200, Hit]
type = HitDef
trigger1 = Time = 2
attr = S, NA
damage = 24, 4
animtype = Light
guardflag = MA
hitflag = MAF
priority = 3, Hit
pausetime = 6,6
sparkno = -1
guard.sparkno = -1
hitsound = -1
guardsound = -1
ground.type = High
ground.slidetime = 8
ground.hittime = 10
ground.velocity = -2
air.velocity = -2,-3

[State 200, End]
type = ChangeState
trigger1 = AnimTime = 0
value = 0
ctrl = 1

[Statedef 210]
type = S
movetype = A
physics = S
anim = 210
ctrl = 0
sprpriority = 2

[State 210, Hit]
type = HitDef
trigger1 = Time = 4
attr = S, NA
damage = 68, 8
animtype = Hard
guardflag = MA
hitflag = MAF
priority = 4, Hit
pausetime = 10,10
sparkno = -1
guard.sparkno = -1
hitsound = -1
guardsound = -1
ground.type = High
ground.slidetime = 12
ground.hittime = 15
ground.velocity = -4
air.velocity = -3,-4

[State 210, End]
type = ChangeState
trigger1 = AnimTime = 0
value = 0
ctrl = 1

[Statedef 230]
type = S
movetype = A
physics = S
anim = 230
ctrl = 0
sprpriority = 2

[State 230, Hit]
type = HitDef
trigger1 = Time = 3
attr = S, NA
damage = 28, 4
animtype = Light
guardflag = MA
hitflag = MAF
priority = 3, Hit
pausetime = 6,6
sparkno = -1
guard.sparkno = -1
hitsound = -1
guardsound = -1
ground.type = Low
ground.slidetime = 8
ground.hittime = 11
ground.velocity = -2
air.velocity = -2,-3

[State 230, End]
type = ChangeState
trigger1 = AnimTime = 0
value = 0
ctrl = 1

[Statedef 240]
type = S
movetype = A
physics = S
anim = 240
ctrl = 0
sprpriority = 2

[State 240, Hit]
type = HitDef
trigger1 = Time = 5
attr = S, NA
damage = 76, 8
animtype = Hard
guardflag = MA
hitflag = MAF
priority = 4, Hit
pausetime = 10,10
sparkno = -1
guard.sparkno = -1
hitsound = -1
guardsound = -1
ground.type = High
ground.slidetime = 12
ground.hittime = 16
ground.velocity = -5
air.velocity = -3,-5

[State 240, End]
type = ChangeState
trigger1 = AnimTime = 0
value = 0
ctrl = 1

; ---------------------------------------------------------------------------
; Air attacks

[Statedef 600]
type = A
movetype = A
physics = A
anim = 600
ctrl = 0
sprpriority = 2

[State 600, Hit]
type = HitDef
trigger1 = Time = 2
attr = A, NA
damage = 42, 5
animtype = Medium
guardflag = HA
hitflag = MAF
priority = 3, Hit
pausetime = 7,7
sparkno = -1
guard.sparkno = -1
hitsound = -1
guardsound = -1
ground.type = High
ground.slidetime = 10
ground.hittime = 13
ground.velocity = -3
air.velocity = -2,-4

[State 600, End]
type = ChangeState
trigger1 = AnimTime = 0
value = 50
ctrl = 1


"""


CMD = """; Mestre Thaynan WIP command file

[Command]
name = "x"
command = x
time = 1

[Command]
name = "y"
command = y
time = 1

[Command]
name = "a"
command = a
time = 1

[Command]
name = "b"
command = b
time = 1

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

[State -1, Air Attack]
type = ChangeState
value = 600
triggerall = command = "x" || command = "y" || command = "a" || command = "b"
triggerall = statetype = A
triggerall = ctrl
trigger1 = 1

[State -1, LP]
type = ChangeState
value = 200
triggerall = command = "x"
triggerall = statetype = S
triggerall = ctrl
trigger1 = 1

[State -1, HP]
type = ChangeState
value = 210
triggerall = command = "y"
triggerall = statetype = S
triggerall = ctrl
trigger1 = 1

[State -1, LK]
type = ChangeState
value = 230
triggerall = command = "a"
triggerall = statetype = S
triggerall = ctrl
trigger1 = 1

[State -1, HK]
type = ChangeState
value = 240
triggerall = command = "b"
triggerall = statetype = S
triggerall = ctrl
trigger1 = 1
"""


README = """Mestre Thaynan WIP Playable Test
================================

This is a temporary playable placeholder using Mestre Thaynan's generated
SFF/AIR files.

What works:
- Selection via data/select.def
- Loads using mestre_thaynan.sff and mestre_thaynan.air
- Idle, walk, jump, crouch using the current extracted Mestre frames
- Four basic buttons: x/y punches, a/b kicks
- Guard/block, hurt, knockdown, and win placeholder frames from the sheet

Known limitations:
- This is not a final balanced character.
- Special moves are intentionally disabled until matching sprite art exists.
- Requires mestre_thaynan.sff to be rebuilt with SprMake2 after sprite changes.
- Mestre's extracted source frames remain in assets/mestre_thaynan/sprites/.
- No custom sounds are included yet.
- Hitboxes are broad temporary boxes for local testing only.

To build Mestre's own SFF with the official Windows tool:
  sprmake2.exe chars\\mestre_thaynan\\mestre_thaynan-sff.def

Portrait note:
- 9000,0 uses portrait_small.pcx at 25x25 for the select-grid icon.
- 9000,1 uses portrait_big.pcx at 120x140 for the large portrait slot.

After sprite extraction changes, rebuild the SFF before testing.
"""


def write_sprmake2_def(path: Path) -> None:
    lines = [
        "[Output]",
        "filename = chars/mestre_thaynan/mestre_thaynan.sff",
        "",
        "[Option]",
        "input.dir = assets/mestre_thaynan/sprites/pcx",
        "sprite.compress.5 = lz5",
        "sprite.compress.8 = rle8",
        "sprite.compress.24 = none",
        "sprite.decompressonload = 0",
        "sprite.detectduplicates = 0",
        "sprite.autocrop = 1",
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
        pcx_path = PCX_DIR / f"{spec.frame}.pcx"
        width, height = pcx_dimensions(pcx_path)
        x_axis = width // 2
        y_axis = max(1, min(height - 1, int(height * spec.ground_ratio)))
        lines.append(f"{spec.group}, {spec.image}, {spec.frame}.pcx, {x_axis}, {y_axis}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_text_files() -> None:
    CHAR_DIR.mkdir(parents=True, exist_ok=True)
    (CHAR_DIR / "mestre_thaynan.def").write_text(DEF, encoding="utf-8")
    (CHAR_DIR / "mestre_thaynan.cns").write_text(CNS, encoding="utf-8")
    (CHAR_DIR / "mestre_thaynan.cmd").write_text(CMD, encoding="utf-8")
    (CHAR_DIR / "readme.txt").write_text(README, encoding="utf-8")
    write_air(CHAR_DIR / "mestre_thaynan.air")
    write_sprmake2_def(CHAR_DIR / "mestre_thaynan-sff.def")


def main() -> None:
    write_text_files()


if __name__ == "__main__":
    main()
