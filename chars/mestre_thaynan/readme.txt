Mestre Thaynan WIP Playable Test
================================

This is a temporary playable placeholder using Mestre Thaynan's generated
SFF/AIR files.

What works:
- Selection via data/select.def
- Loads using mestre_thaynan.sff and mestre_thaynan.air
- Idle, walk, jump, crouch using the current extracted Mestre frames
- Four basic buttons: x/y punches, a/b kicks
- QCF+P: Black Tiger Palm
- DP+P: Crane Anti-Air
- QCB+P: Prayer Guard counter stance
- QCF+K: Sidewalk Step
- QCB+K: Tiger Roar test attack

Known limitations:
- This is not a final balanced character.
- Requires mestre_thaynan.sff to be rebuilt with SprMake2 after sprite changes.
  The SFF binary may be absent from source-control changes when it would contain
  stale sprites from an older reference sheet.
- Mestre's extracted source frames remain in assets/mestre_thaynan/sprites/.
- No custom sounds are included yet.
- Hitboxes are broad temporary boxes for local testing only.

To build Mestre's own SFF with the official Windows tool:
  sprmake2.exe chars\mestre_thaynan\mestre_thaynan-sff.def

Portrait note:
- 9000,0 uses portrait_small.pcx at 25x25 for the select-grid icon.
- 9000,1 uses portrait_big.pcx at 120x140 for the large portrait slot.

After sprite extraction changes, rebuild the SFF before testing.
