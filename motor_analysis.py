import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as spint
from matplotlib.widgets import Cursor

motor_base = {
        "torque_stall": 170, # Newton-meter
        "torque_noload": 0, # Newton-meter
        "speed_noload": 3.8, # rad/s
        "mass": 5.0, # kilogram
        "effcy_tau": np.array([0,10,20,40,70,165]),
        "effcy": np.array([0,0.55,0.75,0.71,0.50,0.05])
}

def define_motor(motor, motor_type):

    # define_motor
    #
    # Determines the attributes of the rover motor. Returns edl_system with
    # properly modified motor.
    #
    # INPUTS:
    #    edl_system and type of motor:
    #       base, base_he, torque, torque_he, speed, speed_he
    #
    # OUTPUTS
    #   edl_system
    #   type : string = {'base', 'base_he', 'torque', 'torque_he', 'speed',
    #   'speed_he'}

    if motor_type.lower() == 'base'.lower():
        motor['type'] = 'base'
        motor['torque_stall'] = 165
        motor['speed_noload'] = 3.85
        motor['cost'] = 2.5e5

    elif motor_type.lower() == 'base_he'.lower():
        motor['type'] = 'base_he'
        motor['torque_stall'] = 165
        motor['speed_noload'] = 3.85
        motor['cost'] = 2.8e5
        motor['effcy'] = motor['effcy']*1.15
        motor['effcy_tau'] = motor['effcy_tau']*1.15

    elif motor_type.lower() == 'torque'.lower():
        motor['type'] = 'torque'
        motor['torque_stall'] = 165*1.25
        motor['speed_noload'] = 3.85
        motor['cost'] = 3e5

    elif motor_type.lower() == 'torque_he'.lower():
        motor['type'] = 'torque_he'
        motor['torque_stall'] = 165*1.25
        motor['speed_noload'] = 3.85
        motor['cost'] = 3.36e5
        motor['effcy'] = motor['effcy']*1.15
        motor['effcy_tau'] = motor['effcy_tau']*1.15

    elif motor_type.lower() == 'speed'.lower():
        motor['type'] = 'speed'
        motor['torque_stall'] = 165*.75
        motor['speed_noload'] = 3.85*2
        motor['cost'] = 3e5
        motor['effcy_tau'] = motor['effcy_tau']*.75

    elif motor_type.lower() == 'speed_he'.lower():
        motor['type'] = 'speed_he'
        motor['torque_stall'] = 165*.75
        motor['speed_noload'] = 3.85*2
        motor['cost'] = 3.36e5
        motor['effcy'] = motor['effcy']*1.15
        motor['effcy_tau'] = motor['effcy_tau']*.75
    else:
       raise Exception('input not recognized')

    return motor

motor_types = ['base','base_he','torque','torque_he','speed','speed_he']
line_markers = ['b-','b--','r-','r--','g-','g--']
markers = ['bo','bo','ro','ro','go','go']


fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

for i in range(len(motor_types)):
    motor_test = define_motor({**motor_base}, motor_types[i])

    X = np.linspace(0,motor_test['torque_stall'],50)  # torque
    Y1 = (motor_test['torque_stall']-X)*motor_test['speed_noload']/(motor_test['torque_stall']-motor_test['torque_noload']) # speed
    eff = spint.CubicSpline(motor_test['effcy_tau'],motor_test['effcy'])
    Y2 = eff(X) # efficiency
    Y3 = X*Y1/Y2 # power consumed

    #ax.plot(X, Y1, label=i, linewidth=2)
    ax1.plot(X, Y1, markers[i], label=motor_types[i], markersize=3)
    ax2.plot(X, Y3, line_markers[i], label=motor_types[i], linewidth=2)

cursor = Cursor(ax1, useblit=True, color='red', linewidth=2)
ax1.set_xlabel('Torque')
ax1.set_ylabel('Rad/s')
ax2.set_ylabel('Watts')
plt.legend()
plt.show()