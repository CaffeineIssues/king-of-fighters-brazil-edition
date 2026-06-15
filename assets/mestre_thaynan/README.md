# Mestre Thaynan Sprite Source Pass

This folder contains the first reference-based sprite source pass for Mestre
Thaynan.

The extracted frames feed the official SprMake2 SFF build used by the temporary
playable test character under `chars/mestre_thaynan/`. After changing these
frames, rebuild `chars/mestre_thaynan/mestre_thaynan.sff` with SprMake2 before
testing.

## Contents

- `sprites/*.png` - transparent RGBA source frames for review and paintover.
- `sprites/pcx/*.pcx` - indexed 256-color frames for future SFF import.
- `sprites/mestre_thaynan_sprite_sheet_preview.png` - labeled contact sheet.
- `sprites/palette_strip.png` - current working palette.
- `reference/black_tiger_maestro_reference_v2.png` - current visual reference
  sheet.
- `reference/black_tiger_maestro_reference.jpg` - previous visual reference
  sheet kept for comparison.
- `tools/generate_mestre_thaynan_sprites.py` - reproducible reference-sheet
  extractor.

## Frame Set

The extracted pass includes:

- Idle loop: `idle_00` through `idle_03`
- Prayer guard: `prayer_guard`
- Walk cycle: `walk_00` through `walk_03`
- Low stance / crouch: `crouch`
- Jump neutral: `jump_neutral`
- Standing normals: `stand_lp`, `stand_hp`, `stand_lk`, `stand_hk` from the
  updated rapid-punch and crane-kick rows (`black_tiger_palm` is also mapped to
  the heavy punch SFF slot for a stronger current test attack).
- Specials: `black_tiger_palm`, `crane_anti_air`, `prayer_counter`,
  `sidewalk_step`, `tiger_roar_start`, `tiger_roar_charge`,
  `tiger_roar_projectile`
- Reactions and KO poses: `hit_high`, `hit_recoil`, `knockdown`, `ko`
- Portrait references: `portrait_neutral`, `portrait_tiger_roar`
- MUGEN portrait slots: `portrait_small` for sprite `9000,0` at 25x25 and
  `portrait_big` for sprite `9000,1` at 120x140
- Costume/stance reference: `jacket_alt_idle`

## Visual Direction

The design follows the provided Black Tiger Maestro sprite sheet:

- Long center-parted dark gray hair.
- Rectangular glasses.
- Lean older martial artist build.
- Navy track jacket with yellow sleeve stripes.
- Light Black Tiger shirt.
- Loose dark pants and black shoes.
- Tiger Roar special effect identity.

## MUGEN Import Notes

The PCX files use palette index 0 as the transparent key color. The extractor
removes edge-connected sheet background, light JPEG fringe, and detached crop
artifacts from normal character frames. They are reference-derived source
frames, not final cropped production frames. Before packaging into SFF:

1. Hand-clean JPEG artifacts around outlines and effects.
2. Normalize sprite axes and foot placement.
3. Add in-betweens for idle, walk, normals, and specials.
4. Crop each frame consistently around the axis.
5. Confirm shared palette behavior across all frames.
6. Build the `.air` animation timings.
7. Import into SFF with the final palette order.

## Current Limitations

- This is an extracted first pass from a compressed JPG sheet, not final
  production pixel art.
- Animations need more in-between frames for KOF-level fluidity.
- Hitboxes, hurtboxes, CLSN boxes, sound, and CNS behavior are not implemented.
- Facial likeness, shirt details, tiger effects, and jacket highlights need
  manual pixel cleanup.
