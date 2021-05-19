#!/usr/bin/python3

import helper
import dispatcher
import sensors
import csv_logger
import config
import logging


def initial_boot_sequence():
    """Performs mandatory steps after wakeup from sleep."""
    logging.info("Initial boot sequence started...")
    helper.wait_for_pijuice_com()  # wait for PiJuice com to initialize
    pijuice = helper.pijuice_init()  # initialize the PiJuice object
    helper.wakeup_enable(pijuice)  # enable the alarm to ensure wakeup after next sleep phase

    system_status = sensors.read_sensors(pijuice)
    csv_logger.write(filename="logs/grid.log", event="boot", data=system_status)
    # Todo: what is the right format for the system_status?


def logging_routine():
    """Performs the logging and computational routine."""
    logging.info("Logging routine started...")

    system_status = sensors.read_sensors()
    csv_logger.write(system_status)

    units_computed = 0

    if system_status["battery_level"] >= config.surplus_threshold:
        logging.info("Battery above threshold, starting computations...")

    # start logging - always log in fixed intervals while pi is online

    while system_status["battery_level"] >= config.surplus_threshold:
        # if battery sufficient, start computing. Continue computing until bat.threshold is breached

        system_status = sensors.read_sensors(helper.pijuice_init())
        csv_logger.write(filename="logs/grid.log", event="compute", data=system_status)

        dispatcher.compute_unit()
        units_computed += 1
        csv_logger.write(filename="logs/computations.log", event="unit_computed", data=units_computed)

        # write to computation log when a unit is completed. Todo: which data to write? uptime? count units in period?
        if units_computed % 5 == 0:
            logging.info("5 units computed.")  # write to system log

    logging.info("%s, %s", "Total units computed during this session:", units_computed)


if __name__ == "__main__ ":
    """Runs the three phases of the microgrid system sequentially when this script is executed."""
    initial_boot_sequence()
    logging_routine()
    dispatcher.shutdown(helper.pijuice_init())
