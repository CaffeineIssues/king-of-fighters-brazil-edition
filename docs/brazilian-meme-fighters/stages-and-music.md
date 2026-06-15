# Stages and Music

Stages should feel like KOF background teams built a Brazilian arcade world:
busy, readable, culturally specific, and reactive without distracting from
combat. Parallax and crowd animation should sell depth while keeping the fight
plane clean.

## Stage Art Rules

- Use 320x240 local coordinates unless a stage has a specific IKEMEN GO target.
- Keep the fight floor visually simple around player feet.
- Use two to four major parallax depth bands.
- Animate background characters in loops between 8 and 24 frames.
- Avoid oversized foreground elements that hide attacks.
- Use muted SNK palettes with strong late-1990s arcade contrast.
- Build alternate round states when possible: crowd excitement, changing lights,
  or environmental reactions after a MAX super.

## Stage Specs

### Favela Rooftop

**Time:** Sunset  
**Mood:** Warm, tense, heroic  
**Suggested Characters:** Luva de Pedreiro, rushdown team routes

#### Visual Layers

1. Distant hills and orange sky gradient.
2. Dense favela rooftops, antennas, water tanks, and hanging laundry.
3. Playable rooftop with cracked concrete, painted goal line, and loose ball.
4. Foreground low wall with subtle shadow only; no occluding objects.

#### Background Animation

- Kites crossing the sky on slow loops.
- Kids reacting to knockdowns.
- Antenna shake on heavy hits.
- Rooftop crowd jumps during supers.

#### MUGEN Notes

- Suggested `boundleft = -170`, `boundright = 170`.
- Suggested `zoffset = 200`.
- Use sparse foreground sprites to preserve character visibility.

### Feira Livre

**Time:** Morning  
**Mood:** Busy, colorful, rhythmic  
**Suggested Characters:** Caneta Azul, zoner team routes

#### Visual Layers

1. Blue morning sky and distant storefront signs.
2. Fruit stands with tarps and price boards.
3. Musicians and vendors behind the fight plane.
4. Tiled street floor with scattered leaves near edges only.

#### Background Animation

- Vendor hand gestures.
- Fruit crates wobbling on slam impacts.
- Street musician strumming loops.
- Birds briefly scatter during MAX supers.

#### MUGEN Notes

- Keep fruit colors less saturated than character palettes.
- Music should leave room for vocal-like lead instruments.

### Carnival Avenue

**Time:** Night  
**Mood:** Spectacle, motion, pressure  
**Suggested Characters:** Carreta Furacao Captain, mix-up team routes

#### Visual Layers

1. City lights and parade route banners.
2. Slow-moving floats.
3. Samba dancers behind barricades.
4. Confetti and spotlights as animated overlays.

#### Background Animation

- Timed confetti bursts.
- Float lights cycling every few seconds.
- Dancers changing pose between rounds.
- Crowd arm wave after guard crush or super finish.

#### MUGEN Notes

- Avoid full-screen confetti during active gameplay; reserve dense particles for
  round intros, KOs, and supers.
- Spotlights should be low contrast so airborne silhouettes remain readable.

### Interior Bar

**Time:** Late night  
**Mood:** Warm, cramped, nostalgic  
**Suggested Characters:** Vampeta, grappler team routes

#### Visual Layers

1. Back wall with shelves, framed football photos, and old posters.
2. CRT televisions showing looping football clips.
3. Pool tables and patrons behind the fight plane.
4. Wooden floor with scuffs and beer-stain reflections.

#### Background Animation

- TV flicker.
- Pool player pause-and-shoot loop.
- Patrons flinch when characters land nearby.
- Ceiling fan slow rotation.

#### MUGEN Notes

- Use warm browns and greens to avoid clashing with player palettes.
- Keep bar stools out of the foreground unless they are very low.

### Beach Boardwalk

**Time:** Late afternoon or night variant  
**Mood:** Breezy, open, stylish  
**Suggested Characters:** ET Bilu night variant, balanced fighters

#### Visual Layers

1. Ocean horizon and distant boats.
2. Boardwalk rails, coconut stands, and beach umbrellas.
3. Skaters and pedestrians behind the fight plane.
4. Palm shadows across pavement.

#### Background Animation

- Ocean shimmer.
- Coconut vendor idle loop.
- Skater passes once per round.
- Night variant: distant strange lights over the water for ET Bilu.

#### MUGEN Notes

- Horizontal camera can be wider than normal to emphasize open space.
- Night variant can reuse geometry with different palette and background sprites.

### LAN House 1999

**Time:** Night  
**Mood:** CRT glow, glitchy, intimate  
**Suggested Characters:** Gil Brother Away, ET Bilu, technical routes

#### Visual Layers

1. Back wall with Counter-Strike-style posters and cheap fluorescent lighting.
2. Rows of CRT monitors with looping screen animations.
3. Players at computers reacting to the match.
4. Tile floor with cable clutter kept outside the playable center.

#### Background Animation

- Monitor scanlines.
- Dial-up connection flash.
- Keyboard player rage loop on close KOs.
- Screen glitches during Gil or Bilu MAX supers.

#### MUGEN Notes

- Use additive glows sparingly; classic MUGEN palettes can posterize heavy glow.
- Keep monitor animations low-frequency to avoid visual noise.

## Music Direction

Music should sound plausible on Neo Geo-style hardware: punchy sample drums,
short loop-friendly phrases, strong bass lines, and memorable leads.

Reference energy:

- KOF 96: team identity and melodic hooks.
- KOF 97: darker atmosphere and urban percussion.
- KOF 98: clean competitive stage themes.
- Real Bout Fatal Fury: punchy grooves and brass-like stabs.

Brazilian influences:

- Samba percussion
- Pagode cavaquinho-style rhythmic leads
- Axe festival hooks
- Forro accordion-like melodies
- Funk carioca percussion patterns
- Football chant call-and-response

## Stage Theme Concepts

| Stage | Tempo | Style | Lead Sound | Notes |
| --- | --- | --- | --- | --- |
| Favela Rooftop | 150 BPM | Samba-rock fighter theme | Brass stab synth | Heroic sunset hook with crowd claps |
| Feira Livre | 138 BPM | Pagode groove | Plucked synth / cavaquinho | Light syncopation, strong bass |
| Carnival Avenue | 160 BPM | Axe / samba parade | Brass ensemble sample | High energy, loop with percussion break |
| Interior Bar | 124 BPM | Funky football bar groove | Electric organ | Warm and heavy, good for grapplers |
| Beach Boardwalk | 132 BPM | Breezy fusion | Clean guitar sample | Alternate night mix adds eerie pads |
| LAN House 1999 | 142 BPM | Breakbeat / chiptune hybrid | FM lead | CRT hum intro and glitch fills |

## Sound Effect Direction

- Hits should be dry and crunchy, closer to KOF 98 than modern anime fighters.
- Projectiles can use short tonal attacks with fast decay.
- MAX supers may add crowd samples, but they should not obscure hit confirms.
- Voice clips should be brief, iconic, and trimmed tightly for arcade cadence.
- Avoid long meme quote playback during neutral.

## Boss Presentation

Boss stages should reuse familiar locations with corrupted or heightened states:

- Ultra Instinct Luva: Favela Rooftop turns into golden stadium sunset.
- Cosmic ET Bilu: Beach Boardwalk night sky fills with geometric constellations.
- Chaos Gil Brother Away: LAN House monitors desync and show false round counts.

Boss music should introduce a darker arrangement of the character's home stage
theme rather than entirely unrelated tracks.
