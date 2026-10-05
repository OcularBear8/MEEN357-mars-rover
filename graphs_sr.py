import numpy as np
import matplotlib.pyplot as plt
from global_dicts import *
from subfunctions import *

speed_range = np.linspace(0, rover['wheel_assembly']['motor']['speed_noload'], 25)
torque = tau_dcmotor(speed_range, rover['wheel_assembly']['motor'])*get_gear_ratio(rover['wheel_assembly']['speed_reducer'])

# speed vs torque
plt.subplot(3, 1, 1)
plt.plot(torque, speed_range)
plt.xlabel('Motor Shaft Torque [N*m]')
plt.ylabel('Speed Reducer Shaft Speed [rad/s]')

# power vs torque
plt.subplot(3, 1, 2)
power = torque * speed_range
plt.plot(torque, power)

plt.xlabel('Speed Reducer Torque [N*m]')
plt.ylabel('Speed Reducer Power [W]')

# power vs speed
plt.subplot(3, 1, 3)
power = torque * speed_range
plt.plot(speed_range, power)
plt.xlabel('Motor Shaft Speed [rad/s]')
plt.ylabel('Speed Reducer Power [W]')

# better formatting
plt.tight_layout()
plt.show()
