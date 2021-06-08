# Microgrid with Raspberry Pi and PiJuice

Measures output of a Raspberry Pi that draws power from a PiJuice module in the form of calculations performed.


## Setup

### Copy the project folder
Copy the raspberry-pi-microgrid project to your /home/pi folder or wherever you want it. Configure
the config.py according to your setup. 

### Permissions
Set permissions for the microgrid project, otherwise cron will not
be able to run the gridcontrol:

`chmod -R 755 raspberry-pi-microgrid/`

### Real Time Clock (RTC)

If the ID EEPROM address is set to 0x50, there might be issues with wakeup enable getting deactivated at every boot. In this case changing it to 0x52 fixed the problem on at least one occasion.

Check the if the RTC driver is loaded
using`i2cdetect -y 1`. There should be 'UU' in position 68. Otherwise the RTC needs
to be added as follows:

Add `dtoverlay=i2c-rtc,ds1339` as a new line to `/boot/config.txt`

The RTC can be read using the command `sudo hwclock -r`. 

### Cronjob (Required to keep microgrid running) 

Open the crontab (as user pi, not sudo!):

`crontab -e`

Add this entry (adjust path to your project):

`@reboot /usr/bin/python3 /home/pi/raspberry-pi-microgrid/gridcontrol.py`



## Modules

### gridcontrol.py

This is the entry point and controls the overall microgrid system. The
gridcontrol needs to be started automatically at boot time. It can
be added to the crontab. Run this file with `python3 gridcontrol.py`
to manually start the microgrid system. 

### dispatcher.py

Contains methods for the general steering ("dispatching") of the microgrid system. This includes methods to start
computations or shutdown the pi.

### helper.py

Has methods to initialize the pijuice communication, get the current time and other useful functions
like changing the wakeup alarm settings.

### csv_logger.py

The csv_logger contains all methods related to writing information to csv files that can be used to analyze the
microgrid system.

### sensors.py

Contains the methods used to retrieve sensor data from the PiJuice.

### config.py

The config contains experiment-specific information such as geographic location and installed solar capacity. This can
be adjusted according to the specific location and setup. It is also used to switch on or off the
utilization of surplus energy to allow different types of experiments to be performed.

## Logs
There are two logs written to /logs:
- microgrid.log for system monitoring and debugging
- grid.csv for quantitative analysis

## Tests
There are some testfiles included in /tests that might need
some adjustments before being usable. Check the comments in these
files and adjust them to test indivodual modules or
methods. 
