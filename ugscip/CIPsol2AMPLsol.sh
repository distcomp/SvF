#!/bin/bash
# Run 
# $ CIPsol2AMPLsol.sh <solution in CIP format> <NL-file>
echo "read $1 write amplsol q" | scipampl $2 -i

