#!/bin/bash
# Stupid simple script to delete out and rerun the rig
if [ -f out.txt ]
	then
		rm out.txt
fi
python test.py