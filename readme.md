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
