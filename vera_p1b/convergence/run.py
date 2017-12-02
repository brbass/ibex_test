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
    for param in [[13, 0.08, 0.02],
                  [14, 0.06, 0.015],
                  [16, 0.04, 0.01],
                  [17, 0.03, 0.0075],
                  [19, 0.02, 0.005],
                  [20, 0.015, 0.00375],
                  [21, 0.01, 0.0025]]:
        point_files.append("vera1e_mesh_{}_{}_{}_0.4423_1.26.xml".format(*param))
        descriptions.append("mult{}".format(param[2]))
    for param in [16, 24, 32, 48, 64, 96, 128]:
        point_files.append("square_1.26_{}.xml".format(param))
        descriptions.append("square{}".format(param))
    for point_file in point_files:
        num_points = int(et.parse(point_file).getroot().find("spatial_discretization").findtext("number_of_points"))
        points.append(num_points)
    
    # Get number of procs
    procs = []
    for point, point_file in zip(points, point_files):
        mem = point * 0.00045
        proc = int(np.floor(16./mem))
        if proc < 1:
            print("case can't run with 0 procs")
        elif proc > 4:
            proc = 4
        procs.append(proc)
    proc_cases = np.unique(procs)[::-1]
    data = []
    desc = []
    pts = []
    for i, proc in enumerate(proc_cases):
        local_data = []
        local_desc = []
        local_pts = []
        for local_proc, pt, point, description in zip(procs, points, point_files, descriptions):
            if local_proc == proc:
                local_data.append(point)
                local_desc.append(description)
                local_pts.append(pt)
        data.append(local_data)
        desc.append(local_desc)
        pts.append(local_pts)
    return proc_cases, pts, data, desc
    
def get_values(num_procs,
               num_points,
               point_files,
               point_descriptions):
    # Get number of threads
    if num_procs == 1:
        num_threads = 4
    elif num_procs == 2:
        num_threads = 2
    else:
        num_threads = 1
    
    # Set up data list
    data = {}
    data["executable"] = "~/code/ibex_parallel/bin/ibex"
    data["num_procs"] = num_procs
    data["parameters"] = ["(POINTS_FILE)",
                          "(TAU)",
                          "(WEIGHTING)",
                          "(INT_CELLS)",
                          "(NUM_THREADS)"]
    data["values"] = []
    data["descriptions"] = []
    for tau in [1.0]:
        for weighting in ["full", "basis"]:
            for num_point, point_file, point_description in zip(num_points, point_files, point_descriptions):
                min_integration_cells = 128
                integration_cells = int(4 * np.sqrt(num_point))
                if integration_cells < min_integration_cells:
                    integration_cells = min_integration_cells
                data["values"].append([point_file,
                                       tau,
                                       weighting,
                                       integration_cells,
                                       num_threads])
                data["descriptions"].append([point_description,
                                             tau,
                                             weighting,
                                             integration_cells,
                                             num_threads])
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
    procs, point_cases, data_cases, descriptions = get_parameters()
    
    # Run cases that share a number of procs
    for proc, local_point, local_data, description in zip(procs, point_cases, data_cases, descriptions):
        # print(proc, description)
        run_case(proc,
                 local_point,
                 local_data,
                 description,
                 run)
        
if __name__ == '__main__':
    run_all(True)
