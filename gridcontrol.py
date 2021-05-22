#!/usr/bin/python3

from microgrid import helper
from microgrid import dispatcher
from microgrid import sensors
from microgrid import csv_logger
from microgrid import config
import logging
import os


def initial_boot_sequence():
    """Performs mandatory steps after wakeup from sleep. Returns the pijuice object for further use."""
    logging.info("%s %s", helper.current_time(), "Initial boot sequence started...")

    helper.wait_for_pijuice_com()  # wait for PiJuice com to initialize
    pijuice = helper.pijuice_init()  # initialize the PiJuice object
    helper.wakeup_enable(pijuice)  # enable the alarm to ensure wakeup after next sleep phase

    system_status = sensors.read_average(pijuice)
    csv_logger.write_row(event="wakeup", data=system_status)
    logging.info("%s %s", helper.current_time(), "Initial boot sequence complete...")

    return pijuice


def computation_routine(pijuice):
    """Performs the logging and computational routine."""
    logging.info("%s %s", helper.current_time(), "Logging and computational routine started...")

    system_status = sensors.read_average(pijuice)
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

    logging.info("%s %s", helper.current_time(), "Battery below threshold, ended computation routine.")
    logging.info("%s, %s, %s", helper.current_time(), "Total units computed during this session: ", units_computed)

    system_status = sensors.read_average(pijuice)

    if units_computed > 0:
        csv_logger.write_row(event="stop_compute", data=system_status)


def shutdown_routine(pijuice):
    logging.info("%s %s", helper.current_time(), "Initiating shutdown routine.")
    system_status = sensors.read_average(pijuice)
    csv_logger.write_row(event="shutdown", data=system_status)

    # Adjust wakeup frequency depending on battery level
    if system_status["battery_level"] < config.hourly_checks_threshold:
        helper.next_wakeup_in(pijuice, minutes=60)
        logging.info("%s %s", helper.current_time(), "Next wake-up in 60 minutes.")
    else:
        helper.next_wakeup_in(pijuice, minutes=15)
        logging.info("%s %s", helper.current_time(), "Next wake-up in 15 minutes.")

    dispatcher.shutdown(pijuice)


if __name__ == "__main__":
    """Runs the three phases of the microgrid system sequentially when this script is executed."""
    # set up logging
    logging.basicConfig(level=logging.INFO, filename=os.path.join(config.ROOT_DIR, "logs/microgrid.log"))

    # Run the three phases sequentially
    pijuice = initial_boot_sequence()  # the initial sequence returns the pijuice object for further use
    computation_routine(pijuice)
    shutdown_routine(pijuice)
