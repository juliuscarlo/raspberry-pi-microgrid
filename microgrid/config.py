#!/usr/bin/python3

import os

# set project root by specifying the path to the gridcontrol.py
ROOT_DIR = os.path.dirname(os.path.abspath("/home/pi/raspberry-pi-microgrid/gridcontrol.py"))

# local information
location = "Mannheim"
solar_capacity = 20

# Adjust at which battery percentage the Pi should start performing calculations
surplus_threshold = 85

# Below this battery level threshold, pi will wait for 60 minutes before next wake-up after shutting down.
hourly_checks_threshold = 65

# How many individual readings should be taken by the sensors.read_average method before averaging?
number_of_reads = 100

# Specify whether surplus should be utilized by the Pi (by calculating units), or if it should only perform logging.
surplus_utilization = True

# Specify headers for the csv files. Must match data from sensors for grid data and from computations for comp data
# Must match the naming convention used in sensors and csv_logger!
grid_headers = ["timestamp",
                "location",
                "solar_capacity",
                "event",
                "isFault",
                "battery_state",
                "power_input_state",
                "power_input_5v_io",
                "battery_temperature",
                "battery_level",
                "battery_voltage",
                "battery_current",
                "io_voltage",
                "io_current"]
