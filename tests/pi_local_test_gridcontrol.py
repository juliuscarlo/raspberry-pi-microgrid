#!/usr/bin/python3
"""Used to test locally on the pi. Must be run from the raspberry-pi-microgrid project root."""

import microgrid.helper
import logging
import gridcontrol as gridcontrol

logging.basicConfig(level=logging.INFO, filename="logs/microgrid.log")

# pijuice = gridcontrol.initial_boot_sequence()

# ridcontrol.logging_routine(pijuice)

# print("Testing shutdown! will shutdown in 120 sec...")
gridcontrol.shutdown_routine(pijuice)
