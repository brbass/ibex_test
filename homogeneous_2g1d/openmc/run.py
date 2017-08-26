import numpy as np
import matplotlib.pyplot as plt

import openmc
import openmc.mgxs as mgxs

#############################
# Multigroup cross sections #
#############################

groups = mgxs.EnergyGroups(group_edges=[0., 1.0e4, 2.0e7])

xs_fuel = openmc.XSdata('fuel', groups)
xs_fuel.order = 1
xs_fuel.set_total([1.0, 2.0])
xs_fuel.set_scatter_matrix([[[0.8, 0.1], [0.1, 0.01]],
                            [[0.01, 0.0], [1.6, 0.1]]])
xs_fuel.set_absorption([0.1, 0.39])
xs_fuel.set_nu_fission([[0.1, 0.0],
                        [0.0, 0.4]])

mg_cross_sections_file = openmc.MGXSLibrary(groups)
mg_cross_sections_file.add_xsdatas([xs_fuel])
mg_cross_sections_file.export_to_hdf5()

#############
# Materials #
#############

mac_fuel = openmc.Macroscopic('fuel')
m_fuel = openmc.Material(material_id=1, name='fuel')
m_fuel.set_density('macro', 1.0)
m_fuel.add_macroscopic(mac_fuel)

materials_file = openmc.Materials([m_fuel])
materials_file.cross_sections = "./mgxs.h5"
materials_file.export_to_xml()

############
# Geometry #
############

s_0 = openmc.XPlane(surface_id=1, x0=0.0, name='s0')
s_1 = openmc.XPlane(surface_id=2, x0=3.0, name='s1')

s_0.boundary_type = 'reflective'
s_1.boundary_type = 'vacuum'

c_fuel = openmc.Cell(cell_id=1, name='fuel')

c_fuel.region = +s_0 & -s_1

c_fuel.fill = m_fuel

root = openmc.Universe(universe_id=0, name='root')
root.add_cells([c_fuel])

geometry = openmc.Geometry(root)
geometry.export_to_xml()

############
# Settings #
############

settings_file = openmc.Settings()
settings_file.energy_mode = "multi-group"
settings_file.batches = 200
settings_file.inactive = 50
settings_file.particles = int(1e6)

bounds = [0.0, 0.0, 0.0, 1.0, 1.0, 1.0]
uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:])
settings_file.source = openmc.source.Source(space=uniform_dist)
settings_file.export_to_xml()

#######
# Run #
#######

openmc.run(threads=4)

################
# Load results #
################

sp = openmc.StatePoint("statepoint.{}.h5".format(settings_file.batches))
print(sp.k_combined)
