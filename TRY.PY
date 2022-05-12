import json
import os
from re import U
import time
import tkinter as tk
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation


jsonlist = os.listdir("calibration")

"""opens local path floder calibration and sorts them by name"""
jsonlist.sort()

if len(jsonlist) == 0:
    print("Calibration directory empty")
    recent_file_selection = "0"
else:
    #print(len(jsonlist))
    recent_file_selection = jsonlist[-1]
    #print(recent_file_selection)


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

def test_ifs():
    ld0_correction_found = True
    ld1_correction_found = False

    if ld0_correction_found == False or ld1_correction_found == False:
            print("False")

def int32(x):
    if x>0xFFFFFFFF:
        raise OverflowError
    if x>0x7FFFFFFF:
        x=int(0x100000000-x)
        if x<2147483648:
            return -x
        else:
            return -2147483648
    return x

def test_behavior():

    unsigned_list = []
    
    value = b'\xaaH\x00\x00 \xc2\x00\x00\x01\x94'

    version_hex = value.hex()

    char_count = 2

    split_hex_version = [version_hex[i:i+char_count]
                            for i in range(0, len(version_hex), char_count)]

    #test_int =  int.from_bytes(b'\xaa`\x00\x12\xad*k\r<\xde', "big")
    
    for i in range(10):
        unsigned_list.append(np.uint8(value[i]))

    print(value[0],value[1],value[2],value[3],value[4],value[5],value[6],value[7],value[8],value[9])
    print(unsigned_list)

    if value[2] == 255:
        unsigned_list[2] = np.uint8(0)
        register = -1
        print("entered")
    else:
        register = 1

    value_mod = (int32(unsigned_list[2]) << 24) | (int32(unsigned_list[3]) << 16) | (int32(unsigned_list[4]) << 8) | (int32(unsigned_list[5]))*register

    print(unsigned_list)

    if split_hex_version[2] == "ff":

        built_from_hex = f"-{split_hex_version[3]}{split_hex_version[4]}.{split_hex_version[5]}"

        value_mod_no_ff  =  (int32(value[3]) << 16) | (int32(value[4]) << 8) | (int32(value[5]))*-1
    else:
        built_from_hex = f"{split_hex_version[3]}{split_hex_version[4]}{split_hex_version[5]}"

        value_mod_no_ff  =  (int32(value[3]) << 16) | (int32(value[4]) << 8) | (int32(value[5]))

    #for i in range(10):
        
        #test_decimal_list.append(int(split_hex_version[i], 16)) 

    #test_decimal_built = int(built_from_hex,16)

    #print(split_hex_version)

   # print(test_decimal_list)

   # print(test_decimal_built)

    print(value_mod)

    #print(value_mod_no_ff)

    #test_convert = np.int32(value)

    #int32(value)

    #convert = int(value,16) 0 , 9 , 132 , 150


test_behavior()