Mestre Thaynan WIP Playable Test
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

To build Mestre's own SFF with the official Windows tool:
  sprmake2.exe chars\mestre_thaynan\mestre_thaynan-sff.def

Portrait note:
- 9000,0 uses portrait_small.pcx at 25x25 for the select-grid icon.
- 9000,1 uses portrait_big.pcx at 120x140 for the large portrait slot.

After the SprMake2 build succeeds, switch mestre_thaynan.def back to:
  sprite  = mestre_thaynan.sff
  anim    = mestre_thaynan.air
