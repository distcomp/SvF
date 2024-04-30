#!/bin/bash
#export LD_LIBRARY_PATH=/s/ls4/users/sasmirnov/built/lib:/s/ls4/users/vvvoloshinov/miniconda2/x86_64-conda_cos6-linux-gnu/sysroot/lib
#export PATH=/s/ls4/users/sasmirnov/built/bin:$PATH

export OPENMP_NUM_THREADS=1
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1

hostname > $1.log.txt
# ipopt $1.nl -AMPL option_file_name=$2 2>&1 >> $1.log.txt
# Keep stderr separately
ipopt $1.nl -AMPL option_file_name=$2 >> $1.log.txt 2> $1.err.txt

