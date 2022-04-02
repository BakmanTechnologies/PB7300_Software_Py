import math
import hashlib
import json
import os


def test_eeprom():
    string1 = "hehe"
    accsii = ""

    for i in string1:
        accsii += str(hex(ord(i)))

    print(accsii)

    hexstring1 = hex(string1)

    print(hexstring1)
    sha1 = hashlib.sha1(hexstring1)
    print(sha1)


jsonlist = os.listdir("calibration")

# selects most recent file

# opens the json file with the retrieved file name string


def open_json():
    """opens local path floder calibration and sorts them by name"""
    jsonlist.sort()
    recent_file_selection = jsonlist[-1]
    print(recent_file_selection)

    with open(f"calibration/{recent_file_selection}") as json_file:
        jsondata = json.load(json_file)
        # importdata = Scandata(jsondata)
        # print(importdata.get_username())
        # print(importdata.get_scanTime())
        # print(importdata.get_upScanFreq())

    return jsondata


def load_json():
    raw_json = open_json()
    print(raw_json)
    print(raw_json["CalibrationTime"])


load_json()
# test_eeprom()


Spectrometer_SN
MainBoard_Version
Limit_Min_Freq_MHz
Limit_Max_Freq_MHz
Limit_Min_Freq_Resolution_MHz
LaserControl
Phase_Modulator_Installed
Phase_Modulator_SN
phaseModulateType
StablizeStartFac
StablizeTransFac
StablizeStartCnt
StablizeTransCnt
PowerMode
PcsBias
SourcePcsCorrection
DetectorPcsCorrection
Channels
coeffUpDw()
gain
ZeroCross
L1_Minus_L0
Second_Harmonic
