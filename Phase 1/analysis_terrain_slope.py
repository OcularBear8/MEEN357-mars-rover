import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import root_scalar
from subfunctions import F_net
from global_dicts import *

CRR = 0.15
slope_array_deg = np.linspace(-15, 35, 25)
print(slope_array_deg)
v_max = np.zeros(len(slope_array_deg))

for i, slope in enumerate(slope_array_deg):
    def accel(omega):
        return F_net(omega, slope, rover, planet, CRR)
    
    try:
        sol = root_scalar(accel, bracket=[0, 4])
        v_max[i] = sol.root * rover['wheel_assembly']['wheel']['radius']
    except ValueError:
        v_max[i] = np.nan

plt.plot(slope_array_deg, v_max)
plt.xlabel('Slope [deg]')
plt.ylabel('Maximum Velocity [m/s]')
plt.show()

