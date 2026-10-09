import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from define_experiment import experiment1

experiment, end_event = experiment1()
alpha_fun = sp.interpolate.CubicSpline(experiment['alpha_dist'], experiment['alpha_deg'], extrapolate=True)
x = np.linspace(0,1000,101)
plt.plot(x, alpha_fun(x), '*-')
plt.xlabel('Position (m)')
plt.ylabel('Terrain Angle (deg)')
plt.show()