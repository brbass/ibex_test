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
    for param in [[13, 0.1, 0.02],
                  [14, 0.075, 0.015],
                  [16, 0.05, 0.01],
                  [17, 0.0375, 0.0075],
                  [20, 0.01875, 0.00375],
                  [19, 0.025, 0.005],
                  [21, 0.0125, 0.0025],
                  [22, 0.009375, 0.001875],
                  [24, 0.008, 0.0016]]:
        point_files.append("vera1e_mesh_{}_{}_{}_0.4101_1.26.xml".format(*param))
        descriptions.append("mult{}-{}-{}".format(param[0], param[1], param[2]))
    for point_file in point_files:
        num_points = int(et.parse(point_file).getroot().find("spatial_discretization").findtext("number_of_points"))
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
                    mem = 0.0005 * num_point * (4 ** (rule - 3))
                    if mem < 100:
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
                    else:
                        print("case {} cannot run with rule {}".format(point_description, rule))
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
