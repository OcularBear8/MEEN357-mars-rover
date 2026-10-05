import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import root_scalar
from subfunctions import *
from global_dicts import *

Crr_array = np.linspace(0.01, 0.5, 25)
slope_array_deg = np.linspace(-15, 35, 25)
CRR, SLOPE = np.meshgrid(Crr_array, slope_array_deg)
VMAX = np.zeros(np.shape(CRR), dtype=float)

N = np.shape(CRR)[0]
for i in range(N):
    for j in range(N):
        Crr_sample = float(CRR[i,j])
        slope_sample = float(SLOPE[i,j])
        def force(omega):
            return F_net(omega, slope_sample, rover, planet, Crr_sample)
            
        try:
            sol = root_scalar(force, bracket=[0, rover['wheel_assembly']['motor']['speed_noload']])
            VMAX[i,j] = sol.root * rover['wheel_assembly']['wheel']['radius']
        except ValueError:
            VMAX[i,j] = np.nan

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot_surface(CRR, SLOPE, VMAX)
ax.set_xlabel('Coefficient of Rolling Resistance')
ax.set_ylabel('Slope [deg]')
ax.set_zlabel('Maximum Velocity [m/s]')
plt.show()