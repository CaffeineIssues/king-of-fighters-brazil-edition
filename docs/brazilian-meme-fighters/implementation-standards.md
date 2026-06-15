# MUGEN / IKEMEN Implementation Standards

This document defines authoring conventions for Brazilian Meme Fighters content.
It is intentionally conservative so unfinished characters do not break the base
MUGEN install.

## Repository Policy

- Do not add a character to `data/select.def` until its `.def`, `.cmd`, `.cns`,
  `.air`, `.sff`, and `.snd` files all load successfully.
- Do not replace stock KFM content.
- Keep work-in-progress design notes under `docs/brazilian-meme-fighters/`.
- Use lowercase directory names with hyphens or underscores for new content.
- Keep character file basenames identical to their directory name.

Example future character layout:

```text
chars/luva_de_pedreiro/
  luva_de_pedreiro.def
  luva_de_pedreiro.cmd
  luva_de_pedreiro.cns
  luva_de_pedreiro.air
  luva_de_pedreiro.sff
  luva_de_pedreiro.snd
  intro.def
  ending.def
  readme.txt
```

Example future stage layout:

```text
stages/favela_rooftop.def
stages/favela_rooftop.sff
sound/favela_rooftop.ogg
```

## Character `.def` Baseline

Use this structure for future playable fighters.

```ini
; Definition file for Brazilian Meme Fighters character

[Info]
name = "Character Name"
displayname = "Character Name"
versiondate = 06,15,2026
mugenversion = 1.0
author = "Brazilian Meme Fighters Team"
pal.defaults = 1,2,3,4
localcoord = 320,240

[Files]
cmd = character_name.cmd
cns = character_name.cns
st = character_name.cns
stcommon = common1.cns
sprite = character_name.sff
anim = character_name.air
sound = character_name.snd
ai = character_name.ai

[Palette Keymap]
x = 1
y = 2
z = 3
a = 4
b = 5
c = 6

[Arcade]
intro.storyboard = intro.def
ending.storyboard = ending.def
```

## State Numbering

| Range | Use |
| --- | --- |
| 0 | Idle |
| 5 | Turn |
| 10 | Crouch |
| 20 | Walk |
| 40 | Jump start |
| 50 | Air |
| 100-199 | System movement extensions |
| 200-699 | Normal attacks |
| 700-799 | Throws |
| 800-899 | Universal defensive actions |
| 900-999 | Taunts, intros, win poses |
| 1000-1999 | Special moves |
| 2000-2999 | Super moves |
| 3000-3999 | MAX supers |
| 4000-4999 | Helpers, projectiles, traps |
| 5000-5999 | Custom hit states and cinematic victim states |
| 9000-9999 | Debug, AI helpers, compatibility states |

## Animation Numbering

Keep animation numbers aligned with state numbers when practical.

| Animation | Number |
| --- | --- |
| Stand idle | 0 |
| Turn | 5 |
| Crouch | 10 |
| Walk forward | 20 |
| Walk backward | 21 |
| Run | 100 |
| Backdash | 105 |
| Jump start | 40 |
| Jump up | 50 |
| Jump forward | 51 |
| Jump back | 52 |
| Standing LP | 200 |
| Standing HP | 210 |
| Standing LK | 230 |
| Standing HK | 240 |
| Crouching LP | 400 |
| Crouching HP | 410 |
| Crouching LK | 430 |
| Crouching HK | 440 |
| Jump LP | 600 |
| Jump HP | 610 |
| Jump LK | 630 |
| Jump HK | 640 |
| Throw attempt | 700 |
| Taunt | 900 |
| Intro | 190 |
| Win pose A | 180 |
| Win pose B | 181 |

## Command Input Standards

Use KOF-like command priority:

1. MAX supers
2. Supers
3. Command throws
4. DP motions
5. Half-circle motions
6. Quarter-circle motions
7. Command normals
8. Normal attacks

Recommended input names:

```ini
[Command]
name = "qcf_x"
command = ~D, DF, F, x
time = 15

[Command]
name = "dp_y"
command = ~F, D, DF, y
time = 15

[Command]
name = "qcf_qcf_xy"
command = ~D, DF, F, D, DF, F, x+y
time = 25
```

## Damage and Meter Targets

Baseline health: 1000.

Suggested damage bands:

- Light normal: 20-35
- Heavy normal: 55-85
- Command normal: 45-75
- Special hit: 70-120
- Meterless BnB: 180-260
- One-stock super route: 300-390
- MAX super route: 430-520
- Command grab super: 330-430, adjusted for grappler mobility

Meter gain should avoid meter-positive loops. If a combo spends meter, it should
not rebuild the same stock before the opponent returns to neutral.

## Cancel Rules

Default KOF-style chain:

```text
close normal -> command normal -> special -> super -> MAX super
```

Recommended restrictions:

- Far heavy normals cancel only when the character archetype needs it.
- Low lights can chain, but hit stun must limit repeated loops.
- Command throws should not combo from lights unless explicitly designed as a
  super or cinematic punish.
- Projectile traps should scale follow-up damage.
- Counter moves should have meaningful whiff recovery.

## AI Behavior Standards

Each character should define three broad behavior bands:

- Low AI: uses normals, basic specials, and occasional unsafe movement.
- Mid AI: confirms common routes and anti-airs obvious jumps.
- High AI: uses archetype-specific plans, meter confirms, and matchup-aware
  spacing without impossible reactions.

Boss AI may break normal limits, but it should still communicate patterns so
players can learn counterplay.

## Sprite and Palette Conventions

- Build sprites at the final intended resolution, not HD then downscaled.
- Reserve outline colors consistently across the roster.
- Keep skin, fabric, metal, and energy ramps separate.
- Target 12-24 colors per major material group when possible.
- Use palette swaps for team colors only after the base palette is readable.
- Test every sprite on dark, bright, and busy stages.

## Stage `.def` Baseline

Future stages should start from the stock `stages/kfm.def` structure and update:

```ini
[Info]
name = "Stage Name"
displayname = "Stage Name"
versiondate = 06,15,2026
mugenversion = 1.1
author = "Brazilian Meme Fighters Team"

[Camera]
startx = 0
starty = 0
boundleft = -160
boundright = 160
boundhigh = -25
boundlow = 0
verticalfollow = .2
tension = 60
zoomout = 1
zoomin = 1

[StageInfo]
zoffset = 200
autoturn = 1
resetBG = 1
localcoord = 320, 240
```

## Character Readme Template

Each completed character should include `readme.txt` with:

```text
Character:
Version:
Author:
Engine target:

Profile:
Archetype:
Game plan:
Weaknesses:

Commands:
Normals:
Command normals:
Specials:
Supers:
MAX super:

Known issues:
Credits:
```

## Playtest Checklist

Before registering a new character:

- Character loads from Training and VS modes.
- All palettes display correctly.
- No missing required animations.
- No debug flood during common movement.
- All specials obey state ranges.
- Supers consume meter and cannot trigger below required meter.
- MAX super consumes intended meter and scales combo damage.
- Throws fail correctly against airborne or invulnerable opponents.
- AI does not lock into one repeated command.
- Arcade mode can complete with the character present.
