#!/bin/bash
set -e
NAME=$(dirname $1)/$(basename $1 .nl)
BASE=$(basename $1 .nl)
NUM_TH=$2
echo "write problem $BASE.conv.cip write solution $BASE.cip.init.sol quit" | scipampl $NAME.nl -i
if grep 'no solution available' $BASE.cip.init.sol > /dev/null; then
    INITSOL=''
    echo 'No initial solution in stub'
else
    INITSOL="-isol $BASE.cip.init.sol"
fi
LC_SET=''
if [ -f presolv.set ]; then
    LC_SET='-sl presolv.set'
fi
ROOT_SET=''
if [ -f root.set ]; then
    ROOT_SET='-sl root.set'
fi
SOLVER_SET=''
if [ -f solver.set ]; then
    SOLVER_SET='-sl solver.set'
fi
touch ug.set
fscip ug.set $BASE.conv.cip $INITSOL -sth $NUM_TH $LC_SET $ROOT_SET $SOLVER_SET
sed -i '/Final Solution/d' $BASE.conv.sol
echo "read $BASE.conv.sol write amplsol q" | scipampl $NAME.nl -i
