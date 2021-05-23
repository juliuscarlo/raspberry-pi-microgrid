# Microgrid with Raspberry Pi and PiJuice

Measures output of a Raspberry Pi that draws power from a PiJuice module in the form of calculations performed.


## Setup

### Copy the project folder
Copy the raspberry-pi-microgrid project to your /home/pi folder or wherever you want it.

### Permissions
Set permissions for the microgrid project, otherwise cron will not
be able to run the gridcontrol:

`chmod -R 755 raspberry-pi-microgrid/`

### Real Time Clock (RTC)

Check if the ID EEPROM address is 0x50. Check the if the RTC driver is loaded
using`i2cdetect -y 1`. There should be 'UU' in position 68. Otherwise the RTC needs
to be added as follows:

Add `dtoverlay=i2c-rtc,ds1339` to `/boot/config.txt`

The RTC can be read using the command `sudo hwclock -r`

Open the crontab (as user pi, not sudo!):

`crontab -e`

Add this entry:

`@reboot /usr/bin/python3 /home/pi/raspberry-pi-microgrid/gridcontrol.py`



## Modules

### gridcontrol.py

This is the entry point and controls the overall microgrid system. The
gridcontrol needs to be started automatically at boot time. It can
be added to the crontab.

### dispatcher.py

Contains methods for the general steering ("dispatching") of the microgrid system. This includes methods to start
computations or shutdown the pi.

### helper.py

Has methods to initialize the pijuice communication, get the current time and other useful functions.

### csv_logger.py

The csv_logger contains all methods related to writing information to csv files that can be used to analyze the
microgrid system.

### sensors.py

Contains the methods used to retrieve sensor data from the PiJuice.

### config.py

The config contains experiment-specific information such as geographic location and installed solar capacity. This can
be adjusted according to the specific location and setup.
