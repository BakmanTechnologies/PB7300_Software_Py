from serial_data_manipulation import SerialDataManipulation
from utils import read_json_from_file


def main():
    """Main function"""
    cal_data = read_json_from_file()
    serial_data_manipulation = SerialDataManipulation(cal_data)
    #serial_data_manipulation.dwell_control(500, 100)
    #serial_data_manipulation.scan(200, 400, 1, 100, 125)
    #serial_data_manipulation.scan_pm()
    serial_data_manipulation.testing_imports()
    serial_data_manipulation.close_port()


if __name__ == "__main__":
    main()
