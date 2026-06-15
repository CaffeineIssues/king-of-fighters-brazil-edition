# Brazilian Meme Fighters

Brazilian Meme Fighters is a MUGEN / IKEMEN GO fighting game concept that
reimagines Brazilian internet memes, viral personalities, television legends,
and social media phenomena as serious SNK-style arcade fighters.

The target is a game that feels like a lost Neo Geo release from 1998: grounded
character proportions, dense pixel shading, strong silhouettes, competitive
move design, and Brazilian cultural identity treated as the core fantasy rather
than a throwaway joke.

## Inspirations

- The King of Fighters '95
- The King of Fighters '96
- The King of Fighters '97
- The King of Fighters '98
- The King of Fighters '99
- Real Bout Fatal Fury

## Design Pillars

### 1. Authentic SNK Feel

Every asset should sit comfortably beside Kyo Kusanagi, Iori Yagami, Terry
Bogard, Leona Heidern, Kim Kaphwan, K', Ralf Jones, and Ryo Sakazaki.

Use:

- KOF 97 / KOF 98 quality pixel art
- Realistic anatomy and arcade fighter proportions
- Detailed hand-shaded sprites
- Readable silhouettes
- Fluid, snappy animation timing
- Natural, slightly restrained palettes

Avoid:

- Chibi proportions
- HD art or AI-upscaled art
- Modern anime rendering
- Neon-heavy palettes
- Low-effort meme cutouts
- Joke-only move kits

### 2. Competitive Gameplay

Every fighter must have a coherent archetype, a real neutral plan, weaknesses,
and viable combo routes.

Supported archetypes:

- Rushdown
- Grappler
- Zoner
- Balanced
- Counter Fighter
- Technical Fighter
- Rekka Specialist
- Charge Character
- Trickster / Setplay Fighter

Even the funniest source material should become a believable fighting game
character with clear decision-making.

### 3. Brazilian Identity

The roster and stages should celebrate Brazilian internet and popular culture
without flattening it into parody.

Reference pools:

- Viral videos
- Social media legends
- Television personalities
- Regional memes
- Internet folklore
- Football culture
- Street culture
- Music scenes including samba, pagode, axe, forro, and funk carioca

## Core Controls

Brazilian Meme Fighters uses a classic KOF four-button layout.

| Button | Action |
| --- | --- |
| LP | Light Punch |
| HP | Heavy Punch |
| LK | Light Kick |
| HK | Heavy Kick |

## Movement Rules

Movement is based primarily on KOF '98:

- Walk
- Dash
- Backdash
- Run
- Roll
- Hop
- Hyper Hop
- Super Jump

Hops and hyper hops are key to offense and anti-zoning. Rolls should be useful
for reads and guard cancels without invalidating neutral.

## Meter Rules

The game uses a three-stock power meter.

Meter is gained by:

- Landing attacks
- Having attacks blocked
- Taking damage
- Advancing or maintaining pressure

Meter is spent on:

- Super Moves
- MAX Supers
- Guard Cancel actions

## Combo Philosophy

Each character should support:

- Simple confirm routes for new players
- Strong grounded routes for practical play
- Corner routes with positional reward
- Metered routes for high damage
- Character-specific expression

Avoid:

- Infinite combos
- Excessive hit stun loops
- Meter-positive loops
- Routes that make command throws or projectiles inescapable by default

## Sprite Standards

Target standing sprite height: 80-110 pixels.

Minimum animation set:

- Idle
- Walk forward
- Walk back
- Run
- Dash / backdash
- Jump start
- Jump ascend / descend
- Crouch
- Standing guard
- Crouching guard
- Air guard where applicable
- Light / heavy normals
- Close normals
- Far normals
- Jump normals
- Throws
- Hit reactions
- Knockdown
- Recovery
- Taunt
- Intro
- Win poses
- Special moves
- Super moves

Target production count: 300-700 frames per complete character.

## MUGEN / IKEMEN State Ranges

Use consistent state ranges across the roster.

| Range | Purpose |
| --- | --- |
| 0 | Idle |
| 5 | Turn |
| 10 | Crouch |
| 20 | Walk |
| 40 | Jump start |
| 50 | Air |
| 1000-1999 | Special moves |
| 2000-2999 | Super moves |
| 3000-3999 | MAX supers |
| 4000-4999 | Throws and unique defensive systems |
| 5000-5999 | Custom hit states and cinematic victims |
| 9000-9999 | Intros, win poses, taunts, helpers, debug states |

## Character Deliverable Checklist

Every playable character needs:

1. Character profile
2. Visual design
3. Story
4. Fighting style
5. Normal attack list
6. At least two command normals
7. At least four special moves
8. At least two super moves
9. At least one MAX super
10. Intro animation
11. Taunt
12. Victory pose A
13. Victory pose B
14. Defeat pose
15. Stage suggestion
16. MUGEN state structure
17. Animation list
18. AI behavior plan

## Content Status

This repository currently contains stock MUGEN sample content. The Brazilian
Meme Fighters material under this directory is a production design layer and
does not register unfinished characters in `data/select.def`, preventing broken
select entries until sprites, sounds, and CNS/CMD files exist.

See:

- `roster.md` for character briefs and move kits.
- `stages-and-music.md` for stage and audio direction.
- `implementation-standards.md` for MUGEN / IKEMEN authoring conventions.

## First Production Target

Mestre Thaynan is the first planned character. His roster entry establishes the
initial character standard for reference-based visual translation, complete move
design, state planning, and AI behavior.
