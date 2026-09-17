import numpy as np
import scipy as sp
import math

def get_mass(rover):
    if type(rover) is not dict: raise Exception('Argument \'rover\' must be dict')
    return 6*(rover['wheel_assembly']['wheel']['mass'] + rover['wheel_assembly']['speed_reducer']['mass'] + rover['wheel_assembly']['motor']['mass']) + rover['chassis']['mass'] + rover['science_payload']['mass'] + rover['power_subsys']['mass']

def get_gear_ratio(speed_reducer):
    # checks for dictionary
    if type(speed_reducer) is not dict: raise Exception('Argument \'speed_reducer\' must be dict')
    # checks for typing
    if speed_reducer['type'].lower() != "reverted": raise Exception('Speed reducer must be reverted type')
    # computes reduction
    return (speed_reducer['diam_gear']/speed_reducer['diam_pinion'])


def tau_dcmotor(omega, motor):
    '''computes output torque based on rotational speed and motor characteristics'''
    # checks if omega is scalar or array
    check_sora(omega, 'omega')
    # computes tau
    if np.iterable(omega): #iterable
        tau = np.array([])
        for i in omega:
            if i<0:
                tau = np.append(tau,motor['torque_stall'])
            elif i<motor['speed_noload']:
                tau = np.append(tau,motor['torque_stall'] - ((motor['torque_stall'] - motor['torque_noload']) / motor['speed_noload']) * i)
            else:
                tau = np.append(tau,0)

        return tau

    else: #scalar case
        if omega < 0:
            return motor['torque_stall']
        elif omega < motor['speed_noload']:
            return motor['torque_stall'] - ((motor['torque_stall'] - motor['torque_noload']) / motor['speed_noload']) * omega
        else:
            return 0

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

def F_rolling(omega, terrain_angle, rover, planet, Crr):
    check_sora(omega, 'omega')
    check_sora(terrain_angle, 'terrain_angle')
    if type(omega) is not type(terrain_angle): raise Exception('omega and terrain_angle must be same type')
    if type(omega) is np.ndarray and omega.shape != terrain_angle.shape: raise Exception('omega and terrain_angle must be same size')
    if type(rover) is not dict: raise Exception('Argument \'rover\' must be dict')
    if type(planet) is not dict: raise Exception('Argument \'planet\' must be dict')
    if type(terrain_angle) is np.ndarray and (min(terrain_angle) < -75 or max(terrain_angle) > 75): raise Exception('Argument \'terrain_angle\' must have values between -75 and +75 degrees')
    if type(terrain_angle) in [int, float] and (terrain_angle < -75 or terrain_angle > 75): raise Exception('Argument \'terrain_angle\' must be between -75 and +75 degrees')
    if type(Crr) not in [int, float]: raise Exception('Argument \'Crr\' must be scalar')
    if Crr <= 0: raise Exception('Argument \'Crr\' must be positive')

    return sp.special.erf(40*rover['wheel_assembly']['wheel']['radius']*omega/get_gear_ratio(rover['wheel_assembly']['speed_reducer']))*Crr*get_mass(rover)*planet['g']*np.cos(terrain_angle)

def F_net(omega, terrain_angle, rover, planet, Crr):
    # check inputs
    check_sora(omega, 'omega')
    check_sora(terrain_angle, 'terrain_angle')
    if type(omega) is not type(terrain_angle): raise Exception('omega and terrain_angle must be same type')
    if type(omega) is np.ndarray and omega.shape != terrain_angle.shape: raise Exception('omega and terrain_angle must be same size')
    if type(rover) is not dict: raise Exception('Argument \'rover\' must be dict')
    if type(planet) is not dict: raise Exception('Argument \'planet\' must be dict')
    if type(terrain_angle) is np.ndarray and (min(terrain_angle) < -75 or max(terrain_angle) > 75): raise Exception('Argument \'terrain_angle\' must have values between -75 and +75 degrees')
    if type(terrain_angle) in [int, float] and (terrain_angle < -75 or terrain_angle > 75): raise Exception('Argument \'terrain_angle\' must be between -75 and +75 degrees')
    if type(Crr) not in [int, float]: raise Exception('Argument \'Crr\' must be scalar')
    if Crr <= 0: raise Exception('Argument \'Crr\' must be positive')

    return F_drive(omega, rover) - F_gravity(terrain_angle,rover, planet) - F_rolling(omega, terrain_angle, rover, planet, Crr)


def check_sora(inp, var_name):
    if type(inp) not in [float,int,np.ndarray]: raise Exception(f'Argument {var_name} must be scalar or vector')