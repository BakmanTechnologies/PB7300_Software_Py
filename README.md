
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

### Initial Setup

The base file structure required to run the program must be setup.  

1. In utils.py create_dir() must be run first time to create /calibration for the calibration files, and /data for saving the data captured. 


Usage:

serial_data_manipulation.py requires an instance of cal_data to work 

cal_data can be populated by read_json_from_file() from utils.py

read_json_from_file() needs a calibration file from the PB7300 in /calibration to work


Main functions

Dwell 

dwell_control()


Scan

scan()


Phase Modulated Scan

scan_pm()

