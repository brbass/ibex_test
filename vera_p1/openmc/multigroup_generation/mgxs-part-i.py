import numpy as np
import matplotlib.pyplot as plt

import openmc
import openmc.mgxs as mgxs

# Instantiate some Nuclides
o16 = openmc.Nuclide('O16')
u234 = openmc.Nuclide('U234')
u235 = openmc.Nuclide('U235')
u236 = openmc.Nuclide('U236')
u238 = openmc.Nuclide('U238')
zr90 = openmc.Nuclide('Zr90')


# With the nuclides we defined, we will now create a material for the homogeneous medium.

# In[4]:

# Instantiate a Material and register the Nuclides
inf_medium = openmc.Material(name='moderator')
inf_medium.set_density('g/cc', 5.)
inf_medium.add_nuclide(h1,  0.028999667)
inf_medium.add_nuclide(o16, 0.01450188)
inf_medium.add_nuclide(u235, 0.000114142)
inf_medium.add_nuclide(u238, 0.006886019)
inf_medium.add_nuclide(zr90, 0.002116053)


# With our material, we can now create a `Materials` object that can be exported to an actual XML file.

# In[5]:

# Instantiate a Materials collection and export to XML
materials_file = openmc.Materials([inf_medium])
materials_file.export_to_xml()


# Now let's move on to the geometry. This problem will be a simple square cell with reflective boundary conditions to simulate an infinite homogeneous medium. The first step is to create the outer bounding surfaces of the problem.

# In[6]:

# Instantiate boundary Planes
min_x = openmc.XPlane(boundary_type='reflective', x0=-0.63)
max_x = openmc.XPlane(boundary_type='reflective', x0=0.63)
min_y = openmc.YPlane(boundary_type='reflective', y0=-0.63)
max_y = openmc.YPlane(boundary_type='reflective', y0=0.63)


# With the surfaces defined, we can now create a cell that is defined by intersections of half-spaces created by the surfaces.

# In[7]:

# Instantiate a Cell
cell = openmc.Cell(cell_id=1, name='cell')

# Register bounding Surfaces with the Cell
cell.region = +min_x & -max_x & +min_y & -max_y

# Fill the Cell with the Material
cell.fill = inf_medium


# OpenMC requires that there is a "root" universe. Let us create a root universe and add our square cell to it.

# In[8]:

# Instantiate Universe
root_universe = openmc.Universe(universe_id=0, name='root universe')
root_universe.add_cell(cell)


# We now must create a geometry that is assigned a root universe and export it to XML.

# In[9]:

# Create Geometry and set root Universe
openmc_geometry = openmc.Geometry()
openmc_geometry.root_universe = root_universe

# Export to "geometry.xml"
openmc_geometry.export_to_xml()


# Next, we must define simulation parameters. In this case, we will use 10 inactive batches and 40 active batches each with 2500 particles.

# In[10]:

# OpenMC simulation parameters
batches = 50
inactive = 10
particles = 2500

# Instantiate a Settings object
settings_file = openmc.Settings()
settings_file.batches = batches
settings_file.inactive = inactive
settings_file.particles = particles
settings_file.output = {'tallies': True}

# Create an initial uniform spatial source distribution over fissionable zones
bounds = [-0.63, -0.63, -0.63, 0.63, 0.63, 0.63]
uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:], only_fissionable=True)
settings_file.source = openmc.source.Source(space=uniform_dist)

# Export to "settings.xml"
settings_file.export_to_xml()


# Now we are ready to generate multi-group cross sections! First, let's define a 2-group structure using the built-in `EnergyGroups` class.

# In[11]:

# Instantiate a 2-group EnergyGroups object
groups = mgxs.EnergyGroups()
groups.group_edges = np.array([0., 0.625, 20.0e6])


# We can now use the `EnergyGroups` object, along with our previously created materials and geometry, to instantiate some `MGXS` objects from the `openmc.mgxs` module. In particular, the following are subclasses of the generic and abstract `MGXS` class:
# 
# * `TotalXS`
# * `TransportXS`
# * `AbsorptionXS`
# * `CaptureXS`
# * `FissionXS`
# * `KappaFissionXS`
# * `ScatterXS`
# * `ScatterMatrixXS`
# * `Chi`
# * `ChiPrompt`
# * `InverseVelocity`
# * `PromptNuFissionXS`
# 
# Of course, we are aware that the fission cross section (`FissionXS`) can sometimes be paired with the fission neutron multiplication to become $\nu\sigma_f$. This can be accomodated in to the `FissionXS` class by setting the `nu` parameter to `True` as shown below.
# 
# Additionally, scattering reactions (like (n,2n)) can also be defined to take in to account the neutron multiplication to become $\nu\sigma_s$. This can be accomodated in the the transport (`TransportXS`), scattering (`ScatterXS`), and scattering-matrix (`ScatterMatrixXS`) cross sections types by setting the `nu` parameter to `True` as shown below.
# 
# These classes provide us with an interface to generate the tally inputs as well as perform post-processing of OpenMC's tally data to compute the respective multi-group cross sections. In this case, let's create the multi-group total, absorption and scattering cross sections with our 2-group structure.

# In[12]:

# Instantiate a few different sections
total = mgxs.TotalXS(domain=cell, groups=groups)
absorption = mgxs.AbsorptionXS(domain=cell, groups=groups)
scattering = mgxs.ScatterXS(domain=cell, groups=groups)

# Note that if we wanted to incorporate neutron multiplication in the
# scattering cross section we would write the previous line as:
# scattering = mgxs.ScatterXS(domain=cell, groups=groups, nu=True)


# Each multi-group cross section object stores its tallies in a Python dictionary called `tallies`. We can inspect the tallies in the dictionary for our `Absorption` object as follows. 

# In[13]:

absorption.tallies


# The `Absorption` object includes tracklength tallies for the 'absorption' and 'flux' scores in the 2-group structure in cell 1. Now that each `MGXS` object contains the tallies that it needs, we must add these tallies to a `Tallies` object to generate the "tallies.xml" input file for OpenMC.

# In[14]:

# Instantiate an empty Tallies object
tallies_file = openmc.Tallies()

# Add total tallies to the tallies file
tallies_file += total.tallies.values()

# Add absorption tallies to the tallies file
tallies_file += absorption.tallies.values()

# Add scattering tallies to the tallies file
tallies_file += scattering.tallies.values()

# Export to "tallies.xml"
tallies_file.export_to_xml()


# Now we a have a complete set of inputs, so we can go ahead and run our simulation.

# In[15]:

# Run OpenMC
openmc.run()


# ## Tally Data Processing

# Our simulation ran successfully and created statepoint and summary output files. We begin our analysis by instantiating a `StatePoint` object. 

# In[16]:

# Load the last statepoint file
sp = openmc.StatePoint('statepoint.50.h5')


# In addition to the statepoint file, our simulation also created a summary file which encapsulates information about the materials and geometry. By default, a `Summary` object is automatically linked when a `StatePoint` is loaded. This is necessary for the `openmc.mgxs` module to properly process the tally data.

# The statepoint is now ready to be analyzed by our multi-group cross sections. We simply have to load the tallies from the `StatePoint` into each object as follows and our `MGXS` objects will compute the cross sections for us under-the-hood.

# In[17]:

# Load the tallies from the statepoint into each MGXS object
total.load_from_statepoint(sp)
absorption.load_from_statepoint(sp)
scattering.load_from_statepoint(sp)


# Voila! Our multi-group cross sections are now ready to rock 'n roll!

# ## Extracting and Storing MGXS Data

# Let's first inspect our total cross section by printing it to the screen.

# In[18]:

total.print_xs()


# Since the `openmc.mgxs` module uses [tally arithmetic](http://openmc.readthedocs.io/en/latest/examples/tally-arithmetic.html) under-the-hood, the cross section is stored as a "derived" `Tally` object. This means that it can be queried and manipulated using all of the same methods supported for the `Tally` class in the OpenMC Python API. For example, we can construct a [Pandas](http://pandas.pydata.org/) `DataFrame` of the multi-group cross section data.

# In[19]:

df = scattering.get_pandas_dataframe()
df.head(10)


# Each multi-group cross section object can be easily exported to a variety of file formats, including CSV, Excel, and LaTeX for storage or data processing.

# In[20]:

absorption.export_xs_data(filename='absorption-xs', format='excel')


# The following code snippet shows how to export all three `MGXS` to the same HDF5 binary data store.

# In[21]:

total.build_hdf5_store(filename='mgxs', append=True)
absorption.build_hdf5_store(filename='mgxs', append=True)
scattering.build_hdf5_store(filename='mgxs', append=True)


# ## Comparing MGXS with Tally Arithmetic

# Finally, we illustrate how one can leverage OpenMC's [tally arithmetic](http://openmc.readthedocs.io/en/latest/examples/tally-arithmetic.html) data processing feature with `MGXS` objects. The `openmc.mgxs` module uses tally arithmetic to compute multi-group cross sections with automated uncertainty propagation. Each `MGXS` object includes an `xs_tally` attribute which is a "derived" `Tally` based on the tallies needed to compute the cross section type of interest. These derived tallies can be used in subsequent tally arithmetic operations. For example, we can use tally artithmetic to confirm that the `TotalXS` is equal to the sum of the `AbsorptionXS` and `ScatterXS` objects.

# In[22]:

# Use tally arithmetic to compute the difference between the total, absorption and scattering
difference = total.xs_tally - absorption.xs_tally - scattering.xs_tally

# The difference is a derived tally which can generate Pandas DataFrames for inspection
difference.get_pandas_dataframe()


# Similarly, we can use tally arithmetic to compute the ratio of `AbsorptionXS` and `ScatterXS` to the `TotalXS`.

# In[23]:

# Use tally arithmetic to compute the absorption-to-total MGXS ratio
absorption_to_total = absorption.xs_tally / total.xs_tally

# The absorption-to-total ratio is a derived tally which can generate Pandas DataFrames for inspection
absorption_to_total.get_pandas_dataframe()


# In[24]:

# Use tally arithmetic to compute the scattering-to-total MGXS ratio
scattering_to_total = scattering.xs_tally / total.xs_tally

# The scattering-to-total ratio is a derived tally which can generate Pandas DataFrames for inspection
scattering_to_total.get_pandas_dataframe()


# Lastly, we sum the derived scatter-to-total and absorption-to-total ratios to confirm that they sum to unity.

# In[25]:

# Use tally arithmetic to ensure that the absorption- and scattering-to-total MGXS ratios sum to unity
sum_ratio = absorption_to_total + scattering_to_total

# The sum ratio is a derived tally which can generate Pandas DataFrames for inspection
sum_ratio.get_pandas_dataframe()

