import math
import hashlib
import json
import os

jsonlist = os.listdir("calibration")

"""opens local path floder calibration and sorts them by name"""
jsonlist.sort()

if len(jsonlist) == 0:
    print("Calibration directory empty")
    recent_file_selection = "0"
else:
    print(len(jsonlist))
    recent_file_selection = jsonlist[-1]
    print(recent_file_selection)


def test_os():
    if os.path.exists(f"calibration/{recent_file_selection}") == True:
        print("File exists.. Opening")
        with open(f"calibration/{recent_file_selection}") as json_file:
            jsondata = json.load(json_file)
        print(jsondata["CalibrationTime"])
    else:
        print("No calibration file exists, must read EEPROM")


test_os()
