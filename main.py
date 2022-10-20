from serial_data_manipulation import SerialDataManipulation
from utils import read_json_from_file


def main():
    """Main function"""
    cal_data = read_json_from_file()
    serial_data_manipulation = SerialDataManipulation(cal_data)
    # serial_data_manipulation.dwell(500, 100, 50)
    # serial_data_manipulation.scan(1300, 1500, 1, 100)
    # serial_data_manipulation.dwellpm(500, 100, 10, 2.5)
    # serial_data_manipulation.scan_pm(500, 520, 1, 100, 2.5)
    serial_data_manipulation.close_port()


if __name__ == "__main__":
    main()
