#!/bin/bash
# echo "write problem $1.cip quit" | scipampl $1.nl -i
echo "write problem $1.cip write solution $1.cip.init.sol quit" | scipampl $1.nl -i

