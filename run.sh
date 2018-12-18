#!/bin/bash

# the -B option prevents python bytecode files from being written
if [ "-d" == "$@" ]
then
    python -B src/candyrandy.py --debug
else
    python -B src/candyrandy.py
fi