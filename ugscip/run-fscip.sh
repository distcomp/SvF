#!/bin/bash
set -e
NAME=$(dirname $1)/$(basename $1 .nl)
BASE=$(basename $1 .nl)
NUM_TH=$2
echo "write problem $BASE.conv.cip write solution $BASE.cip.init.sol quit" | scip $NAME -AMPL -i
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
    ROOT_SET='-sr root.set'
fi
SOLVER_SET=''
if [ -f scip.set ]; then
    SOLVER_SET='-s scip.set'
fi
touch ug.set
fscip ug.set $BASE.conv.cip $INITSOL -sth $NUM_TH $LC_SET $ROOT_SET $SOLVER_SET | tee fscip.log
sed -i '/Final Solution/d' $BASE.conv.sol
echo "read $BASE.conv.sol q" | scip $NAME -AMPL -i

STATUS=$(grep 'SCIP Status' fscip.log | awk '-F[' '{print $2}' | sed 's/\]//')
#echo "status" $STATUS
case "$STATUS" in
    "optimal solution found")
        OBJNO=0
        OBJSTAT='optimal solution found'
        ;;
    "")
        OBJNO=0
        OBJSTAT='optimal solution found'
        ;;
    "infeasible")
        OBJNO=200
        OBJSTAT='infeasible'
        ;;
    "unbounded")
        OBJNO=300
        OBJSTAT='unbounded'
        ;;
    *)
        OBJNO=400
        OBJSTAT='limit'
        ;;
esac

sed -i "s/unknown/$OBJSTAT/" $BASE.sol
sed -i "s/objno \([0-9]*\) \([0-9]*\)/objno \1 $OBJNO/" $BASE.sol
