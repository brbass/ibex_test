import numpy as np
import matplotlib.pyplot as plt

import openmc
import openmc.mgxs as mgxs

################
# Load results #
################

sp = openmc.StatePoint("statepoint.200.h5")

# K-eff results
keff = sp.k_combined
print(keff)
np.savetxt("k_eigenvalue.txt", keff)

# Tally results
tally = sp.get_tally(name='flux')
flux = tally.get_slice(scores=['flux-Y0,0'])# 'flux-Y1,-1', 'flux-Y1,0', 'flux-Y1,1'

# Get mesh
labc = 1./2. * np.array([40.4568, 48.5482, 60.6852])
mesh = openmc.Mesh()
mesh.dimension = [20, 24, 30]
mesh.lower_left = -labc / 2
mesh.upper_right = labc / 2

# Normalize data
flux_vals = np.resize(flux.mean, (14400, 1))
std_dev_vals = np.resize(flux.std_dev, (14400, 1))
av_val = np.mean(flux_vals)
flux_vals /= av_val
std_dev_vals /= av_val

# Change to ibex indexing
reshaped_flux = np.empty_like(flux_vals)
reshaped_std_dev = np.empty_like(flux_vals)
for i, mesh_index in enumerate(mesh.cell_generator()):
    ind = np.subtract(mesh_index, 1)
    ibex_ind = ind[2] + mesh.dimension[2] * (ind[1] + mesh.dimension[1] * ind[0])
    reshaped_flux[ibex_ind] = flux_vals[i]
    reshaped_std_dev[ibex_ind] = std_dev_vals[i]
print(np.amax(reshaped_std_dev))

# Save average flux values
np.savetxt("benchmark_flux.txt", reshaped_flux, delimiter="\t")
np.savetxt("benchmark_stddev.txt", reshaped_std_dev, delimiter="\t")

