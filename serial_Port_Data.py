import serial


class serial_data():

    calibration_time = ""
    operator_name = ""
    spectrometer_SN = ""
    mainboard_version = ""
    MainBoard_Version = ""
    Limit_Min_Freq_MHz = 0
    Limit_Max_Freq_MHz = 0
    Limit_Min_Freq_Resolution_MHz = "100"
    LaserControl = ""
    Phase_Modulator_Installed = False
    Phase_Modulator_SN = ""
    phaseModulateType = ""
    StablizeStartFac = 0.0
    StablizeTransFac = 0.0
    StablizeStartCnt = 0
    StablizeTransCnt = 0
    PowerMode = "CC"
    PcsBias = 0
    SourcePcsCorrection = 0
    DetectorPcsCorrection = 0
    Channels = 0
    coeffUpDw = []
    gain: 0
    ZeroCross = False
    L1_Minus_L0 = False
    LD0 = {
        DateCode = "Jul 2012",
		SN = "0035"
		PN = "1316-001"
		CalBias_mA = 90
		DWNSCAN_START_TEMP_SEG_1 = "10"
		DWNSCAN_STOP_TEMP_SEG_1 = "65"
		DWNSCAN_START_TEMP_SEG_2 = null
		DWNSCAN_STOP_TEMP_SEG_2 = null
		DWNSCAN_COEF_SEG_1 = [
			385179.5167954948,
			-26.67414433279482,
			0.006032782294777112,
			-0.00018274937627475385,
			2.4257574347351596e-7,
			5.219003050873216e-9
		],
		"DWNSCAN_COEF_SEG_2": [
			0,
			0,
			0,
			0,
			0,
			0
		],
		"UPSCAN_START_TEMP_SEG_1": "10",
		"UPSCAN_STOP_TEMP_SEG_1": "65",
		"UPSCAN_START_TEMP_SEG_2": null,
		"UPSCAN_STOP_TEMP_SEG_2": null,
		"UPSCAN_COEF_SEG_1": [
			385177.38516970016,
			-26.558374011535908,
			-0.005651585727185294,
			0.0002324179557597461,
			-0.000006248188740569251,
			4.455788170047888e-8
		],
		"UPSCAN_COEF_SEG_2": [
			0,
			0,
			0,
			0,
			0,
			0
		],
		"UPSCAN_COEF_SEG_1_RSquared": 0,
		"UPSCAN_COEF_SEG_2_RSquared": 0,
		"DWNSCAN_COEF_SEG_1_RSquared": 0,
		"DWNSCAN_COEF_SEG_2_RSquared": 0,
		"DWNSCAN_Breakpoint": [
			"55.0",
			"-115.850000000035",
			"14.0",
			"964.679999999993",
			"14.0",
			"1981.35999999999"
		],
		"Upscan_Breakpoint": [
			"55.0",
			"-117.469999999972",
			"14.0",
			"964.320000000007",
			"14.0",
			"1984.06"
		],
		"Wavelength_nm": "780",
		"Imax_mA": 120,
		"ChipVendor": "Eagleyard",
		"BFPD_power_ration_at_100mA": "",
		"Upscan_NumberTemperatureCalibrationSegments": 1,
		"DWNSCAN_NumberTemperatureCalibrationSegments": 1,
		"TecCorrection": 0
    ]
    }
