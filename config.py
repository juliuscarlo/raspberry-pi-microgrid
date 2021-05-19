#!/usr/bin/python3

# local information
location = "Mannheim"
solar_watts = 20

# Adjust at which battery percentage the Pi should start performing calculations
surplus_threshold = 85

# Specify headers for the csv logs. Must match data from sensors.
grid_headers = ["1", "2"]  # TODO: add correct headers for the grid csv file
computations_headers = ["x", "y"]  # TODO: add correct headers for computations csv file

