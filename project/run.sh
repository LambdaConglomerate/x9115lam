#!/bin/bash
# Cleanup first
if [ -f ./out/out.txt ]
	then
		rm ./out/out.txt
fi
cd metrics/Spread
# Partially stolen from here http://stackoverflow.com/questions/6363441/check-if-a-file-exists-with-wildcard-in-shell-script
for f in ./Obtained_PF/*; do
	if [ -e "$f" ]
		then
			mv ./Obtained_PF/* ./old_obtained/
		break
	fi
done
cd ..
cd ..
# Run rig
python test.py
# Only run hypervolume if -h flag is used.
# Partially stolen from here http://wiki.bash-hackers.org/howto/getopts_tutorial
while getopts ":h" opt; do
  case $opt in
    h)
      echo "Calculate Hypervolume" >&2
      cd metrics/HyperVolume/
	  python hypervolume_runner.py
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done
cd ../Spread/
python Spread.py