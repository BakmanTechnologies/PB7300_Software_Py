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


def test_setting():
    temp_scaled = int(100 / 3)

    temp_hex = hex(temp_scaled)

    print(temp_hex)

    n = 2

    split_hex_list = [temp_hex[i:i+n]
                      for i in range(0, len(temp_hex), n)]

    print(split_hex_list)

    current_msb = "00"

    current_lsb = str(split_hex_list[2])


test_setting()
