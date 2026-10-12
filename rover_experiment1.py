import numpy as np
import matplotlib.pyplot as plt
from define_experiment import experiment1
from global_dicts import rover, planet
from subfunctions import simulate_rover

# defining experiment conditions
experiment, end_event = experiment1()
end_event['max_distance'] = 1000
end_event['max_time'] = 10000
end_event['min_velocity'] = 0.01

rover = simulate_rover(rover, planet, experiment, end_event)

print(rover['telemetry']['battery_energy'])

# Position plot
plt.subplot(3, 1, 1)
plt.plot(rover['telemetry']['Time'], rover['telemetry']['position'])
plt.ylabel('Position (m)')

# Velocity plot
plt.subplot(3, 1, 2)
plt.plot(rover['telemetry']['Time'], rover['telemetry']['velocity'])
plt.ylabel('Velocity (m/s)')

# Power plot
plt.subplot(3, 1, 3)
plt.plot(rover['telemetry']['Time'], rover['telemetry']['power'])
plt.ylabel('Power (W)')
plt.xlabel('Time (s)')
plt.show()
