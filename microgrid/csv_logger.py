#!/usr/bin/python3

import os
import logging
from microgrid import config
from microgrid import helper


def write_row(event, data, filename="grid.csv"):
    """Appends a line to a csv file. Creates the file, if it does not exist yet. Files are in /logs folder.
    Timestamp is generated at write time, location-specific data is read from the config.

    A comma is used as the separator.

    Args:
        filename (str): The name of the csv file to which a line is appended, default is grid.csv
        event (str): The event that has triggered the log.
        data (dict): The data to be written in the new line of the file.
    """

    timestamp = helper.current_time()
    location = config.location
    solar_capacity = config.solar_capacity

    # First the general info is converted to csv format and concatenated to the row string
    row = ""
    row += timestamp + ","
    row += location + ","
    row += str(solar_capacity) + ","
    row += event

    # Then the info from the sensor data dict is read and concatenated to the row string item by item
    for item in config.grid_headers[4:]:
        row += ","
        row += str(data[item])

    # If there is no file yet, create it with headers
    path = os.path.join(config.ROOT_DIR, "logs", filename)

    if not os.path.isfile(path):
        with open(path, 'a') as file:
            file.write(",".join(config.grid_headers) + "\n")

    with open(path, 'a') as file:
        file.write(row + "\n")

    logging.info("%s %s", helper.current_time(), "Row of data appended to csv log.")
