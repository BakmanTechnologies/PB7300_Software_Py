from serial_commands_PB7200 import SerialCommands
from serial_data_manipulation import SerialDataManipulation
from utils import read_json_from_file
from cal_data import CalData


def main():
    """Main function"""
    cal_data = read_json_from_file()
    serial_data_manipulation = SerialDataManipulation(cal_data)
    serial_data_manipulation.dwell_control(400, 10)
    serial_data_manipulation.close_port()


if __name__ == "__main__":
    main()
