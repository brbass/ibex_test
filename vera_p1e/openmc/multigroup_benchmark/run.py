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

xs_ifba = openmc.XSdata('ifba', groups)
xs_ifba.order = 1
xs_ifba.set_total([0.400687673, 18.807866148])
xs_ifba.set_scatter_matrix([[[0.272518929, 0.038021479], [0.001179693, -0.000343355]],
                            [[0.0, 0.0], [0.284174375, 0.009850593]]])
xs_ifba.set_absorption([0.127074818, 18.523609366])
xs_ifba.set_nu_fission([[0.0, 0.0],
                        [0.0, 0.0]])

xs_gap = openmc.XSdata('gap', groups)
xs_gap.order = 1
xs_gap.set_total([0.000060712, 0.000021233])
xs_gap.set_scatter_matrix([[[0.000060487, 0.000011767], [0.000000400, -0.000000079]],
                           [[0.0, 0.0], [0.000021243, 0.000003495]]])
xs_gap.set_absorption([0.0, 0.0])
xs_gap.set_nu_fission([[0.0, 0.0],
                        [0.0, 0.0]])

xs_clad = openmc.XSdata('clad', groups)
xs_clad.order = 1
xs_clad.set_total([0.318128762, 0.296467308])
xs_clad.set_scatter_matrix([[[0.316009612, 0.052994156], [0.000284867, -0.000078583]],
                            [[0.0, 0.0], [0.293736124, 0.002164244]]])
xs_clad.set_absorption([0.001835039, 0.002731249])
xs_clad.set_nu_fission([[0.0, 0.0],
                        [0.0, 0.0]])

xs_mod = openmc.XSdata('moderator', groups)
xs_mod.order = 1
xs_mod.set_total([0.589533143, 1.404056519])
xs_mod.set_scatter_matrix([[[0.542576514, 0.323899243], [0.046780637, 0.020173486]],
                            [[0.000000034, 0.000000034], [1.389920798, 0.598442391]]])
xs_mod.set_absorption([0.000172617, 0.014134002])
xs_mod.set_nu_fission([[0.0, 0.0],
                        [0.0, 0.0]])

mg_cross_sections_file = openmc.MGXSLibrary(groups)
mg_cross_sections_file.add_xsdatas([xs_fuel, xs_ifba, xs_gap, xs_clad, xs_mod])
mg_cross_sections_file.export_to_hdf5()

#############
# Materials #
#############

mac_fuel = openmc.Macroscopic('fuel')
m_fuel = openmc.Material(material_id=1, name='fuel')
m_fuel.set_density('macro', 1.0)
m_fuel.add_macroscopic(mac_fuel)

mac_ifba = openmc.Macroscopic('ifba')
m_ifba = openmc.Material(material_id=2, name='ifba')
m_ifba.set_density('macro', 1.0)
m_ifba.add_macroscopic(mac_ifba)

mac_gap = openmc.Macroscopic('gap')
m_gap = openmc.Material(material_id=3, name='gap')
m_gap.set_density('macro', 1.0)
m_gap.add_macroscopic(mac_gap)

mac_clad = openmc.Macroscopic('clad')
m_clad = openmc.Material(material_id=4, name='clad')
m_clad.set_density('macro', 1.0)
m_clad.add_macroscopic(mac_clad)

mac_mod = openmc.Macroscopic('moderator')
m_mod = openmc.Material(material_id=5, name='mod')
m_mod.set_density('macro', 1.0)
m_mod.add_macroscopic(mac_mod)

materials_file = openmc.Materials([m_fuel, m_ifba, m_gap, m_clad, m_mod])
materials_file.cross_sections = "./mgxs.h5"
materials_file.export_to_xml()

############
# Geometry #
############

s_fuel = openmc.ZCylinder(surface_id=1, x0=0, y0=0, R=0.4096, name='fuel')
s_ifba = openmc.ZCylinder(surface_id=2, x0=0, y0=0, R=0.4106, name='ifba')
s_gap = openmc.ZCylinder(surface_id=3, x0=0, y0=0, R=0.418, name='gap')
s_clad = openmc.ZCylinder(surface_id=4, x0=0, y0=0, R=0.475, name='clad')
s_left = openmc.XPlane(surface_id=5, x0=-0.63, name='left')
s_right = openmc.XPlane(surface_id=6, x0=0.63, name='right')
s_bot = openmc.YPlane(surface_id=7, y0=-0.63, name='bottom')
s_top = openmc.YPlane(surface_id=8, y0=0.63, name='top')

s_left.boundary_type = 'reflective'
s_right.boundary_type = 'reflective'
s_top.boundary_type = 'reflective'
s_bot.boundary_type = 'reflective'

c_fuel = openmc.Cell(cell_id=1, name='fuel')
c_ifba = openmc.Cell(cell_id=2, name='ifba')
c_gap = openmc.Cell(cell_id=3, name='gap')
c_clad = openmc.Cell(cell_id=4, name='clad')
c_mod = openmc.Cell(cell_id=5, name='mod')

c_fuel.region = -s_fuel
c_ifba.region = +s_fuel & -s_ifba
c_gap.region = +s_ifba & -s_gap
c_clad.region = +s_gap & -s_clad
c_mod.region = +s_clad & +s_left & -s_right & +s_bot & -s_top

c_fuel.fill = m_fuel
c_ifba.fill = m_ifba
c_gap.fill = m_gap
c_clad.fill = m_clad
c_mod.fill = m_mod

root = openmc.Universe(universe_id=0, name='root')
root.add_cells([c_fuel, c_ifba, c_gap, c_clad, c_mod])

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