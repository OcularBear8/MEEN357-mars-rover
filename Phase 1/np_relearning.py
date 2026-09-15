import numpy as np
import subfunctions as sf

rover = {
    "wheel_assembly": {
        "wheel": {
            "radius": 0.3, # meter
            "mass": 1.0 # kilogram
        },
        
        "speed_reducer": {
            "type": "reverted",
            "diam_pinion": 0.04, # meter
            "diam_gear": 0.07, # meter
            "mass": 1.5 # kilogram
        },
        
        "motor": {
            "torque_stall": 170, # Newton-meter
            "torque_noload": 0, # Newton-meter
            "speed_noload": 3.8, # rad/s
            "mass": 5.0 # kilogram
        }
    },
    
    "chassis": {
        "mass": 659 # kilogram
    },
    
    "science_payload": {
        "mass": 75 # kilogram
    },

    "power_subsys": {
        "mass": 90 # kilogram
    }
}

planet = {
    "g": 3.72 # meters/second/second
}

print(sf.tau_dcmotor(np.linspace(0,1,20), rover["wheel_assembly"]["motor"]))
print(sf.tau_dcmotor(5, rover["wheel_assembly"]["motor"]))
print(sf.tau_dcmotor(-2.0, rover["wheel_assembly"]["motor"]))
print(sf.tau_dcmotor('yup', rover["wheel_assembly"]["motor"]))

#print(sf.get_mass(rover))
#print(sf.F_gravity(np.linspace(0,1,20), rover, planet))

#print(np.array([0,0]).shape == np.array([1,1]).shape)

