import json
import os
import time
import tkinter as tk
from matplotlib import pyplot as plt
import matplotlib.animation as animation


master = tk.Tk()

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


def test_timer():
    plt.ion()

    while 1:
        print("Testing!")
        time.sleep(1)


fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)


def animate(i):

    xar = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    yar = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
    ax1.clear()
    ax1.plot(xar, yar)


ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
test_timer()
