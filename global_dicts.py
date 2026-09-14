rover = {
    "wheel_assembly": {
        "wheel": {
            "radius": 0.3 # meter
            "mass": 1.0 # kilogram
        }
        
        "speed_reducer": {
            "type": "reverted"
            "diam_pinion": 0.04 # meter
            "diam_gear": 0.07 # meter
            "mass": 1.5 # kilogram
        }
        
        "motor": {
            "torque_stall": 170 # Newton-meter
            "torque_noload": 0 # Newton-meter
            "speed_noload": 3.8 # rad/s
            "mass": 5.0 # kilogram
        }
    }
    
    "chassis": {
        "mass": 659 # kilogram
    }
    
    "science_payload": {
        "mass": 75 # kilogram
    }

    "power_subsys": {
        "mass": 90 # kilogram
    }
}

planet = {
    "g": 3.72 # meters/second/second
}
