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
xs_fuel.set_total([0.401619210, 0.563859308])
xs_fuel.set_scatter_matrix([[[0.385045400, 0.049995743], [0.000805057, -0.000257614]],
                            [[0.0, 0.0], [0.403512783, 0.005676677]]])
xs_fuel.set_absorption([0.015771915, 0.160395302])
xs_fuel.set_nu_fission([[0.013865154, 0.000000015],
                        [0.208251042, 0.000000155]])

xs_ifba = openmc.XSdata('ifba', groups)
xs_ifba.order = 1
xs_ifba.set_total([0.400068065, 18.782435513])
xs_ifba.set_scatter_matrix([[[0.272554529, 0.038063324], [0.001166271, -0.000339365]],
                            [[0.0, 0.0], [0.285776128, 0.009928280]]])
xs_ifba.set_absorption([0.126362189, 18.496500773])
xs_ifba.set_nu_fission([[0.0, 0.0],
                        [0.0, 0.0]])

xs_gap = openmc.XSdata('gap', groups)
xs_gap.order = 1
xs_gap.set_total([0.000060758, 0.000021811])
xs_gap.set_scatter_matrix([[[0.000059793, 0.000011277], [0.000000401, -0.000000075]],
                           [[0.0, 0.0], [0.000021778, 0.000003630]]])
xs_gap.set_absorption([0.0, 0.0])
xs_gap.set_nu_fission([[0.0, 0.0],
                        [0.0, 0.0]])

xs_clad = openmc.XSdata('clad', groups)
xs_clad.order = 1
xs_clad.set_total([0.318118514, 0.296462951])
xs_clad.set_scatter_matrix([[[0.316006772, 0.053046979], [0.000282946, -0.000074858]],
                            [[0.0, 0.0], [0.293734642, 0.002157170]]])
xs_clad.set_absorption([0.001828382, 0.002728367])
xs_clad.set_nu_fission([[0.0, 0.0],
                        [0.0, 0.0]])

xs_mod = openmc.XSdata('moderator', groups)
xs_mod.order = 1
xs_mod.set_total([0.589009186, 1.403414263])
xs_mod.set_scatter_matrix([[[0.542417092, 0.323740085], [0.046425726, 0.019997399]],
                           [[0.000000039, 0.000000039], [1.389298953, 0.598440853]]])
xs_mod.set_absorption([0.000172240, 0.014117546])
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
s_xmin = openmc.XPlane(surface_id=5, x0=-0.63, name='xmin')
s_xmax = openmc.XPlane(surface_id=6, x0=0.63, name='xmax')
s_ymin = openmc.YPlane(surface_id=7, y0=-0.63, name='ymin')
s_ymax = openmc.YPlane(surface_id=8, y0=0.63, name='ymax')
s_zmin = openmc.ZPlane(surface_id=9, z0=-0.63, name='zmin')
s_zmax = openmc.ZPlane(surface_id=10, z0=0.63, name='zmax')

s_xmin.boundary_type = 'reflective'
s_xmax.boundary_type = 'reflective'
s_ymin.boundary_type = 'reflective'
s_ymax.boundary_type = 'reflective'
s_zmin.boundary_type = 'reflective'
s_zmax.boundary_type = 'reflective'

c_fuel = openmc.Cell(cell_id=1, name='fuel')
c_ifba = openmc.Cell(cell_id=2, name='ifba')
c_gap = openmc.Cell(cell_id=3, name='gap')
c_clad = openmc.Cell(cell_id=4, name='clad')
c_mod = openmc.Cell(cell_id=5, name='mod')

c_fuel.region = -s_fuel & +s_zmin & -s_zmax
c_ifba.region = +s_fuel & -s_ifba & +s_zmin & -s_zmax
c_gap.region = +s_ifba & -s_gap & +s_zmin & -s_zmax
c_clad.region = +s_gap & -s_clad & +s_zmin & -s_zmax
c_mod.region = +s_clad & +s_xmin & -s_xmax & +s_ymin & -s_ymax & +s_zmin & -s_zmax

c_fuel.fill = m_fuel
c_ifba.fill = m_ifba
c_gap.fill = m_gap
c_clad.fill = m_clad
c_mod.fill = m_mod

root = openmc.Universe(universe_id=0, name='root')
root.add_cells([c_fuel, c_ifba, c_gap, c_clad, c_mod])

geometry = openmc.Geometry(root)
geometry.export_to_xml()

###########
# Tallies #
###########

mesh = openmc.Mesh()
mesh.dimension = [20, 20, 1]
mesh.lower_left = [-0.63, -0.63, -0.63]
mesh.upper_right = [0.63, 0.63, 0.63]

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

openmc.run(threads=8)

################
# Load results #
################

# sp = openmc.StatePoint("statepoint.{}.h5".format(settings_file.batches))
