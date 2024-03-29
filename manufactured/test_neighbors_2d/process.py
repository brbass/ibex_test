import numpy as np
import sys
import glob
import xml.etree.ElementTree as et
from ibex_io import get_scalar, get_vector, unpack3

def get_error(output_filename):
    source_doc = open(output_filename)
    output_doc = et.parse(source_doc)
    output_node = output_doc.getroot()

    num_groups = get_scalar("number_of_groups", int, output_node.find("energy_discretization"))
    num_moments = get_scalar("number_of_moments", int, output_node.find("angular_discretization"))
    error_data = get_vector("l1", float, output_node.find("error"))
    phi_data = get_vector("phi", float, output_node.find("solver").find("values"))
    num_cells = int(len(phi_data) / (num_moments * num_groups))
    error = unpack3(error_data,
                    num_cells,
                    num_moments,
                    num_groups)
    phi = unpack3(phi_data,
                  num_cells,
                  num_moments,
                  num_groups)
    l1 = np.mean(error[:, 0, 0]) / np.mean(phi[:, 0, 0])
    time = get_scalar("total", float, output_node.find("timing"))

    source_doc.close()
    
    return l1, time

def get_errors(fileout):
    # Get errors for each set of output data
    output_filenames = sorted(glob.glob("*.xml.out"))
    for output_filename in output_filenames:
        try:
            data = get_error(output_filename)
        except:
            print("test {} output format incorrect".format(output_filename))
            print("\t{}".format(sys.exc_info()))
            return
        
        # Output data
        output_string = output_filename.lstrip("test_").rstrip(".xml.out")
        input_values = output_string.split("_")
        for input_value in input_values:
            fileout.write("{}\t".format(input_value))
        for val in data:
            fileout.write("{}\t".format(val))
        fileout.write("\n")
        
if __name__ == '__main__':
    with open("output.txt", 'a') as fileout:
        get_errors(fileout)
