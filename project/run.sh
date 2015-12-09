#!/bin/bash
# Cleanup first
cd metrics/Spread
# Partially stolen from here http://stackoverflow.com/questions/6363441/check-if-a-file-exists-with-wildcard-in-shell-script
for f in ./obtained/*; do
	if [ -e "$f" ]
		then
			mv ./obtained/* ./old_obtained/
		break
	fi
done
cd ..
cd HyperVolume
for f in ./obtained/*; do
  if [ -e "$f" ]
    then
      mv ./obtained/* ./old_obtained/
    break
  fi
done
cd ..
cd Convergence
for f in ./obtained/*; do
  if [ -e "$f" ]
    then
      mv ./obtained/* ./old_obtained/
    break
  fi
done
cd ..
cd ..
# # # Run rig
# python test.py
# Partially stolen from here http://wiki.bash-hackers.org/howto/getopts_tutorial
while getopts ":hscx:o:" opt; do
  case $opt in
    x)
      echo "Running rig, outputting log to: "
      echo "out/"$OPTARG
      if [ -f ./out/$OPTARG ]
        then
          rm ./out/$OPTARG
      fi
      python test.py $OPTARG
      echo "Outputting metric data to: "
      # DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
      DIR=$(pwd)
      F=$DIR"/metrics/out/"$OPTARG
      if [ -f $F ]
        then
          rm $F
      fi
      echo $F
      echo "Calculate Hypervolume" >&2
      cd metrics/HyperVolume/
      python hypervolume_runner.py >> $F
      cd ..
      cd ..
      echo "Calculate Spread" >&2
      cd metrics/Spread/
      if [ ! -d "./Obtained_PF" ]
        then 
          mkdir ./Obtained_PF
      fi
      python SpreadMill.py >> $F
      cd ..
      cd ..
      echo "Calculate Convergence" >&2
      cd metrics/Convergence/
      python convergence.py >> $F
      cd ..
      cd ..
      ;;
    h)
      echo "Calculate Hypervolume" >&2
      cd metrics/HyperVolume/
	    python hypervolume_runner.py
      cd ..
      cd ..
      ;;
    s)
      echo "Calculate Spread" >&2
      cd metrics/Spread/
      python Spread.py
      cd ..
      cd ..
      ;;
    c)
      echo "Calculate Convergence" >&2
      cd metrics/Convergence/
      python convergence.py
      cd ..
      cd ..
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done
