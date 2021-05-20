#!/usr/bin/python3

# TODO: Maybe add debugging level logging in case we run into issues?

# TODO: Add average functionality? Doesn't make sense for status, but maybe for other readings
def read_sensors(pijuice, frequency=10):
    """Gets sensor readings from PiJuice module.

    Args:
        pijuice (obj): The initialized PiJuice object.
        frequency (int): The number of readings to take.

    Returns:
        data (dict): Sensor readings from the PiJuice module.

    Example values:
    {'data': {'isFault': False, 'isButton': False, 'battery': 'CHARGING_FROM_IN', 'powerInput': 'PRESENT',
              'powerInput5vIo': 'NOT_PRESENT'}, 'error': 'NO_ERROR'}
    29 99 4188 -65 5025 796
    """

    data = dict()

    status = pijuice.status.GetStatus()["data"]
    # unpack the status information so that we can handle the data easily in a single dictionary
    data["isFault"] = status["isFault"]  # e.g. False
    data["battery_state"] = status["battery"]  # e.g. 'CHARGING_FROM_IN'
    data["power_input_state"] = status["powerInput"]  # e.g. 'PRESENT',
    data["power_input_5v_io"] = status["powerInput5vIo"]  # e.g. 'NOT_PRESENT'

    # TODO: Add loop that averages the sensor data using the specified frequency
    # since these are all integer variables, we can e.g. make a loop of X readings and keep the average
    data["battery_temperature"] = pijuice.status.GetBatteryTemperature()["data"]
    data["battery_level"] = pijuice.status.GetChargeLevel()["data"]
    data["battery_voltage"] = pijuice.status.GetBatteryVoltage()["data"]
    data["battery_current"] = pijuice.status.GetBatteryCurrent()["data"]
    data["io_voltage"] = pijuice.status.GetIoVoltage()["data"]
    data["io_current"] = pijuice.status.GetIoCurrent()["data"]

    return data

    # logging.info('Starting logging.py...')
    # for i in range(100):
    #     logging.info('%s %s %s %s %s %s %s %s', current_time, general_status, battery_temperature, battery_level,
    #                  battery_voltage, battery_current, io_voltage, io_current)
    #
    #     time.sleep(1)
