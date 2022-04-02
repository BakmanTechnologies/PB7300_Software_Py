from serial_commands_PB7200 import SerialCommands
from serial_data_manipulation import SerialDataManipulation
import time


def main():
    """Main function"""
    serial_commands_class = SerialCommands()
    serial_data_manipulation = SerialDataManipulation()
    serial_data_manipulation.get_json_string()
    serial_commands_class.close_port()


if __name__ == "__main__":
    main()
