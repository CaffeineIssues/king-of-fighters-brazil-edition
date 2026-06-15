#!/usr/bin/env python3
"""Build a WIP playable Mestre Thaynan character.

This creates a minimal test character that uses the known-good KFM sprite and
animation files as a temporary base:

  chars/mestre_thaynan/
    mestre_thaynan.def
    mestre_thaynan.cmd
    mestre_thaynan.cns
    mestre_thaynan.air
    mestre_thaynan-sff.def
    readme.txt

The reference-extracted Mestre frames remain in assets/mestre_thaynan/. Use the
generated SprMake2 definition to build a real Mestre SFF on Windows with the
official Elecbyte tool. The resulting character is a local testing placeholder,
not a finished competitive release.
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
    SpriteSpec(6, 0, "crouch"),
    SpriteSpec(10, 0, "crouch"),
    SpriteSpec(11, 0, "crouch"),
    SpriteSpec(12, 0, "idle_00"),
    SpriteSpec(20, 0, "walk_00"),
    SpriteSpec(20, 1, "walk_01"),
    SpriteSpec(20, 2, "walk_02"),
    SpriteSpec(20, 3, "walk_03"),
    SpriteSpec(21, 0, "walk_03"),
    SpriteSpec(21, 1, "walk_02"),
    SpriteSpec(21, 2, "walk_01"),
    SpriteSpec(21, 3, "walk_00"),
    SpriteSpec(40, 0, "crouch"),
    SpriteSpec(41, 0, "jump_neutral", 0.88),
    SpriteSpec(42, 0, "jump_neutral", 0.88),
    SpriteSpec(43, 0, "jump_neutral", 0.88),
    SpriteSpec(44, 0, "jump_neutral", 0.88),
    SpriteSpec(47, 0, "idle_00"),
    SpriteSpec(100, 0, "walk_00"),
    SpriteSpec(100, 1, "walk_01"),
    SpriteSpec(100, 2, "walk_02"),
    SpriteSpec(100, 3, "walk_03"),
    SpriteSpec(105, 0, "sidewalk_step"),
    SpriteSpec(120, 0, "prayer_guard"),
    SpriteSpec(130, 0, "prayer_guard"),
    SpriteSpec(131, 0, "prayer_guard"),
    SpriteSpec(132, 0, "prayer_guard"),
    SpriteSpec(140, 0, "crouch"),
    SpriteSpec(150, 0, "hit_high", 0.90),
    SpriteSpec(151, 0, "hit_recoil", 0.90),
    SpriteSpec(152, 0, "hit_high", 0.90),
    SpriteSpec(154, 0, "hit_recoil", 0.90),
    SpriteSpec(170, 0, "ko"),
    SpriteSpec(175, 0, "jacket_alt_idle"),
    SpriteSpec(190, 0, "jacket_alt_idle"),
    SpriteSpec(200, 0, "stand_lp"),
    SpriteSpec(210, 0, "stand_hp"),
    SpriteSpec(230, 0, "stand_lk"),
    SpriteSpec(240, 0, "stand_hk", 0.88),
    SpriteSpec(400, 0, "crouch"),
    SpriteSpec(410, 0, "stand_hp"),
    SpriteSpec(430, 0, "crouch"),
    SpriteSpec(440, 0, "stand_hk", 0.88),
    SpriteSpec(600, 0, "jump_neutral", 0.88),
    SpriteSpec(610, 0, "crane_anti_air", 0.88),
    SpriteSpec(630, 0, "jump_neutral", 0.88),
    SpriteSpec(640, 0, "crane_anti_air", 0.88),
    SpriteSpec(900, 0, "jacket_alt_idle"),
    SpriteSpec(1000, 0, "black_tiger_palm"),
    SpriteSpec(1100, 0, "crane_anti_air", 0.88),
    SpriteSpec(1200, 0, "prayer_guard"),
    SpriteSpec(1210, 0, "prayer_counter"),
    SpriteSpec(1300, 0, "sidewalk_step"),
    SpriteSpec(1400, 0, "tiger_roar_start"),
    SpriteSpec(1400, 1, "tiger_roar_charge"),
    SpriteSpec(1400, 2, "prayer_counter"),
    SpriteSpec(1400, 3, "tiger_roar_projectile"),
    SpriteSpec(5000, 0, "hit_high", 0.90),
    SpriteSpec(5001, 0, "hit_recoil", 0.90),
    SpriteSpec(5002, 0, "hit_recoil", 0.90),
    SpriteSpec(5010, 0, "hit_high", 0.90),
    SpriteSpec(5011, 0, "hit_recoil", 0.90),
    SpriteSpec(5012, 0, "hit_recoil", 0.90),
    SpriteSpec(5020, 0, "hit_recoil", 0.90),
    SpriteSpec(5021, 0, "hit_recoil", 0.90),
    SpriteSpec(5022, 0, "hit_recoil", 0.90),
    SpriteSpec(5030, 0, "hit_recoil", 0.90),
    SpriteSpec(5035, 0, "knockdown"),
    SpriteSpec(5040, 0, "knockdown"),
    SpriteSpec(5050, 0, "hit_recoil", 0.90),
    SpriteSpec(5060, 0, "knockdown"),
    SpriteSpec(5070, 0, "knockdown"),
    SpriteSpec(5080, 0, "knockdown"),
    SpriteSpec(5100, 0, "knockdown"),
    SpriteSpec(5101, 0, "knockdown"),
    SpriteSpec(5110, 0, "knockdown"),
    SpriteSpec(5120, 0, "idle_00"),
    SpriteSpec(5150, 0, "ko"),
    SpriteSpec(5200, 0, "idle_00"),
    SpriteSpec(5210, 0, "idle_00"),
    SpriteSpec(5300, 0, "jacket_alt_idle"),
    SpriteSpec(9000, 0, "portrait_neutral", 0.96),
    SpriteSpec(9000, 1, "portrait_tiger_roar", 0.96),
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


def write_air(path: Path) -> None:
    chunks = [
        "; Mestre Thaynan WIP animation file",
        action(0, [(0, 0, 8), (0, 1, 8), (0, 2, 8), (0, 3, 8)]),
        action(5, [(5, 0, 4)]),
        action(6, [(6, 0, 4)]),
        action(10, [(10, 0, 4)]),
        action(11, [(11, 0, 6)]),
        action(12, [(12, 0, 4)]),
        action(20, [(20, 0, 5), (20, 1, 5), (20, 2, 5), (20, 3, 5)]),
        action(21, [(21, 0, 5), (21, 1, 5), (21, 2, 5), (21, 3, 5)]),
        action(40, [(40, 0, 4)]),
        action(41, [(41, 0, 6)]),
        action(42, [(42, 0, 6)]),
        action(43, [(43, 0, 6)]),
        action(44, [(44, 0, 6)]),
        action(47, [(47, 0, 3)]),
        action(100, [(100, 0, 4), (100, 1, 4), (100, 2, 4), (100, 3, 4)]),
        action(105, [(105, 0, 8)]),
        action(120, [(120, 0, 8)]),
        action(130, [(130, 0, 8)]),
        action(131, [(131, 0, 8)]),
        action(132, [(132, 0, 8)]),
        action(140, [(140, 0, 8)]),
        action(150, [(150, 0, 4)]),
        action(151, [(151, 0, 4)]),
        action(152, [(152, 0, 4)]),
        action(154, [(154, 0, 4)]),
        action(170, [(170, 0, 60)]),
        action(175, [(175, 0, 60)]),
        action(190, [(190, 0, 60)]),
        action(200, [(200, 0, 8)], "10,-65, 55,-40"),
        action(210, [(210, 0, 12)], "12,-78, 62,-43"),
        action(230, [(230, 0, 8)], "12,-25, 45,-5"),
        action(240, [(240, 0, 14)], "10,-75, 70,-24"),
        action(400, [(400, 0, 8)], "10,-42, 48,-8"),
        action(410, [(410, 0, 12)], "10,-70, 58,-35"),
        action(430, [(430, 0, 8)], "8,-24, 48,-4"),
        action(440, [(440, 0, 14)], "10,-58, 70,-15"),
        action(600, [(600, 0, 8)], "8,-70, 42,-35"),
        action(610, [(610, 0, 12)], "8,-80, 70,-28"),
        action(630, [(630, 0, 8)], "8,-60, 42,-20"),
        action(640, [(640, 0, 12)], "8,-78, 72,-24"),
        action(900, [(900, 0, 40)]),
        action(1000, [(1000, 0, 16)], "15,-70, 70,-35"),
        action(1100, [(1100, 0, 18)], "8,-90, 72,-26"),
        action(1200, [(1200, 0, 18)]),
        action(1210, [(1210, 0, 18)], "10,-75, 76,-20"),
        action(1300, [(1300, 0, 14)]),
        action(1400, [(1400, 0, 8), (1400, 1, 8), (1400, 2, 10), (1400, 3, 12)], "18,-75, 92,-20"),
    ]
    for anim in [5000, 5010, 5020, 5030, 5050]:
        chunks.append(action(anim, [(anim, 0, 6)]))
        chunks.append(action(anim + 1, [(anim if anim != 5030 else 5001, 0, 6)]))
        chunks.append(action(anim + 2, [(anim if anim != 5030 else 5001, 0, 6)]))
    chunks.extend(
        [
            action(5035, [(5035, 0, 12)]),
            action(5040, [(5040, 0, 12)]),
            action(5060, [(5060, 0, 12)]),
            action(5070, [(5070, 0, 12)]),
            action(5080, [(5080, 0, 12)]),
            action(5100, [(5100, 0, 12)]),
            action(5101, [(5101, 0, 12)]),
            action(5110, [(5110, 0, 12)]),
            action(5120, [(5120, 0, 12)]),
            action(5150, [(5150, 0, 60)]),
            action(5200, [(5200, 0, 12)]),
            action(5210, [(5210, 0, 12)]),
            action(5300, [(5300, 0, 60)]),
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
sprite  = ../kfm/kfm.sff
anim    = ../kfm/kfm.air

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

; ---------------------------------------------------------------------------
; Specials

[Statedef 1000]
type = S
movetype = A
physics = S
anim = 1000
ctrl = 0
velset = 0,0
sprpriority = 2

[State 1000, Hit]
type = HitDef
trigger1 = Time = 4
attr = S, SA
damage = 92, 10
animtype = Hard
guardflag = MA
hitflag = MAF
priority = 4, Hit
pausetime = 12,12
sparkno = -1
guard.sparkno = -1
hitsound = -1
guardsound = -1
ground.type = High
ground.slidetime = 15
ground.hittime = 18
ground.velocity = -6
air.velocity = -3,-5

[State 1000, End]
type = ChangeState
trigger1 = AnimTime = 0
value = 0
ctrl = 1

[Statedef 1100]
type = S
movetype = A
physics = S
anim = 1100
ctrl = 0
velset = 0,0
sprpriority = 2

[State 1100, Hit]
type = HitDef
trigger1 = Time = 3
attr = S, SA
damage = 84, 8
animtype = Up
guardflag = MA
hitflag = MAF
priority = 4, Hit
pausetime = 10,10
sparkno = -1
guard.sparkno = -1
hitsound = -1
guardsound = -1
ground.type = High
ground.slidetime = 8
ground.hittime = 16
ground.velocity = -2,-7
air.velocity = -2,-7
fall = 1

[State 1100, End]
type = ChangeState
trigger1 = AnimTime = 0
value = 0
ctrl = 1

[Statedef 1200]
type = S
movetype = I
physics = S
anim = 1200
ctrl = 0
velset = 0,0
sprpriority = 2

[State 1200, CounterWindow]
type = HitOverride
trigger1 = Time < 16
attr = SCA, NA, SA
slot = 0
stateno = 1210
time = 1

[State 1200, End]
type = ChangeState
trigger1 = AnimTime = 0
value = 0
ctrl = 1

[Statedef 1210]
type = S
movetype = A
physics = S
anim = 1210
ctrl = 0
velset = 0,0
sprpriority = 2

[State 1210, Hit]
type = HitDef
trigger1 = Time = 2
attr = S, SA
damage = 110, 10
animtype = Hard
guardflag = MA
hitflag = MAF
priority = 5, Hit
pausetime = 12,12
sparkno = -1
guard.sparkno = -1
hitsound = -1
guardsound = -1
ground.type = High
ground.slidetime = 14
ground.hittime = 20
ground.velocity = -7
air.velocity = -3,-6

[State 1210, End]
type = ChangeState
trigger1 = AnimTime = 0
value = 0
ctrl = 1

[Statedef 1300]
type = S
movetype = I
physics = S
anim = 1300
ctrl = 0
velset = 3.4,0
sprpriority = 2

[State 1300, End]
type = ChangeState
trigger1 = AnimTime = 0
value = 0
ctrl = 1

[Statedef 1400]
type = S
movetype = A
physics = S
anim = 1400
ctrl = 0
velset = 0,0
sprpriority = 2

[State 1400, Hit]
type = HitDef
trigger1 = Time = 12
attr = S, SA
damage = 130, 14
animtype = Hard
guardflag = MA
hitflag = MAF
priority = 5, Hit
pausetime = 14,14
sparkno = -1
guard.sparkno = -1
hitsound = -1
guardsound = -1
ground.type = High
ground.slidetime = 16
ground.hittime = 22
ground.velocity = -8
air.velocity = -4,-6

[State 1400, End]
type = ChangeState
trigger1 = AnimTime = 0
value = 0
ctrl = 1
"""


CMD = """; Mestre Thaynan WIP command file

[Command]
name = "QCF_x"
command = ~D, DF, F, x
time = 15

[Command]
name = "QCF_y"
command = ~D, DF, F, y
time = 15

[Command]
name = "DP_x"
command = ~F, D, DF, x
time = 15

[Command]
name = "DP_y"
command = ~F, D, DF, y
time = 15

[Command]
name = "QCB_x"
command = ~D, DB, B, x
time = 15

[Command]
name = "QCB_y"
command = ~D, DB, B, y
time = 15

[Command]
name = "QCF_a"
command = ~D, DF, F, a
time = 15

[Command]
name = "QCF_b"
command = ~D, DF, F, b
time = 15

[Command]
name = "QCB_a"
command = ~D, DB, B, a
time = 15

[Command]
name = "QCB_b"
command = ~D, DB, B, b
time = 15

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

[State -1, Black Tiger Palm]
type = ChangeState
value = 1000
triggerall = command = "QCF_x" || command = "QCF_y"
triggerall = statetype = S
triggerall = ctrl
trigger1 = 1

[State -1, Crane Anti-Air]
type = ChangeState
value = 1100
triggerall = command = "DP_x" || command = "DP_y"
triggerall = statetype = S
triggerall = ctrl
trigger1 = 1

[State -1, Prayer Guard]
type = ChangeState
value = 1200
triggerall = command = "QCB_x" || command = "QCB_y"
triggerall = statetype = S
triggerall = ctrl
trigger1 = 1

[State -1, Sidewalk Step]
type = ChangeState
value = 1300
triggerall = command = "QCF_a" || command = "QCF_b"
triggerall = statetype = S
triggerall = ctrl
trigger1 = 1

[State -1, Tiger Roar]
type = ChangeState
value = 1400
triggerall = command = "QCB_a" || command = "QCB_b"
triggerall = statetype = S
triggerall = ctrl
trigger1 = 1

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

This is a temporary playable placeholder using KFM's known-good SFF/AIR files
as a base while Mestre Thaynan's reference-extracted sprites are prepared for a
proper SprMake2 build.

What works:
- Selection via data/select.def
- Selection via data/select.def without loading the broken experimental SFF
- Idle, walk, jump, crouch using KFM base animations
- Four basic buttons: x/y punches, a/b kicks
- QCF+P: Black Tiger Palm
- DP+P: Crane Anti-Air
- QCB+P: Prayer Guard counter stance
- QCF+K: Sidewalk Step
- QCB+K: Tiger Roar test attack

Known limitations:
- This is not a final balanced character.
- Visuals are temporarily KFM until Mestre's official SFF is built.
- Mestre's extracted source frames remain in assets/mestre_thaynan/sprites/.
- No custom sounds are included yet.
- Hitboxes are broad temporary boxes for local testing only.
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
