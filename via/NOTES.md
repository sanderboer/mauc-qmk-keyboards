# VIA – notitie (TODO later)

## Status
- Firmware op alle 6 boards heeft `VIA_ENABLE = yes` en bouwt schoon (`qmk lint` ok).
- Unieke PID per board: absolem `0x0000`, yask `0x0001`, chonky `0x0002`,
  box_o_alps `0x0003`, stm32f4x1 `0x0004`, signum `0x0005` (alle `0xFEED`).
- `dynamic_keymap.layer_count = 6` (5 lagen in gebruik + 1 reserve).
- VIA-app ziet de boards wel (naam + VID/PID), maar definitie laden faalt.

## Fout in VIA-app
- Eerst: "Fetching v3 definition failed" (logisch: custom board staat niet
  in VIA's centrale repo).
- Daarna: handmatig laden van `via/*.json` via Design-tab ("Load Draft
  Definition") geeft errors.

## Wat al geprobeerd / vastgesteld
- Firmware spreekt VIA-protocol `0x000D` (13) → VIA eist een **V3-definitie**.
- JSONs zijn omgezet naar V3: `"lighting"` eruit, absolem heeft
  `"menus": ["qmk_rgblight"]` + `"keycodes": ["qmk_rgblight_keycodes"]`,
  de rest heeft geen `menus`. `firmwareVersion` weggelaten (= default 0).
- Toch nog load-errors in de app. Exacte melding onbekend – bij oppakken
  eerst de letterlijke foutmelding uit VIA noteren.

## Hypotheses om te checken
1. V3-schema eist meer velden of andere `keymap`-entry-vorm dan `"r,c"`-strings.
   Vergelijk met een werkende V3-definitie uit
   https://github.com/the-via/keyboards/tree/master/v3
   (formaat + verplichte velden checken tegen
   https://www.caniusevia.com/docs/specification).
2. `menus` weglaten vs lege lijst – testen wat de Design-tab accepteert.
3. `"keycodes"`-module weglaten bij absolem en kijken of de basisdefinitie
   dan wel laadt (stap voor stap opbouwen).
4. Check of het aan de app-versie ligt (desktop vs usevia.app, V2-toggle
   "Use V2 definitions" staat er nog als fallback).

## Officiële weg (als sideloaden blijft falen of voor auto-herkenning)
Vereist volgens https://github.com/the-via/keyboards:
1. Keyboard-source gemerged in upstream `qmk/qmk_firmware` master
   (grootste stap: QMK-review per board).
2. `keymaps/via` keymap gemerged in `the-via/qmk_userspace_via` main
   (wij hebben nu alleen `keymaps/default`).
3. Definitie-PR naar `the-via/keyboards` master:
   `v3/<vendor>/<board>/<board>.json` (onze `via/*.json` zijn daarvoor
   de basis, na V3-fix).

## Niet vergeten
- L+U-posities op de base-laag met rust laten in VIA (anders breekt de
  L+U → Scroll-Lock-combo; combos blijven firmware-only).
- Linux: `sudo ./util/install_udev.sh` in `~/qmk_firmware` voor
  browser/app-toegang tot het board.
