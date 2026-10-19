import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from define_experiment import experiment1

# defining experiment conditions
experiment, end_event = experiment1()
# terrain angle interpolation
alpha_fun = sp.interpolate.CubicSpline(experiment['alpha_dist'], experiment['alpha_deg'], extrapolate=True)
# plotting
x = np.linspace(0,1000,101)
plt.plot(x, alpha_fun(x), '*-')
plt.xlabel('Position (m)')
plt.ylabel('Terrain Angle (deg)')
plt.show()