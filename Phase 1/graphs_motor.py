import numpy as np
import matplotlib.pyplot as plt
from global_dicts import *
from subfunctions import *

speed_range = np.linspace(0, rover['wheel_assembly']['motor']['speed_noload'], 25)
torque_range = np.linspace(0, 200, 25)

def P_dcmotor(tau, motor):
    check_sora(tau, 'tau')
    power = -1 * (motor['speed_noload'] / motor['torque_stall']) * tau ** 2 + motor['speed_noload'] * tau
    # ensuring power is nonnegative
    if type(tau) is np.ndarray:
        for i, element in enumerate(power):
            if element < 0: power[i] = 0
    else:
        if power < 0: power = 0
    return power

# speed vs torque
plt.subplot(3, 1, 1)
torque = tau_dcmotor(speed_range, rover['wheel_assembly']['motor'])
plt.plot(torque, speed_range)
plt.xlabel('Motor Shaft Torque [N*m]')
plt.ylabel('Motor Shaft Speed [rad/s]')

# power vs torque
plt.subplot(3, 1, 2)
torque = tau_dcmotor(speed_range, rover['wheel_assembly']['motor'])
power = torque * speed_range
plt.plot(torque, power)

plt.xlabel('Motor Shaft Torque [N*m]')
plt.ylabel('Motor Power [W]')

# power vs speed
plt.subplot(3, 1, 3)
torque = tau_dcmotor(speed_range, rover['wheel_assembly']['motor'])
power = torque * speed_range
plt.plot(speed_range, power)
plt.xlabel('Motor Shaft Speed [rad/s]')
plt.ylabel('Motor Power [W]')

# better formatting
plt.tight_layout()
plt.show()
