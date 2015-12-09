import os
from os import path
from os.path import isfile

def metric_parser(filepath, separator=" "):
    assert(isfile(filepath) == True), "file doesn't exist"
    content = []

    with open(filepath, "r") as f:
        out = open(filepath.replace(".txt", ".csv"), 'w')
        state = 0
        s_c = c_c = 1
        output_array = []
        output_array.append(["Model", "Hypervolume", "Spread", "Convergence"])
        for line in f:
            if line.startswith("HYPERVOLUME"):
                state = 1
            elif line.startswith("SPREAD"):
                state = 2
            elif line.startswith("CONVERGENCE"):
                state = 3
            elif line not in ['\n', '\r\n']:
                if state == 1 and line.startswith("Name"):
                    output_array.append([line.split(" ")[1].split("_")[1].split(".")[0], line.split(" ")[3].replace("\n", ""), "", ""])
                elif state == 2 and line.startswith("Spread"):
                    output_array[s_c][2] = line.split("  ")[1].replace("\n", "")
                    s_c = s_c + 1
                elif state == 3 and line.startswith("Convergence"):
                    output_array[c_c][3] = line.split(" ")[1].replace("\n", "")
                    c_c = c_c + 1

        for out_line in output_array:
            out.write(out_line[0] + "," + out_line[1] + "," + out_line[2] + "," + out_line[3] + "\n")
            
        out.close()

files = [f for f in os.listdir("../out/") if f.endswith("txt")]

for f in files:
    metric_parser("../out/" + f)
