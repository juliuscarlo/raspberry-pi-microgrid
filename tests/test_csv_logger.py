#!/usr/bin/python3
"""Tests the csv logger, can be run in any environment."""

import unittest
from microgrid.csv_logger import write_row


# Test the csv writer

class TestCsvLogger(unittest.TestCase):
    def test_write_row(self):
        """ Test that the writer writes a csv. It will be in the tests/logs folder."""
        test_data = {'isFault': "False", 'battery_state': 'CHARGING_FROM_5V_IO', 'power_input_state': 'NOT_PRESENT',
                     'power_input_5v_io': 'PRESENT', 'battery_temperature': 34, 'battery_level': 90,
                     'battery_voltage': 4190, 'battery_current': -541, 'io_voltage': 4976, 'io_current': -332}

        write_row(event="start_compute", data=test_data)


if __name__ == "__main__":
    unittest.main()
