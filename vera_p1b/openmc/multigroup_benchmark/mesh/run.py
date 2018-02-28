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
xs_fuel.set_total([0.399697649, 0.581826884])
xs_fuel.set_scatter_matrix([[[0.383829618, 0.049482651], [0.000830382, -0.000261476]],
                            [[0.0, 0.0], [0.405420306, 0.006013128]]])
xs_fuel.set_absorption([0.015034826, 0.176411437])
xs_fuel.set_nu_fission([[0.013687612, 0.000000015],
                        [0.255838918, 0.000000189]])

xs_gap = openmc.XSdata('gap', groups)
xs_gap.order = 1
xs_gap.set_total([0.000060070, 0.000021458])
xs_gap.set_scatter_matrix([[[0.000059744, 0.000011213], [0.000000396, -0.000000063]],
                            [[0.0, 0.0], [0.000021460, -0.000000063]]])
xs_gap.set_absorption([0.0, 0.0])
xs_gap.set_nu_fission([[0.0, 0.0],
                        [0.0, 0.0]])

xs_clad = openmc.XSdata('clad', groups)
xs_clad.order = 1
xs_clad.set_total([0.319205599, 0.297115812])
xs_clad.set_scatter_matrix([[[0.317083075, 0.052759371], [0.000287583, -0.000078648]],
                            [[0.0, 0.0], [0.294003048, 0.002146731]]])
xs_clad.set_absorption([0.001839085, 0.003113031])
xs_clad.set_nu_fission([[0.0, 0.0],
                        [0.0, 0.0]])

xs_mod = openmc.XSdata('moderator', groups)
xs_mod.order = 1
xs_mod.set_total([0.528320878, 1.316352822])
xs_mod.set_scatter_matrix([[[0.486251066, 0.290403747], [0.041923677, 0.018069833]],
                            [[0.000000031, 0.000000031], [1.301429236, 0.523147177]]])
xs_mod.set_absorption([0.000151816, 0.014922417])
xs_mod.set_nu_fission([[0.0, 0.0],
                        [0.0, 0.0]])

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

s_fuel = openmc.ZCylinder(surface_id=1, x0=0, y0=0, R=0.4096, name='fuel')
s_gap = openmc.ZCylinder(surface_id=2, x0=0, y0=0, R=0.418, name='gap')
s_clad = openmc.ZCylinder(surface_id=3, x0=0, y0=0, R=0.475, name='clad')
s_xmin = openmc.XPlane(surface_id=5, x0=-0.63, name='xmin')
s_xmax = openmc.XPlane(surface_id=6, x0=0.63, name='xmax')
s_ymin = openmc.YPlane(surface_id=7, y0=-0.63, name='ymin')
s_ymax = openmc.YPlane(surface_id=8, y0=0.63, name='ymax')
s_zmin = openmc.ZPlane(surface_id=9, z0=-6300, name='zmin')
s_zmax = openmc.ZPlane(surface_id=10, z0=6300, name='zmax')

s_xmin.boundary_type = 'reflective'
s_xmax.boundary_type = 'reflective'
s_ymin.boundary_type = 'reflective'
s_ymax.boundary_type = 'reflective'
s_zmin.boundary_type = 'reflective'
s_zmax.boundary_type = 'reflective'

c_fuel = openmc.Cell(cell_id=1, name='fuel')
c_gap = openmc.Cell(cell_id=2, name='gap')
c_clad = openmc.Cell(cell_id=3, name='clad')
c_mod = openmc.Cell(cell_id=4, name='mod')

c_fuel.region = -s_fuel & +s_zmin & -s_zmax
c_gap.region = +s_fuel & -s_gap & +s_zmin & -s_zmax
c_clad.region = +s_gap & -s_clad & +s_zmin & -s_zmax
c_mod.region = +s_clad & +s_xmin & -s_xmax & +s_ymin & -s_ymax & +s_zmin & -s_zmax

c_fuel.fill = m_fuel
c_gap.fill = m_gap
c_clad.fill = m_clad
c_mod.fill = m_mod

root = openmc.Universe(universe_id=0, name='root')
root.add_cells([c_fuel, c_gap, c_clad, c_mod])

geometry = openmc.Geometry(root)
geometry.export_to_xml()

###########
# Tallies #
###########

mesh = openmc.Mesh()
mesh.dimension = [100, 100, 1]
mesh.lower_left = [-0.63, -0.63, -6300]
mesh.upper_right = [0.63, 0.63, 6300]

mesh_filter = openmc.MeshFilter(mesh)

energy_filter = openmc.EnergyFilter(groups.group_edges)

tally = openmc.Tally(name='flux')
tally.filters = [mesh_filter, energy_filter]
tally.scores = ['flux-Y1', 'fission']

tallies_file = openmc.Tallies()
tallies_file.append(tally)
tallies_file.export_to_xml()

############
# Settings #
############

settings_file = openmc.Settings()
settings_file.energy_mode = "multi-group"
settings_file.batches = 200
settings_file.inactive = 50
settings_file.particles = int(1e5)

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
