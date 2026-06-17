# Praça dos Eucaliptos (Tianguá) Stage Source

Source assets for the MUGEN stage `stages/praca_dos_eucaliptos_tiangua.def`.

## Files

- `reference.png` - original linked reference image.
- `clean_full.png` - full-size cleaned image with the Gemini logo removed.
- `../../stages/praca_dos_eucaliptos_tiangua_source.png` - RGB stage source.
- `../../stages/praca_dos_eucaliptos_tiangua_source_8bit.png` - indexed source
  used by SprMake2.

## Build

From the repository root on Windows:

```bat
sprmake2.exe stages\praca_dos_eucaliptos_tiangua-sff.def
```

This creates:

```text
stages/praca_dos_eucaliptos_tiangua.sff
```
