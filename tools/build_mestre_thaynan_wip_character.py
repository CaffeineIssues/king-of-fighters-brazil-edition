#!/usr/bin/env python3
"""Build the minimal Mestre Thaynan WIP character files.

This restart build only wires actions that exist in the current reference sheet:
idle, walk forward, light punch, and high kick. Missing required MUGEN states
reuse standing frames as placeholders, including hurt states.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PCX_DIR = ROOT / "assets" / "mestre_thaynan" / "sprites" / "pcx"
CHAR_DIR = ROOT / "chars" / "mestre_thaynan"
GAMEPLAY_AXIS_X = 130
GAMEPLAY_AXIS_Y = 158


@dataclass(frozen=True)
class SpriteSpec:
    group: int
    image: int
    frame: str
    ground_ratio: float = 0.94


def specs_for(group: int, prefix: str, count: int, ground_ratio: float = 0.94) -> list[SpriteSpec]:
    return [SpriteSpec(group, idx, f"{prefix}_{idx:02d}", ground_ratio) for idx in range(count)]


SPRITES = [
    *specs_for(0, "idle", 3),
    SpriteSpec(5, 0, "idle_00"),
    SpriteSpec(6, 0, "idle_00"),
    *specs_for(10, "idle", 3),
    *specs_for(11, "idle", 3),
    SpriteSpec(12, 0, "idle_00"),
    *specs_for(20, "walk", 6),
    *list(reversed([SpriteSpec(21, idx, f"walk_{idx:02d}") for idx in range(6)])),
    SpriteSpec(40, 0, "idle_00"),
    *specs_for(41, "idle", 3),
    *specs_for(42, "idle", 3),
    *specs_for(43, "idle", 3),
    *specs_for(44, "idle", 3),
    SpriteSpec(47, 0, "idle_00"),
    *specs_for(100, "walk", 6),
    SpriteSpec(105, 0, "walk_00"),
    *specs_for(120, "idle", 3),
    *specs_for(130, "idle", 3),
    *specs_for(131, "idle", 3),
    *specs_for(132, "idle", 3),
    *specs_for(140, "idle", 3),
    *specs_for(150, "idle", 3),
    *specs_for(151, "idle", 3),
    *specs_for(152, "idle", 3),
    *specs_for(154, "idle", 3),
    SpriteSpec(170, 0, "idle_00"),
    SpriteSpec(175, 0, "idle_00"),
    SpriteSpec(190, 0, "idle_00"),
    SpriteSpec(200, 0, "stand_lp_03"),
    SpriteSpec(200, 1, "stand_lp_00"),
    SpriteSpec(205, 0, "stand_lp_03"),
    SpriteSpec(205, 1, "stand_lp_00"),
    SpriteSpec(210, 0, "stand_lp_03"),
    SpriteSpec(210, 1, "stand_lp_01"),
    *specs_for(230, "stand_hk", 5, 0.88),
    *specs_for(240, "stand_hk", 5, 0.88),
    *specs_for(400, "idle", 3),
    SpriteSpec(410, 0, "stand_lp_03"),
    SpriteSpec(410, 1, "stand_lp_01"),
    *specs_for(430, "idle", 3),
    *specs_for(440, "stand_hk", 5, 0.88),
    *specs_for(5000, "idle", 3),
    *specs_for(5001, "idle", 3),
    *specs_for(5002, "idle", 3),
    *specs_for(5010, "idle", 3),
    *specs_for(5011, "idle", 3),
    *specs_for(5012, "idle", 3),
    *specs_for(5020, "idle", 3),
    *specs_for(5021, "idle", 3),
    *specs_for(5022, "idle", 3),
    *specs_for(5030, "idle", 3),
    *specs_for(5035, "idle", 3),
    *specs_for(5040, "idle", 3),
    *specs_for(5050, "idle", 3),
    *specs_for(5060, "idle", 3),
    *specs_for(5070, "idle", 3),
    *specs_for(5080, "idle", 3),
    *specs_for(5100, "idle", 3),
    *specs_for(5101, "idle", 3),
    *specs_for(5110, "idle", 3),
    SpriteSpec(5120, 0, "idle_00"),
    SpriteSpec(5150, 0, "idle_00"),
    SpriteSpec(5200, 0, "idle_00"),
    SpriteSpec(5210, 0, "idle_00"),
    *specs_for(5300, "idle", 3),
    SpriteSpec(9000, 0, "portrait_small", 0.96),
    SpriteSpec(9000, 1, "portrait_big", 0.96),
]


def pcx_dimensions(path: Path) -> tuple[int, int]:
    with Image.open(path) as img:
        return img.size


def action(action_no: int, frames: list[tuple[int, int, int]], clsn1: str | None = None) -> str:
    lines = [
        f"[Begin Action {action_no}]",
        "Clsn2Default: 2",
        " Clsn2[0] = -18, 0, 20, -58",
        " Clsn2[1] = -10, -58, 10, -92",
    ]
    if clsn1:
        for group, image, ticks in frames:
            lines.extend(["Clsn1: 1", f" Clsn1[0] = {clsn1}"])
            lines.append(f"{group},{image}, 0,0, {ticks}")
        return "\n".join(lines)

    for group, image, ticks in frames:
        lines.append(f"{group},{image}, 0,0, {ticks}")
    return "\n".join(lines)


def seq(group: int, count: int, ticks: int) -> list[tuple[int, int, int]]:
    return [(group, idx, ticks) for idx in range(count)]


def write_air(path: Path) -> None:
    chunks = [
        "; Mestre Thaynan minimal WIP animation file",
        action(0, seq(0, 3, 8)),
        action(5, [(5, 0, 4)]),
        action(6, [(6, 0, 4)]),
        action(10, seq(10, 3, 4)),
        action(11, seq(11, 3, 4)),
        action(12, [(12, 0, 4)]),
        action(20, seq(20, 6, 5)),
        action(21, seq(21, 6, 5)),
        action(40, [(40, 0, 4)]),
        action(41, seq(41, 3, 6)),
        action(42, seq(42, 3, 6)),
        action(43, seq(43, 3, 6)),
        action(44, seq(44, 3, 6)),
        action(47, [(47, 0, 3)]),
        action(100, seq(100, 6, 3)),
        action(105, [(105, 0, 8)]),
        action(120, seq(120, 3, 5)),
        action(130, seq(130, 3, 5)),
        action(131, seq(131, 3, 5)),
        action(132, seq(132, 3, 5)),
        action(140, seq(140, 3, 5)),
        action(150, seq(150, 3, 5)),
        action(151, seq(151, 3, 5)),
        action(152, seq(152, 3, 5)),
        action(154, seq(154, 3, 5)),
        action(170, [(170, 0, 60)]),
        action(175, [(175, 0, 60)]),
        action(190, [(190, 0, 60)]),
        action(200, seq(200, 2, 4), "0,-64, 78,-28"),
        action(205, seq(205, 2, 4), "0,-64, 82,-28"),
        action(210, seq(210, 2, 5), "0,-66, 86,-26"),
        action(230, seq(230, 5, 4), "-2,-94, 92,-8"),
        action(240, seq(240, 5, 4), "-2,-96, 98,-8"),
        action(400, seq(400, 3, 5)),
        action(410, seq(410, 2, 5), "0,-66, 86,-26"),
        action(430, seq(430, 3, 5)),
        action(440, seq(440, 5, 4), "-2,-96, 98,-8"),
    ]
    for anim in [5000, 5001, 5002, 5010, 5011, 5012, 5020, 5021, 5022, 5030, 5035, 5040, 5050, 5060, 5070, 5080, 5100, 5101, 5110, 5300]:
        chunks.append(action(anim, seq(anim, 3, 5)))
    chunks.extend(
        [
            action(5120, [(5120, 0, 12)]),
            action(5150, [(5150, 0, 60)]),
            action(5200, [(5200, 0, 12)]),
            action(5210, [(5210, 0, 12)]),
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
xscale = 1.15
yscale = 1.15
ground.back = 15
ground.front = 16
air.back = 12
air.front = 12
height = 60
attack.dist = 160
proj.attack.dist = 90
proj.doscale = 0
head.pos = -5, -90
mid.pos = -5, -60
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

[Statedef 200]
type = S
movetype = A
physics = S
anim = 200
ctrl = 0
sprpriority = 2

[State 200, Hit]
type = HitDef
trigger1 = Time = 0
persistent = 0
attr = S, NA
damage = 35, 4
animtype = Light
guardflag = MA
hitflag = MAF
priority = 3, Hit
pausetime = 0,0
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

[Statedef 205]
type = S
movetype = A
physics = S
anim = 205
ctrl = 0
sprpriority = 2

[State 205, Hit]
type = HitDef
trigger1 = Time = 0
persistent = 0
attr = S, NA
damage = 52, 6
animtype = Medium
guardflag = MA
hitflag = MAF
priority = 3, Hit
pausetime = 0,0
sparkno = -1
guard.sparkno = -1
hitsound = -1
guardsound = -1
ground.type = High
ground.slidetime = 10
ground.hittime = 13
ground.velocity = -3
air.velocity = -2,-4

[State 205, End]
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
trigger1 = Time = 0
persistent = 0
attr = S, NA
damage = 72, 8
animtype = Hard
guardflag = MA
hitflag = MAF
priority = 4, Hit
pausetime = 0,0
sparkno = -1
guard.sparkno = -1
hitsound = -1
guardsound = -1
ground.type = High
ground.slidetime = 12
ground.hittime = 16
ground.velocity = -5
air.velocity = -3,-5

[State 210, End]
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
trigger1 = Time = 0
persistent = 0
attr = S, NA
damage = 78, 8
animtype = Hard
guardflag = MA
hitflag = MAF
priority = 4, Hit
pausetime = 0,0
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
"""


CMD = """; Mestre Thaynan minimal WIP command file

[Command]
name = "x"
command = x
time = 1

[Command]
name = "y"
command = y
time = 1

[Command]
name = "z"
command = z
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

[State -1, Light Punch]
type = ChangeState
value = 200
triggerall = command = "x"
triggerall = statetype = S
triggerall = ctrl
trigger1 = 1

[State -1, Medium Punch]
type = ChangeState
value = 205
triggerall = command = "z"
triggerall = statetype = S
triggerall = ctrl
trigger1 = 1

[State -1, Heavy Punch]
type = ChangeState
value = 210
triggerall = command = "y"
triggerall = statetype = S
triggerall = ctrl
trigger1 = 1

[State -1, High Kick]
type = ChangeState
value = 240
triggerall = command = "b"
triggerall = statetype = S
triggerall = ctrl
trigger1 = 1
"""


README = """Mestre Thaynan WIP Playable Test
================================

This is a restart pass using only the simplified reference sheet.

What works:
- Selection via data/select.def
- Loads using mestre_thaynan.sff and mestre_thaynan.air
- Idle and walk frames from the sheet
- Light punch on x
- Medium punch on z, using punch sprite 3
- Heavy punch on y, using punch sprite 2
- High kick on b
- Standing/idle frames as required fallback and hurt placeholders

Known limitations:
- This is not a final balanced character.
- No special moves until matching sprite art exists.
- No custom sounds are included yet.
- Hitboxes are broad temporary boxes for local testing only.
- Rebuild mestre_thaynan.sff with SprMake2 after sprite changes.

To build the SFF with the official Windows tool:
  sprmake2.exe chars\\mestre_thaynan\\mestre_thaynan-sff.def
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
        pcx_path = PCX_DIR / f"{spec.frame}.pcx"
        width, height = pcx_dimensions(pcx_path)
        if spec.frame.startswith("portrait_"):
            x_axis = width // 2
            y_axis = max(1, min(height - 1, round(height * spec.ground_ratio)))
        else:
            x_axis = GAMEPLAY_AXIS_X
            y_axis = GAMEPLAY_AXIS_Y
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
