#!/bin/sh

# the -B option prevents python bytecode files from being written
if [["$@" == "--debug"]]
then
    python -B src/candyrandy.py --debug
else
    python -B src/candyrandy.py
fi