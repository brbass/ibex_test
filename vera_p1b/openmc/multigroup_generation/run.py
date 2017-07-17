import numpy as np
import matplotlib.pyplot as plt

import openmc
import openmc.mgxs as mgxs

############
# Nuclides #
############

n1001 = openmc.Nuclide('H1')
n2004 = openmc.Nuclide('He4')
n5010 = openmc.Nuclide('B10')
n5011 = openmc.Nuclide('B11')
n8016 = openmc.Nuclide('O16')
n24050 = openmc.Nuclide('Cr50')
n24052 = openmc.Nuclide('Cr52')
n24053 = openmc.Nuclide('Cr53')
n24054 = openmc.Nuclide('Cr54')
n26054 = openmc.Nuclide('Fe54')
n26056 = openmc.Nuclide('Fe56')
n26057 = openmc.Nuclide('Fe57')
n26058 = openmc.Nuclide('Fe58')
n40090 = openmc.Nuclide('Zr90')
n40091 = openmc.Nuclide('Zr91')
n40092 = openmc.Nuclide('Zr92')
n40094 = openmc.Nuclide('Zr94')
n40096 = openmc.Nuclide('Zr96')
n50112 = openmc.Nuclide('Sn112')
n50114 = openmc.Nuclide('Sn114')
n50115 = openmc.Nuclide('Sn115')
n50116 = openmc.Nuclide('Sn116')
n50117 = openmc.Nuclide('Sn117')
n50118 = openmc.Nuclide('Sn118')
n50119 = openmc.Nuclide('Sn119')
n50120 = openmc.Nuclide('Sn120')
n50122 = openmc.Nuclide('Sn122')
n50124 = openmc.Nuclide('Sn124')
n72174 = openmc.Nuclide('Hf174')
n72176 = openmc.Nuclide('Hf176')
n72177 = openmc.Nuclide('Hf177')
n72178 = openmc.Nuclide('Hf178')
n72179 = openmc.Nuclide('Hf179')
n72180 = openmc.Nuclide('Hf180')
n92234 = openmc.Nuclide('U234')
n92235 = openmc.Nuclide('U235')
n92236 = openmc.Nuclide('U236')
n92238 = openmc.Nuclide('U238')

#############
# Materials #
#############

m_fuel = openmc.Material(name='fuel', temperature=600)
m_fuel.set_density('g/cc', 10.257)
m_fuel.add_nuclide(n8016,  4.57642e-02)
m_fuel.add_s_alpha_beta('c_O_in_UO2')
m_fuel.add_nuclide(n92234, 6.11864e-06)
m_fuel.add_nuclide(n92235, 7.18132e-04)
m_fuel.add_nuclide(n92236, 3.29861e-06)
m_fuel.add_nuclide(n92238, 2.21546e-02)
m_fuel.add_s_alpha_beta('c_U_in_UO2')

m_gap = openmc.Material(name='gap', temperature=600)
m_gap.set_density('g/cc', 0.0001786)
m_gap.add_nuclide(n2004, 2.68714e-05)

m_clad = openmc.Material(name='cladding', temperature=600)
m_clad.set_density('g/cc', 6.56)
m_clad.add_nuclide(n24050, 3.30121e-06)
m_clad.add_nuclide(n24052, 6.36606e-05)
m_clad.add_nuclide(n24053, 7.21860e-06)
m_clad.add_nuclide(n24054, 1.79686e-06)
m_clad.add_nuclide(n26054, 8.68307e-06)
m_clad.add_nuclide(n26056, 1.36306e-04)
m_clad.add_nuclide(n26057, 3.14789e-06)
m_clad.add_nuclide(n26058, 4.18926e-07)
m_clad.add_nuclide(n40090, 2.18865e-02)
m_clad.add_nuclide(n40091, 4.77292e-03)
m_clad.add_nuclide(n40092, 7.29551e-03)
m_clad.add_nuclide(n40094, 7.39335e-03)
m_clad.add_nuclide(n40096, 1.19110e-03)
m_clad.add_nuclide(n50112, 4.68066e-06)
m_clad.add_nuclide(n50114, 3.18478e-06)
m_clad.add_nuclide(n50115, 1.64064e-06)
m_clad.add_nuclide(n50116, 7.01616e-05)
m_clad.add_nuclide(n50117, 3.70592e-05)
m_clad.add_nuclide(n50118, 1.16872e-04)
m_clad.add_nuclide(n50119, 4.14504e-05)
m_clad.add_nuclide(n50120, 1.57212e-04)
m_clad.add_nuclide(n50122, 2.23417e-05)
m_clad.add_nuclide(n50124, 2.79392e-05)
m_clad.add_nuclide(n72174, 3.54138e-09)
m_clad.add_nuclide(n72176, 1.16423e-07)
m_clad.add_nuclide(n72177, 4.11686e-07)
m_clad.add_nuclide(n72178, 6.03806e-07)
m_clad.add_nuclide(n72179, 3.01460e-07)
m_clad.add_nuclide(n72180, 7.76449e-07)

m_mod = openmc.Material(name='moderator', temperature=600)
m_mod.set_density('g/cc', 0.661)
m_mod.add_nuclide(n1001, 4.41459e-02)
m_mod.add_s_alpha_beta('c_H_in_H2O')
m_mod.add_nuclide(n5010, 9.52537e-06)
m_mod.add_nuclide(n5011, 3.83408e-05)
m_mod.add_nuclide(n8016, 2.20729e-02)

# m_ifba = openmc.Material(name='ifba', temperature=600)
# m_ifba.set_density('g/cc', 3.85)
# m_ifba.add_nuclide(n5010, 2.16410e-02)
# m_ifba.add_nuclide(n5011, 1.96824e-02)
# m_ifba.add_nuclide(n40090, 1.06304e-02)
# m_ifba.add_nuclide(n40091, 2.31824e-03)
# m_ifba.add_nuclide(n40092, 3.54348e-03)
# m_ifba.add_nuclide(n40094, 3.59100e-03)
# m_ifba.add_nuclide(n40096, 5.78528e-04)

materials_file = openmc.Materials([m_fuel, m_gap, m_clad, m_mod])
materials_file.export_to_xml()

############
# Geometry #
############

s_fuel = openmc.ZCylinder(surface_id=1, x0=0, y0=0, R=0.4096, name='fuel')
s_gap = openmc.ZCylinder(surface_id=2, x0=0, y0=0, R=0.418, name='gap')
s_clad = openmc.ZCylinder(surface_id=3, x0=0, y0=0, R=0.475, name='clad')
s_left = openmc.XPlane(surface_id=4, x0=-0.63, name='left')
s_right = openmc.XPlane(surface_id=5, x0=0.63, name='right')
s_bot = openmc.YPlane(surface_id=6, y0=-0.63, name='bottom')
s_top = openmc.YPlane(surface_id=7, y0=0.63, name='top')

s_left.boundary_type = 'reflective'
s_right.boundary_type = 'reflective'
s_top.boundary_type = 'reflective'
s_bot.boundary_type = 'reflective'

c_fuel = openmc.Cell(cell_id=1, name='fuel')
c_gap = openmc.Cell(cell_id=2, name='gap')
c_clad = openmc.Cell(cell_id=3, name='clad')
c_mod = openmc.Cell(cell_id=4, name='mod')

c_fuel.region = -s_fuel
c_gap.region = +s_fuel & -s_gap
c_clad.region = +s_gap & -s_clad
c_mod.region = +s_clad & +s_left & -s_right & +s_bot & -s_top

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
settings_file.batches = 200
settings_file.inactive = 50
settings_file.particles = int(1e7)

bounds = [-0.41, -0.41, -0.41, 0.41, 0.41, 0.41]
uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:])
settings_file.source = openmc.source.Source(space=uniform_dist)
settings_file.export_to_xml()

#############################
# Multigroup cross sections #
#############################

groups = mgxs.EnergyGroups()
groups.group_edges = np.array([0., 1.0e2, 2.0e7])

tallies_file = openmc.Tallies()

xs_store = []

for cell in [c_fuel, c_gap, c_clad, c_mod]:
    sigma_t = mgxs.TotalXS(domain=cell, groups=groups, name="{}-sigma_t".format(cell.name))
    sigma_a = mgxs.AbsorptionXS(domain=cell, groups=groups, name="{}-sigma_a".format(cell.name))
    sigma_s = mgxs.ScatterMatrixXS(domain=cell, groups=groups, name="{}-sigma_s".format(cell.name))
    sigma_s.legendre_order = 1
    nu_sigma_f = mgxs.NuFissionMatrixXS(domain=cell, groups=groups, name="{}-nu_sigma_f".format(cell.name))
    
    for xs in [sigma_t, sigma_a, sigma_s, nu_sigma_f]:
        tallies_file += xs.tallies.values()
        xs_store.append(xs)
    
tallies_file.export_to_xml()

#######
# Run #
#######

openmc.run(threads=4)

################
# Load results #
################

sp = openmc.StatePoint("statepoint.{}.h5".format(settings_file.batches))

for xs in xs_store:
    xs.load_from_statepoint(sp)
    xs.export_xs_data(filename=xs.name)
