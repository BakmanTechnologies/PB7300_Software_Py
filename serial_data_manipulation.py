import numpy as np
from serial_commands_PB7300 import SerialCommands
import hashlib


class SerialDataManipulation():

    def __init__(self, cal_data) -> None:
        self.cal_data = cal_data
        self.serial_commands_class = SerialCommands()

    def get_json_string(self):
        """Obtains string of the JSON calibration file in the EEPROM"""

        numlist = []
        string_json = ""
        for i in range(4000):
            numlist.append(self.serial_commands_class.read_eeprom(i))
            if numlist[i] == "ÿ":
                break
            string_json += numlist[i]
        json = string_json

        return json

    def sha1_from_json(self, json_string):
        """Receives json string from EEPROM, SHA1 string and boolean result from SHA1 comparison"""

        # Separates SHA1 from the json string, calculates new SHA1 from read json and compares the two
        split1 = json_string.split("©")
        split2 = split1[1].split("{", 1)
        sha1_from_eeprom = split2[0]
        json_string_cut = "{" + split2[1]
        json_string_cut_bytes = bytes(str(json_string_cut).encode("ascii"))
        sha1_calculate = hashlib.sha1(json_string_cut_bytes).hexdigest()
        sha1_calculate_cap = str.upper(sha1_calculate)

        return sha1_from_eeprom, sha1_calculate_cap

    def check_SHA1(self, SHA1_from_EEPROM, SHA1_calculated):
        is_SHA1_ok = False
        if SHA1_from_EEPROM == SHA1_calculated:
            is_SHA1_ok = True
            print("SHA1 is valid")
        return is_SHA1_ok

    def save_json_to_file(self, json_string, SHA1_calculated):
        with open(f"calibration/{SHA1_calculated}.json", 'w') as outfile:
            outfile.write(json_string)

    def read_json_from_eeprom(self):
        json_string = self.get_json_string()

        SHA1_from_EEPROM, SHA1_calculated = self.sha1_from_json(json_string)

        self.check_SHA1(SHA1_from_EEPROM, SHA1_calculated)

        self.save_json_to_file(json_string, SHA1_calculated)

    def close_port(self):
        self.serial_commands_class.close_port()

    def calculate_temps_for_target_ghz(self, target_ghz):
        """Calculates temperatures for achieving a desired GHz target, returns LD0, LD1 temp"""
        ld0_temp = 0
        ld1_temp = 0

        LASER_TEMP_MAX = 65
        LASER_TEMP_MIN = 5

        laser_0_breakpoints_freq = []
        laser_1_breakpoints_freq = []

        laser_0_breakpoints_temp = []
        laser_1_breakpoints_temp = []

        laser_0_breakpoints_temp.append(self.cal_data.LD0.upscan_breakpoint[0])
        laser_0_breakpoints_freq.append(self.cal_data.LD0.upscan_breakpoint[1])
        laser_0_breakpoints_temp.append(self.cal_data.LD0.upscan_breakpoint[2])
        laser_0_breakpoints_freq.append(self.cal_data.LD0.upscan_breakpoint[3])
        laser_0_breakpoints_temp.append(self.cal_data.LD0.upscan_breakpoint[4])
        laser_0_breakpoints_freq.append(self.cal_data.LD0.upscan_breakpoint[5])

        laser_1_breakpoints_temp.append(self.cal_data.LD1.upscan_breakpoint[0])
        laser_1_breakpoints_freq.append(self.cal_data.LD1.upscan_breakpoint[1])
        laser_1_breakpoints_temp.append(self.cal_data.LD1.upscan_breakpoint[2])
        laser_1_breakpoints_freq.append(self.cal_data.LD1.upscan_breakpoint[3])
        laser_1_breakpoints_temp.append(self.cal_data.LD1.upscan_breakpoint[4])
        laser_1_breakpoints_freq.append(self.cal_data.LD1.upscan_breakpoint[5])

        print(laser_0_breakpoints_freq, laser_0_breakpoints_temp,
              laser_1_breakpoints_freq, laser_1_breakpoints_temp)

        laser_0_set_1 = [float(laser_0_breakpoints_temp[0]),
                         float(laser_0_breakpoints_temp[1])]
        laser_0_set_2 = [float(laser_0_breakpoints_freq[0]),
                         float(laser_0_breakpoints_freq[1])]

        laser_0_set_3 = [float(laser_0_breakpoints_temp[1]),
                         float(laser_0_breakpoints_temp[2])]
        laser_0_set_4 = [float(laser_0_breakpoints_freq[1]),
                         float(laser_0_breakpoints_freq[2])]

        print("LD0")

        print("First Seg:")

        slope_1 = (laser_0_set_1[0] - laser_0_set_1[1]) / \
            (laser_0_set_2[0] - laser_0_set_2[1])

        intercept_1 = (laser_0_set_1[0] - slope_1*laser_0_set_2[0])

        laser_0_temp_seg_1 = slope_1*target_ghz+intercept_1

        print(laser_0_temp_seg_1)

        print("Second Seg:")

        slope_2 = (laser_0_set_3[0] - laser_0_set_3[1]) / \
            (laser_0_set_4[0] - laser_0_set_4[1])

        intercept_2 = (laser_0_set_3[0] - slope_1*laser_0_set_4[0])

        laser_0_temp_seg_2 = slope_2*target_ghz+intercept_2

        print(laser_0_temp_seg_2)

        print("LD1")

        laser_1_set_1 = [float(laser_1_breakpoints_temp[0]),
                         float(laser_1_breakpoints_temp[1])]
        laser_1_set_2 = [float(laser_1_breakpoints_freq[0]),
                         float(laser_1_breakpoints_freq[1])]

        laser_1_set_3 = [float(laser_1_breakpoints_temp[1]),
                         float(laser_1_breakpoints_temp[2])]
        laser_1_set_4 = [float(laser_1_breakpoints_freq[1]),
                         float(laser_1_breakpoints_freq[2])]

        print("First Seg:")

        slope_3 = (laser_1_set_1[0] - laser_1_set_1[1]) / \
            (laser_1_set_2[0] - laser_1_set_2[1])

        intercept_3 = (laser_1_set_1[0] - slope_3*laser_1_set_2[0])

        laser_1_temp_seg_1 = slope_3*target_ghz+intercept_3

        print(laser_1_temp_seg_1)

        print("Second Seg:")

        slope_4 = (laser_1_set_3[0] - laser_1_set_3[1]) / \
            (laser_1_set_4[0] - laser_1_set_4[1])

        intercept_4 = (laser_1_set_3[0] - slope_4*laser_1_set_4[0])

        laser_1_temp_seg_2 = slope_4*target_ghz+intercept_4

        print(laser_1_temp_seg_2)

        if laser_0_set_1[1] >= target_ghz:
            ld0_temp = laser_0_temp_seg_1
            ld1_temp = laser_1_temp_seg_1
        else:
            ld0_temp = laser_0_temp_seg_2
            ld1_temp = laser_1_temp_seg_2

        if ld0_temp > LASER_TEMP_MAX:
            ld0_temp = LASER_TEMP_MAX
        elif ld0_temp < LASER_TEMP_MIN:
            ld0_temp = LASER_TEMP_MIN
        elif ld1_temp > LASER_TEMP_MAX:
            ld1_temp = LASER_TEMP_MAX
        elif ld1_temp < LASER_TEMP_MIN:
            ld1_temp = LASER_TEMP_MIN

        return ld0_temp, ld1_temp

    def calculate_freq_using_poly(self):

        temp = 25

        coefficients = [float(self.cal_data.LD0.dwnscan_coef_seg_1[0]),
                        float(self.cal_data.LD0.dwnscan_coef_seg_1[1]),
                        float(self.cal_data.LD0.dwnscan_coef_seg_1[2]),
                        float(self.cal_data.LD0.dwnscan_coef_seg_1[3]),
                        float(self.cal_data.LD0.dwnscan_coef_seg_1[4]),
                        float(self.cal_data.LD0.dwnscan_coef_seg_1[5])]

        actual_freq = (coefficients[0]*(temp**0) +
                       coefficients[1]*(temp**1) +
                       coefficients[2]*(temp**2) +
                       coefficients[3]*(temp**3) +
                       coefficients[4]*(temp**4) +
                       coefficients[5]*(temp**5)
                       )

        print(actual_freq)

    def dwell_control(self, target_ghz, time_constant):
        ld0_temp, ld1_temp = self.calculate_temps_for_target_ghz(target_ghz)
        self.serial_commands_class.set_LD0_Temperature(ld0_temp)
        self.serial_commands_class.set_LD1_Temperature(ld1_temp)
        self.serial_commands_class.PCS_enable()
        self.serial_commands_class.TEC_enable()
        self.serial_commands_class.set_lockin_time_constant(time_constant)
        self.serial_commands_class.set_lockin_gain()
        self.serial_commands_class.lockin_enable()
        self.serial_commands_class.laser_bias_enable()

    def testing_imports(self):
        print(self.cal_data.LD0.upscan_coef_seg_1[1])
        print(self.cal_data.LD0.upscan_breakpoint[1])
