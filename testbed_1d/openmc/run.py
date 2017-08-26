import numpy as np
import matplotlib.pyplot as plt

import openmc
import openmc.mgxs as mgxs

#############################
# Multigroup cross sections #
#############################

groups = mgxs.EnergyGroups(group_edges=[0., 2.0e7])

xs_fuel = openmc.XSdata('fuel', groups)
xs_fuel.order = 1
xs_fuel.set_total([1.0])
xs_fuel.set_scatter_matrix([[[0.8, 0.1]]])
xs_fuel.set_absorption([0.2])
xs_fuel.set_nu_fission([[0.4]])

xs_gap = openmc.XSdata('gap', groups)
xs_gap.order = 1
xs_gap.set_total([0.0001])
xs_gap.set_scatter_matrix([[[0.0001, 0.00001]]])
xs_gap.set_absorption([0.0])
xs_gap.set_nu_fission([[0.0]])

xs_clad = openmc.XSdata('clad', groups)
xs_clad.order = 1
xs_clad.set_total([0.3])
xs_clad.set_scatter_matrix([[[0.3, 0.01]]])
xs_clad.set_absorption([0.0])
xs_clad.set_nu_fission([[0.0]])

xs_mod = openmc.XSdata('moderator', groups)
xs_mod.order = 1
xs_mod.set_total([10.0])
xs_mod.set_scatter_matrix([[[5.0, 1.0]]])
xs_mod.set_absorption([5.0])
xs_mod.set_nu_fission([[0.0]])

mg_cross_sections_file = openmc.MGXSLibrary(groups)
mg_cross_sections_file.add_xsdatas([xs_fuel, xs_gap, xs_clad, xs_mod])
mg_cross_sections_file.export_to_hdf5()

#############
# Materials #
#############

mac_fuel = openmc.Macroscopic('fuel')
m_fuel = openmc.Material(material_id=1, name='fuel')
m_fuel.set_density('macro', 1.0)
m_fuel.add_macroscopic(mac_fuel)

mac_gap = openmc.Macroscopic('gap')
m_gap = openmc.Material(material_id=2, name='gap')
m_gap.set_density('macro', 1.0)
m_gap.add_macroscopic(mac_gap)

mac_clad = openmc.Macroscopic('clad')
m_clad = openmc.Material(material_id=3, name='clad')
m_clad.set_density('macro', 1.0)
m_clad.add_macroscopic(mac_clad)

mac_mod = openmc.Macroscopic('moderator')
m_mod = openmc.Material(material_id=4, name='mod')
m_mod.set_density('macro', 1.0)
m_mod.add_macroscopic(mac_mod)

materials_file = openmc.Materials([m_fuel, m_gap, m_clad, m_mod])
materials_file.cross_sections = "./mgxs.h5"
materials_file.export_to_xml()

############
# Geometry #
############

s_0 = openmc.XPlane(surface_id=1, x0=0.0, name='s0')
s_1 = openmc.XPlane(surface_id=2, x0=1.0, name='s1')
s_2 = openmc.XPlane(surface_id=3, x0=1.1, name='s2')
s_3 = openmc.XPlane(surface_id=4, x0=1.4, name='s3')
s_4 = openmc.XPlane(surface_id=5, x0=3.0, name='s4')

s_0.boundary_type = 'reflective'
s_4.boundary_type = 'vacuum'

c_fuel = openmc.Cell(cell_id=1, name='fuel')
c_gap = openmc.Cell(cell_id=2, name='gap')
c_clad = openmc.Cell(cell_id=3, name='clad')
c_mod = openmc.Cell(cell_id=4, name='mod')

c_fuel.region = +s_0 & -s_1
c_gap.region = +s_1 & -s_2
c_clad.region = +s_2 & -s_3
c_mod.region =  +s_3 & -s_4

c_fuel.fill = m_fuel
c_gap.fill = m_gap
c_clad.fill = m_clad
c_mod.fill = m_mod

root = openmc.Universe(universe_id=0, name='root')
root.add_cells([c_fuel, c_gap, c_clad, c_mod])

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

#openmc.run(threads=4)

################
# Load results #
################

sp = openmc.StatePoint("statepoint.{}.h5".format(settings_file.batches))
print(sp.k_combined)
