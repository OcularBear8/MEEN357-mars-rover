import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from subfunctions import F_net
from global_dicts import *

CRR = 0.15
slope_array_deg = np.linspace(-15, 35, 25)
v_max = np.zeros(len(slope_array_deg))

for i, slope in enumerate(slope_array_deg):
    def accel(omega):
        return F_net(omega, slope, rover, planet, CRR)
    
    omega_test = np.linspace(0, 4, 100)
    F_test = np.array([accel(omega) for omega in omega_test])
    roots = []

    for j in range(len(omega_test) - 1):
        if F_test[j] * F_test[j + 1] < 0:
            root = brentq(accel, omega_test[j], omega_test[j + 1])
            roots.append(root)

    if roots:
        omega_largest = max(roots)
        v_max[i] = rover['wheel_assembly']['wheel']['radius'] * omega_largest
    else:
        v_max[i] = np.nan

print(v_max)

