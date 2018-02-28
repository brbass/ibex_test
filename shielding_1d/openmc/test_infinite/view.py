import numpy as np
import matplotlib.pyplot as plt

import openmc
import openmc.mgxs as mgxs

################
# Load results #
################

sp = openmc.StatePoint("statepoint.100.h5")

# Tally results
tally = sp.get_tally(name='flux')
#print(tally)
flux = tally.get_slice(scores=['flux'])
print(flux.mean.flatten())

print(sp.source[0])
