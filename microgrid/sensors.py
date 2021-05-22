#!/usr/bin/python3

import time
import statistics
from microgrid import config


def read_sensors(pijuice):
    """Gets sensor readings from PiJuice module.

    Args:
        pijuice (obj): The initialized PiJuice object.

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
    data["isFault"] = str(status["isFault"])  # e.g. False
    data["battery_state"] = status["battery"]  # e.g. 'CHARGING_FROM_IN'
    data["power_input_state"] = status["powerInput"]  # e.g. 'PRESENT',
    data["power_input_5v_io"] = status["powerInput5vIo"]  # e.g. 'NOT_PRESENT'

    # since these are all integer variables, we can e.g. make a loop of X readings and keep the average
    data["battery_temperature"] = pijuice.status.GetBatteryTemperature()["data"]
    data["battery_level"] = pijuice.status.GetChargeLevel()["data"]
    data["battery_voltage"] = pijuice.status.GetBatteryVoltage()["data"]
    data["battery_current"] = pijuice.status.GetBatteryCurrent()["data"]
    data["io_voltage"] = pijuice.status.GetIoVoltage()["data"]
    data["io_current"] = pijuice.status.GetIoCurrent()["data"]

    return data


def read_average(pijuice, frequency=config.number_of_reads):
    """Takes n sensor readings and calculates a single value for each variable. Returns the sensor readings dict."""

    data = dict()

    single_read = read_sensors(pijuice)  # initial read
    for key, value in single_read.items():
        data[key] = [value]  # make list structure to append values from later readings

    for n in range(1, frequency):
        time.sleep(0.01)
        single_read = read_sensors(pijuice)
        for key, value in single_read.items():
            data[key].append(value)

    # Reduce the n readings to a single reading, chose a measure depending on the data type
    for key in data.keys():
        if type(data[key][0]) == str:
            data[key] = statistics.mode(data[key])  # use mode for strings (most frequent value)
        else:
            data[key] = statistics.mean(data[key])  # use mean for numerical values

    return data
