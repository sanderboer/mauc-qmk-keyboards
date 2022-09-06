#!/bin/sh

conda env update -f environment.yml
conda activate qmk
qmk setup

#qmk compile -kb absolem_mauc -km default

