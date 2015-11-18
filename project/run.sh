#!/bin/bash
# Stupid simple script to delete out and rerun the rig
if [ -f ./out/out.txt ]
	then
		rm ./out/out.txt
fi
python test.py