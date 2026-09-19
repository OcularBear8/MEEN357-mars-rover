import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import root_scalar
from subfunctions import F_net
from global_dicts import *

terrain_slope = 0
Crr_array = np.linspace(0.01, 0.5, 25)
v_max = np.zeros(len(Crr_array))

for i, Crr in enumerate(Crr_array):
    def accel(omega):
        return F_net(omega, terrain_slope, rover, planet, Crr)

    try:
        sol = root_scalar(accel, bracket=[0, rover['wheel_assembly']['motor']['speed_noload']])
        v_max[i] = sol.root
    except ValueError:
        v_max[i] = np.nan

plt.plot(Crr_array, v_max)
plt.xlabel('Rolling Resistance')
plt.ylabel('Maximum Velocity [m/s]')
plt.show()

print(v_max)