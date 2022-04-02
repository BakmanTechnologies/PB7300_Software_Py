from serial_commands_PB7200 import SerialCommands
import hashlib
import json
import os


class SerialDataManipulation:
    serial_commands_class = SerialCommands()

    list_data = []

    jsonlist = os.listdir("calibration")

    """opens local path floder calibration and sorts them by name"""
    jsonlist.sort()
    recent_file_selection = jsonlist[-1]
    print(recent_file_selection)

    with open(f"calibration/{recent_file_selection}") as json_file:
        jsondata = json.load(json_file)

    class cal_data():
        calibration_time = ""
        operator_name = ""
        spectrometer_sn = ""
        mainboard_version = ""
        limit_min_freq_MHz = 0
        limit_max_freq_MHz = 0
        limit_min_freq_resolution_MHz = ""
        lasercontrol = ""
        phase_modulator_installed = False
        phase_modulator_SN = ""
        phase_modulate_type = ""
        stablize_start_fac = 0
        stablize_trans_tac = 0
        stablize_start_cnt = 0
        stablize_trans_cnt = 0
        power_mode = ""
        pcs_bias = 0
        source_pcs_correction = 0
        detector_pcs_correction = 0
        channels = 0
        coeff_Up_Down = []
        gain = 0
        zero_cross = False
        L1_minus_L0 = False
        second_harmonic = False

    def get_list_values(self):
        return self.list_data

    def get_json_string(self):

        numlist = []
        string_json = ""
        for i in range(4000):
            numlist.append(self.serial_commands_class.read_eeprom(i))
            if numlist[i] == "ÿ":
                break
            string_json += numlist[i]
        print("List of values", numlist)
        print(string_json)
        json = string_json
        self.serial_commands_class.close_port()

        return json

    def sha1_from_json(self, json_string):
        """Breaks string apart"""
        is_SHA1_ok = False
        split1 = json_string.split("©")
        split2 = split1[1].split("{")
        sha1_from_eeprom = split2[0]
        json_string_cut = "{" + split2[1]

        sha1_check = hashlib.sha1(json_string_cut)

        if sha1_from_eeprom == sha1_check:
            is_SHA1_ok = True

        return is_SHA1_ok
