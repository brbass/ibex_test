from mesh_functions import *
import numpy as np
import argparse

def get_points(num_radii,
               max_delta,
               initial_delta,
               ring_start = 0.4101,
               length = 1.26,
               exclude_corners = False):
    # Set parameters
    initial_delta = np.abs(initial_delta)
    r0 = ring_start - initial_delta / 2
    r1 = ring_start + initial_delta / 2
    r = 0.0
    dr0 = -initial_delta
    a = np.power((r - r0) / dr0, 1. / (num_radii - 1.))
    l = length
    l2 = l / 2
    print("delta multiplication factor: a = ", a)
    ind_add = int(np.ceil(l2 / max_delta))
    
    # Get points and spacing for each radius
    points_ifba = [r0, r1]
    delta_ifba = [initial_delta, initial_delta]
    delta_fuel = [min(max_delta, initial_delta * np.power(a, n + 1)) for n in range(0, num_radii + ind_add)]
    points_fuel = [r0 - delta_fuel[0]]
    for i in range(num_radii + ind_add - 1):
        point = points_fuel[-1] - delta_fuel[i + 1]
        if point >= 0:
            if point < delta_fuel[-2] / 4:
                point = 0.
            points_fuel.append(point)
    delta_fuel = delta_fuel[0:len(points_fuel)]
    delta_mod = [min(max_delta, initial_delta * np.power(a, n + 1)) for n in range(0, num_radii + ind_add)]
    points_mod = [r1 + delta_mod[0]]
    for i in range(num_radii + ind_add - 1):
        point = points_mod[-1] + delta_mod[i + 1]
        points_mod.append(point)
    
    # Combine sets of points
    points_r = np.concatenate((points_fuel, points_ifba, points_mod))
    delta_r = np.abs(np.concatenate((delta_fuel, delta_ifba, delta_mod)))
    indices = np.argsort(points_r)
    points_r = points_r[indices]
    delta_r = delta_r[indices]
    spacing_r = [delta_r[0]]
    for i in range(1, len(points_r) - 1):
        spacing_r.append((delta_r[i + 1] + delta_r[i - 1]) / 2)
    spacing_r.append(delta_r[-1])

    # Get full set of points
    points = []
    for i, (r, spacing) in enumerate(zip(points_r, spacing_r)):
        points_temp = get_ring_points(r, spacing)
        for point_temp in points_temp:
            points.append(point_temp)

    # Get distance to ignore near boundary
    index = (np.abs(points_r - l2)).argmin()
    delta_l = delta_r[index]
    l_ignore = (l2 - 0.7 * delta_l)

    # Remove those points outside boundary
    points_all = points
    points = []
    for point in points_all:
        if np.abs(point[0]) < l_ignore and np.abs(point[1]) < l_ignore:
            points.append(point)

    # Add points along boundary
    num_intervals_l = int(np.ceil(l / delta_l))
    num_points_l = num_intervals_l + 1
    delta_l = l / num_intervals_l
    for sign in [-1, 1]:
        if exclude_corners:
            for i in range(1, num_points_l - 1):
                pos = -l2 + delta_l * i
                points.append([pos, sign * l2])
        else:
            for i in range(num_points_l):
                pos = -l2 + delta_l * i
                points.append([pos, sign * l2])
        for i in range(1, num_points_l - 1):
            pos = -l2 + delta_l * i
            points.append([sign * l2, pos])
            
    # Return result
    num_points = len(points)
    points = np.array(points)
    return num_points, points

def output_points(num_radii,
                  max_delta,
                  initial_delta,
                  ring_start = 0.4101,
                  length = 1.26,
                  exclude_corners = False):
    # Get points and output path
    num_points, points = get_points(num_radii, max_delta, initial_delta, ring_start, exclude_corners)
    print("mesh has {} points".format(num_points))
    if exclude_corners:
        corner_string = "_exclude"
    else:
        corner_string = ""
    output_path = "vera1e_mesh_{}_{}_{}_{}_{}{}.xml".format(num_radii,
                                                            max_delta,
                                                            initial_delta,
                                                            ring_start,
                                                            length,
                                                            corner_string)

    # Get node and add input data
    node = xml_points(2, # dimension
                      num_points,
                      points)
    et.SubElement(node, "num_radii").text = str(num_radii)
    et.SubElement(node, "max_delta").text = str(max_delta)
    et.SubElement(node, "initial_delta").text = str(initial_delta)
    
    # Output xml node
    et.ElementTree(node).write(output_path,
                               pretty_print=True,
                               xml_declaration=True)
    
    # Plot if desired
    if False:
        plt.figure()
        plt.scatter(points[:, 0], points[:, 1], s=2)
        plt.axes().set_aspect('equal')
        plt.show()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_radii", type=int, required=True, help="number of points inside the radius")
    parser.add_argument("--initial_delta", type=float, required=True)
    parser.add_argument("--max_delta", type=float, required=True)
    parser.add_argument("--exclude_corners", action='store_true', default=False,
                        help="exclude corner points")
    parser.add_argument("--length", type=float, required=False, default=1.26,
                        help="square side length")
    parser.add_argument("--ring_start", type=float, required=False, default=0.4101,
                        help="center location of the ring")
    args = parser.parse_args()
    output_points(args.num_radii,
                  args.max_delta,
                  args.initial_delta,
                  args.ring_start,
                  args.length,
                  args.exclude_corners)