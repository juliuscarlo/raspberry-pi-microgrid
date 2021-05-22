#!/usr/bin/python3

import os

# TODO: also manage the sensor frequency from here, as well as the other thresholds for computing etc.

# set project root by specifying the path to the gridcontrol.py
ROOT_DIR = os.path.dirname(os.path.abspath("/home/pi/raspberry-pi-microgrid/gridcontrol.py"))

# local information
location = "Mannheim"
solar_capacity = 20

# Adjust at which battery percentage the Pi should start performing calculations
surplus_threshold = 85

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
