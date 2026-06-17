He-man do Sertao WIP Test
=========================

This is a minimal idle-only test character.

What works:
- Selection via data/select.def
- Two-frame idle loop
- Required movement/hurt states reuse the idle frames as placeholders

Known limitations:
- No attacks yet.
- No custom sounds yet.
- Rebuild he_man_do_sertao.sff with SprMake2 after sprite changes.

Build:
  sprmake2.exe chars\he_man_do_sertao\he_man_do_sertao-sff.def
