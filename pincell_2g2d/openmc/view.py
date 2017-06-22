import numpy as np

import openmc
import openmc.mgxs

###############################################################################
#                   Post-Processing
###############################################################################

statepoint = openmc.StatePoint('statepoint.200.h5')

print(statepoint)
print(statepoint.k_combined)
