howto tl;dr

symlink the dirs in `keyboards/` in this repo into the `keyboards/` dir of the "real" qmk repo:

    ln -s /Raid/Projects/Github/mauc-qmk/keyboards/<name> ~/qmk_firmware/keyboards/<name>

install the conda env from this repo, then activate it:

    conda env update -f environment.yml
    conda activate qmk

to build/flash the keebs, go into the real repo root and do:

    qmk compile -kb yask_bois -km default
    qmk flash   -kb yask_bois -km default -bl uf2-split-left
    qmk flash   -kb yask_bois -km default -bl uf2-split-right

    qmk compile -kb chonky_bois -km default
    qmk flash   -kb chonky_bois -km default -bl avrdude-split-left
    qmk flash   -kb chonky_bois -km default -bl avrdude-split-right

    qmk compile -kb box_o_alps -km default
    qmk flash   -kb box_o_alps -km default -bl avrdude

    qmk compile -kb box_o_alps_stm32f4x1 -km default
    qmk flash   -kb box_o_alps_stm32f4x1 -km default -bl dfu-util

    qmk compile -kb absolem_mauc -km default
    qmk flash   -kb absolem_mauc -km default -bl dfu

    qmk compile -kb signum_absolem -km default
    qmk flash   -kb signum_absolem -km default -bl dfu

VIA live remapping
------------------
All keymaps have VIA_ENABLE, so after flashing once you can remap keys
without recompiling. Each keyboard has a unique PID (0x0000-0x0005).

1. Linux needs udev rules once (also fixes the qmk doctor warning):
       cd ~/qmk_firmware && sudo ./util/install_udev.sh
2. Open the VIA app (or https://usevia.com in Chromium) and connect the board.
3. Load the matching draft definition from via/<name>.json
   (Settings tab -> Show Design tab -> Load Draft Definition).
4. Remap away. Do NOT remap the L and U positions on the base layer,
   that breaks the L+U -> Scroll Lock combo (combos stay firmware-only,
   VIA cannot edit them).

EEPROM vs firmware (read this when a reflash "does nothing")
------------------------------------------------------------
On first boot VIA copies the firmware keymap into EEPROM and from then
on the EEPROM copy wins. So after `qmk flash`, if the old key is still
there (e.g. `/` instead of ScrollLock), the firmware is fine — the
stale EEPROM shadow is the problem. Fix:

1. Press the EEPROM-clear key in the `_MISC` layer (`QK_CLEAR_EEPROM`,
   next to `QK_BOOT`), or VIA Settings -> Reset EEPROM.
2. Unplug/replug.
3. On splits (yask_bois, chonky_bois): reflash BOTH halves afterwards,
   because clearing wipes the `EE_HANDS` handedness with it
   (`uf2-split-left` + `uf2-split-right`, or both `avrdude-split-*`).

   Same procedure after changing `layer_count`: it reshapes the EEPROM
   layout, so a clear + both-halves reflash is required for it to take
   effect.
