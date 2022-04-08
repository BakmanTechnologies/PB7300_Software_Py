from serial_commands_PB7200 import SerialCommands
from cal_data import CalData
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

    def testing_imports(self):
        print(self.cal_data.LD0.upscan_coef_seg_1[1])
