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
    csv_logger.write_grid_csv(filename="grid.csv", event="wakeup", data=system_status)
    # Todo: what is the right format for the system_status?
    logging.info("%s %s", helper.current_time(), "Initial boot sequence complete...")
    return pijuice


def logging_routine(pijuice):
    """Performs the logging and computational routine."""
    logging.info("%s %s", helper.current_time(), "Logging and computational routine started...")

    system_status = sensors.read_sensors(pijuice)
    logging.info("%s %s", helper.current_time(), system_status)
    csv_logger.write_grid_csv(filename="grid.csv", event="idle", data=system_status)

    units_computed = {"units_computed": 0}  # counts the units computed during a computing session

    if system_status["battery_level"] >= config.surplus_threshold:
        logging.info("%s %s", helper.current_time(), "Battery above threshold, starting computations...")
        csv_logger.write_grid_csv(filename="grid.csv", event="start_compute", data=system_status)

    # start logging - always log in fixed intervals while pi is online

    while system_status["battery_level"] >= config.surplus_threshold:
        # if battery sufficient, start computing. Continue computing until battery threshold is breached
        units_computed["units_computed"] += dispatcher.compute_unit()
        system_status = sensors.read_sensors(pijuice)
        csv_logger.write_grid_csv(filename="grid.csv", event="unit_computed", data=system_status)
        csv_logger.write_grid_csv(filename="computations.csv", event="unit_computed", data=units_computed)

        # write to computation log when a unit is completed. Todo: which data to write? uptime? count units in period?
        if units_computed["units_computed"] % 5 == 0:
            logging.info("%s %s", helper.current_time(), "5 units computed.")  # write to system log

    logging.info("%s %s", helper.current_time(), "Battery below threshold, computations stopped...")
    logging.info("%s, %s, %s", helper.current_time(), "Total units computed during this session: ",
                 units_computed["units_computed"])


if __name__ == "__main__ ":
    """Runs the three phases of the microgrid system sequentially when this script is executed."""
    pijuice = initial_boot_sequence()  # the initial sequence returns the pijuice object for further use
    logging_routine(pijuice)
    dispatcher.shutdown(pijuice)
