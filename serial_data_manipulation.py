from serial_commands_PB7300 import SerialCommands
import time
from datetime import datetime
import utils


class SerialDataManipulation():
    error_freq_last_ghz = 0
    error_freq_i = 0
    set_freq = 0
    stable_count = 0
    MIN_POWER_VALUE = 0.000001

    def __init__(self, cal_data) -> None:
        self.cal_data = cal_data
        self.serial_commands_class = SerialCommands()

    def close_port(self):
        self.serial_commands_class.close_port()

    def calculate_temps_for_target_ghz(self, target_ghz, is_up_scan):
        """Calculates temperatures for achieving a desired GHz target, returns LD0, LD1 temp"""
        ld0_temp = 0
        ld1_temp = 0

        LASER_TEMP_MAX = 65
        LASER_TEMP_MIN = 5

        if is_up_scan:

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

        else:

            laser_0_breakpoints_freq_1 = float(self.cal_data.LD0.dwnscan_breakpoint[1])
            laser_0_breakpoints_freq_2 = float(self.cal_data.LD0.dwnscan_breakpoint[3])
            laser_0_breakpoints_freq_3 = float(self.cal_data.LD0.dwnscan_breakpoint[5])
            laser_1_breakpoints_freq_1 = float(self.cal_data.LD1.dwnscan_breakpoint[1])
            laser_1_breakpoints_freq_2 = float(self.cal_data.LD1.dwnscan_breakpoint[3])
            laser_1_breakpoints_freq_3 = float(self.cal_data.LD1.dwnscan_breakpoint[5])

            laser_0_breakpoints_temp_1 = float(self.cal_data.LD0.dwnscan_breakpoint[0])
            laser_0_breakpoints_temp_2 = float(self.cal_data.LD0.dwnscan_breakpoint[2])
            laser_0_breakpoints_temp_3 = float(self.cal_data.LD0.dwnscan_breakpoint[4])
            laser_1_breakpoints_temp_1 = float(self.cal_data.LD1.dwnscan_breakpoint[0])
            laser_1_breakpoints_temp_2 = float(self.cal_data.LD1.dwnscan_breakpoint[2])
            laser_1_breakpoints_temp_3 = float(self.cal_data.LD1.dwnscan_breakpoint[4])
        # LD0
        # Seg 1

        ld0_slope_seg_1 = (laser_0_breakpoints_temp_2 - laser_0_breakpoints_temp_1) / \
            (laser_0_breakpoints_freq_2 - laser_0_breakpoints_freq_1)

        ld0_intercept_seg_1 = (laser_0_breakpoints_temp_1 - ld0_slope_seg_1*laser_0_breakpoints_freq_1)

        laser_0_temp_seg_1 = ld0_slope_seg_1 * target_ghz + ld0_intercept_seg_1

        # Seg 2

        ld0_slope_seg_2 = (laser_0_breakpoints_temp_3 - laser_0_breakpoints_temp_2) / \
            (laser_0_breakpoints_freq_3 - laser_0_breakpoints_freq_2)

        ld0_intercept_seg_2 = (laser_0_breakpoints_temp_2 - ld0_slope_seg_2*laser_0_breakpoints_freq_2)

        laser_0_temp_seg_2 = ld0_slope_seg_2 * target_ghz + ld0_intercept_seg_2

        # LD1
        # Seg 1

        ld1_slope_seg_1 = (laser_1_breakpoints_temp_2 - laser_1_breakpoints_temp_1) / \
            (laser_1_breakpoints_freq_2 - laser_1_breakpoints_freq_1)

        ld1_intercept_seg_1 = (laser_1_breakpoints_temp_1 - ld1_slope_seg_1*laser_1_breakpoints_freq_1)

        laser_1_temp_seg_1 = ld1_slope_seg_1 * target_ghz + ld1_intercept_seg_1

        # Seg 2

        ld1_slope_seg_2 = (laser_1_breakpoints_temp_3 - laser_1_breakpoints_temp_2) / \
            (laser_1_breakpoints_freq_3 - laser_1_breakpoints_freq_2)

        ld1_intercept_seg_2 = (laser_1_breakpoints_temp_2 - ld1_slope_seg_2*laser_1_breakpoints_freq_2)

        laser_1_temp_seg_2 = ld1_slope_seg_2 * target_ghz + ld1_intercept_seg_2

        if target_ghz <= laser_0_breakpoints_freq_2 :
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

        # LD0

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

        # LD1
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

    def dwell(self, target_ghz: float, time_constant: int, number_of_data_points: int):
        """Dwell function, takes a target frequency to maintain,
        with a time constant to send the PB7300 the speed at which
        it will be polled for data and the number of data points to take"""
        if not self.check_ghz_range_limit(target_ghz):
            return None

        time_start_dwell = datetime.now()
        scantime = time_start_dwell.strftime("%d-%m-%Y_%H-%M-%S")
        start_time = time.time()
        time_table = []
        dwell_normalized = []
        temps_read_ld0 = []
        temps_read_ld1 = []
        lockin_1st_list = []
        actual_ghz = []
        count_values = []

        file_name = f"dwelldata_{scantime}"

        utils.create_csv_file(file_name)

        # Startup procedure for PB7300

        ld0_temp, ld1_temp = self.calculate_temps_for_target_ghz(target_ghz, is_up_scan=True)
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

        # Loop that keeps dwell active for number in range() temporary solution
        for i in range(number_of_data_points):
            elapsed_time = round((time.time() - start_time), 2)

            lockin_1st, temp_read_ld0, temp_read_ld1 = self.serial_commands_class.read_lockin_1st_and_both_temps()

            print("Time Stamp: ", elapsed_time)

            count, lockin_2nd = self.serial_commands_class.read_sample_count_second_lockin_output()

            #print("Lock in sample count: ", count)

            normalize_1, normalize_2 = self.normalize_lockin_dwell(
                count, lockin_1st, lockin_2nd)

            true_ghz = self.calculate_freq_using_poly(temp_read_ld0, temp_read_ld1)

            dwell_normalized.append(normalize_1)
            # temps_read_ld0.append(temp_read_ld0)
            # temps_read_ld1.append(temp_read_ld1)
            time_table.append(elapsed_time)
            # lockin_1st_list.append(lockin_1st)
            # count_values.append(count)
            actual_ghz.append(true_ghz)

            # Active control
            self._correct_for_target(true_ghz, target_ghz)

            # Save to csv
            info = {"Time": time_table[i],
                    "Power": dwell_normalized[i], }

            utils.save_to_csv(info, file_name)

            time.sleep(time_constant/1000)

        # Shutdown sequence for the PB7300
        self.serial_commands_class.set_LD0_Temperature(25)
        self.serial_commands_class.set_LD1_Temperature(25)
        self.serial_commands_class.TEC_disable()
        self.serial_commands_class.fan_off()
        self.serial_commands_class.PCS_disable()
        self.serial_commands_class.laser_bias_disable()
        self.serial_commands_class.lockin_disable()

        utils.simple_dwell_graph(time_table, dwell_normalized)

        return time_table, dwell_normalized

    def dwell_pm(self, target_ghz: float, time_constant: int, number_of_data_points: int, modulation_voltage: float):
        """Dwell function, takes a target frequency to maintain,
        with a time constant to tell the intrument the speed at which
        it will be polled for data, and the number of data points to take"""
        if not self.check_ghz_range_limit(target_ghz):
            return None

        if self.cal_data.phase_modulator_installed:
            self.serial_commands_class.phase_modulation_voltage_setting(modulation_voltage)
            print("Modulating!!")

        time_start_dwell = datetime.now()
        scantime = time_start_dwell.strftime("%d-%m-%Y_%H-%M-%S")
        start_time = time.time()
        time_table = []
        dwell_normalized = []
        first_harmonic_normalized = []
        second_harmonic_normalized = []
        temps_read_ld0 = []
        temps_read_ld1 = []
        lockin_1st_list = []
        actual_ghz = []
        count_values = []

        file_name = f"dwellpm_data_{scantime}"

        utils.create_csv_file(file_name)

        # Startup procedure for PB7300

        ld0_temp, ld1_temp = self.calculate_temps_for_target_ghz(target_ghz, is_up_scan=True)
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

        # Loop that keeps dwell active for number in range() temporary solution
        for i in range(number_of_data_points):
            elapsed_time = round((time.time() - start_time), 2)

            lockin_1st, temp_read_ld0, temp_read_ld1 = self.serial_commands_class.read_lockin_1st_and_both_temps()
            print("Time Stamp: ", elapsed_time)
            count, lockin_2nd = self.serial_commands_class.read_sample_count_second_lockin_output()
            # print("Lock in sample count: ", count)
            normalize_1, normalize_2 = self.normalize_lockin_dwell(
                count, lockin_1st, lockin_2nd)
            true_ghz = self.calculate_freq_using_poly(temp_read_ld0, temp_read_ld1)
            first_harmonic_normalized.append(normalize_1)
            second_harmonic_normalized.append(normalize_2)
            # temps_read_ld0.append(temp_read_ld0)
            # temps_read_ld1.append(temp_read_ld1)
            time_table.append(elapsed_time)
            # lockin_1st_list.append(lockin_1st)
            # count_values.append(count)
            actual_ghz.append(true_ghz)

            # Active control
            self._correct_for_target(true_ghz, target_ghz)

            # Save to csv
            info = {"Time": time_table[i],
                    "First Harmonic": first_harmonic_normalized[i],
                    "Second Harmonic": second_harmonic_normalized[i]}

            utils.save_to_csv(info, file_name)

            time.sleep(time_constant/1000)

        # Shutdown sequence for the PB7300
        self.serial_commands_class.set_LD0_Temperature(25)
        self.serial_commands_class.set_LD1_Temperature(25)
        self.serial_commands_class.TEC_disable()
        self.serial_commands_class.fan_off()
        self.serial_commands_class.PCS_disable()
        self.serial_commands_class.laser_bias_disable()
        self.serial_commands_class.lockin_disable()

        utils.simple_dwell_graph(time_table, first_harmonic_normalized)

        return time_table, first_harmonic_normalized, second_harmonic_normalized

    def scan(self, start_freq_ghz: float, stop_freq_ghz: float, step_size_ghz: float, time_constant_ms: int, only_up: bool = False):
        """Scan function, takes start frequency,
        stop frequency, step size and time constant,
        will run from start frequency to stop frequency
        and back saving the scan to csv in /scan"""

        if not self.check_ghz_range_limit(start_freq_ghz):
            return None
        if not self.check_ghz_range_limit(stop_freq_ghz):
            return None

        ld0_temps_up = []
        ld1_temps_up = []
        ld0_temps_down = []
        ld1_temps_down = []
        calculated_ghz = []
        lockin_1st_normalized = []
        lockin_2nd_normalized = []
        temps_read_ld0 = []
        temps_read_ld1 = []
        lockin_1st_list = []
        count_values = []
        actual_ghz = []
        time_start_scan = datetime.now()
        scantime = time_start_scan.strftime("%d-%m-%Y_%H-%M-%S")
        is_up_scan = True

        file_name = f"scandata_{scantime}"

        utils.create_csv_file(file_name)

        start_mhz = int(start_freq_ghz*1000)
        stop_mhz = int(stop_freq_ghz*1000)
        step_size_mhz = int(step_size_ghz*1000)
        target_ghz_list = list(range(start_mhz, stop_mhz + 1, step_size_mhz))

        for i in range(len(target_ghz_list)):
            target_ghz_list[i] = target_ghz_list[i]/1000

        # Calculates up temps
        for i in range(len(target_ghz_list)):
            ld0_temp, ld1_temp = self.calculate_temps_for_target_ghz(
                target_ghz_list[i], is_up_scan)
            ld0_temps_up.append(ld0_temp)
            ld1_temps_up.append(ld1_temp)
            calculated_ghz.append(
                self.calculate_freq_using_poly(ld0_temp, ld1_temp))

        # Calculates down temps
        for i in range(len(target_ghz_list)):
            ld0_temp, ld1_temp = self.calculate_temps_for_target_ghz(
                target_ghz_list[i], is_up_scan=False)
            ld0_temps_down.append(ld0_temp)
            ld1_temps_down.append(ld1_temp)
            calculated_ghz.append(
                self.calculate_freq_using_poly(ld0_temp, ld1_temp))

        # Startup procedure for PB7300
        self.serial_commands_class.lock_in_mode()
        self.serial_commands_class.set_LD0_Temperature(25)
        self.serial_commands_class.set_LD1_Temperature(25)
        time.sleep(0.02)
        self.serial_commands_class.fan_on_high()
        self.serial_commands_class.set_LD0_Power(self.cal_data.LD0.cal_bias)
        self.serial_commands_class.set_LD1_Power(self.cal_data.LD1.cal_bias)
        time.sleep(0.02)
        self.serial_commands_class.PCS_enable()
        time.sleep(0.02)
        self.serial_commands_class.TEC_enable()
        time.sleep(0.02)
        self.serial_commands_class.set_lockin_time_constant(time_constant_ms)
        self.serial_commands_class.set_lockin_gain(self.cal_data.gain)
        self.serial_commands_class.lockin_enable()
        time.sleep(0.02)
        self.serial_commands_class.laser_bias_enable()

        # Intitial stabilization
        self.stabilize_initial(ld0_temps_up[0], ld1_temps_up[0])

        #Clear count before read
        self.serial_commands_class.read_lockin_1st_and_both_temps()
        self.serial_commands_class.read_sample_count_second_lockin_output()

        # Up scan
        for j in range(len(target_ghz_list)):
            self.serial_commands_class.set_LD0_Temperature(ld0_temps_up[j])
            self.serial_commands_class.set_LD1_Temperature(ld1_temps_up[j])
            lockin_1st, temp_read_ld0, temp_read_ld1 = self.serial_commands_class.read_lockin_1st_and_both_temps()
            print(f"Target freq: {target_ghz_list[j]}")
            count, lockin_2nd = self.serial_commands_class.read_sample_count_second_lockin_output()
            normalize_1, normalize_2 = self.normalize_lockin_scan(
                count, lockin_1st, lockin_2nd)
            true_ghz = round(self.calculate_freq_using_poly(temp_read_ld0, temp_read_ld1),4)
            lockin_1st_normalized.append(normalize_1)
            # lockin_2nd_normalized.append(normalize_2)
            # temps_read_ld0.append(temp_read_ld0)
            # temps_read_ld1.append(temp_read_ld1)
            lockin_1st_list.append(lockin_1st)
            # count_values.append(count)
            actual_ghz.append(true_ghz)

            info = {"Frequency": actual_ghz[j],
                    "Power": lockin_1st_normalized[j], }

            utils.save_to_csv(info, file_name)

            time.sleep(time_constant_ms/1000)

        if only_up:
            self.serial_commands_class.set_LD0_Temperature(25)
            self.serial_commands_class.set_LD1_Temperature(25)
            self.serial_commands_class.TEC_disable()
            self.serial_commands_class.fan_off()
            self.serial_commands_class.PCS_disable()
            self.serial_commands_class.laser_bias_disable()
            self.serial_commands_class.lockin_disable()

            utils.simple_scan_graph(actual_ghz, lockin_1st_normalized)

            return actual_ghz, lockin_1st_normalized

        # Down Scan

        self.stabilize_initial(ld0_temps_down[-1], ld1_temps_down[-1])

        #Clear count before read
        self.serial_commands_class.read_lockin_1st_and_both_temps()
        self.serial_commands_class.read_sample_count_second_lockin_output()

        for k in reversed(range(len(target_ghz_list))):
            self.serial_commands_class.set_LD0_Temperature(ld0_temps_down[k])
            self.serial_commands_class.set_LD1_Temperature(ld1_temps_down[k])
            lockin_1st, temp_read_ld0, temp_read_ld1 = self.serial_commands_class.read_lockin_1st_and_both_temps()
            print(f"Target freq: {target_ghz_list[k]}")
            count, lockin_2nd = self.serial_commands_class.read_sample_count_second_lockin_output()
            normalize_1, normalize_2 = self.normalize_lockin_scan(
                count, lockin_1st, lockin_2nd)
            true_ghz = self.calculate_freq_using_poly(temp_read_ld0, temp_read_ld1)
            lockin_1st_normalized.append(normalize_1)
            # temps_read_ld0.append(temp_read_ld0)
            # temps_read_ld1.append(temp_read_ld1)
            # count_values.append(count)
            actual_ghz.append(true_ghz)

            info = {"Frequency": actual_ghz[-1],
                    "Power": lockin_1st_normalized[-1], }

            utils.save_to_csv(info, file_name)

            time.sleep(time_constant_ms/1000)

        # Shutdown sequence
        self.serial_commands_class.set_LD0_Temperature(25)
        self.serial_commands_class.set_LD1_Temperature(25)
        self.serial_commands_class.TEC_disable()
        self.serial_commands_class.fan_off()
        self.serial_commands_class.PCS_disable()
        self.serial_commands_class.laser_bias_disable()
        self.serial_commands_class.lockin_disable()

        utils.simple_scan_graph(actual_ghz, lockin_1st_normalized)

        return actual_ghz, lockin_1st_normalized

    def scan_pm(self, start_freq_ghz: float, stop_freq_ghz: float, step_size_ghz: float, time_constant_ms: int, modulation_voltage: float, only_up: bool = False):
        """Scan function, takes start frequency,
        stop frequency, step size, time constant,
        and modulation volatage, will run from start
        frequency to stop frequency saving the scan to csv in /data"""

        if 0 > modulation_voltage > 5:
            print(f"Modulation voltage must be between 0-5 volts, value is : {modulation_voltage}")

        # Start phase modulation
        if self.cal_data.phase_modulator_installed:
            self.serial_commands_class.phase_modulation_voltage_setting(modulation_voltage)

        if not self.check_ghz_range_limit(start_freq_ghz):
            return None
        if not self.check_ghz_range_limit(stop_freq_ghz):
            return None

        ld0_temps_up = []
        ld1_temps_up = []
        ld0_temps_down = []
        ld1_temps_down = []
        calculated_ghz = []
        lockin_1st_normalized = []
        lockin_2nd_normalized = []
        temps_read_ld0 = []
        temps_read_ld1 = []
        lockin_1st_list = []
        count_values = []
        actual_ghz = []
        time_start_scan = datetime.now()
        scantime = time_start_scan.strftime("%d-%m-%Y_%H-%M-%S")
        is_up_scan = True

        file_name = f"scanpm_data_{scantime}"

        utils.create_csv_file(file_name)

        start_mhz = int(start_freq_ghz*1000)
        stop_mhz = int(stop_freq_ghz*1000)
        step_size_mhz = int(step_size_ghz*1000)
        target_ghz_list = list(range(start_mhz, stop_mhz + 1, step_size_mhz))

        for i in range(len(target_ghz_list)):
            target_ghz_list[i] = target_ghz_list[i]/1000

        # Calculates up temps
        for i in range(len(target_ghz_list)):
            ld0_temp, ld1_temp = self.calculate_temps_for_target_ghz(
                target_ghz_list[i], is_up_scan)
            ld0_temps_up.append(ld0_temp)
            ld1_temps_up.append(ld1_temp)
            calculated_ghz.append(
                self.calculate_freq_using_poly(ld0_temp, ld1_temp))

        # Calculates down temps
        for i in range(len(target_ghz_list)):
            ld0_temp, ld1_temp = self.calculate_temps_for_target_ghz(
                target_ghz_list[i], is_up_scan=False)
            ld0_temps_down.append(ld0_temp)
            ld1_temps_down.append(ld1_temp)
            calculated_ghz.append(
                self.calculate_freq_using_poly(ld0_temp, ld1_temp))

        # Startup procedure for PB7300
        self.serial_commands_class.lock_in_mode()
        self.serial_commands_class.set_LD0_Temperature(25)
        self.serial_commands_class.set_LD1_Temperature(25)
        time.sleep(0.02)
        self.serial_commands_class.fan_on_high()
        self.serial_commands_class.set_LD0_Power(self.cal_data.LD0.cal_bias)
        self.serial_commands_class.set_LD1_Power(self.cal_data.LD1.cal_bias)
        time.sleep(0.02)
        self.serial_commands_class.PCS_enable()
        time.sleep(0.02)
        self.serial_commands_class.TEC_enable()
        time.sleep(0.02)
        self.serial_commands_class.set_lockin_time_constant(time_constant_ms)
        self.serial_commands_class.set_lockin_gain(self.cal_data.gain)
        self.serial_commands_class.lockin_enable()
        time.sleep(0.02)
        self.serial_commands_class.laser_bias_enable()

        # Intitial stabilization
        self.stabilize_initial(ld0_temps_up[0], ld1_temps_up[0])

        #Clear count before read
        self.serial_commands_class.read_lockin_1st_and_both_temps()
        self.serial_commands_class.read_sample_count_second_lockin_output()

        # Up scan
        for j in range(len(target_ghz_list)):
            self.serial_commands_class.set_LD0_Temperature(ld0_temps_up[j])
            self.serial_commands_class.set_LD1_Temperature(ld1_temps_up[j])
            lockin_1st, temp_read_ld0, temp_read_ld1 = self.serial_commands_class.read_lockin_1st_and_both_temps()
            print(f"Target freq: {target_ghz_list[j]}")
            count, lockin_2nd = self.serial_commands_class.read_sample_count_second_lockin_output()
            normalize_1, normalize_2 = self.normalize_lockin_scan(
                count, lockin_1st, lockin_2nd)
            true_ghz = round(self.calculate_freq_using_poly(temp_read_ld0, temp_read_ld1),4)
            lockin_1st_normalized.append(normalize_1)
            lockin_2nd_normalized.append(normalize_2)
            # lockin_2nd_normalized.append(normalize_2)
            # temps_read_ld0.append(temp_read_ld0)
            # temps_read_ld1.append(temp_read_ld1)
            # lockin_1st_list.append(lockin_1st)
            #count_values.append(count)
            actual_ghz.append(true_ghz)

            info = {"Frequency": actual_ghz[j],
                    "First Harmonic": lockin_1st_normalized[j],
                    "Second Harmonic": lockin_2nd_normalized[j]}

            utils.save_to_csv(info, file_name)

            time.sleep(time_constant_ms/1000)
        
        if only_up:
            self.serial_commands_class.set_LD0_Temperature(25)
            self.serial_commands_class.set_LD1_Temperature(25)
            self.serial_commands_class.TEC_disable()
            self.serial_commands_class.fan_off()
            self.serial_commands_class.PCS_disable()
            self.serial_commands_class.laser_bias_disable()
            self.serial_commands_class.lockin_disable()

            utils.simple_scan_graph(actual_ghz, lockin_1st_normalized)

            return actual_ghz, lockin_1st_normalized, lockin_2nd_normalized

        # Down Scan

        self.stabilize_initial(ld0_temps_down[-1], ld1_temps_down[-1])

        #Clear count before read
        self.serial_commands_class.read_lockin_1st_and_both_temps()
        self.serial_commands_class.read_sample_count_second_lockin_output()

        for k in reversed(range(len(target_ghz_list))):
            self.serial_commands_class.set_LD0_Temperature(ld0_temps_down[k])
            self.serial_commands_class.set_LD1_Temperature(ld1_temps_down[k])
            lockin_1st, temp_read_ld0, temp_read_ld1 = self.serial_commands_class.read_lockin_1st_and_both_temps()
            print(f"Target freq: {target_ghz_list[k]}")
            count, lockin_2nd = self.serial_commands_class.read_sample_count_second_lockin_output()
            normalize_1, normalize_2 = self.normalize_lockin_scan(
                count, lockin_1st, lockin_2nd)
            true_ghz = self.calculate_freq_using_poly(temp_read_ld0, temp_read_ld1)
            lockin_1st_normalized.append(normalize_1)
            lockin_2nd_normalized.append(normalize_2)
            # temps_read_ld0.append(temp_read_ld0)
            # temps_read_ld1.append(temp_read_ld1)
            # count_values.append(count)
            actual_ghz.append(true_ghz)

            info = {"Frequency": actual_ghz[-1],
                    "First Harmonic": lockin_1st_normalized[-1],
                    "Second Harmonic": lockin_2nd_normalized[-1]}

            utils.save_to_csv(info, file_name)

            time.sleep(time_constant_ms/1000)

        # Shutdown sequence
        self.serial_commands_class.set_LD0_Temperature(25)
        self.serial_commands_class.set_LD1_Temperature(25)
        self.serial_commands_class.TEC_disable()
        self.serial_commands_class.fan_off()
        self.serial_commands_class.PCS_disable()
        self.serial_commands_class.laser_bias_disable()
        self.serial_commands_class.lockin_disable()

        utils.simple_scan_graph(actual_ghz, lockin_1st_normalized)

        return actual_ghz, lockin_1st_normalized, lockin_2nd_normalized

    def _correct_for_target(self, actual_ghz, target_ghz):
        """Takes the real ghz and compares to target, self corrects towards target."""

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
        ld0_corrected, ld1_corrected = self.calculate_temps_for_target_ghz(self.set_freq, is_up_scan=True)

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

    def normalize_lockin_dwell(self, count, lockin_value_1, lockin_value_2):

        data_sample_1st_lockin = (lockin_value_1/count)**2
        if lockin_value_2:
            data_sample_2nd_lockin = ((lockin_value_1/count)**2)
        else:
            data_sample_2nd_lockin = 0

        if data_sample_1st_lockin < 1:
            data_sample_1st_lockin = 1
        elif data_sample_2nd_lockin < 1:
            data_sample_2nd_lockin = 1

        return data_sample_1st_lockin, data_sample_2nd_lockin

    def normalize_lockin_scan(self, count, lockin_value_1, lockin_value_2):

        data_sample_1st_lockin = (lockin_value_1/count)**2
        if lockin_value_2:
            data_sample_2nd_lockin = ((lockin_value_1/count)**2)
        else:
            data_sample_2nd_lockin = 0
        
        if lockin_value_1 < self.MIN_POWER_VALUE:
            lockin_value_1 = self.MIN_POWER_VALUE
        elif lockin_value_2 < self.MIN_POWER_VALUE:
            lockin_value_2 = self.MIN_POWER_VALUE
            
        return data_sample_1st_lockin, data_sample_2nd_lockin

    def stabilize_initial(self, ld0_target_temp, ld1_target_temp):

        ld0_stable = False
        ld1_stable = False

        ld0_stabilization_count = 0
        ld1_stabilization_count = 0

        self.serial_commands_class.set_LD0_Temperature(ld0_target_temp)
        self.serial_commands_class.set_LD1_Temperature(ld1_target_temp)

        stabilization_factor = self.cal_data.stablize_start_fac
        stabilization_count = self.cal_data.stablize_start_cnt

        current_ld0_temp = self.serial_commands_class.read_temp_LD0()
        current_ld1_temp = self.serial_commands_class.read_temp_LD1()

        while not ld0_stable and not ld1_stable:
            time.sleep(0.2)

            actual_ld0_temp = self.serial_commands_class.read_temp_LD0()
            actual_ld1_temp = self.serial_commands_class.read_temp_LD1()

            if actual_ld0_temp < (current_ld0_temp + stabilization_factor) and actual_ld0_temp > (current_ld0_temp - stabilization_factor):
                ld0_stabilization_count += 1
            else:
                ld0_stabilization_count = 0

            if ld0_stabilization_count >= stabilization_count:
                ld0_stable = True

            if actual_ld1_temp < (current_ld1_temp + stabilization_factor) and actual_ld1_temp > (current_ld1_temp - stabilization_factor):
                ld1_stabilization_count += 1
            else:
                ld1_stabilization_count = 0

            if ld1_stabilization_count >= stabilization_count:
                ld1_stable = True
            
            current_ld0_temp = actual_ld0_temp
            current_ld1_temp = actual_ld1_temp
            
            print("Stabilizing Temperatures...")
            print(ld0_stabilization_count, ld1_stabilization_count)
            print(actual_ld0_temp, actual_ld1_temp)
        
    def simple_stabilize(self, ld0_target_temp, ld1_target_temp):

        self.serial_commands_class.set_LD0_Temperature(ld0_target_temp)
        self.serial_commands_class.set_LD1_Temperature(ld1_target_temp)

        time.sleep(1)

    def display_system_info(self):
        min_freq  = self.cal_data.limit_min_freq_MHz / 1000
        max_freq = self.cal_data.limit_max_freq_MHz / 1000

        print("Minimum frequency(GHz): ", min_freq)
        print("Maximum frequency(GHz): ", max_freq)

    def check_ghz_range_limit(self, target_frequency):
        min_freq  = self.cal_data.limit_min_freq_MHz / 1000
        max_freq = self.cal_data.limit_max_freq_MHz / 1000

        if min_freq <= target_frequency <= max_freq:
            return True
        else:
            print("Target frequency outside of system range.")
            print("Requested frequency(GHz): ", target_frequency)
            self.display_system_info()
            return False

    def check_scan_range(self, start_freq, stop_freq):

        if start_freq >= stop_freq:
            print("Scan Stop frequency must be greater than Start frequency")
            print("Start frequency requested: ", start_freq)
            print("Stop frequency requested: ", stop_freq)

    def test_commands(self):
        self.serial_commands_class.read_version()

    def testing_imports(self):
        print(self.cal_data.LD0.upscan_coef_seg_1[1])
        print(self.cal_data.LD0.upscan_breakpoint[1])
        print(self.cal_data.LD0.cal_bias)
        print(self.cal_data.LD1.cal_bias)
        print(self.cal_data.zero_cross)
        print(self.cal_data.L1_minus_L0)
        print(self.cal_data.gain)
        print(self.cal_data.stablize_start_fac)
        print(self.cal_data.stablize_start_cnt)
        print(self.serial_commands_class.read_version())

        
