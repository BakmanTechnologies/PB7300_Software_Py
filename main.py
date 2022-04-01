from serial_commands_PB7200 import SerialCommands
from serial_data_manipulation import SerialDataManipulation
import time


def main():
    """Main function"""
    serial_commands_class = SerialCommands()
    numlist = []
    word = ""
    for i in range(200):
        numlist.append(serial_commands_class.test_eeprom(i))
        word += numlist[i]
    print("List of values", numlist)
    print(word)
    serial_commands_class.close_port()


if __name__ == "__main__":
    main()
