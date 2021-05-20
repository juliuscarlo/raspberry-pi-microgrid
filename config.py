#!/usr/bin/python3

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
