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
print(tally)
flux = tally.get_slice(scores=['flux-Y0,0'])
print(flux)

# Save average flux values
flux_vals = np.resize(flux.mean, (10000, 2))
av_val = np.mean(flux_vals)
flux_vals = flux_vals / av_val

np.savetxt("mesh_tally.txt", flux_vals, delimiter="\t")
