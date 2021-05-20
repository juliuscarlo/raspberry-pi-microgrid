# Microgrid with Raspberry Pi and PiJuice

Measures output of a Raspberry Pi that draws power from a PiJuice module in the form of calculations performed.

## Modules

### master_script.py

The master_script needs to be run at boot. It can be added to the Pi crontab. This contains the general logic
of the microgrid.

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