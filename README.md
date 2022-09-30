Created for Bakman Technologies by Ricardo Franco

This program is designed to talk to the PB7300 instrument through a RS-232 serial port

It requires the factory calibration file from the unit in the /calibration folder to operate

It requires a /data folder to save the dwell or scan files


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

