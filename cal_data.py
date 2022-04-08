
class CalData():
    """Contains all data obtained from calibration json"""

    def __init__(self, calibration_data=None):
        self.calibration_time = calibration_data.get("CalibrationTime", "")
        self.operator_name = calibration_data.get("Operator_Name", "")
        self.spectrometer_sn = calibration_data.get("Spectrometer_SN", "")
        self.mainboard_version = calibration_data.get("MainBoard_Version", "")
        self.limit_min_freq_MHz = calibration_data.get("Limit_Min_Freq_MHz", 0)
        self.limit_max_freq_MHz = calibration_data.get("Limit_Max_Freq_MHz", 0)
        self.limit_min_freq_resolution_MHz = calibration_data.get(
            "Limit_Min_Freq_Resolution_MHz", "")
        self.lasercontrol = calibration_data.get("LaserControl", "")
        self.phase_modulator_installed = calibration_data.get(
            "Phase_Modulator_Installed", False)
        self.phase_modulator_SN = calibration_data.get(
            "Phase_Modulator_SN", "")
        self.phase_modulate_type = calibration_data.get(
            "phaseModulateType", "")
        self.stablize_start_fac = calibration_data.get("StablizeStartFac", 0)
        self.stablize_trans_tac = calibration_data.get("StablizeTransFac", 0)
        self.stablize_start_cnt = calibration_data.get("StablizeStartCnt", 0)
        self.stablize_trans_cnt = calibration_data.get("StablizeTransCnt", 0)
        self.power_mode = calibration_data.get("PowerMode", "")
        self.pcs_bias = calibration_data.get("PcsBias", 0)
        self.source_pcs_correction = calibration_data.get(
            "SourcePcsCorrection", 0)
        self.detector_pcs_correction = calibration_data.get(
            "DetectorPcsCorrection", 0)
        self.channels = calibration_data.get("Channels", 0)
        self.coeff_Up_Down = calibration_data.get("coeffUpDw", [])
        self.gain = calibration_data.get("gain", 0)
        self.zero_cross = calibration_data.get("upScanFreq", False)
        self.L1_minus_L0 = calibration_data.get("upScanTemp", False)
        self.second_harmonic = calibration_data.get("second_harmonic", False)
        self.LD0 = LaserData(calibration_data.get("LD0", {}))
        self.LD1 = LaserData(calibration_data.get("LD1", {}))


class LaserData():
    """Contains LD0, LD1 data from calibration, is contained within caldata above"""

    def __init__(self, laser_data) -> None:
        self.date_code = laser_data.get("DateCode", "")
        self.serial_number = laser_data.get("SN", "")
        self.part_number = laser_data.get("PN", "")
        self.cal_bias = laser_data.get("CalBias_mA", 0)
        self.dwnscan_start_temp_seg_1 = laser_data.get(
            "DWNSCAN_START_TEMP_SEG_1", "")
        self.dwnscan_stop_temp_seg_1 = laser_data.get(
            "DWNSCAN_STOP_TEMP_SEG_1", "")
        self.dwnscan_start_temp_seg_2 = laser_data.get(
            "DWNSCAN_START_TEMP_SEG_2", "")
        self.dwnscan_stop_temp_seg_2 = laser_data.get(
            "DWNSCAN_STOP_TEMP_SEG_2", "")
        self.dwnscan_coef_seg_1 = laser_data.get("DWNSCAN_COEF_SEG_1", [])
        self.dwnscan_coef_seg_2 = laser_data.get("DWNSCAN_COEF_SEG_2", [])
        self.upscan_start_temp_seg_1 = laser_data.get(
            "UPSCAN_START_TEMP_SEG_1", "")
        self.upscan_stop_temp_seg_1 = laser_data.get(
            "UPSCAN_STOP_TEMP_SEG_1", "")
        self.upscan_start_temp_seg_2 = laser_data.get(
            "UPSCAN_START_TEMP_SEG_2", "")
        self.upscan_stop_temp_seg_2 = laser_data.get(
            "UPSCAN_STOP_TEMP_SEG_2", "")
        self.upscan_coef_seg_1 = laser_data.get("UPSCAN_COEF_SEG_1", [])
        self.upscan_coef_seg_2 = laser_data.get("UPSCAN_COEF_SEG_2", [])
        self.upscan_coef_seg_1_rsquared = laser_data.get(
            "UPSCAN_COEF_SEG_1_RSquared", 0)
        self.upscan_coef_seg_2_rsquared = laser_data.get(
            "UPSCAN_COEF_SEG_2_RSquared", 0)
        self.dwnscan_coef_seg_1_rsquared = laser_data.get(
            "DWNSCAN_COEF_SEG_1_RSquared", 0)
        self.dwnscan_coef_seg_2_rsquared = laser_data.get(
            "DWNSCAN_COEF_SEG_2_RSquared", 0)
        self.dwnscan_breakpoint = laser_data.get("DWNSCAN_Breakpoint", [])
        self.upscan_breakpoint = laser_data.get("Upscan_Breakpoint", [])
        self.wavelength_nm = laser_data.get("Wavelength_nm", "")
        self.imax_ma = laser_data.get("Imax_mA", 0)
        self.chipvendor = laser_data.get("ChipVendor", "")
        self.bfpd_power_ratio_100ma = laser_data.get(
            "BFPD_power_ration_at_100mA", "")
        self.upscan_number_temp_cal_segments = laser_data.get(
            "Upscan_NumberTemperatureCalibrationSegments", 0)
        self.dwnscan_number_temp_cal_segments = laser_data.get(
            "DWNSCAN_NumberTemperatureCalibrationSegments", 0)
        self.tec_correction = laser_data.get("TecCorrection", 0)
