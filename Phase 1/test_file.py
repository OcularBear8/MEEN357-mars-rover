import numpy as np
import matplotlib.pyplot as plt
from subfunctions import *
from global_dicts import *

CRR = 0.15

slope = -2

omega_test = np.linspace(0, 4, 25)

F_test = np.array([
    F_net(omega, slope, rover, planet, CRR)
    for omega in omega_test
])

plt.plot(omega_test, F_test)
plt.axhline(0, color='black')
plt.xlabel('Omega')
plt.ylabel('F_net')
plt.grid()
plt.show()