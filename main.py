from serial_data_manipulation import SerialDataManipulation
from utils import read_json_from_file, read_json_from_eeprom


def main():
    """Main function"""
    read_json_from_eeprom()
    cal_data = read_json_from_file()
    serial_data_manipulation = SerialDataManipulation(cal_data)
    #serial_data_manipulation.dwell_control(500, 100)
    #serial_data_manipulation.scan(200, 400, 1, 100, 125)
    #serial_data_manipulation.scan_pm()
    serial_data_manipulation.close_port()


if __name__ == "__main__":
    main()
