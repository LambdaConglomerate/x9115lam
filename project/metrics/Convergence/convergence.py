class ConvergenceContainer():
    def __init__(self, model_name, filename, obtained_results, true_results):
        self.name = filename
        self.model_name = model_name
        self.dimension = len(obtained_results[0])
        self.obtained_results = obtained_results  # list of list
        self.true_results = true_results

    def __str__(self):
        return "Name: " + self.name + " Convergence: " + str(self.Convergence)

def file_reader(filepath, separator=" "):
    from os.path import isfile
    assert(isfile(filepath) == True), "file doesn't exist"
    content = []
    for line in open(filepath, "r"):
        content.append([float(element) for element in line.split(separator) if element != "\n"])
    return content

def Convergence_wrapper():
    obtained_folder_path = "../Spread/Obtained_PF/"
    true_folder_path = "../Spread/True_PF/"

    from os import listdir
    obtained_filenames = [obtained_folder_path + file for file in listdir(obtained_folder_path)]
    model_names = [filename.split("/")[-1].split("_")[1].split(".")[0] for filename in obtained_filenames]
    true_filenames = [true_folder_path + model_name + ".txt" for model_name in model_names]

    fronts = [ConvergenceContainer(model_name, filename.split("/")[-1], file_reader(o_filename), file_reader(t_filename)) for model_name, o_filename, t_filename in zip(model_names, obtained_filenames, true_filenames)]
    Convergence(fronts)

def Convergence(fronts):
    min_dists = list()

    convergence_file = open(".\convergence.txt", 'w')

    for front in fronts:
        for solution in front.obtained_results:
            min_dist = 1e100

            for true_solution in front.true_results:
                dist = 0

                for i in xrange(front.dimension):
                    dist += (solution[i] - true_solution[i]) ** 2

                dist = dist ** 0.5

                if dist < min_dist:
                    min_dist = dist

            min_dists.append(min_dist)

        mins_sum = sum(min_dists)
        mins_average = mins_sum / len(min_dists)
        outString = front.model_name + " " + str(mins_average)
        convergence_file.write(outString)

Convergence_wrapper()
