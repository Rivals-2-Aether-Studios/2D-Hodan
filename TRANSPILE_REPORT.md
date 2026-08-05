# R1 → R2 Transpile Report — Hodan

- **Author:** team NeRVe
- **Source version:** 3.4
- **Mod ID (R2):** 3752556104
- **Class name:** `Hodan2`

## Pipeline summary

- 0 GML scripts transpiled
- 2131 top-level statements emitted from 44117 tokens
- 0 emitter warnings (see below)

## Files emitted

| Source | Output |
|---|---|

## Emitter warnings

None.

## Known gaps (manual review)

- **Drawing**: pre_draw / post_draw (and other_pre_draw / other_post_draw)
  ARE wired — they run each frame via the entry point's RunDrawChunks
  (drained by the Lua2D entity's EndFrame into replicated draw slots).
  css_draw / draw_hud remain unwired (no R2 Lua path for UI draws).
- **AI**: ai_init / ai_update — emitted but not wired (Tier 4 deferred).
- **Runes**: `has_rune(...)` always returns `false`; rune-gated branches
  are dead code unless the modder reimplements as R2 attribute checks.
- **Charge / multi-tier projectiles**: R1 mods often layer charge state
  on top of base projectiles. Transpiled logic preserves the GML, but
  the underlying engine seam (engine reading from r1_state) is still
  Phase 3+ work. See `R1Compat/README.md`.

## Next manual steps

1. Run `unrealtool run assets_import.py` from the output directory to
   import textures, sprites, flipbooks, sounds, and stamp the
   character data assets into the editor.
2. Open the editor, find `Char_Hodan2` under
   `Game/ModContent/3752556104/UnrealAssets/`, and verify the wiring.
3. PIE-spawn and walk through the smoke checklist (see `R1Compat/README.md`).
