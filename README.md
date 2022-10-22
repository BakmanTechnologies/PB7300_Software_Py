
# PB7300 Control Software
Created for Bakman Technologies by Ricardo Franco
## Requirements

* Windows 10
* Python 3.8.xx
* PB7300 Spectrometer Rev5+


## Installation

1. Create virtual environment in root directory using venv 

  `python -m venv env `

2. Activate virtual environment

  `source env/Scripts/activate`

3. Install dependencies

  `pip install -r requirements.txt`


## Overview
This program is designed to talk to the PB7300 instrument through a serial port.

When running for the first time the software will check if the /calibration and /data directories exists, if not it will create them in the base directory /PB7300_Software_Py 

The software will look in /calibration for the factory calibration file, if empty it will extract the calibration from the EEPROM memory and save it in /calibration.

The software needs this calibration file in order to run. Modifying this file is heavily discouraged as it contains vital information for running the PB7300 Spectrometer. Any change to the values in this file may affect the performance and may even risk damaging the lasers permanently


## Setup

Turn on the PB7300 and connect to it using the USB-B to USB-A cable.

COM Port Setup (Windows):

1. Open Windows Device Manager and look for the Ports (COM & LPT) section.
![mmc_KJy5jJBwH0](https://user-images.githubusercontent.com/86385396/197352945-67bbbd13-b5cb-4ddc-b6ff-3d5b4cf9f918.png)

2. Right click on the corresponing com port for the PB7300 and select properties, in this case its COM5. If you are not sure which COM port corresponds to the PB7300 you can turn it off and check the device manager again to see which COM port is missing. Navigate to the Port Settings tab and change the Bits per second to 115200.

![mmc_5irggirXga](https://user-images.githubusercontent.com/86385396/197353813-4b91a908-f4ab-416b-bb2f-5a448b68a590.png)

3. In the same Port Settings tab select the Advanced button. This will open the advanced port settings. Under BM Options change the latency timer to 1(msec). Select OK in the advance setting windows and OK in the Port Settings tab. Restart your computer to apply these settings.

![mmc_L9YtIR7WJh](https://user-images.githubusercontent.com/86385396/197355917-986ab906-2e8e-4213-a03c-74aa8aee6309.png)

## Description:
`serial_commands_PB7300.py:`
Contains the command list to operate the PB7300 Rev5. Modifying this file is highly discouraged as it can affect the performance of the spectrometer and potentially damage the lasers.

`serial_data_manipulation.py:`
Contains the main functions to use the PB7300, requires an instance of a populated cal_data to be passed as an argument to be used.

`cal_data.py:`
Contains python class to be populated by deserialized json values. Modifying this file is highly discouraged as it can affect the performance of the spectrometer and potentially damage the lasers.

`utils.py:`
Contains helper functions for setting up and using the script. Creates file directories on first run. Checks for calibration .json, extracts json file from eeprom memory if missing and deserializes json to cal_data object. Creates .csv data files to dump scan and dwell data from serial_data_manipulation.py.

## Main functions

### Dwell 
`dwell(self, target_ghz: float, time_constant: int, number_of_data_points: int):`

Sets a target frequency in GHz and mantains it for a given amount of data points to take. Returns list of time stamps (seconds) and lockin power readings (arb).

target_ghz: Frequency at which the system will reach and mantain.

time_constant: Speed at which the values are going to be read from the PB7300 in miliseconds. (100 ms recommended) Lowering it under 50ms risks encountering com port errors.

number_of_data_points: Amount of data points to be saved, dwell ends when value is reached.



### Scan
`scan(self, start_freq_ghz: float, stop_freq_ghz: float, step_size_ghz: float, time_constant_ms: int, only_up: Boolean = False):`

Scans in a set range of GHz from start to stop and back once. Returns list of frequencies (GHz) and and lockin power readings (arb).

start_freq_ghz: Frequency in GHz to start the scan at.

stop_freq_ghz: Frequency in GHz to stop the scan at.

step_size_ghz: Step size between each reading of the scan in GHz. Supports decimal values.

time_constant_ms: Speed at which the values are going to be read from the PB7300 in miliseconds. (100 ms recommended) Lowering it under 50ms risks encountering com port errors.


Phase Modulation

`scan_pm()`
`dwell_pm()`

These funcions work the same as their non modulated counterparts they simply turn on the phase modulation in the PB7300 before it starts to operate.

## Usage
The script can be run on its own by using the main.py included in the repo, the first time running the script main should look like this:

`cal_data = read_json_from_file()`

`serial_data_manipulation = SerialDataManipulation(cal_data)`

`serial_data_manipulation.display_system_info()`

`serial_data_manipulation.close_port()`

After this initial setup the script should be setup for regular operation.

Just uncomment one of the main functions and replace the example values with the values desired to operate with. 



## Troubleshooting:
Due to the nature of serial communication most of the errors encountered during script operation can be attributed to the communication speed on the COM port. The COM port settings above MUST be used for proper operation of the PB7300 using the python script. 

In serial_commands_PB7300.py line 28 contains a constant READ_WRITE_DELAY, this can be changed to allow time for the returning bytes to be read if the com port is having speed issues. Small increments should be made as the effect is over the entire com port pipeline.

These are the errors expected from COM port speed issues.

rx_bytes referenced before assignment.

AttributeError: 'NoneType' object has no attribute 'hex'

There seems to be a component of witchcraft involved in serial communication that I do not possess knowledge of, so please bear that in mind if you have difficulty with this aspect of the code. 
