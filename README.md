
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

Usage:

serial_data_manipulation.py requires an instance of cal_data to work 

cal_data can be populated by read_json_from_file() from utils.py




### Main functions

Dwell 
`dwell()`

Sets a target frequency in GHz and mantains it for a given amount of data points to take.

Scan
`scan()`

Scans in a set range of GHz from start to stop and back once.

Phase Modulation

`scan_pm()`
`dwell_pm()`

These funcions work the same as their non modulated counterparts they simply turn on the phase modulation in the PB7300 before it starts to operate.