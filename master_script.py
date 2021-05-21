#!/usr/bin/python3

import helper
import dispatcher
import sensors
import csv_logger
import config
import logging


def initial_boot_sequence():
    """Performs mandatory steps after wakeup from sleep. Returns the pijuice object for further use."""
    logging.info("%s %s", helper.current_time(), "Initial boot sequence started...")

    helper.wait_for_pijuice_com()  # wait for PiJuice com to initialize
    pijuice = helper.pijuice_init()  # initialize the PiJuice object
    helper.wakeup_enable(pijuice)  # enable the alarm to ensure wakeup after next sleep phase

    system_status = sensors.read_sensors(pijuice)
    csv_logger.write_row(event="wakeup", data=system_status)
    logging.info("%s %s", helper.current_time(), "Initial boot sequence complete...")

    # TODO: add a check for battery level. If  70 <= battery_level <= 85 set the alarm to 15 minute intervals
    # for <70 leave the alarm at one hour intervals. This allows the pi to react more quickly to high energy
    # production when the solar panel is working at full capacity.

    return pijuice


def logging_routine(pijuice):
    """Performs the logging and computational routine."""
    logging.info("%s %s", helper.current_time(), "Logging and computational routine started...")

    system_status = sensors.read_sensors(pijuice)
    logging.info("%s %s", helper.current_time(), system_status)

    units_computed = 0  # counts the units computed during a computing session

    if system_status["battery_level"] >= config.surplus_threshold:
        logging.info("%s %s", helper.current_time(), "Battery above threshold, starting computations...")
        csv_logger.write_row(event="start_compute", data=system_status)

    while system_status["battery_level"] >= config.surplus_threshold:
        # if battery sufficient, start computing. Continue computing until battery threshold is breached.

        system_status = dispatcher.compute_unit(pijuice)
        units_computed += 1
        csv_logger.write_row(event="unit_computed", data=system_status)

        if units_computed % 5 == 0:
            logging.info("%s %s %s", helper.current_time(), system_status, " --> 5 units computed. ")

    logging.info("%s %s", helper.current_time(), "Battery below threshold, stopped computations.")
    logging.info("%s, %s, %s", helper.current_time(), "Total units computed during this session: ", units_computed)

    system_status = sensors.read_sensors(pijuice)
    csv_logger.write_row(event="stop_compute", data=system_status)


def shutdown_routine(pijuice):
    logging.info("%s %s", helper.current_time(), "Initiating shutdown routine.")
    system_status = sensors.read_sensors(pijuice)
    csv_logger.write_row(event="shutdown", data=system_status)
    dispatcher.shutdown(pijuice)


if __name__ == "__main__ ":
    """Runs the three phases of the microgrid system sequentially when this script is executed."""

    # set up logging
    logging.basicConfig(level=logging.INFO, filename="logs/microgrid.log")

    # Run the three phases sequentially
    pijuice = initial_boot_sequence()  # the initial sequence returns the pijuice object for further use
    logging_routine(pijuice)
    shutdown_routine(pijuice)
