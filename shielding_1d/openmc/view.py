import numpy as np
import matplotlib.pyplot as plt

import openmc
import openmc.mgxs as mgxs

################
# Load results #
################

sp = openmc.StatePoint("statepoint.100.h5")

# Tally results
volume_fraction = 0.5 / (4. / 10000.)
tally = sp.get_tally(name='flux')
flux = tally.get_slice(scores=['flux'])
flux_vals = np.resize(flux.mean, (10000, 2))[:, [1, 0]] * volume_fraction
print(flux_vals)
np.savetxt("mesh_tally.txt", flux_vals, delimiter="\t")
