import numpy as np
import matplotlib.pyplot as plt

import openmc
import openmc.mgxs as mgxs

#############################
# Multigroup cross sections #
#############################

groups = mgxs.EnergyGroups(group_edges=[0., 2.0e7])

xs_pu = openmc.XSdata('pu', groups)
xs_pu.order = 1
xs_pu.set_total([0.322644801])
xs_pu.set_scatter_matrix([[[0.255040685, 0.094644991]]])
xs_pu.set_absorption([0.067603418])
xs_pu.set_nu_fission([[0.201891561]])

xs_th = openmc.XSdata('th', groups)
xs_th.order = 1
xs_th.set_total([0.290248656])
xs_th.set_scatter_matrix([[[0.284558789, 0.060957181]]])
xs_th.set_absorption([0.005690072])
xs_th.set_nu_fission([[0.000973016]])

mg_cross_sections_file = openmc.MGXSLibrary(groups)
mg_cross_sections_file.add_xsdatas([xs_pu, xs_th])
mg_cross_sections_file.export_to_hdf5()

#############
# Materials #
#############

mac_pu = openmc.Macroscopic('pu')
m_pu = openmc.Material(material_id=1, name='pu')
m_pu.set_density('macro', 1.0)
m_pu.add_macroscopic(mac_pu)

mac_th = openmc.Macroscopic('th')
m_th = openmc.Material(material_id=2, name='th')
m_th.set_density('macro', 1.0)
m_th.add_macroscopic(mac_th)

materials_file = openmc.Materials([m_pu, m_th])
materials_file.cross_sections = "./mgxs.h5"
materials_file.export_to_xml()

############
# Geometry #
############

rabc = np.power([1./4.3652, 1./5.2382, 1./6.5478], 2)
s_pu = openmc.Quadric(surface_id=1, a=rabc[0], b=rabc[1], c=rabc[2], k=-1.0, name='pu')

labc = np.array([40.4568, 48.5482, 60.6852])
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

root = openmc.Universe(universe_id=1, name='root')
root.add_cells([c_pu, c_th])

geometry = openmc.Geometry(root)
geometry.export_to_xml()

###########
# Tallies #
###########

mesh = openmc.Mesh()
mesh.dimension = [20, 24, 30]
mesh.lower_left = -labc / 2
mesh.upper_right = labc / 2

mesh_filter = openmc.MeshFilter(mesh)

tally = openmc.Tally(name='flux')
tally.filters = [mesh_filter]
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
settings_file.particles = int(1e7)

bounds = [-5., -6., -7., 5., 6., 7.]
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
