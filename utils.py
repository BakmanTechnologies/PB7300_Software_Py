from cal_data import CalData
import json
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv

fieldnames_dwell = ["Time", "Power"]
fieldnames_scan = ["Frequency", "Power"]


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

def simple_graph(x,y):
    plt.plot(x, y)

    plt.style.use('fivethirtyeight')

    #ax = fig.add_subplot(2, 1, 1)

    # ax.set_yscale('log')

    plt.yscale('log')

    plt.title('Title')
    plt.xlabel('Time')
    plt.ylabel('Power')
    #line = graph.plot(y, color='blue', lw=2)
    # To show the plot
    #ani = FuncAnimation(plt.gcf(), animate, interval = 100)

    plt.axis([x[0], x[-1], 10e-2, 10e8])
    plt.show()

def create_csv_file(scantime):
    
    with open(f"data/dwelldata_{scantime}.csv", 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames_dwell)
        csv_writer.writeheader()

def save_to_csv(info, scantime):

    with open(f"data/dwelldata_{scantime}.csv", 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames_dwell)
        csv_writer.writerow(info)

def create_csv_file_scan(scantime):
    
    with open(f"data/dwelldata_{scantime}.csv", 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames_scan)
        csv_writer.writeheader()

def save_to_csv_scan(info, scantime):

    with open(f"data/dwelldata_{scantime}.csv", 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames_scan)
        csv_writer.writerow(info)