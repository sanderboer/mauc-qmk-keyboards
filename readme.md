howto tl;dr

ln -s the dirs in keyboards in this repo in the keyboards dir of the "real" qmk repo.
install the conda env from this repo.
activate it:
conda activate qmk

to build the keebs go into the real repo root and do:
qmk clean && qmk flash -kb yask_bois -km default -bl uf2-split-left
qmk clean && qmk flash -kb yask_bois -km default -bl uf2-split-right

qmk flash -kb chonky_bois -km default -bl avrdude-split-left
qmk flash -kb chonky_bois -km default -bl avrdude-split-right

make box_o_alps_stm32f4x1:default:dfu-util
