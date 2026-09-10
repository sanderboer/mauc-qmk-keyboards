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
