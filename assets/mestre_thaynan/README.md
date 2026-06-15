# Mestre Thaynan Sprite Source Pass

This folder contains the first sprite source pass for Mestre Thaynan.

The frames are intentionally not registered in `data/select.def` yet because
the character does not have complete `.def`, `.cmd`, `.cns`, `.air`, `.sff`, and
`.snd` files.

## Contents

- `sprites/*.png` - transparent RGBA source frames for review and paintover.
- `sprites/pcx/*.pcx` - indexed 256-color frames for future SFF import.
- `sprites/mestre_thaynan_sprite_sheet_preview.png` - labeled contact sheet.
- `sprites/palette_strip.png` - current working palette.
- `tools/generate_mestre_thaynan_sprites.py` - reproducible source generator.

## Frame Set

The first pass includes:

- Idle loop: `idle_00` through `idle_03`
- Prayer guard: `prayer_guard`
- Walk cycle: `walk_00` through `walk_03`
- Crouch: `crouch`
- Jump neutral: `jump_neutral`
- Standing normals: `stand_lp`, `stand_hp`, `stand_lk`, `stand_hk`
- Specials: `black_tiger_palm`, `crane_anti_air`, `prayer_counter`,
  `sidewalk_step`
- Reactions and extra poses: `hit_high`, `win_bow`, `jacket_alt_idle`

## Visual Direction

The design follows the reference images:

- Long center-parted dark gray hair.
- Rectangular glasses.
- Lean older martial artist build.
- Sleeveless black kung fu shirt with white markings.
- Loose dark pants and black shoes.
- Pale neck cord / towel accent.
- Alternate navy jacket and white Black Tiger shirt costume.

## MUGEN Import Notes

The PCX files use palette index 0 as the transparent key color. They are source
frames, not final cropped production frames. Before packaging into SFF:

1. Hand-clean silhouettes and facial pixels.
2. Add in-betweens for walk, normals, and specials.
3. Crop each frame consistently around the axis.
4. Confirm shared palette behavior across all frames.
5. Build the `.air` animation timings.
6. Import into SFF with the final palette order.

## Current Limitations

- This is a generated first pass, not final production pixel art.
- Animations need more in-between frames for KOF-level fluidity.
- Hitboxes, hurtboxes, CLSN boxes, sound, and CNS behavior are not implemented.
- Facial likeness and embroidered shirt details need manual pixel cleanup.
