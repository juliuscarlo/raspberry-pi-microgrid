#!/usr/bin/python3

from datetime import datetime
import os
import time
import logging

logging.basicConfig(level=logging.INFO, filename="logs/microgrid.log")


# TODO: maybe find a better way to simulate computation, something that can be limited in time precisely
def compute_unit():
    """Loads the Pis CPU cores to simulate computational tasks. The sysbench program computes prime numbers up to
    the specified integer. The sleep was implemented with a margin to allow for the computations to finish (since
    they are not running in Python). This is to avoid multiple of these computational tasks to be spawned
    simultaneously.

    Returns:
        Bool: True when (approximately) done computing one unit.
    """

    os.system("sysbench --num-threads=4 --test=cpu --cpu-max-prime=5000 run")
    time.sleep(15)

    return True


def shutdown(pijuice):
    """Shutdown the Pi after 120 seconds of safety margin to prevent fatal instantaneous shutdowns performed at
    reboot by the crontab that make debugging impossible. Then cut power to the Pi with a 30 sec delay, to ensure
    that the Pi has enough time to safely shutdown before being cut off from power.

    Args:
        pijuice (obj): The initialized PiJuice object.
    """

    logging.info('Shutdown will be issued in 2:00 minutes. PiJuice will cut power in 2:30 minutes.')
    time.sleep(120)
    pijuice.power.SetPowerOff(30)
    os.system("sudo shutdown -h now")
