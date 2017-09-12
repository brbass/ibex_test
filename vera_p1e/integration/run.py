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
    data["executable"] = "ibex"
    data["num_procs"] = num_procs
    data["parameters"] = ["(POINTS_FILE)",
                          "(TAU)",
                          "(WEIGHTING)",
                          "(INT_ORD)"]
    data["values"] = []
    for tau in [0.0, 0.1, 0.2, 0.5, 1.0]:
        for weighting in ["full"]:
            for integration_ordinates in [4, 8, 16, 32, 64]:
                radius = 1.0
                data["values"].append([points_file,
                                       tau,
                                       weighting,
                                       integration_ordinates])
    data["descriptions"] = copy.deepcopy(data["values"])
    for desc in data["descriptions"]:
        desc[0] = points_description
    data["prefix"] = "verap1e"
    data["postfix"] = ".xml"
    data["template_filename"] = "template.xml"
    
    # Run case
    input_filenames = full_run_from_template(data,
                                             True) # Save input files
    
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
            fileout.write("\n")
        except:
            print("test {} failed to output data".format(input_filename))
    
def run():
    # Run cases
    with open("output_integration.txt", 'a') as fileout:
        for test_case, num_procs in zip([6, 8], [2, 1]):
            run_case(num_procs, # num procs
                     test_case,
                     "scaled_pincell_{}.xml".format(test_case),
                     "scaled{}".format(test_case),
                     fileout)
            
if __name__ == '__main__':
    run()
