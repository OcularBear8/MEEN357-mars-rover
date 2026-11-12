"""###########################################################################
# This file is the top-level script for running a simulation of the EDL system
# as a study to determine parachute size.
# It loads the appropriate info into the workspace and calls simulate_edl.
# After returning from simulate_edl, it graphs some of the simulation
# trajectory data.
###########################################################################"""

import numpy as np
import matplotlib.pyplot as plt
from define_edl_system import *
from subfunctions_EDL import *
from define_planet import *
from define_mission_events import *

# *************************************
# load dicts that define the EDL system (includes rover), planet,
# mission events and so forth.
def initialize_edl(diam):
    edl_system = define_edl_system_1()
    edl_system['altitude'] = 11000    # [m] initial altitude
    edl_system['velocity'] = -590     # [m/s] initial velocity
    edl_system['parachute']['deployed'] = True   # our parachute is open
    edl_system['parachute']['ejected'] = False   # and still attached
    edl_system['rover']['on_ground'] = False # the rover has not yet landed
    edl_system['parachute']['diameter'] = diam
    return edl_system
mars = define_planet()
mission_events = define_mission_events()

parachute_diam = np.linspace(14, 19, 11)

tmax = 2000   # [s] maximum simulated time

# looping through each parachute diameter and storing results
end_time = np.array([])
landing_speed = np.array([])
success = np.array([])
for diam in parachute_diam:
    # reinitialize for every simulate_edl run
    edl_system = initialize_edl(diam)
    t, y, _ = simulate_edl(edl_system, mars, mission_events, tmax, True)
    # collect simulation end time
    end_time = np.append(end_time, t[-1])
    # collect rover landing speed
    landing_speed = np.append(landing_speed, y[0][-1])
    # check for rover touchdown success
    if y[1][-1] >= edl_system["sky_crane"]["danger_altitude"] and abs(y[0][-1] + y[5][-1]) <= abs(edl_system["sky_crane"]["danger_speed"]):
        success = np.append(success, 1)
    else: success = np.append(success, 0)

# visualize the simulation results
fig, axs = plt.subplots(3) 
plt.tight_layout()
axs[0].plot(parachute_diam, end_time)
axs[0].set_title('simulated time vs parachute diameter', fontsize=10)
axs[0].set_ylabel('simulated time (s)')
axs[0].grid()
axs[1].plot(parachute_diam, landing_speed)
axs[1].set_title('rover speed vs parachute diameter', fontsize=10)
axs[1].set_ylabel('rover landing speed (m/s)')
axs[1].grid()
axs[2].plot(parachute_diam, success)
axs[2].set_title('rover landing success vs parachute diameter', fontsize=10)
axs[2].set_ylabel('failure (0), success (1)')
axs[2].set_xlabel('parachute diameter (m)')
axs[2].grid()

plt.show()

