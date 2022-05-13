from serial_commands_PB7300 import SerialCommands
import hashlib
import time
from utils import simple_graph


class SerialDataManipulation():
    error_freq_last_ghz = 0
    error_freq_i = 0
    set_freq = 0
    stable_count = 0


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
            if i > 2:
                string_json += numlist[i]
        json = string_json

        return json

    def sha1_from_json(self, json_string):
        """Receives json string from EEPROM, SHA1 string and boolean result from SHA1 comparison"""
        print(json_string)
        # Separates SHA1 from the json string, calculates new SHA1 from read json and compares the two
        split2 = json_string.split("{", 1)
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

        laser_0_breakpoints_freq_1 = float(self.cal_data.LD0.upscan_breakpoint[1])
        laser_0_breakpoints_freq_2 = float(self.cal_data.LD0.upscan_breakpoint[3])
        laser_0_breakpoints_freq_3 = float(self.cal_data.LD0.upscan_breakpoint[5])
        laser_1_breakpoints_freq_1 = float(self.cal_data.LD1.upscan_breakpoint[1])
        laser_1_breakpoints_freq_2 = float(self.cal_data.LD1.upscan_breakpoint[3])
        laser_1_breakpoints_freq_3 = float(self.cal_data.LD1.upscan_breakpoint[5])

        laser_0_breakpoints_temp_1 = float(self.cal_data.LD0.upscan_breakpoint[0])
        laser_0_breakpoints_temp_2 = float(self.cal_data.LD0.upscan_breakpoint[2])
        laser_0_breakpoints_temp_3 = float(self.cal_data.LD0.upscan_breakpoint[4])
        laser_1_breakpoints_temp_1 = float(self.cal_data.LD1.upscan_breakpoint[0])
        laser_1_breakpoints_temp_2 = float(self.cal_data.LD1.upscan_breakpoint[2])
        laser_1_breakpoints_temp_3 = float(self.cal_data.LD1.upscan_breakpoint[4])

        #LD0
        #Seg 1

        ld0_slope_seg_1 = (laser_0_breakpoints_temp_2 - laser_0_breakpoints_temp_1) / \
            (laser_0_breakpoints_freq_2 - laser_0_breakpoints_freq_1)

        ld0_intercept_seg_1 = (laser_0_breakpoints_temp_1 - ld0_slope_seg_1*laser_0_breakpoints_freq_1)

        laser_0_temp_seg_1 = ld0_slope_seg_1 * target_ghz + ld0_intercept_seg_1

        #Seg 2

        ld0_slope_seg_2 = (laser_0_breakpoints_temp_3 - laser_0_breakpoints_temp_2) / \
            (laser_0_breakpoints_freq_3 - laser_0_breakpoints_freq_2)

        ld0_intercept_seg_2 = (laser_0_breakpoints_temp_2 - ld0_slope_seg_2*laser_0_breakpoints_freq_2)

        laser_0_temp_seg_2 = ld0_slope_seg_2 * target_ghz + ld0_intercept_seg_2

        #LD1
        #Seg 1

        ld1_slope_seg_1 = (laser_1_breakpoints_temp_2 - laser_1_breakpoints_temp_1) / \
            (laser_1_breakpoints_freq_2 - laser_1_breakpoints_freq_1)

        ld1_intercept_seg_1 = (laser_1_breakpoints_temp_1 - ld1_slope_seg_1*laser_1_breakpoints_freq_1)

        laser_1_temp_seg_1 = ld1_slope_seg_1 * target_ghz + ld1_intercept_seg_1

        #Seg 2

        ld1_slope_seg_2 = (laser_1_breakpoints_temp_3 - laser_1_breakpoints_temp_2) / \
            (laser_1_breakpoints_freq_3 - laser_1_breakpoints_freq_2)

        ld1_intercept_seg_2 = (laser_1_breakpoints_temp_1 - ld1_slope_seg_2*laser_1_breakpoints_freq_1)

        laser_1_temp_seg_2 = ld1_slope_seg_2 * target_ghz + ld1_intercept_seg_2

        if laser_0_breakpoints_freq_2 >= target_ghz:
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

    def calculate_freq_using_poly(self, ld0_temp, ld1_temp):
        """Using LD0, LD1 temps calculates freq using 5th order polynomials, returns ghz value"""
        ld0_correction_found = False
        ld1_correction_found = False
        result = 0

        #LD0
        ld0_coefficients = [float(self.cal_data.LD0.dwnscan_coef_seg_1[0]),
                        float(self.cal_data.LD0.dwnscan_coef_seg_1[1]),
                        float(self.cal_data.LD0.dwnscan_coef_seg_1[2]),
                        float(self.cal_data.LD0.dwnscan_coef_seg_1[3]),
                        float(self.cal_data.LD0.dwnscan_coef_seg_1[4]),
                        float(self.cal_data.LD0.dwnscan_coef_seg_1[5])]

        ld0_actual_freq = (ld0_coefficients[0]*(ld0_temp**0) +
                       ld0_coefficients[1]*(ld0_temp**1) +
                       ld0_coefficients[2]*(ld0_temp**2) +
                       ld0_coefficients[3]*(ld0_temp**3) +
                       ld0_coefficients[4]*(ld0_temp**4) +
                       ld0_coefficients[5]*(ld0_temp**5)
                       )
        if ld0_actual_freq != 0:
            ld0_correction_found = True

        #LD1
        ld1_coefficients = [float(self.cal_data.LD1.dwnscan_coef_seg_1[0]),
                        float(self.cal_data.LD1.dwnscan_coef_seg_1[1]),
                        float(self.cal_data.LD1.dwnscan_coef_seg_1[2]),
                        float(self.cal_data.LD1.dwnscan_coef_seg_1[3]),
                        float(self.cal_data.LD1.dwnscan_coef_seg_1[4]),
                        float(self.cal_data.LD1.dwnscan_coef_seg_1[5])]

        ld1_actual_freq = (ld1_coefficients[0]*(ld1_temp**0) +
                       ld1_coefficients[1]*(ld1_temp**1) +
                       ld1_coefficients[2]*(ld1_temp**2) +
                       ld1_coefficients[3]*(ld1_temp**3) +
                       ld1_coefficients[4]*(ld1_temp**4) +
                       ld1_coefficients[5]*(ld1_temp**5)
                       )

        if ld1_actual_freq != 0:
            ld1_correction_found = True

        if ld0_correction_found == False or ld1_correction_found == False:
            return 0
        if self.cal_data.zero_cross:
            result = abs(ld0_actual_freq - ld1_actual_freq)
        elif self.cal_data.L1_minus_L0:
            result = ld1_actual_freq - ld0_actual_freq
        else: 
            result = ld0_actual_freq - ld1_actual_freq

        return result

    def dwell_control(self, target_ghz, time_constant):
        start_time = time.time()
        time_table = []
        dwell_normalized = []
        temps_read_ld0 = []
        temps_read_ld1 = []
        lockin_1st_list = []
        actual_ghz = []
        count_values = []


        # Startup procedure for PB7300 
        ld0_temp, ld1_temp = self.calculate_temps_for_target_ghz(target_ghz)
        self.serial_commands_class.lock_in_mode()
        self.serial_commands_class.set_LD0_Temperature(ld0_temp)
        self.serial_commands_class.set_LD1_Temperature(ld1_temp)
        time.sleep(0.02)
        self.serial_commands_class.fan_on_high()
        self.serial_commands_class.set_LD0_Power(self.cal_data.LD0.cal_bias)
        self.serial_commands_class.set_LD1_Power(self.cal_data.LD1.cal_bias)
        time.sleep(0.02)
        self.serial_commands_class.PCS_enable()
        time.sleep(0.02)
        self.serial_commands_class.TEC_enable()
        time.sleep(0.02)
        self.serial_commands_class.set_lockin_time_constant(time_constant)
        self.serial_commands_class.set_lockin_gain(self.cal_data.gain)
        self.serial_commands_class.lockin_enable()
        time.sleep(0.02)
        self.serial_commands_class.laser_bias_enable()

        #Loop that keeps dwell active for number in range() temporary solution
        for i in range(200):
            elapsed_time = time.time() - start_time
            lockin_1st, temp_read_ld0, temp_read_ld1 = self.serial_commands_class.read_lockin_1st_and_both_temps()
            print("Time Stamp: ", elapsed_time)
            count, lockin_2nd = self.serial_commands_class.read_sample_count_second_lockin_output()
            print("Lock in sample count: ", count)
            normalize_1, normalize_2 = self.normalize_lockin(
                count, lockin_1st, lockin_2nd)

            dwell_normalized.append(normalize_1)
            temps_read_ld0.append(temp_read_ld0)
            temps_read_ld1.append(temp_read_ld1)
            time_table.append(elapsed_time)
            lockin_1st_list.append(lockin_1st)
            count_values.append(count)
            actual_ghz.append(true_ghz)

            true_ghz = self.calculate_freq_using_poly(temp_read_ld0,temp_read_ld1)

            #Active control
            self.correct_for_target(true_ghz,target_ghz)


            time.sleep(time_constant/1000)
    
        # Shutdown sequence for the PB7300
        self.serial_commands_class.set_LD0_Temperature(25)
        self.serial_commands_class.set_LD1_Temperature(25)
        self.serial_commands_class.TEC_disable()
        self.serial_commands_class.fan_off()
        self.serial_commands_class.PCS_disable()
        self.serial_commands_class.laser_bias_disable()
        self.serial_commands_class.lockin_disable()

        print("Time: ",time_table)
        print("Dwell normalized: ",dwell_normalized)
        print("Lockin raw: ",lockin_1st_list)
        print("Actual ghz: ",actual_ghz)
        print("LD0 temps: ", temps_read_ld0)
        print("LD1 temps: ", temps_read_ld1)
        print("Count: ", count_values)

        simple_graph(time_table,dwell_normalized)

        self.close_port()

    def correct_for_target(self, actual_ghz, target_ghz):
        """Takes the real ghz and compares to target, self corrects towards target"""

        MAX_FREQ_DEVIATION_GHZ = 25
        CORRECTION_FACTOR_P = 0.1
        CORRECTION_FACTOR_I = 0.000001

        # Calculates delta between the real ghz and target
        error_freq_ghz = target_ghz - actual_ghz

        # error_freq_i is a variable with class scope, value persists on dwell loop
        self.error_freq_i = self.error_freq_i + error_freq_ghz

        # calculates adjusted frequency to match target frequency
        self.set_freq = self.set_freq + \
            (CORRECTION_FACTOR_P * error_freq_ghz) + \
            (CORRECTION_FACTOR_I * self.error_freq_i)
        
        # if set_freq values are +-25 off target freq after correction, freq is set to target +-25
        if self.set_freq > target_ghz + MAX_FREQ_DEVIATION_GHZ:
            self.set_freq = target_ghz + MAX_FREQ_DEVIATION_GHZ
        elif self.set_freq < target_ghz - MAX_FREQ_DEVIATION_GHZ:
            self.set_freq = target_ghz - MAX_FREQ_DEVIATION_GHZ
        
        # Laser temps are calculated to achieve new set_freq
        ld0_corrected , ld1_corrected = self.calculate_temps_for_target_ghz(self.set_freq)

        # Laser temp is adjusted for LD0, LD1
        self.serial_commands_class.set_LD0_Temperature(ld0_corrected)
        self.serial_commands_class.set_LD1_Temperature(ld1_corrected)
        
        # Stabilization measure, unused at the moment
        if abs(error_freq_ghz) > 0.25:
            self.stable_count = 0
        else:
            self.stable_count = self.stable_count + 1
        
        # error_freq_last_ghz previous value is replaced with most recent
        self.error_freq_last_ghz = error_freq_ghz

    def dwell_timer(self):
        # self.dwell_control()
        time.sleep(10)

    def normalize_lockin(self, count, lockin_value_1, lockin_value_2):

        data_sample_1st_lockin = (lockin_value_1/count)**2
        if lockin_value_2:
            data_sample_2nd_lockin = ((lockin_value_1/count)**2)
        else:
            data_sample_2nd_lockin = 0
        
        if lockin_value_1 < 1:
            lockin_value_1 = 1
        elif lockin_value_2 < 1:
            lockin_value_2 = 1
            
        return data_sample_1st_lockin, data_sample_2nd_lockin


    def test_commands(self):
        # print(self.serial_commands_class.read_version())
        #lockin_1st, t1, t2 = self.serial_commands_class.read_lockin_1st_and_both_temps()
        #count, lockin_2nd = self.serial_commands_class.read_sample_count_second_lockin_output()
        #self.normalize_lockin(count, lockin_1st, lockin_2nd)
        # self.serial_commands_class.read_laser_currents()

        self.serial_commands_class.read_pcs_current(0, 0)

    def testing_imports(self):
        print(self.cal_data.LD0.upscan_coef_seg_1[1])
        print(self.cal_data.LD0.upscan_breakpoint[1])
        print(self.cal_data.LD0.cal_bias)
        print(self.cal_data.LD1.cal_bias)
        print(self.cal_data.zero_cross)
        print(self.cal_data.L1_minus_L0)
        print(self.cal_data.gain)
