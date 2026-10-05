import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import global_dicts as gd

# y = np.array([0,1])
# print(np.shape(y))
# print(np.shape(y) == (2,))

from define_experiment import experiment1

experiment, end_event = experiment1()

plt.plot(gd.rover["wheel_assembly"]["motor"]["effcy_tau"],gd.rover["wheel_assembly"]["motor"]["effcy"])

#alpha_fun = sp.interpolate.CubicSpline(experiment['alpha_dist'], experiment['alpha_deg'], extrapolate=True)
#x = np.linspace(0,1000,101)
#plt.plot(x, alpha_fun(x))
#plt.plot(experiment['alpha_dist'], experiment['alpha_deg'])
plt.show()
