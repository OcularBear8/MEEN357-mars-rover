import numpy as np
import matplotlib.pyplot as plt
from subfunctions import *
from global_dicts import *

omegas = np.linspace(0, 4, 25)
gravity = F_rolling(omegas, np.full(25, 2), rover, planet, 0.15)

plt.plot(omegas, gravity, 'o-')
plt.axhline()
plt.axvline()
plt.show()
