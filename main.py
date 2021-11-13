from serial_commands_PB7200 import SerialCommands
from serial_data_manipulation import SerialDataManipulation
import time


def main():
    """Main function"""
    serial_commands_class = SerialCommands()
    serial_commands_class.laser_bias_disable()
    serial_commands_class.close_port()
    # list = serial_commands_class.get_data()
    # serial_data_manipulation = SerialDataManipulation(list)
    # testing = serial_data_manipulation.get_list_values()
    # print(testing)


if __name__ == "__main__":
    main()
