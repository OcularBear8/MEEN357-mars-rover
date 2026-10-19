import numpy as np

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
            "mass": 5.0, # kilogram
            "effcy_tau": np.array([0,10,20,40,70,165]), 
            "effcy": np.array([0,0.55,0.75,0.71,0.50,0.05])
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
    },

    "telemetry": {
        "Time": np.array([]), # seconds
        "completion_time": 0, # seconds
        "velocity": np.array([]), # meters per second
        "position": np.array([]), # meters
        "distance_traveled": 0, # meters
        "max_velocity": 0, # meters per second
        "average_velocity": 0, # meters per second
        "power": np.array([]), # Watts
        "battery_energy": 0, # Joules
        "energy_per_distance": 0 # Joules per meter

    }
}

planet = {
    "g": 3.72 # meters/second/second
}
