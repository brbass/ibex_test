import numpy as np
import matplotlib.pyplot as plt

import openmc
import openmc.mgxs as mgxs

#############################
# Multigroup cross sections #
#############################

groups = mgxs.EnergyGroups(group_edges=[0., 1.0e2, 2.0e7])

xs_source = openmc.XSdata('source', groups)
xs_source.order = 1
xs_source.set_total([1.0, 2.0])
xs_source.set_scatter_matrix([[[0.9, 0.1], [0.05, 0.0]],
                              [[0.05, 0.0], [0.8, 0.0]]])
xs_source.set_absorption([0.05, 1.15])
xs_source.set_nu_fission([0.0, 1.0])
xs_source.set_chi([1.0, 0.0])
# xs_source.set_scatter_matrix([[[0.0, 0.0], [0.0, 0.0]],
#                               [[0.0, 0.0], [0.0, 0.0]]])
# xs_source.set_absorption([1.0, 2.0])
# xs_source.set_nu_fission([0.0, 0.0])
# xs_source.set_chi([1.0, 0.0])

xs_thin = openmc.XSdata('thin', groups)
xs_thin.order = 1
xs_thin.set_total([0.5, 1.0])
xs_thin.set_scatter_matrix([[[0.05, 0.0], [0.45, 0.1]],
                            [[0.0, 0.0], [1.0, 0.01]]])
xs_thin.set_absorption([0.0, 0.0])
xs_thin.set_nu_fission([0.0, 0.0])
xs_thin.set_chi([0.0, 0.0])
# xs_thin.set_scatter_matrix([[[0.0, 0.0], [0.0, 0.0]],
#                               [[0.0, 0.0], [0.0, 0.0]]])
# xs_thin.set_absorption([0.5, 1.0])
# xs_thin.set_nu_fission([0.0, 0.0])
# xs_thin.set_chi([1.0, 0.0])

xs_thick = openmc.XSdata('thick', groups)
xs_thick.order = 1
xs_thick.set_total([0.5, 10.0])
xs_thick.set_scatter_matrix([[[0.0, 0.0], [0.0, 0.0]],
                             [[0.0, 0.0], [0.0, 0.0]]])
xs_thick.set_absorption([0.5, 10.0])
xs_thick.set_nu_fission([0.0, 0.0])
xs_thick.set_chi([0.0, 0.0])

mg_cross_sections_file = openmc.MGXSLibrary(groups)
mg_cross_sections_file.add_xsdatas([xs_source, xs_thin, xs_thick])
mg_cross_sections_file.export_to_hdf5()

#############
# Materials #
#############

mac_source = openmc.Macroscopic('source')
m_source = openmc.Material(material_id=1, name='source')
m_source.set_density('macro', 1.0)
m_source.add_macroscopic(mac_source)

mac_thin = openmc.Macroscopic('thin')
m_thin = openmc.Material(material_id=2, name='thin')
m_thin.set_density('macro', 1.0)
m_thin.add_macroscopic(mac_thin)

mac_thick = openmc.Macroscopic('thick')
m_thick = openmc.Material(material_id=3, name='thick')
m_thick.set_density('macro', 1.0)
m_thick.add_macroscopic(mac_thick)

materials_file = openmc.Materials([m_source, m_thin, m_thick])
materials_file.cross_sections = "./mgxs.h5"
materials_file.export_to_xml()

############
# Geometry #
############

x_pos = [0.0, 0.5, 3.0, 4.0]
inf_dist = 10000.0

s_x1 = openmc.XPlane(surface_id=1, x0=x_pos[0], name='x1')
s_x2 = openmc.XPlane(surface_id=2, x0=x_pos[1], name='x2')
s_x3 = openmc.XPlane(surface_id=3, x0=x_pos[2], name='x3')
s_x4 = openmc.XPlane(surface_id=4, x0=x_pos[3], name='x4')
s_ymin = openmc.YPlane(surface_id=5, y0=-inf_dist, name='ymin')
s_ymax = openmc.YPlane(surface_id=6, y0=inf_dist, name='ymax')
s_zmin = openmc.ZPlane(surface_id=7, z0=-inf_dist, name='zmin')
s_zmax = openmc.ZPlane(surface_id=8, z0=inf_dist, name='zmax')

s_x1.boundary_type = 'reflective'
s_x4.boundary_type = 'vacuum'
s_ymin.boundary_type = 'reflective'
s_ymax.boundary_type = 'reflective'
s_zmin.boundary_type = 'reflective'
s_zmax.boundary_type = 'reflective'

c_source = openmc.Cell(cell_id=1, name='source')
c_thin = openmc.Cell(cell_id=2, name='thin')
c_thick = openmc.Cell(cell_id=3, name='thick')

c_source.region = +s_x1 & -s_x2 & +s_ymin & -s_ymax & +s_zmin & -s_zmax
c_thin.region = +s_x2 & -s_x3 & +s_ymin & -s_ymax & +s_zmin & -s_zmax
c_thick.region = +s_x3 & -s_x4 & +s_ymin & -s_ymax & +s_zmin & -s_zmax

c_source.fill = m_source
c_thin.fill = m_thin
c_thick.fill = m_thick

root = openmc.Universe(universe_id=1, name='root')
root.add_cells([c_source, c_thin, c_thick])

geometry = openmc.Geometry(root)
geometry.export_to_xml()

###########
# Tallies #
###########

mesh = openmc.Mesh()
mesh.dimension = [1000, 1, 1]
mesh.lower_left = [x_pos[0], -inf_dist, -inf_dist]
mesh.upper_right = [x_pos[-1], inf_dist, inf_dist]

mesh_filter = openmc.MeshFilter(mesh)
energy_filter = openmc.EnergyFilter(groups.group_edges)

tally = openmc.Tally(name='flux')
tally.filters = [mesh_filter, energy_filter]
tally.scores = ['flux']

tallies_file = openmc.Tallies()
tallies_file.append(tally)
tallies_file.export_to_xml()

############
# Settings #
############

dist_source = 2.0
uniform_dist = openmc.stats.Box([x_pos[0], -dist_source, -dist_source],
                                [x_pos[1], dist_source, dist_source])
isotropic_dist = openmc.stats.Isotropic()
energy_dist = openmc.stats.Discrete([0.], [1.0])
source = openmc.Source(uniform_dist,
                       isotropic_dist,
                       energy_dist,
                       strength=1)
settings_file = openmc.Settings()
settings_file.energy_mode = "multi-group"
settings_file.run_mode = "fixed source"
settings_file.batches = 100
settings_file.particles = int(1e7)
settings_file.survival_biasing = True
settings_file.verbosity = 6
settings_file.source = source
settings_file.export_to_xml()

#######
# Run #
#######

openmc.run(threads=4)

################
# Load results #
################

# sp = openmc.StatePoint("statepoint.{}.h5".format(settings_file.batches))
