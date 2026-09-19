import numpy as np
import matplotlib.pyplot as plt
from global_dicts import *
from subfunctions import *

speed_range = np.linspace(0, rover['wheel_assembly']['motor']['speed_noload'], 25)

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
