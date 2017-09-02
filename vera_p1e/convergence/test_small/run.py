import copy
from ibex_io import run_from_template

def run():
    data = {}
    data["executable"] = "ibex"
    data["num_procs"] = 4
    data["parameters"] = ["(POINTS_FILE)",
                          "(TAU)",
                          "(NEIGHBORS)"]
    data["values"] = [["scaled_pincell_2.xml",
                       "scaled_pincell_3.xml",
                       "scaled_pincell_4.xml",
                       "square_pincell_1.xml",
                       "square_pincell_2.xml",
                       "square_pincell_3.xml"],
                      [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
                      [8, 10, 12, 15]]
    data["descriptions"] = copy.copy(data["values"])
    data["descriptions"][0] = ["scaled2", "scaled3", "scaled4", "square1", "square2", "square3"]
    data["prefix"] = "test"
    data["postfix"] = ".xml"
    data["template_filename"] = "template.xml"

    run_from_template(data)
    
if __name__ == '__main__':
    run()
