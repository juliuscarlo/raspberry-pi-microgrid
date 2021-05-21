#!/usr/bin/python3
"""Used to test locally on the pi. Must be run from the microgrid module folder."""
from microgrid import sensors
from microgrid import dispatcher
from pijuice import PiJuice



def pijuice_init():
    """Initialize the PiJuice module"""
    pijuice = PiJuice(1, 0x14)
    return pijuice


pijuice = pijuice_init()

data = sensors.read_sensors(pijuice)

print("single read: ")
print(data)

data = sensors.read_average(pijuice, frequency=100)
# print(data)
print("multi read: ")
print(data)

print("Test the dispatcher...")
data = dispatcher.compute_unit(pijuice)
print(data)
