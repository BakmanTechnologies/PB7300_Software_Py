from serial_data_manipulation import SerialDataManipulation
from utils import read_json_from_file


def main():
    """Main function"""

    # Set com_port = None to prompt for the com port
    com_port = "/dev/serial0"
    cal_data = read_json_from_file(com_port)
    serial_data_manipulation = SerialDataManipulation(cal_data, com_port)
    serial_data_manipulation.display_system_info()
    serial_data_manipulation.testing_imports()

    input("Press enter to continue:")
    serial_data_manipulation.test_commands()

    # serial_data_manipulation.dwell(800, 100, 150)
    serial_data_manipulation.scan(350, 700, 1, 100, True)
    # serial_data_manipulation.dwell_pm(500, 100, 10, 2.5)
    # serial_data_manipulation.scan_pm(1300, 1500, 0.5, 100, 2.5)
    serial_data_manipulation.close_port()


if __name__ == "__main__":
    main()
