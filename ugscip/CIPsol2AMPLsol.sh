#!/bin/bash
# Run 
# $ CIPsol2AMPLsol.sh <solution in CIP format> <NL-file>
echo "read $1 q" | scip $2 -AMPL -i

