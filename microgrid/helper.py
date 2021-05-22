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


def set_wakeup_frequency(pijuice, minutes):
    """Sets the intervals in which the PiJuice powers up the pi from sleep.

    Args:
        pijuice (obj): The initialized PiJuice object.
        minutes (int): Number of minutes after the full hour at which to wakeup. Should be 0, 15 or 30.
    """
    pijuice.rtcAlarm.SetAlarm({'second': 0, 'minute': minutes, 'hour': 'EVERY_HOUR', 'day': 'EVERY_DAY'})
