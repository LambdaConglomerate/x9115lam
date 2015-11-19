#!/bin/bash
# Cleanup first
if [ -f ./out/out.txt ]
	then
		rm ./out/out.txt
fi
# Partially stolen from here http://stackoverflow.com/questions/6363441/check-if-a-file-exists-with-wildcard-in-shell-script
for f in ./Obtained_PF/*; do
	if [ -e "$f" ]
		then
			mv ./Obtained_PF/* ./old_obtained/
		break
	fi
done

# Run rig
python test.py
cd metrics/HyperVolume/
python hypervolume_runner.py
cd ../Spread/
python Spread.py