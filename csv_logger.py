#!/usr/bin/python3

from datetime import datetime
import os
import time
import logging
import config
import helper


def write(filename, event, data):
    """Appends a line to a csv file. Creates the file, if it does not exist yet.

    Args:
        filename (str): The name of the csv file to which a line is appended.
        timestamp (str): The current date and time. Is calculated by default.
        location (str): The local timezone.
        event (str): The event that has triggered the log.
        data (dict): The sensor data read from the PiJuice module.
    """

    timestamp = helper.current_time()
    location = config.location
    solar_watts = config.solar_watts

    # TODO: add all the components that need to be logged to the row as strings, separated by a comma
    row = str(event)
    path = os.path.join("/logs", filename)

    with open(path, 'a') as file:
        file.write(row + "\n")

    logging.info("add a smart logging comment here.")
