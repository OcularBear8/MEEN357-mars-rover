import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from global_dicts import rover

# efficiency function interpolation
effcy_fun = sp.interpolate.CubicSpline(rover["wheel_assembly"]["motor"]["effcy_tau"],rover["wheel_assembly"]["motor"]["effcy"], extrapolate=True)
# plotting
x = np.linspace(0,170,101)
plt.plot(x, effcy_fun(x), '*-')
plt.xlabel('Torque (Nm)')
plt.ylabel('Efficiency')
plt.show()