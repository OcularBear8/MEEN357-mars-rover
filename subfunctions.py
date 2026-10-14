import numpy as np
import scipy as sp

def get_mass(rover):
    """Returns mass of the rover.

    Args:
        rover (dict): Physical parameters of the rover.

    Raises:
        Exception: Error if rover is not a dictionary.

    Returns:
        float: Mass of the rover.
    """
    
    if type(rover) is not dict: raise Exception('Argument \'rover\' must be dict')
    return 6*(rover['wheel_assembly']['wheel']['mass'] + rover['wheel_assembly']['speed_reducer']['mass'] + rover['wheel_assembly']['motor']['mass']) + rover['chassis']['mass'] + rover['science_payload']['mass'] + rover['power_subsys']['mass']


def get_gear_ratio(speed_reducer):
    """Computes the total gear ratio of the planetary speed reducer.

    Args:
        speed_reducer (dict): Physical parameters of the speed reducer.

    Raises:
        Exception: Error if speed_reducer is not a dictionary.
        Exception: Error if speed_reducer is not a "reverted" type.

    Returns:
        float: total gear reduction
    """
    # checks for dictionary
    if type(speed_reducer) is not dict: raise Exception('Argument \'speed_reducer\' must be dict')
    # checks for typing
    if speed_reducer['type'].lower() != "reverted": raise Exception('Speed reducer must be reverted type')
    # computes reduction
    return (speed_reducer['diam_gear']/speed_reducer['diam_pinion'])**2


def tau_dcmotor(omega, motor):
    """Computes output torque based on rotational speed and motor characteristics

    Args:
        omega (np.ndarray or scalar float/int): Speed(s) of the motor.
        motor (dict): Physical parameters of the motor.

    Raises:
        Exception: Error if omega is not a scalar or array.
        Exception: Error if motor is not a dictionary.

    Returns:
        np.ndarray or scalar float/int: Applied Torque(s) by the motor.
    """
    # checks if omega is scalar or array
    check_sora(omega, 'omega')
    if not isinstance(motor, dict): raise Exception('Argument \'rover\' must be dict')
    # computes tau
    conditions = [omega < 0,omega <= motor['speed_noload'], omega > motor['speed_noload']]
    choices = [motor['torque_stall'], motor['torque_stall'] - ((motor['torque_stall'] - motor['torque_noload']) / motor['speed_noload']) * omega, 0]
    tau = np.select(conditions,choices,default=np.nan)
    if np.shape(tau) == (1,):
        return tau[0]
    else:
        return tau

def F_drive(omega, rover):
    """_summary_

    Args:
        omega (_type_): _description_
        rover (_type_): _description_

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """
    check_sora(omega, 'omega')
    if type(rover) is not dict: raise Exception('Argument \'rover\' must be dict')
    tau = 6 * tau_dcmotor(omega, rover['wheel_assembly']['motor']) * get_gear_ratio(rover['wheel_assembly']['speed_reducer'])
    return tau / rover['wheel_assembly']['wheel']['radius']

def F_gravity(terrain_angle, rover, planet):
    """_summary_

    Args:
        terrain_angle (_type_): _description_
        rover (_type_): _description_
        planet (_type_): _description_

    Raises:
        Exception: _description_
        Exception: _description_
        Exception: _description_
        Exception: _description_

    Returns:
        _type_: _description_
    """
    check_sora(terrain_angle, 'terrain_angle')
    if type(rover) is not dict: raise Exception('Argument \'rover\' must be dict')
    if type(planet) is not dict: raise Exception('Argument \'planet\' must be dict')
    if type(terrain_angle) is np.ndarray and (min(terrain_angle.flatten()) < -75 or max(terrain_angle.flatten()) > 75): raise Exception('Argument \'terrain_angle\' must have values between -75 and +75 degrees')
    if np.isscalar(terrain_angle) != np.isscalar(terrain_angle) and (terrain_angle < -75 or terrain_angle > 75): raise Exception('Argument \'terrain_angle\' must be between -75 and +75 degrees')
    return -1*get_mass(rover) * planet['g'] * np.sin(np.radians(terrain_angle))

def F_rolling(omega, terrain_angle, rover, planet, Crr):
    """_summary_

    Args:
        omega (_type_): _description_
        terrain_angle (_type_): _description_
        rover (_type_): _description_
        planet (_type_): _description_
        Crr (_type_): _description_

    Raises:
        Exception: _description_
        Exception: _description_
        Exception: _description_
        Exception: _description_
        Exception: _description_
        Exception: _description_
        Exception: _description_
        Exception: _description_

    Returns:
        _type_: _description_
    """
    # lots of input checking
    check_sora(omega, 'omega')
    check_sora(terrain_angle, 'terrain_angle')
    if isinstance(omega, np.ndarray) and not isinstance(terrain_angle, np.ndarray): raise Exception('omega and terrain_angle must be same type')
    if type(omega) is np.ndarray and omega.shape != terrain_angle.shape: raise Exception('omega and terrain_angle must be same size')
    if type(rover) is not dict: raise Exception('Argument \'rover\' must be dict')
    if type(planet) is not dict: raise Exception('Argument \'planet\' must be dict')
    if type(terrain_angle) is np.ndarray and (min(terrain_angle.flatten()) < -75 or max(terrain_angle.flatten()) > 75): raise Exception('Argument \'terrain_angle\' must have values between -75 and +75 degrees')
    if np.isscalar(terrain_angle) != np.isscalar(terrain_angle) and (terrain_angle < -75 or terrain_angle > 75): raise Exception('Argument \'terrain_angle\' must be between -75 and +75 degrees')
    if np.isscalar(Crr) != np.isscalar(Crr): raise Exception('Argument \'Crr\' must be scalar')
    if Crr <= 0: raise Exception('Argument \'Crr\' must be positive')

    return -1*sp.special.erf(40*rover['wheel_assembly']['wheel']['radius']*omega/get_gear_ratio(rover['wheel_assembly']['speed_reducer']))*Crr*get_mass(rover)*planet['g']*np.cos(np.radians(terrain_angle))

def F_net(omega, terrain_angle, rover, planet, Crr):
    """_summary_

    Args:
        omega (_type_): _description_
        terrain_angle (_type_): _description_
        rover (_type_): _description_
        planet (_type_): _description_
        Crr (_type_): _description_

    Raises:
        Exception: _description_
        Exception: _description_
        Exception: _description_
        Exception: _description_
        Exception: _description_
        Exception: _description_
        Exception: _description_
        Exception: _description_

    Returns:
        _type_: _description_
    """
    # check inputs
    check_sora(omega, 'omega')
    check_sora(terrain_angle, 'terrain_angle')
    if isinstance(omega, np.ndarray) and not isinstance(terrain_angle, np.ndarray): raise Exception('omega and terrain_angle must be same type')
    if isinstance(omega, np.ndarray) and isinstance(terrain_angle, np.ndarray) and omega.shape != terrain_angle.shape: raise Exception('omega and terrain_angle must be same size')
    if type(rover) is not dict: raise Exception('Argument \'rover\' must be dict')
    if type(planet) is not dict: raise Exception('Argument \'planet\' must be dict')
    if type(terrain_angle) is np.ndarray and (min(terrain_angle.flatten()) < -75 or max(terrain_angle.flatten()) > 75): raise Exception('Argument \'terrain_angle\' must have values between -75 and +75 degrees')
    if isinstance(terrain_angle, (float, int, np.number)) and (terrain_angle < -75 or terrain_angle > 75): raise Exception('Argument \'terrain_angle\' must be between -75 and +75 degrees')
    if not isinstance(Crr, (float, int, np.number)): raise Exception('Argument \'Crr\' must be scalar')
    if Crr <= 0: raise Exception('Argument \'Crr\' must be positive')

    return F_drive(omega, rover) + F_gravity(terrain_angle,rover, planet) + F_rolling(omega, terrain_angle, rover, planet, Crr)

def motorW(v, rover):
    """Calculates the rotational speed of the motor shaft in rad/s from the translatinal velocity of the rover and the physical parameters of the rover.

    Args:
        v (np.ndarray or scalar float/int): Rover translational velocity (m/s)
        rover (dict): Physical parameters of the rover.

    Raises:
        Exception: Error if v is not a scalar or vector.

    Returns:
        np.ndarray or scalar float/int: motor speed (rad/s)
    """
    check_sora(v, 'v')
    return get_gear_ratio(rover['wheel_assembly']['speed_reducer']) * v / rover['wheel_assembly']['wheel']['radius']

def rover_dynamics(t, y, rover, planet, experiment):
    """_summary_

    Args:
        t (_type_): _description_
        y (_type_): _description_
        rover (_type_): _description_
        planet (_type_): _description_
        experiment (_type_): _description_

    Raises:
        Exception: _description_
        Exception: _description_
        Exception: _description_
        Exception: _description_
        Exception: _description_
        Exception: _description_

    Returns:
        _type_: _description_
    """
    if not isinstance(t, (float, int, np.number)): raise Exception(f'Argument \'t\' must be scalar')
    if not isinstance(y, np.ndarray): raise Exception(f'Argument \'y\' must be a vector')
    if np.shape(y) != (2,): raise Exception(f'Argument \'y\' must be a two-element array')
    if not isinstance(rover, dict): raise Exception(f'Argument \'rover\' must be dict')
    if not isinstance(planet, dict): raise Exception(f'Argument \'planet\' must be dict')
    if not isinstance(experiment, dict): raise Exception(f'Argument \'experiment\' must be dict')
    alpha_fun = sp.interpolate.CubicSpline(experiment['alpha_dist'], experiment['alpha_deg'], extrapolate=True)
    return np.array([F_net(motorW(y[0], rover), alpha_fun(y[1]), rover, planet, experiment['Crr']) / get_mass(rover), y[0]])

def mechpower(v, rover):
    """_summary_

    Args:
        v (_type_): _description_
        rover (_type_): _description_

    Raises:
        Exception: _description_
        Exception: _description_

    Returns:
        _type_: _description_
    """
    # input check
    check_sora(v, 'v')
    if isinstance(v, np.ndarray):
        if v.ndim > 1:
            raise Exception(f'Argument v must be a single-dimensional array')
    if type(rover) is not dict: raise Exception('Argument \'rover\' must be dict')
    
    return motorW(v, rover) * tau_dcmotor(motorW(v, rover), rover['wheel_assembly']['motor'])

def battenergy(t, v, rover):
    """_summary_

    Args:
        t (_type_): _description_
        v (_type_): _description_
        rover (_type_): _description_

    Raises:
        Exception: _description_
        Exception: _description_

    Returns:
        _type_: _description_
    """
    check_sora(t, "time")
    check_sora(v, "velocity")
    if t.shape != v.shape: raise Exception('t and v must be same size')
    if type(rover) is not dict: raise Exception('Argument \'rover\' must be dict')

    # interpolate for efficiency
    effcy_fun = sp.interpolate.CubicSpline(rover["wheel_assembly"]["motor"]["effcy_tau"],rover["wheel_assembly"]["motor"]["effcy"], extrapolate=True)

    # function for battery power with respect to time
    Y = []

    for i in range(len(t)):
        Y.append(6*mechpower(v[i], rover) / effcy_fun(tau_dcmotor(motorW(v[i],rover),rover["wheel_assembly"]["motor"])))

    # returns integral
    return sp.integrate.trapezoid(Y,t)



def simulate_rover(rover, planet, experiment, end_event):
    """_summary_

    Args:
        rover (_type_): _description_
        planet (_type_): _description_
        experiment (_type_): _description_
        end_event (_type_): _description_

    Raises:
        Exception: _description_
        Exception: _description_
        Exception: _description_
        Exception: _description_

    Returns:
        _type_: _description_
    """
    # type checking
    if not isinstance(rover, dict): raise Exception(f'Argument \'rover\' must be dict')
    if not isinstance(planet, dict): raise Exception(f'Argument \'planet\' must be dict')
    if not isinstance(experiment, dict): raise Exception(f'Argument \'experiment\' must be dict')
    if not isinstance(end_event, dict): raise Exception(f'Argument \'end_event\' must be dict')
    trajectory = lambda t, y: rover_dynamics(t, y, rover, planet, experiment)
    # IVP solver, using DOP853 for 8th-order RK
    # end_events to stop ivp solver
    sol = sp.integrate.solve_ivp(trajectory, experiment['time_range'], experiment['initial_conditions'], method='BDF', t_eval=np.linspace(0, 20000, 40000), events=end_of_mission_event(end_event))
    time, pos, vel = sol.t, sol.y[1], sol.y[0]
    power = mechpower(vel, rover)
    battery_energy = battenergy(time, vel, rover)
    # update rover telemetry data
    rover['telemetry']['Time'] = time
    rover['telemetry']['completion_time'] = time[-1]
    rover['telemetry']['velocity'] = vel
    rover['telemetry']['position'] = pos
    rover['telemetry']['distance_traveled'] = pos[-1]
    rover['telemetry']['max_velocity'] = max(vel)
    rover['telemetry']['average_velocity'] = np.average(vel)
    rover['telemetry']['power'] = power
    rover['telemetry']['battery_energy'] = battery_energy
    rover['telemetry']['energy_per_distance'] = battery_energy / pos[-1]
    return rover
    
def end_of_mission_event(end_event):
    """
    Defines an event that terminates the mission simulation. Mission is over
    when rover reaches a certain distance, has moved for a maximum simulation 
    time or has reached a minimum velocity.            
    """
    
    mission_distance = end_event['max_distance']
    mission_max_time = end_event['max_time']
    mission_min_velocity = end_event['min_velocity']
    
    # Assume that y[1] is the distance traveled
    distance_left = lambda t,y: mission_distance - y[1]
    distance_left.terminal = True
    
    time_left = lambda t,y: mission_max_time - t
    time_left.terminal = True
    
    velocity_threshold = lambda t,y: y[0] - mission_min_velocity;
    velocity_threshold.terminal = True
    velocity_threshold.direction = -1
    
    # terminal indicates whether any of the conditions can lead to the
    # termination of the ODE solver. In this case all conditions can terminate
    # the simulation independently.
    
    # direction indicates whether the direction along which the different
    # conditions is reached matters or does not matter. In this case, only
    # the direction in which the velocity treshold is arrived at matters
    # (negative)
    
    events = [distance_left, time_left, velocity_threshold]
    
    return events

def check_sora(inp, var_name):
    if isinstance(inp, np.ndarray):
        for i in inp.flatten():
            if not isinstance(i, (float, int, np.number)): raise Exception(f'Argument {var_name} must be scalar or vector')
    else:
        if not isinstance(inp, (float, int, np.number)): raise Exception(f'Argument {var_name} must be scalar or vector')