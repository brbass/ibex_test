import numpy as np
import matplotlib.pyplot as plt

import openmc
import openmc.mgxs as mgxs

############
# Nuclides #
############

n_Pu239 = openmc.Nuclide('Pu239')
n_Pu240 = openmc.Nuclide('Pu240')
n_Pu241 = openmc.Nuclide('Pu241')
# n_Ga69 = openmc.Nuclide('Ga69')
# n_Ga71 = openmc.Nuclide('Ga71')
n_Ga = openmc.Element('Ga')
n_Th = openmc.Nuclide('Th232')

#############
# Materials #
#############

m_pu = openmc.Material(name='pu', temperature=293.6)
m_pu.set_density('g/cc', 15.29)
m_pu.add_nuclide(n_Pu239, 3.6049e-2)
m_pu.add_nuclide(n_Pu240, 1.9562e-3)
m_pu.add_nuclide(n_Pu241, 1.3338e-4)
m_pu.add_element(n_Ga, 1.3338e-3)

m_th = openmc.Material(name='th', temperature=293.6)
m_th.set_density('g/cc', 11.58)
m_th.add_nuclide(n_Th, 1.0)

materials_file = openmc.Materials([m_pu, m_th])
materials_file.export_to_xml()

############
# Geometry #
############

rabc = np.power([1./4.3652, 1./5.2382, 1./6.5478], 2)
s_pu = openmc.Quadric(surface_id=1, a=rabc[0], b=rabc[1], c=rabc[2], k=-1.0, name='pu')
#s_pu = openmc.Sphere(surface_id=1, R=6.0)

labc = [40.4568, 48.5482, 60.6852]
s_xmin = openmc.XPlane(surface_id=2, x0=-labc[0]/2, name='xmin')
s_xmax = openmc.XPlane(surface_id=3, x0=labc[0]/2, name='xmax')
s_ymin = openmc.YPlane(surface_id=4, y0=-labc[1]/2, name='ymin')
s_ymax = openmc.YPlane(surface_id=5, y0=labc[1]/2, name='ymax')
s_zmin = openmc.ZPlane(surface_id=6, z0=-labc[2]/2, name='zmin')
s_zmax = openmc.ZPlane(surface_id=7, z0=labc[2]/2, name='zmax')

s_xmin.boundary_type = 'vacuum'
s_xmax.boundary_type = 'vacuum'
s_ymin.boundary_type = 'vacuum'
s_ymax.boundary_type = 'vacuum'
s_zmin.boundary_type = 'vacuum'
s_zmax.boundary_type = 'vacuum'

c_pu = openmc.Cell(cell_id=1, name='pu')
c_th = openmc.Cell(cell_id=2, name='th')

c_pu.region = -s_pu
c_th.region = +s_pu & +s_xmin & -s_xmax & +s_ymin & -s_ymax & +s_zmin & -s_zmax

c_pu.fill = m_pu
c_th.fill = m_th

root = openmc.Universe(universe_id=0, name='root')
root.add_cells([c_pu, c_th])

geometry = openmc.Geometry(root)
geometry.export_to_xml()

############
# Settings #
############

settings_file = openmc.Settings()
settings_file.batches = 200
settings_file.inactive = 50
settings_file.particles = int(1e7)

bounds = [-5., -6., -7., 5., 6., 7.]
uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:])
settings_file.source = openmc.source.Source(space=uniform_dist)
settings_file.export_to_xml()

#############################
# Multigroup cross sections #
#############################

groups = mgxs.EnergyGroups()
groups.group_edges = np.array([0., 2.0e7])#np.array([0., 1.0e5, 2.0e7])

tallies_file = openmc.Tallies()

xs_store = []

for cell in [c_pu, c_th]:
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
