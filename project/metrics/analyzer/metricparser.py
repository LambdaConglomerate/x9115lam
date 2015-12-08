import os
from os import path
from os.path import isfile

def metric_parser(filepath, separator=" "):
    print filepath
    assert(isfile(filepath) == True), "file doesn't exist"
    content = []

    with open(filepath, "r") as f:
        out = open(filepath.replace(".txt", ".csv"), 'w')
        state = 0
        for line in f:
            if line.startswith("HYPERVOLUME"):
                out.write("Hypervolume\n\n")
                state = 1
            elif line.startswith("SPREAD"):
                out.write("\nSpread\n\n")
                state = 2
            elif line.startswith("CONVERGENCE"):
                out.write("\nConvergence\n\n")
                state = 3
            elif line not in ['\n', '\r\n']:
                if state == 1 and line.startswith("Name"):
                    out.write(line.split(" ")[1].split("_")[1].split(".")[0] + "," + line.split(" ")[3])
                elif state == 2 and line.startswith("Model"):
                    out.write(line.split("  ")[1].split(".")[0] + ",")
                elif state == 2 and line.startswith("Spread"):
                    out.write(line.split("  ")[1])
                elif state == 3 and line.startswith("Model"):
                    out.write(line.split("  ")[1].split(".")[0].replace("\n", "") + ",")
                elif state == 3 and line.startswith("Convergence"):
                    out.write(line.split(" ")[1])

        out.close()

files = [f for f in os.listdir("../out/")]

for f in files:
    metric_parser("../out/" + f)
