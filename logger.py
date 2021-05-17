#!/usr/bin/python3

from datetime import datetime
import os
import time
import logging
from pijuice import PiJuice


logging.basicConfig(level=logging.INFO, filename="microgrid.log")

pijuice = PiJuice(1, 0x14)

logging.info('Starting logging.py...')
for i in range(10):
   currentTime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

   generalStatus = pijuice.status.GetStatus()

   batteryTemperature = pijuice.status.GetBatteryTemperature()["data"]
   batteryLevel = pijuice.status.GetChargeLevel()["data"]
   batteryVoltage = pijuice.status.GetBatteryVoltage()["data"]
   batteryCurrent = pijuice.status.GetBatteryCurrent()["data"]

   IoVoltage = pijuice.status.GetIoVoltage()["data"]
   IoCurrent = pijuice.status.GetIoCurrent()["data"]

   #print(currentTime, generalStatus, "bat temp:", batteryTemperature, "bat Level:", batteryLevel, \
   #"bat V:", batteryVoltage, "bat mA:", batteryCurrent, "Io V:", IoVoltage, "Io mA:", IoCurrent)

   logging.info('%s %s %s %s %s %s %s %s', currentTime, generalStatus, batteryTemperature, batteryLevel, batteryVoltage, batteryCurrent, IoVoltage, IoCurrent)

   time.sleep(1)

logging.info('Status check complete. Commencing battery-level check.')
unitsCalculated = 0
if batteryLevel >= 85:
   logging.info('Loading all 4 CPU cores.')
while batteryLevel >= 85:
   # make the pi calculate stuff with all 4 cores and keep track of performed calculations
   os.system("sysbench --num-threads=4 --test=cpu --cpu-max-prime=5000 run")
   time.sleep(15)
   unitsCalculated += 1
   if unitsCalculated % 5 == 0:
      logging.info('Completed 5 Calculations.')
   # update the battery level so that the while loop can be exited when the battery is below the threshold
   batteryLevel = pijuice.status.GetChargeLevel()["data"]

# If while loop exits, write to log what happened
logging.info('%s %s', 'Units calculated during this session: ', unitsCalculated)
logging.info('%s %s %s %s %s %s %s %s', currentTime, generalStatus, batteryTemperature, batteryLevel, batteryVoltage, batteryCurrent, IoVoltage, IoCurrent)
logging.info('Battery below threshold, shutting down pi.')

# Cut power to the pi with 30 sec delay, shutdown the pi and wait for battery to go over the threshold again
logging.info('Shutdown will be issued in 2:00 minutes. PiJuice will cut power in 2:30 minutes.')
time.sleep(120)
pijuice.power.SetPowerOff(30)
os.system("sudo shutdown -h now")
