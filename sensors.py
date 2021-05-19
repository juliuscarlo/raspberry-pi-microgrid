#!/usr/bin/python3

from datetime import datetime
import os
import time
import logging
from pijuice import PiJuice

logging.basicConfig(level=logging.INFO, filename="logs/microgrid.log")


# TODO: Add average functionality? Doesn't make sense for status, but maybe for other readings
def read_sensors(pijuice, frequency):
    """Gets sensor readings from PiJuice module.

    Args:
        pijuice (obj): The initialized PiJuice object.
        frequency (int): The number of readings to take.

    Returns:
        data (dict): Sensor readings from the PiJuice module.
    """

    data = dict()
    data["general_status"] = pijuice.status.GetStatus()

    # TODO: Add loop that averages using the specified frequency
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
