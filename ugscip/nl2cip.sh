#!/bin/bash
echo "write problem $1.cip quit" | scip $1 -AMPL -i

