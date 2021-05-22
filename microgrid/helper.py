#!/usr/bin/python3

from datetime import datetime
import os
import time
from pijuice import PiJuice


def pijuice_init():
    """Initialize the PiJuice module"""
    pijuice = PiJuice(1, 0x14)
    return pijuice


def current_time():
    """Returns the current timedate."""
    now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    return now


def wait_for_pijuice_com():
    """Waits for PiJuice communication to initialize."""
    while not os.path.exists('/dev/i2c-1'):
        time.sleep(0.1)


def wakeup_enable(pijuice):
    """Enables the wakeup alarm of the PiJuice module. Must be run every time the Pi boots, otherwise the PiJuice
    will be unable to wake up the Pi after it shuts down! Since the start could be very early in the boot sequence,
    it is necessary to wait for the i2c-1 device.
    """
    pijuice.rtcAlarm.SetWakeupEnabled(True)


def next_wakeup_in(pijuice, minutes):
    """Sets the interval in minutes from now, when the pi should wake up from sleep again.

    Args:
        pijuice (obj): The initialized PiJuice object.
        minutes (int): Number of minutes from now the pi should wake up.
    """
    # calculate the minute value needed for the specified interval (mod 60 keeps values senseful across the full hour)
    m = (datetime.now().minute + minutes) % 60
    pijuice.rtcAlarm.SetAlarm({'second': 0, 'minute': m, 'hour': 'EVERY_HOUR', 'day': 'EVERY_DAY'})


def set_wakeup_on_charge(pijuice, battery_level):
    """Sets a battery_level at which the pijuice will start up the pi automatically.

    Args:
        pijuice (obj): The initialized PiJuice object.
        battery_level (int): senseful values are between 10 and 90.
    """
    pijuice.power.SetWakeUpOnCharge(battery_level)
