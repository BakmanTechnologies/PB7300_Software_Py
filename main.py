from serial_data_manipulation import SerialDataManipulation
from utils import read_json_from_file


def main():
    """Main function"""
    cal_data = read_json_from_file()
    serial_data_manipulation = SerialDataManipulation(cal_data)
    serial_data_manipulation.dwell_control(400, 100)
    serial_data_manipulation.close_port()


if __name__ == "__main__":
    main()
