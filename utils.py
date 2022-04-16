from cal_data import CalData
import json
import os


def read_json_from_file():

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

    if os.path.exists(f"calibration/{recent_file_selection}"):
        print("File exists.. Opening")
        with open(f"calibration/{recent_file_selection}") as json_file:
            jsondata = json.load(json_file)
        # print(jsondata["CalibrationTime"])

    else:
        print("No calibration file exists, must read EEPROM")
        # TODO: Make it create json from eeprom to initialize cal_data

    cal_data = CalData(jsondata)

    return cal_data
