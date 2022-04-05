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

    if len(jsonlist) == 0:
        print("Calibration directory empty")
        recent_file_selection = "0"
    else:
        print(len(jsonlist))
        recent_file_selection = jsonlist[-1]
        print(recent_file_selection)

    if os.path.exists(f"calibration/{recent_file_selection}") == True:
        print("File exists.. Opening")
        with open(f"calibration/{recent_file_selection}") as json_file:
            jsondata = json.load(json_file)
        print(jsondata["CalibrationTime"])
    else:
        print("No calibration file exists, must read EEPROM")

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
        """Obtains string of the JSON calibration file in the EEPROM"""

        numlist = []
        string_json = ""
        for i in range(4000):
            numlist.append(self.serial_commands_class.read_eeprom(i))
            if numlist[i] == "ÿ":
                break
            string_json += numlist[i]
        json = string_json
        self.serial_commands_class.close_port()

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
