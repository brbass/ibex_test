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

# Tally results
tally = sp.get_tally(name='flux')
flux = tally.get_slice(scores=['flux-Y0,0'])

# Normalize values
flux_vals = np.resize(flux.mean, (10000, 2))[:, ::-1]
std_dev_vals = np.resize(flux.std_dev, (10000, 2))[:, ::-1]
av_val = np.mean(flux_vals)
flux_vals /= av_val
std_dev_vals /= av_val
print([np.amax(std_dev_vals[:, i]) for i in range(2)])
print([np.mean(std_dev_vals[:, i]) for i in range(2)])

# Save average flux values
np.savetxt("eigenvector_flux.txt", flux_vals, delimiter="\t")
np.savetxt("eigenvector_stddev.txt", std_dev_vals, delimiter="\t")


