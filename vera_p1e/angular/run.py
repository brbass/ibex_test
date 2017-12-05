from ibex_io import full_run_from_template
from ibex_io import full_save_from_template
import copy
import sys
import numpy as np
import xml.etree.ElementTree as et

def get_parameters():
    point_files = []
    descriptions = []
    points = []
    for param in [[19, 0.04, 0.004],
                  [20, 0.03, 0.003],
                  [22, 0.02, 0.002]]:
        point_files.append("vera1e_mesh_{}_{}_{}.xml".format(*param))
        descriptions.append("mult{}".format(param[2]))
    # for param in [16, 24, 32, 48, 64, 96, 128, 192, 256]:
    #     point_files.append("square_1.26_{}.xml".format(param))
    #     descriptions.append("square{}".format(param))
    for point_file in point_files:
        num_points = int(et.parse(point_file).getroot().find("spatial_discretization").findtext("number_of_points"))
        mem = 0.00045 * 16 * num_points
        if mem > 100:
            print("more memory required for case {}".format(descriptions[-1]))
            return
        points.append(num_points)
    
    return points, point_files, descriptions
    
def get_values(num_procs,
               num_points,
               point_files,
               point_descriptions):
    # Set up data list
    data = {}
    data["executable"] = "ibex"
    data["num_procs"] = num_procs
    data["parameters"] = ["(POINTS_FILE)",
                          "(ANGULAR_RULE)",
                          "(TAU)",
                          "(WEIGHTING)",
                          "(INT_CELLS)"]
    data["values"] = []
    data["descriptions"] = []
    for tau in [1.0]:
        for weighting in ["full"]:
            for rule in [1, 2, 3, 4, 5]:
                for num_point, point_file, point_description in zip(num_points, point_files, point_descriptions):
                    min_integration_cells = 128
                    integration_cells = int(4 * np.sqrt(num_point))
                    if integration_cells < min_integration_cells:
                        integration_cells = min_integration_cells
                    data["values"].append([point_file,
                                           rule,
                                           tau,
                                           weighting,
                                           integration_cells])
                    data["descriptions"].append([point_description,
                                                 rule,
                                                 tau,
                                                 weighting,
                                                 integration_cells])
    data["prefix"] = "test"
    data["postfix"] = ".xml"
    data["template_filename"] = "template.xml"
    
    return data

def run_case(num_procs,
             num_points,
             point_files,
             point_descriptions,
             run = True):
    # Get data
    data = get_values(num_procs,
                      num_points,
                      point_files,
                      point_descriptions)
    
    # Run case
    if run:
        input_filenames = full_run_from_template(data,
                                                 True) # Save input files
    else:
        input_filenames = full_save_from_template(data,
                                                  True) # Save input files

def run_all(run = True):
    # Get cases
    points, point_files, descriptions = get_parameters()
    
    run_case(1, # num cases to run at once
             points,
             point_files,
             descriptions,
             run)
        
if __name__ == '__main__':
    run_all(True)
