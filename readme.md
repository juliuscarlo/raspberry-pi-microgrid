# Microgrid with Raspberry Pi and PiJuice

Measures output of a Raspberry Pi that draws power from a PiJuice module in the form of calculations performed.

## Modules

### gridcontrol.py

This is the entry point and controls the overall microgrid system. The
gridcontrol needs to be started automatically at boot time. It can
be added to the crontab.

Open the crontab (as user pi, not sudo!):

`crontab -e`

Add this entry to run the 

`@reboot /usr/bin/python3 /home/pi/raspberry-pi-microgrid/gridcontrol.py`

Set permissions for the microgrid project, otherwise cron will not
be able to run the gridcontrol:

`chmod -R 755 raspberry-pi-microgrid/`

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