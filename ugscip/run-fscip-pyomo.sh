#!/bin/bash
set -e

# if first arg is --version call scip
if [ "$1" == "--version" ]; then
    scip --version
    exit 0
fi

NAME=$(dirname $1)/$(basename $1 .nl)
BASE=$(basename $1 .nl)

#echo 'RUNNING WITH ' $1

# if NUM_THREADS environment variable is not set, set it to the number of cores
if [ -z "$NUM_THREADS" ]; then
    NUM_THREADS=$(nproc)
fi
echo "NUM_THREADS=$NUM_THREADS"

echo "write problem $NAME.conv.cip write solution $NAME.cip.init.sol quit" | scip $NAME -AMPL -i
if grep 'no solution available' $NAME.cip.init.sol > /dev/null; then
    INITSOL=''
    echo 'No initial solution in stub'
else
    INITSOL="-isol $NAME.cip.init.sol"
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

touch ${NAME}-ug.set
fscip ${NAME}-ug.set $NAME.conv.cip $INITSOL -sth $NUM_THREADS $LC_SET $ROOT_SET $SOLVER_SET > ${NAME}-fscip.log
mv $BASE.conv.sol $NAME.conv.sol
sed -i '/Final Solution/d' $NAME.conv.sol
echo "read $NAME.conv.sol q" | scip $NAME -AMPL -i

STATUS=$(grep 'SCIP Status' ${NAME}-fscip.log | awk '-F[' '{print $2}' | sed 's/\]//')
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

sed -i "s/unknown/$OBJSTAT/" $NAME.sol
sed -i "s/objno \([0-9]*\) \([0-9]*\)/objno \1 $OBJNO/" $NAME.sol
