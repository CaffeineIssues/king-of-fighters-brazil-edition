Mestre Thaynan WIP Playable Test
================================

This is a restart pass using only the simplified reference sheet.

What works:
- Selection via data/select.def
- Loads using mestre_thaynan.sff and mestre_thaynan.air
- Idle and walk frames from the sheet
- Light punch on x
- High kick on b
- Standing/idle frames as required fallback and hurt placeholders

Known limitations:
- This is not a final balanced character.
- No special moves until matching sprite art exists.
- No custom sounds are included yet.
- Hitboxes are broad temporary boxes for local testing only.
- Rebuild mestre_thaynan.sff with SprMake2 after sprite changes.

To build the SFF with the official Windows tool:
  sprmake2.exe chars\mestre_thaynan\mestre_thaynan-sff.def
