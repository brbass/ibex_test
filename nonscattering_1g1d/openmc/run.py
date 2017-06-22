import numpy as np

import openmc
import openmc.mgxs

###############################################################################
#                      Simulation Input File Parameters
###############################################################################

# OpenMC simulation parameters
batches = 200
inactive = 50
particles = int(1e4)

###############################################################################
#                 Exporting to OpenMC mgxs.h5 file
###############################################################################

# Instantiate the energy group data
groups = openmc.mgxs.EnergyGroups(group_edges=[1e-5, 2.0e6])

# Instantiate the cross section data
fuel_xsdata = openmc.XSdata('fuel', groups)
fuel_xsdata.order = 1
fuel_xsdata.set_total([1.0])
fuel_xsdata.set_absorption([1.0])
fuel_xsdata.set_scatter_matrix([[[0.0, 0.0]]])
fuel_xsdata.set_fission([0.5])
fuel_xsdata.set_nu_fission([1.0])
fuel_xsdata.set_chi([1.0])

mg_cross_sections_file = openmc.MGXSLibrary(groups)
mg_cross_sections_file.add_xsdatas([fuel_xsdata])
mg_cross_sections_file.export_to_hdf5()

###############################################################################
#                 Exporting to OpenMC materials.xml file
###############################################################################

# Instantiate some Macroscopic Data
fuel_data = openmc.Macroscopic('fuel')

# Instantiate some Materials and register the appropriate Macroscopic objects
fuel_mat = openmc.Material(material_id=1, name='fuel')
fuel_mat.set_density('macro', 1.0)
fuel_mat.add_macroscopic(fuel_data)

# Instantiate a Materials collection and export to XML
materials_file = openmc.Materials([fuel_mat])
materials_file.cross_sections = "./mgxs.h5"
materials_file.export_to_xml()

###############################################################################
#                 Exporting to OpenMC geometry.xml file
###############################################################################

# Instantiate ZCylinder surfaces
xmin = openmc.XPlane(surface_id=4, x0=-0.627, name='xmin')
xmax = openmc.XPlane(surface_id=5, x0=0.627, name='xmax')
ymin = openmc.YPlane(surface_id=4, y0=-0.627, name='ymin')
ymax = openmc.YPlane(surface_id=5, y0=0.627, name='ymax')
zmin = openmc.ZPlane(surface_id=4, z0=-0.627, name='zmin')
zmax = openmc.ZPlane(surface_id=5, z0=0.627, name='zmax')

xmin.boundary_type = 'vacuum'
xmax.boundary_type = 'vacuum'
ymin.boundary_type = 'reflective'
ymax.boundary_type = 'reflective'
zmin.boundary_type = 'reflective'
zmax.boundary_type = 'reflective'

# Instantiate Cells
fuel_cell = openmc.Cell(cell_id=1, name='fuel cell')

# Use surface half-spaces to define regions
fuel_cell.region = +xmin & -xmax & +ymin & -ymax & +zmin & - zmax

# Register Materials with Cells
fuel_cell.fill = fuel_mat

# Instantiate Universe
root = openmc.Universe(universe_id=0, name='root universe')

# Register Cells with Universe
root.add_cells([fuel_cell])

# Instantiate a Geometry, register the root Universe, and export to XML
geometry = openmc.Geometry(root)
geometry.export_to_xml()

###############################################################################
#                   Exporting to OpenMC settings.xml file
###############################################################################

# Instantiate a Settings object, set all runtime parameters, and export to XML
settings_file = openmc.Settings()
settings_file.energy_mode = "multi-group"
settings_file.batches = batches
settings_file.inactive = inactive
settings_file.particles = particles

# Create an initial uniform spatial source distribution over fissionable zones
bounds = [-0.627, -0.627, -0.627, 0.627, 0.627, 0.627]
uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:], only_fissionable=True)
settings_file.source = openmc.source.Source(space=uniform_dist)

settings_file.export_to_xml()

###############################################################################
#                   Run OpenMC
###############################################################################

openmc.run(threads=4)

###############################################################################
#                   Post-Processing
###############################################################################

statepoint = openmc.StatePoint('statepoint.{}.h5'.format(batches))

# print(statepoint.k_combined)
