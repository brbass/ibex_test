import copy
from ibex_io import full_run_from_template
from ibex_io import get_data

def run_case(num_procs,
             test_case,
             points_file,
             points_description,
             fileout):
    # Set up data list
    data = {}
    data["executable"] = "echo"
    data["num_procs"] = num_procs
    data["parameters"] = ["(POINTS_FILE)",
                          "(TAU)",
                          "(WEIGHTING)",
                          "(INT_CELLS)",
                          "(RADIUS)"]
    data["values"] = []
    for tau in [0.0, 0.1, 0.2, 0.5, 1.0]:
        for weighting in ["full"]:
            for integration_cells in [511, 512, 513, 1024]:
                radius = 1.0
                data["values"].append([points_file,
                                       tau,
                                       weighting,
                                       integration_cells,
                                       radius])
            for radius in [0.9, 1.0, 1.1]:
                integration_cells = 512
                data["values"].append([points_file,
                                       tau,
                                       weighting,
                                       integration_cells,
                                       radius])
    data["descriptions"] = copy.deepcopy(data["values"])
    for desc in data["descriptions"]:
        desc[0] = points_description
    data["prefix"] = "test"
    data["postfix"] = ".xml"
    data["template_filename"] = "template.xml"
    
    # Run case
    input_filenames = full_run_from_template(data,
                                             False) # Save input files
    
    # Get output
    for i, input_filename in enumerate(input_filenames):
        try:
            data_out = get_data("{}.out".format(input_filename))
            for val in [points_description, test_case, data["values"][i][1], data["values"][i][3], data["values"][i][4]]:
                fileout.write("{}\t".format(val))
            for par in ["number_of_moments", "number_of_ordinates", "number_of_points", "weighting", "k_eigenvalue"]:
                fileout.write("{}\t".format(data_out[par]))
            for par in ["spatial_initialization", "sweep_initialization", "solve"]:
                fileout.write("{}\t".format(data_out["timing"][par]))
            fileout.write("{}".format((data_out["k_eigenvalue"] - 0.772801396)*1e5))
        except:
            print("test {} failed to output data".format(input_filename))
        fileout.write("\n")
    
def run():
    # Run cases
    with open("output_sensitivity.txt", 'a') as fileout:
        for test_case, num_procs in zip([5, 6], [3, 2]):
            run_case(num_procs, # num procs
                     test_case,
                     "scaled_pincell_{}.xml".format(test_case),
                     "scaled{}".format(test_case),
                     fileout)
            
if __name__ == '__main__':
    run()
