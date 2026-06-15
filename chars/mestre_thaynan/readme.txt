Mestre Thaynan WIP Playable Test
================================

This is a temporary playable placeholder using KFM's known-good SFF/AIR files
as a base while Mestre Thaynan's reference-extracted sprites are prepared for a
proper SprMake2 build.

What works:
- Selection via data/select.def
- Loads using KFM's known-good SFF/AIR files instead of the broken experimental SFF
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

To build Mestre's own SFF later with the official Windows tool:
  sprmake2.exe chars\mestre_thaynan\mestre_thaynan-sff.def

After that succeeds, switch mestre_thaynan.def back to:
  sprite  = mestre_thaynan.sff
  anim    = mestre_thaynan.air
