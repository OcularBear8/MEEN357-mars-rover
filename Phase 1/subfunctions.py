import numpy as np

def get_mass(rover):
    if type(rover) is not dict: raise Exception('Argument \'rover\' must be dict')
    return 6*(rover['wheel_assembly']['wheel']['mass'] + rover['wheel_assembly']['speed_reducer']['mass'] + rover['wheel_assembly']['motor']['mass']) + rover['chassis']['mass'] + rover['science_payload']['mass'] + rover['power_subsys']['mass']

def get_gear_ratio():
    pass

def tau_dcmotor(omega, motor):
    '''computes output torque based on rotational speed and motor characteristics'''
    # checks if omega is scalar or array
    check_sora(omega, 'omega')
    # TODO: 
    # computes tau
    tau = np.subtract(motor['torque_stall'],((motor['torque_stall']-motor['torque_noload'])/motor['speed_noload'])*omega)
    
    return tau # torque at motor shaft (Nm)

def F_drive(omega, rover):
    check_sora(omega, 'omega')
    if type(rover) is not dict: raise Exception('Argument \'rover\' must be dict')
    tau = tau_dcmotor(omega, rover['wheel_assembly']['motor'])
    return tau / rover['wheel_assembly']['wheel']['radius']

def F_gravity(terrain_angle, rover, planet):
    check_sora(terrain_angle, 'terrain_angle')
    if type(rover) is not dict: raise Exception('Argument \'rover\' must be dict')
    if type(planet) is not dict: raise Exception('Argument \'planet\' must be dict')
    if type(terrain_angle) is np.ndarray and (min(terrain_angle) < -75 or max(terrain_angle) > 75): raise Exception('Argument \'terrain_angle\' must have values between -75 and +75 degrees')
    if type(terrain_angle) in [int, float] and (terrain_angle < -75 or terrain_angle > 75): raise Exception('Argument \'terrain_angle\' must be between -75 and +75 degrees')
    return -1 * get_mass(rover) * planet['g'] * np.sin(np.radians(terrain_angle))

def F_rolling():
    if

def F_net():
    pass

def check_sora(inp, var_name):
    if type(inp) not in [float,int,np.ndarray]: raise Exception(f'Argument {var_name} must be scalar or vector')