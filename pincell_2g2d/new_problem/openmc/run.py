import numpy as np

import openmc
import openmc.mgxs

###############################################################################
#                      Simulation Input File Parameters
###############################################################################

# OpenMC simulation parameters
batches = 200
inactive = 50
particles = int(1e5)

###############################################################################
#                 Exporting to OpenMC mgxs.h5 file
###############################################################################

# Instantiate the energy group data
groups = openmc.mgxs.EnergyGroups(group_edges=[1e-5, 1e2, 20.0e6])

# Instantiate the cross section data
fuel_xsdata = openmc.XSdata('fuel', groups)
fuel_xsdata.order = 1
fuel_xsdata.set_total([1.0, 2.0])
fuel_xsdata.set_scatter_matrix([[[0.8, 0.1], [0.03, 0.0]],
                                [[0.0, 0.0], [0.4, 0.0]]])
fuel_xsdata.set_fission([0.1, 0.9])
fuel_xsdata.set_absorption([0.17, 1.6])
fuel_xsdata.set_nu_fission([0.23, 2.07])
fuel_xsdata.set_chi([1.0, 0.0])

clad_xsdata = openmc.XSdata('clad', groups)
clad_xsdata.order = 1
clad_xsdata.set_total([0.2, 0.4])
clad_xsdata.set_scatter_matrix([[[0.1, 0.03], [0.0, 0.0]],
                                [[0.0, 0.0], [0.2, 0.0]]])
clad_xsdata.set_absorption([0.1, 0.2])

mod_xsdata = openmc.XSdata('mod', groups)
mod_xsdata.order = 1
mod_xsdata.set_total([2.0, 4.0])
mod_xsdata.set_scatter_matrix([[[1.84, 0.4], [0.15, 0.001]],
                               [[0.04, 0.0], [3.95, 0.0]]])
mod_xsdata.set_absorption([0.01, 0.01])

mg_cross_sections_file = openmc.MGXSLibrary(groups)
mg_cross_sections_file.add_xsdatas([fuel_xsdata, clad_xsdata, mod_xsdata])
mg_cross_sections_file.export_to_hdf5()

###############################################################################
#                 Exporting to OpenMC materials.xml file
###############################################################################

# Instantiate some Macroscopic Data
fuel_data = openmc.Macroscopic('fuel')
clad_data = openmc.Macroscopic('clad')
mod_data = openmc.Macroscopic('mod')

# Instantiate some Materials and register the appropriate Macroscopic objects
fuel_mat = openmc.Material(material_id=1, name='fuel')
fuel_mat.set_density('macro', 1.0)
fuel_mat.add_macroscopic(fuel_data)

clad_mat = openmc.Material(material_id=2, name='clad')
clad_mat.set_density('macro', 1.0)
clad_mat.add_macroscopic(clad_data)

mod_mat = openmc.Material(material_id=3, name='mod')
mod_mat.set_density('macro', 1.0)
mod_mat.add_macroscopic(mod_data)

# Instantiate a Materials collection and export to XML
materials_file = openmc.Materials([fuel_mat, clad_mat, mod_mat])
materials_file.cross_sections = "./mgxs.h5"
materials_file.export_to_xml()

###############################################################################
#                 Exporting to OpenMC geometry.xml file
###############################################################################

# Instantiate ZCylinder surfaces
fuel_cyl = openmc.ZCylinder(surface_id=1, x0=0, y0=0, R=0.4095, name='fuel cylinder')
clad_cyl = openmc.ZCylinder(surface_id=2, x0=0, y0=0, R=0.475, name='clad cylinder')
left = openmc.XPlane(surface_id=4, x0=-0.627, name='left')
right = openmc.XPlane(surface_id=5, x0=0.627, name='right')
bottom = openmc.YPlane(surface_id=6, y0=-0.627, name='bottom')
top = openmc.YPlane(surface_id=7, y0=0.627, name='top')

left.boundary_type = 'reflective'
right.boundary_type = 'reflective'
top.boundary_type = 'reflective'
bottom.boundary_type = 'reflective'

# Instantiate Cells
fuel_cell = openmc.Cell(cell_id=1, name='fuel cell')
clad_cell = openmc.Cell(cell_id=2, name='clad cell')
mod_cell = openmc.Cell(cell_id=3, name='mod cell')

# Use surface half-spaces to define regions
fuel_cell.region = -fuel_cyl
clad_cell.region = +fuel_cyl & -clad_cyl
mod_cell.region = +clad_cyl & +left & -right & +bottom & -top

# Register Materials with Cells
fuel_cell.fill = fuel_mat
clad_cell.fill = clad_mat
mod_cell.fill = mod_mat

# Instantiate Universe
root = openmc.Universe(universe_id=0, name='root universe')

# Register Cells with Universe
root.add_cells([fuel_cell, clad_cell, mod_cell])

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
bounds = [-0.5, -0.5, -1, 0.5, 0.5, 1]
uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:])
settings_file.source = openmc.source.Source(space=uniform_dist)

settings_file.export_to_xml()

###############################################################################
#                   Run OpenMC
###############################################################################

openmc.run(threads=4)

