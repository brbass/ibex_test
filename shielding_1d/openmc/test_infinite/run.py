import numpy as np
import matplotlib.pyplot as plt
from bisect import bisect

import openmc
import openmc.mgxs as mgxs

#############################
# Multigroup cross sections #
#############################

groups = mgxs.EnergyGroups(group_edges=[7., 8., 9., 10.])

xs_source = openmc.XSdata('source', groups)
xs_source.order = 1
xs_source.set_total([1.5, 2.0, 3.0])
xs_source.set_scatter_matrix([[[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]],
                              [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]],
                              [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]])
xs_source.set_absorption([1.5, 2.0, 3.0])
xs_source.set_nu_fission([0.0, 0.0, 0.0])
xs_source.set_chi([1.0, 0.0, 0.0])

mg_cross_sections_file = openmc.MGXSLibrary(groups)
mg_cross_sections_file.add_xsdatas([xs_source])
mg_cross_sections_file.export_to_hdf5()

#############
# Materials #
#############

mac_source = openmc.Macroscopic('source')
m_source = openmc.Material(material_id=1, name='source')
m_source.set_density('macro', 1.0)
m_source.add_macroscopic(mac_source)

materials_file = openmc.Materials([m_source])
materials_file.cross_sections = "./mgxs.h5"
materials_file.export_to_xml()

############
# Geometry #
############

length=2.
s_xmin = openmc.XPlane(surface_id=1, x0=-length/2, name='xmin')
s_xmax = openmc.XPlane(surface_id=2, x0=length/2, name='xmax')
s_ymin = openmc.YPlane(surface_id=3, y0=-length/2, name='ymin')
s_ymax = openmc.YPlane(surface_id=4, y0=length/2, name='ymax')
s_zmin = openmc.ZPlane(surface_id=5, z0=-length/2, name='zmin')
s_zmax = openmc.ZPlane(surface_id=6, z0=length/2+1, name='zmax')

s_xmin.boundary_type = 'reflective'
s_xmax.boundary_type = 'reflective'
s_ymin.boundary_type = 'reflective'
s_ymax.boundary_type = 'reflective'
s_zmin.boundary_type = 'reflective'
s_zmax.boundary_type = 'reflective'

c_source = openmc.Cell(cell_id=1, name='source')

c_source.region = +s_xmin & -s_xmax & +s_ymin & -s_ymax & +s_zmin & -s_zmax

c_source.fill = m_source

root = openmc.Universe(universe_id=1, name='root')
root.add_cells([c_source])

geometry = openmc.Geometry(root)
geometry.export_to_xml()

###########
# Tallies #
###########

mesh = openmc.Mesh()
mesh.dimension = [1, 1, 1]
mesh.lower_left = [-length/2, -length/2, -length/2]
mesh.upper_right = [length/2, length/2, length/2+1]

mesh_filter = openmc.MeshFilter(mesh)
energy_filter = openmc.EnergyFilter(groups.group_edges)

tally = openmc.Tally(name='flux')
tally.filters = [mesh_filter, energy_filter]
tally.scores = ['flux']

tallies_file = openmc.Tallies()
tallies_file.append(tally)
tallies_file.export_to_xml()

for energy_to_test in [6.5, 7.5, 8.5, 9.5, 10.5]:

    ############
    # Settings #
    ############
    
    if energy_to_test < groups.group_edges[0]:
        expected_group = 1
    elif energy_to_test > groups.group_edges[-1]:
        expected_group = groups.num_groups
    else:
        expected_group = bisect(groups.group_edges, energy_to_test)
        
    uniform_dist = openmc.stats.Box([-length/2, -length/2, -length/2],
                                    [length/2, length/2, length/2])
    isotropic_dist = openmc.stats.Isotropic()
    energy_dist = openmc.stats.Discrete([energy_to_test], [1.0])
    source = openmc.Source(uniform_dist,
                           isotropic_dist,
                           energy_dist)
    settings_file = openmc.Settings()
    settings_file.energy_mode = "multi-group"
    settings_file.run_mode = "fixed source"
    settings_file.batches = 100
    settings_file.particles = int(1e2)
    settings_file.survival_biasing = True
    settings_file.verbosity = 1
    settings_file.source = source
    settings_file.sourcepoint['write'] = True
    settings_file.sourcepoint['separate'] = False
    settings_file.sourcepoint['batches'] = [settings_file.batches]
    settings_file.export_to_xml()
    
    #######
    # Run #
    #######
    
    openmc.run(threads=4)
    
    ################
    # Load results #
    ################
    
    sp = openmc.StatePoint("statepoint.{}.h5".format(settings_file.batches))
    print("group calculated in OpenMC: {}".format(sp.source[0][3]))
    print("expected group: {}".format(expected_group))
    print()
