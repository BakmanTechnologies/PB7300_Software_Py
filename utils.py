import json
import os
from cal_data import CalData
import matplotlib.pyplot as plt
import csv

fieldnames_dwell = ["Time", "Power"]
fieldnames_scan = ["Frequency", "Power"]
fieldnames_scanpm = ["Frequency", "First Harmonic", "Second Harmonic"]


def read_json_from_file():
    """Opens local path floder calibration and sorts them by name"""

    jsonlist = os.listdir("calibration")

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


def create_dir():
    dir_list = os.listdir()

    if "calibration" and "data" in dir_list:
        pass
    else:
        os.mkdir("calibration")
        os.mkdir("data")

def simple_graph(x, y):
    """Outputs a simple graph at the of a scan or dwell"""

    plt.plot(x, y)

    plt.style.use('fivethirtyeight')
    plt.yscale('log')

    plt.title('Title')
    plt.xlabel('Time')
    plt.ylabel('Power')

    plt.axis([x[0], x[-1], 10e-2, 10e8])
    plt.show()


def create_csv_file(scantime):
    """Creates a file with the scantime at start of dwell"""

    with open(f"data/dwelldata_{scantime}.csv", 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames_dwell)
        csv_writer.writeheader()


def save_to_csv(info, scantime):
    """Saves to file created for dwell,
     takes a dictionary info with values to save"""

    with open(f"data/dwelldata_{scantime}.csv", 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames_dwell)
        csv_writer.writerow(info)


def create_csv_file_scan(scantime):
    """Creates a file with the scantime at start of a scan"""

    with open(f"data/dwelldata_{scantime}.csv", 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames_scan)
        csv_writer.writeheader()


def create_csv_file_scanpm(scantime):
    """Creates a file with the scantime
     at start of a phase modulated scan"""

    with open(f"data/dwelldata_{scantime}.csv", 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames_scanpm)
        csv_writer.writeheader()


def save_to_csv_scan(info, scantime):
    """Saves to file created for scan,
     takes a dictionary info with values to save"""

    with open(f"data/dwelldata_{scantime}.csv", 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames_scan)
        csv_writer.writerow(info)


def save_to_csv_scanpm(info, scantime):
    """Saves to file created for scan,
     takes a dictionary info with values to save"""

    with open(f"data/dwelldata_{scantime}.csv", 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames_scanpm)
        csv_writer.writerow(info)