import numpy as np
import matplotlib.pyplot as plt

import openmc
import openmc.mgxs as mgxs

#############################
# Multigroup cross sections #
#############################

groups = mgxs.EnergyGroups(group_edges=[0., 1.0e2, 2.0e7])

xs_fuel = openmc.XSdata('fuel', groups)
xs_fuel.order = 1
xs_fuel.set_total([0.398430149, 0.566537670])
xs_fuel.set_scatter_matrix([[[0.382535056, 0.049926556], [0.000821017, -0.000258533]],
                            [[0.0, 0.0], [0.408203703, 0.006196203]]]);
xs_fuel.set_absorption([0.015075423, 0.158330901])
xs_fuel.set_nu_fission([[0.013877940, 0.000000015],
                        [0.208179836, 0.000000160]])

xs_mod = openmc.XSdata('moderator', groups)
xs_mod.order = 1
xs_mod.set_total([0.589533143, 1.404056519])
xs_mod.set_scatter_matrix([[[0.542576514, 0.323899243], [0.046780637, 0.020173486]],
                            [[0.000000034, 0.000000034], [1.389920798, 0.598442391]]])
xs_mod.set_absorption([0.000172617, 0.014134002])
xs_mod.set_nu_fission([[0.0, 0.0],
                        [0.0, 0.0]])

mg_cross_sections_file = openmc.MGXSLibrary(groups)
mg_cross_sections_file.add_xsdatas([xs_fuel, xs_mod])
mg_cross_sections_file.export_to_hdf5()

#############
# Materials #
#############

mac_fuel = openmc.Macroscopic('fuel')
m_fuel = openmc.Material(material_id=1, name='fuel')
m_fuel.set_density('macro', 1.0)
m_fuel.add_macroscopic(mac_fuel)

mac_mod = openmc.Macroscopic('moderator')
m_mod = openmc.Material(material_id=5, name='mod')
m_mod.set_density('macro', 1.0)
m_mod.add_macroscopic(mac_mod)

materials_file = openmc.Materials([m_fuel, m_mod])
materials_file.cross_sections = "./mgxs.h5"
materials_file.export_to_xml()

############
# Geometry #
############

s_fuel = openmc.Sphere(surface_id=1, x0=0, y0=0, z0=0, R=0.4096, name='fuel')
s_xmin = openmc.XPlane(surface_id=2, x0=-0.63, name='xmin')
s_xmax = openmc.XPlane(surface_id=3, x0=0.63, name='xmax')
s_ymin = openmc.YPlane(surface_id=4, y0=-0.63, name='ymin')
s_ymax = openmc.YPlane(surface_id=5, y0=0.63, name='ymax')
s_zmin = openmc.ZPlane(surface_id=6, z0=-0.63, name='zmin')
s_zmax = openmc.ZPlane(surface_id=7, z0=0.63, name='zmin')

s_xmin.boundary_type = 'reflective'
s_xmax.boundary_type = 'reflective'
s_ymin.boundary_type = 'reflective'
s_ymax.boundary_type = 'reflective'
s_zmin.boundary_type = 'reflective'
s_zmax.boundary_type = 'reflective'

c_fuel = openmc.Cell(cell_id=1, name='fuel')
c_mod = openmc.Cell(cell_id=2, name='mod')

c_fuel.region = -s_fuel
c_mod.region = +s_fuel & +s_xmin & -s_xmax & +s_ymin & -s_ymax & +s_zmin & -s_zmax

c_fuel.fill = m_fuel
c_mod.fill = m_mod

root = openmc.Universe(universe_id=0, name='root')
root.add_cells([c_fuel, c_mod])

geometry = openmc.Geometry(root)
geometry.export_to_xml()

############
# Settings #
############

settings_file = openmc.Settings()
settings_file.energy_mode = "multi-group"
settings_file.batches = 200
settings_file.inactive = 50
settings_file.particles = int(1e7)

bounds = [-0.42, -0.42, -0.42, 0.42, 0.42, 0.42]
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

# sp = openmc.StatePoint("statepoint.{}.h5".format(settings_file.batches))
