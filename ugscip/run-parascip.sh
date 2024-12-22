#!/bin/bash
set -e
NAME=$(dirname $1)/$(basename $1 .nl)
BASE=$(basename $1 .nl)
NPROC=$2
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
PART=""
if [[ "$SLURM_DEF_PART" != "" ]]; then
    PART="-p $SLURM_DEF_PART"
fi
JOBID=$(sbatch $PART -n $NPROC --wrap="mpirun parascip ug.set $BASE.conv.cip $INITSOL $LC_SET $ROOT_SET $SOLVER_SET" | awk '/Submitted batch job/ { print $4 }')
while true
do
    STATUS=$(scontrol show job $JOBID | awk '/JobState=/ { print $1 }')
    if [[ "$STATUS" == "JobState=COMPLETED" ]]; then
        break
    fi
    #echo $STATUS
    sleep 1
done
#salloc $PART -n $NPROC mpirun parascip_port ug.set $BASE.conv.cip $INITSOL $LC_SET $ROOT_SET $SOLVER_SET
#mpirun parascip parascip.set $BASE.conv.cip
sed -i '/Final Solution/d' $BASE.conv.sol
echo "read $BASE.conv.sol q" | scip $NAME -AMPL -i
