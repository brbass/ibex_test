import numpy as np
import matplotlib.pyplot as plt

import openmc
import openmc.mgxs as mgxs

################
# Load results #
################

sp = openmc.StatePoint("statepoint.100.h5")

# Tally results
num_cells = 1000
volume_fraction = 0.5 / (4. / num_cells)
tally = sp.get_tally(name='flux')
flux = tally.get_slice(scores=['flux'])
flux_vals = np.resize(flux.mean, (num_cells, 2))[:, [1, 0]] * volume_fraction
std_dev_vals = np.resize(flux.std_dev, (num_cells, 2))[:, [1, 0]] * volume_fraction
print([np.amax(std_dev_vals[:, i]) for i in [0, 1]])
np.savetxt("eigenvector_flux.txt", flux_vals, delimiter="\t")
np.savetxt("eigenvector_stddev.txt", std_dev_vals, delimiter="\t")
