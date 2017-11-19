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
print(len(flux.mean))
print(len(flux.std_dev))
print(flux.mean)
print(flux.std_dev)

