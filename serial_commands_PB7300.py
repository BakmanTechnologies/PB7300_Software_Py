import serial
import serial.tools.list_ports as ports
import time
from serial.serialutil import EIGHTBITS, PARITY_NONE, STOPBITS_ONE
import math
import numpy as np


class SerialCommands:
    """Class containing serial port commands"""
    # WARNING! POTENTIAL LASER DAMAGE
    # Modifying this file is heavily discouraged as it contains vital
    # commands for running the PB7300 Spectrometer.
    # Any change to the commands in this file may affect the performance
    # of the spectrometer and risk damaging the lasers permanently.

    PB7300COMPort = serial.Serial()
    TEMP_READ_SCALING_CONST_N = 1411.3
    TEMP_READ_SCALING_CONST_C = 924.023

    TEMP_SET_SCALING_CONST_L = 936.96
    TEMP_SET_SCALING_CONST_D = 54.08

    CURRENT_REV5 = 160

    COM_PORT = "COM0"

    def __init__(self):
        if self.PB7300COMPort.is_open:
            pass
        else:
            PORTS = list(ports.comports())
            print("Ports Available: ")
            for p in PORTS:
                print(p)
            print("PB7300 Python Command Module v0.6")
            com_select = input("Specify COM port selection: ")

            # Opens serial port with set properties
            self.PB7300COMPort.port = com_select
            self.PB7300COMPort.baudrate = 115200
            self.PB7300COMPort.parity = PARITY_NONE
            self.PB7300COMPort.bytesize = EIGHTBITS
            self.PB7300COMPort.stopbits = STOPBITS_ONE
            self.PB7300COMPort.rtscts = True
            self.PB7300COMPort.write_timeout = 10

            try:
                self.PB7300COMPort.open()
                print("Succeded in opening PB7300 port")
            except serial.SerialException as e:
                print("Failed to open port", e)

    def build_tx_bytes(self, hex_list):
        """ Builds the 6 bytes to send from a hex values list """

        sync_byte = hex_list[0]
        command_byte = hex_list[1]
        third_byte = hex_list[2]
        fourth_byte = hex_list[3]
        fifth_byte = hex_list[4]
        sixth_byte = hex_list[5]

        tx_bytes_hex = f"{sync_byte} {command_byte} {third_byte} {fourth_byte} {fifth_byte} {sixth_byte}"

        tx_byte_array = bytearray.fromhex(tx_bytes_hex)
        return tx_byte_array

    def write_serial(self, tx_bytes):
        """Function recieves tx_bytes list to send, returns rxBytes bytearray"""

        self.PB7300COMPort.reset_input_buffer()

        # send the characterS to the device
        self.PB7300COMPort.write(tx_bytes)

        time.sleep(0.001)

        while self.PB7300COMPort.in_waiting > 0:
            # Reading Bytes
            rx_bytes = self.PB7300COMPort.read(10)
        try:
            return rx_bytes
        except UnboundLocalError as ex:
            print("No values to read")
            print(ex)
            rx_bytes = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            self.shutdown()

    def close_port(self):
        """Closes com port at end of program"""
        self.PB7300COMPort.close()

    def convert_hex_and_split_bytes(self, unsplit):
        """Converts bytes to hex list"""
        version_hex = unsplit.hex()

        char_count = 2

        split_hex_version = [version_hex[i:i+char_count]
                             for i in range(0, len(version_hex), char_count)]

        return split_hex_version

    def split_hex(self, unsplit):
        """splits hex string every 2 chars to list"""
        char_count = 2

        split_hex_version = [unsplit[i:i+char_count]
                             for i in range(0, len(unsplit), char_count)]

        return split_hex_version

    def convert_hex_to_dec(self, raw_bytes):
        """converts list of 10 hex bytes to decimal returns decimal list"""

        converted_version_list = []

        for i in range(10):
            converted_version_list.append(int(raw_bytes[i], 16))

        return converted_version_list

    def convert_hex_to_dec_values(self, hex_value):
        """converts individual values to decimal"""

        dec_value = int(hex_value, 16)

        return dec_value

    # Serial functions

    # Set temperatures ~~~~~~~~~~~~~~~~~~~~~~
    def set_LD0_Temperature(self, set_temp):
        """Sets the LD0 temperature"""
        if set_temp < 5:
            set_temp = 5
        elif set_temp > 65:
            set_temp = 65

        temp_scaled = int(
            (set_temp * self.TEMP_SET_SCALING_CONST_L)+self.TEMP_SET_SCALING_CONST_D)

        temp_hex = hex(temp_scaled)

        n = 2

        split_hex_list = [temp_hex[i:i+n]
                          for i in range(0, len(temp_hex), n)]

        temp_msb = str(split_hex_list[1])

        temp_lsb = str(split_hex_list[2])

        hex_list = []
        hex_list.append("AA")
        hex_list.append("10")
        hex_list.append(temp_msb)
        hex_list.append(temp_lsb)
        hex_list.append("00")
        hex_list.append("00")

        tx_bytes = self.build_tx_bytes(hex_list)

        lockin_and_temps_bytes = self.write_serial(tx_bytes)

        split_hex_list = self.convert_hex_and_split_bytes(
            lockin_and_temps_bytes)

        temp_1_msb_hex = split_hex_list[6]

        temp_1_lsb_hex = split_hex_list[7]

        # laser 1

        temp_1_msb_decimal = self.convert_hex_to_dec_values(temp_1_msb_hex)

        temp_1_msb_decimal_float = float(temp_1_msb_decimal)

        temp_1_lsb_decimal = self.convert_hex_to_dec_values(temp_1_lsb_hex)

        temp_1_lsb_decimal_float = float(temp_1_lsb_decimal)

        temp_1_full_decimal_unscaled = (
            (((((2**8) * temp_1_msb_decimal_float)+temp_1_lsb_decimal_float)/self.TEMP_SET_SCALING_CONST_L)) - self.TEMP_SET_SCALING_CONST_D)

    def set_LD1_Temperature(self, set_temp):
        """Sets the LD1 temperature"""

        if set_temp < 5:
            set_temp = 5
        elif set_temp > 65:
            set_temp = 65

        temp_scaled = int(
            (set_temp * self.TEMP_SET_SCALING_CONST_L)+self.TEMP_SET_SCALING_CONST_D)

        temp_hex = hex(temp_scaled)

        n = 2

        split_hex_list = [temp_hex[i:i+n]
                          for i in range(0, len(temp_hex), n)]

        temp_msb = str(split_hex_list[1])

        temp_lsb = str(split_hex_list[2])

        hex_list = []
        hex_list.append("AA")
        hex_list.append("11")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append(temp_msb)
        hex_list.append(temp_lsb)

        tx_bytes = self.build_tx_bytes(hex_list)

        echo_temps = self.write_serial(tx_bytes)

        split_hex_list = self.convert_hex_and_split_bytes(echo_temps)

        temp_2_msb_hex = split_hex_list[8]

        temp_2_lsb_hex = split_hex_list[9]

        # laser 2

        temp_2_msb_decimal = self.convert_hex_to_dec_values(temp_2_msb_hex)

        temp_2_msb_decimal_float = float(temp_2_msb_decimal)

        temp_2_lsb_decimal = self.convert_hex_to_dec_values(temp_2_lsb_hex)

        temp_2_lsb_decimal_float = float(temp_2_lsb_decimal)

        temp_2_full_decimal_unscaled = (
            (((((2**8) * temp_2_msb_decimal_float)+temp_2_lsb_decimal_float)/self.TEMP_SET_SCALING_CONST_L)) - self.TEMP_SET_SCALING_CONST_D)

    # Read temperatures ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def read_temp_LD0(self):
        """Reads the LD0 temperature"""

        hex_list = []
        hex_list.append("AA")
        hex_list.append("20")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")

        tx_bytes = self.build_tx_bytes(hex_list)

        lockin_and_temps_bytes = self.write_serial(tx_bytes)

        split_hex_list = self.convert_hex_and_split_bytes(
            lockin_and_temps_bytes)

        temp_1_msb_hex = split_hex_list[6]

        temp_1_lsb_hex = split_hex_list[7]

        # laser 1

        temp_1_msb_decimal = self.convert_hex_to_dec_values(temp_1_msb_hex)

        temp_1_msb_decimal_float = float(temp_1_msb_decimal)

        temp_1_lsb_decimal = self.convert_hex_to_dec_values(temp_1_lsb_hex)

        temp_1_lsb_decimal_float = float(temp_1_lsb_decimal)

        temp_1_full_decimal_unscaled = (
            (((((2**8) * temp_1_msb_decimal_float)+temp_1_lsb_decimal_float)- self.TEMP_READ_SCALING_CONST_N)) / self.TEMP_READ_SCALING_CONST_C)

        return temp_1_full_decimal_unscaled

    def read_temp_LD1(self):
        """Reads the LD1 temp"""

        hex_list = []
        hex_list.append("AA")
        hex_list.append("21")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")

        tx_bytes = self.build_tx_bytes(hex_list)

        echo_temps = self.write_serial(tx_bytes)

        split_hex_list = self.convert_hex_and_split_bytes(echo_temps)

        temp_2_msb_hex = split_hex_list[8]

        temp_2_lsb_hex = split_hex_list[9]

        # laser 2

        temp_2_msb_decimal = self.convert_hex_to_dec_values(temp_2_msb_hex)

        temp_2_msb_decimal_float = float(temp_2_msb_decimal)

        temp_2_lsb_decimal = self.convert_hex_to_dec_values(temp_2_lsb_hex)

        temp_2_lsb_decimal_float = float(temp_2_lsb_decimal)

        temp_2_full_decimal_unscaled = (
            (((((2**8) * temp_2_msb_decimal_float)+temp_2_lsb_decimal_float)-self.TEMP_READ_SCALING_CONST_N)) /self.TEMP_READ_SCALING_CONST_C)

        return temp_2_full_decimal_unscaled

    # Read then set ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def read_then_set_temp_LD0(self, set_temp):
        """Reads then sets the LD0 temp"""

        #TEST_TEMP = 25

        temp_scaled = int(
            (set_temp * self.TEMP_SET_SCALING_CONST_L)+self.TEMP_SET_SCALING_CONST_D)

        temp_hex = hex(temp_scaled)

        n = 2

        split_hex_list = [temp_hex[i:i+n]
                          for i in range(0, len(temp_hex), n)]

        temp_msb = str(split_hex_list[1])

        temp_lsb = str(split_hex_list[2])

        hex_list = []
        hex_list.append("AA")
        hex_list.append("30")
        hex_list.append(temp_msb)
        hex_list.append(temp_lsb)
        hex_list.append("00")
        hex_list.append("00")

        tx_bytes = self.build_tx_bytes(hex_list)

        echo_temps = self.write_serial(tx_bytes)

        split_hex_list = self.convert_hex_and_split_bytes(echo_temps)

        temp_1_msb_hex = split_hex_list[6]

        temp_1_lsb_hex = split_hex_list[7]

        # laser 1

        temp_1_msb_decimal = self.convert_hex_to_dec_values(temp_1_msb_hex)

        temp_1_msb_decimal_float = float(temp_1_msb_decimal)

        temp_1_lsb_decimal = self.convert_hex_to_dec_values(temp_1_lsb_hex)

        temp_1_lsb_decimal_float = float(temp_1_lsb_decimal)

        temp_1_full_decimal_unscaled = (
            (((((2**8) * temp_1_msb_decimal_float)+temp_1_lsb_decimal_float)/self.TEMP_READ_SCALING_CONST_N)) - self.TEMP_READ_SCALING_CONST_C)

    def read_then_set_temp_LD1(self, set_temp):
        """Reads the LD1 temp"""

        TEST_TEMP = 25

        temp_scaled = int(
            (set_temp * self.TEMP_SET_SCALING_CONST_L)+self.TEMP_SET_SCALING_CONST_D)

        temp_hex = hex(temp_scaled)

        n = 2

        split_hex_list = [temp_hex[i:i+n]
                          for i in range(0, len(temp_hex), n)]

        temp_msb = str(split_hex_list[1])

        temp_lsb = str(split_hex_list[2])

        hex_list = []
        hex_list.append("AA")
        hex_list.append("31")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append(temp_msb)
        hex_list.append(temp_lsb)

        tx_bytes = self.build_tx_bytes(hex_list)

        echo_temps = self.write_serial(tx_bytes)

        split_hex_list = self.convert_hex_and_split_bytes(echo_temps)

        temp_2_msb_hex = split_hex_list[8]
        temp_2_lsb_hex = split_hex_list[9]

        # laser 1

        temp_2_msb_decimal = self.convert_hex_to_dec_values(temp_2_msb_hex)

        temp_2_msb_decimal_float = float(temp_2_msb_decimal)

        temp_2_lsb_decimal = self.convert_hex_to_dec_values(temp_2_lsb_hex)

        temp_2_lsb_decimal_float = float(temp_2_lsb_decimal)

        temp_2_full_decimal_unscaled = (
            (((((2**8) * temp_2_msb_decimal_float)+temp_2_lsb_decimal_float)-self.TEMP_READ_SCALING_CONST_N)) / self.TEMP_READ_SCALING_CONST_C)

    def read_then_set_temp_LD0_and_LD1(self, set_temp_ld0, set_temp_ld1):
        """Reads the LD1 temp"""
        # TODO needs to get proper scaling placed
        # TEMP 1

        TEST_TEMP_1 = 25

        temp_1_scaled = int(
            (set_temp_ld0 * self.TEMP_SET_SCALING_CONST_L)+self.TEMP_SET_SCALING_CONST_D)

        temp_1_hex = hex(temp_1_scaled)

        n = 2

        split_hex_list_1 = [temp_1_hex[i:i+n]
                            for i in range(0, len(temp_1_hex), n)]

        temp_1_msb = str(split_hex_list_1[1])

        temp_1_lsb = str(split_hex_list_1[2])

        # TEMP 2

        TEST_TEMP_2 = 25

        temp_2_scaled = int(
            (set_temp_ld1 * self.TEMP_SET_SCALING_CONST_L)+self.TEMP_SET_SCALING_CONST_D)

        temp_2_hex = hex(temp_2_scaled)

        split_hex_list_2 = [temp_2_hex[i:i+n]
                            for i in range(0, len(temp_2_hex), n)]

        temp_2_msb = str(split_hex_list_2[1])

        temp_2_lsb = str(split_hex_list_2[2])

        hex_list = []
        hex_list.append("AA")
        hex_list.append("40")
        hex_list.append(temp_1_msb)
        hex_list.append(temp_1_lsb)
        hex_list.append(temp_2_msb)
        hex_list.append(temp_2_lsb)

        tx_bytes = self.build_tx_bytes(hex_list)

        echo_temps = self.write_serial(tx_bytes)

        split_hex_list = self.convert_hex_and_split_bytes(echo_temps)

        temp_1_msb_hex = split_hex_list[6]
        temp_1_lsb_hex = split_hex_list[7]

        temp_2_msb_hex = split_hex_list[8]
        temp_2_lsb_hex = split_hex_list[9]

        # laser 1

        temp_1_msb_decimal = self.convert_hex_to_dec_values(temp_1_msb_hex)

        temp_1_msb_decimal_float = float(temp_1_msb_decimal)

        temp_1_lsb_decimal = self.convert_hex_to_dec_values(temp_1_lsb_hex)

        temp_1_lsb_decimal_float = float(temp_1_lsb_decimal)

        temp_1_full_decimal_unscaled = (
            (((((2**8) * temp_1_msb_decimal_float) +
             temp_1_lsb_decimal_float)/self.TEMP_READ_SCALING_CONST_N))
            - self.TEMP_READ_SCALING_CONST_C)

        # laser 2

        temp_2_msb_decimal = self.convert_hex_to_dec_values(temp_2_msb_hex)

        temp_2_msb_decimal_float = float(temp_2_msb_decimal)

        temp_2_lsb_decimal = self.convert_hex_to_dec_values(temp_2_lsb_hex)

        temp_2_lsb_decimal_float = float(temp_2_lsb_decimal)

        temp_2_full_decimal_unscaled = (
            (((((2**8) * temp_2_msb_decimal_float) +
             temp_2_lsb_decimal_float)/self.TEMP_READ_SCALING_CONST_N))
            - self.TEMP_READ_SCALING_CONST_C)

    def read_sample_count_second_lockin_output(self):
        """reads lock-in 1st harmonic"""

        hex_list = []
        hex_list.append("AA")
        hex_list.append("48")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")

        tx_bytes = self.build_tx_bytes(hex_list)

        lockin_bytes = self.write_serial(tx_bytes)

        # Sample count

        count_1st_msb = lockin_bytes[2]

        count_2nd_msb = lockin_bytes[3]

        count_3rd_msb = lockin_bytes[4]

        count_lsb = lockin_bytes[5]

        count_full_decimal = (np.int32(count_1st_msb) << 24) | (np.int32(count_2nd_msb) << 16) | (np.int32(count_3rd_msb) << 8) | (np.int32(count_lsb))

        # second lock in

        second_lock_in_1st_msb = lockin_bytes[6]

        second_lock_in_2nd_msb = lockin_bytes[7]

        second_lock_in_3rd_msb = lockin_bytes[8]

        second_lock_in_lsb = lockin_bytes[9]

        second_lock_in_full_decimal = (np.int32(second_lock_in_1st_msb) << 24) | (np.int32(second_lock_in_2nd_msb) << 16) | (np.int32(second_lock_in_3rd_msb) << 8) | (np.int32(second_lock_in_lsb))

        return float(count_full_decimal), float(second_lock_in_full_decimal)

    # Lock-in mode ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def lock_in_mode(self):
        """Lock in mode is set 0 = RC filter with no flush, 1 = RC filter with flush on read, 2 = Integrate with flush on read"""
        mode_0 = "00"
        mode_1 = "01"
        mode_2 = "02"

        hex_list = []
        hex_list.append("AA")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append(mode_2)

        tx_bytes = self.build_tx_bytes(hex_list)

        self.write_serial(tx_bytes)

    # Read lock in ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def read_lockin_1st_harmonic(self):
        """reads lock-in 1st harmonic"""

        hex_list = []
        hex_list.append("AA")
        hex_list.append("50")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")

        tx_bytes = self.build_tx_bytes(hex_list)

        lockin_bytes = self.write_serial(tx_bytes)

        split_hex_list = self.convert_hex_and_split_bytes(lockin_bytes)

        lock_in_1st_msb = split_hex_list[2]

        lock_in_2nd_msb = split_hex_list[3]

        lock_in_3rd_msb = split_hex_list[4]

        lock_in_lsb = split_hex_list[5]

        lock_in_lsb_full_decimal = int(lock_in_lsb, 16)

        lock_in_msb_full = f"{lock_in_1st_msb}{lock_in_2nd_msb}{lock_in_3rd_msb}"

        lock_in_msb_full_decimal = int(lock_in_msb_full, 16)

        lock_in_full_decimal = f"{lock_in_msb_full_decimal}.{lock_in_lsb_full_decimal}"

    def read_lockin_1st_and_both_temps(self):
        """Reads lock-in 1st harmonic, LD0 temp, LD1 temp"""

        hex_list = []
        hex_list.append("AA")
        hex_list.append("60")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")

        tx_bytes = self.build_tx_bytes(hex_list)

        lockin_and_temps_bytes = self.write_serial(tx_bytes)

        split_hex_list = self.convert_hex_and_split_bytes(
            lockin_and_temps_bytes)

        #Temperature bytes do not require bitwise operations

        temp_1_msb_hex = split_hex_list[6]

        temp_1_lsb_hex = split_hex_list[7]

        temp_2_msb_hex = split_hex_list[8]

        temp_2_lsb_hex = split_hex_list[9]

        # Bit shifting to obtain lockin value
        # Values from bytearray are 8-bit unsigned integers, they are then converted to 32-bit signed integers

        unsigned_list = []

        # Unsigned 8bit integer list created from incoming bytearray
        for i in range(10):
            unsigned_list.append(np.uint8(lockin_and_temps_bytes[i]))

        # Bit shifting required for processing MSBs and LSBs
        lock_in_full_decimal_unscaled = (np.int32(unsigned_list[2]) << 24) | (np.int32(unsigned_list[3]) << 16) | (np.int32(unsigned_list[4]) << 8) | (np.int32(unsigned_list[5]))

        # Value is scaled by X16 to undo firmware scaling
        lock_in_full_decimal_scaled = float(lock_in_full_decimal_unscaled)*16

        # laser 1

        temp_1_msb_decimal = self.convert_hex_to_dec_values(temp_1_msb_hex)

        temp_1_msb_decimal_float = float(temp_1_msb_decimal)

        temp_1_lsb_decimal = self.convert_hex_to_dec_values(temp_1_lsb_hex)

        temp_1_lsb_decimal_float = float(temp_1_lsb_decimal)

        temp_1_full_decimal_unscaled = (
            (((((2**8) * temp_1_msb_decimal_float)+temp_1_lsb_decimal_float)-self.TEMP_READ_SCALING_CONST_N)) / self.TEMP_READ_SCALING_CONST_C)

        # laser 2

        temp_2_msb_decimal = self.convert_hex_to_dec_values(temp_2_msb_hex)

        temp_2_msb_decimal_float = float(temp_2_msb_decimal)

        temp_2_lsb_decimal = self.convert_hex_to_dec_values(temp_2_lsb_hex)

        temp_2_lsb_decimal_float = float(temp_2_lsb_decimal)

        temp_2_full_decimal_unscaled = (
            (((((2**8) * temp_2_msb_decimal_float)+temp_2_lsb_decimal_float)-self.TEMP_READ_SCALING_CONST_N)) / self.TEMP_READ_SCALING_CONST_C)

        return lock_in_full_decimal_scaled, temp_1_full_decimal_unscaled, temp_2_full_decimal_unscaled

    # Set laser power ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def set_LD0_Power(self, set_power):
        """Sets the LD0 power"""

        temp_scaled = int(set_power * self.CURRENT_REV5)

        temp_hex = hex(temp_scaled)

        n = 2

        split_hex_list = [temp_hex[i:i+n]
                          for i in range(0, len(temp_hex), n)]

        current_msb = str(split_hex_list[1])

        current_lsb = str(split_hex_list[2])

        hex_list = []
        hex_list.append("AA")
        hex_list.append("80")
        hex_list.append(current_msb)
        hex_list.append(current_lsb)
        hex_list.append("00")
        hex_list.append("00")

        tx_bytes = self.build_tx_bytes(hex_list)

        echo_current = self.write_serial(tx_bytes)

        split_hex_list = self.convert_hex_and_split_bytes(echo_current)

        current_1_msb_hex = split_hex_list[6]

        current_1_lsb_hex = split_hex_list[7]

        current_1_msb_decimal = self.convert_hex_to_dec_values(
            current_1_msb_hex)

        current_1_msb_decimal_float = float(current_1_msb_decimal)

        current_1_lsb_decimal = self.convert_hex_to_dec_values(
            current_1_lsb_hex)

        current_1_lsb_decimal_float = float(current_1_lsb_decimal)

        current_1_full_decimal_unscaled = (
            (((2**8) * current_1_msb_decimal_float)+current_1_lsb_decimal_float)/self.CURRENT_REV5)

    def set_LD1_Power(self, set_power):
        """Sets the LD1 power"""

        #TEST_CURRENT = 100

        temp_scaled = int(set_power * self.CURRENT_REV5)

        temp_hex = hex(temp_scaled)

        n = 2

        split_hex_list = [temp_hex[i:i+n]
                          for i in range(0, len(temp_hex), n)]

        current_msb = str(split_hex_list[1])

        current_lsb = str(split_hex_list[2])

        hex_list = []
        hex_list.append("AA")
        hex_list.append("81")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append(current_msb)
        hex_list.append(current_lsb)

        tx_bytes = self.build_tx_bytes(hex_list)

        echo_current = self.write_serial(tx_bytes)

        split_hex_list = self.convert_hex_and_split_bytes(echo_current)

        current_2_msb_hex = split_hex_list[8]

        current_2_lsb_hex = split_hex_list[9]

        # laser 1

        current_2_msb_decimal = self.convert_hex_to_dec_values(
            current_2_msb_hex)

        current_2_msb_decimal_float = float(current_2_msb_decimal)

        current_2_lsb_decimal = self.convert_hex_to_dec_values(
            current_2_lsb_hex)

        current_2_lsb_decimal_float = float(current_2_lsb_decimal)

        current_2_full_decimal_unscaled = (
            (((2**8) * current_2_msb_decimal_float)+current_2_lsb_decimal_float)/self.CURRENT_REV5)

    # TEC control ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def TEC_enable(self):
        """Enables the TEC"""

        hex_list = []
        hex_list.append("AA")
        hex_list.append("90")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")

        tx_bytes = self.build_tx_bytes(hex_list)

        TEC_enable_comm = self.write_serial(tx_bytes)

    def TEC_disable(self):
        """Disables the TEC"""

        hex_list = []
        hex_list.append("AA")
        hex_list.append("91")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")

        tx_bytes = self.build_tx_bytes(hex_list)

        TEC_disable_comm = self.write_serial(tx_bytes)

    # Phase Modulation Control ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def phase_modulation_voltage_setting(self, modulation_voltage: float):
        """Enables the PCS"""

        scaled_modulation_voltage = str(math.ceil(modulation_voltage*25.4))

        hex_list = []
        hex_list.append("AA")
        hex_list.append("93")
        hex_list.append("B3")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append(scaled_modulation_voltage)

        tx_bytes = self.build_tx_bytes(hex_list)

        self.write_serial(tx_bytes)

        print(f"Phase modulation set to {modulation_voltage}")

    # PCS Control ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def PCS_enable(self):
        """Enables the PCS"""

        hex_list = []
        hex_list.append("AA")
        hex_list.append("A0")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")

        tx_bytes = self.build_tx_bytes(hex_list)

        PCS_enable_command = self.write_serial(tx_bytes)

    def PCS_disable(self):
        """Disables the PCS"""

        hex_list = []
        hex_list.append("AA")
        hex_list.append("A1")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")

        tx_bytes = self.build_tx_bytes(hex_list)

        PCS_disable_command = self.write_serial(tx_bytes)

    def read_pcs_current(self, channel, source_or_detector):
        """Reads dsp temperature value"""

        if channel == 0:
            channel_byte = "00"
        else:
            channel_byte = "01"

        if source_or_detector == 0:
            source_byte = "00"
        else:
            source_byte = "01"

        hex_list = []
        hex_list.append("AA")
        hex_list.append("C2")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append(channel_byte)
        hex_list.append(source_byte)

        tx_bytes = self.build_tx_bytes(hex_list)

        pcs_current_bytes = self.write_serial(tx_bytes)

        split_hex_list = self.convert_hex_and_split_bytes(
            pcs_current_bytes)

        pcs_current_msb_hex = split_hex_list[8]

        pcs_current_lsb_hex = split_hex_list[9]

        pcs_current_msb_decimal = self.convert_hex_to_dec_values(
            pcs_current_msb_hex)

        pcs_current_msb_decimal_float = float(pcs_current_msb_decimal)

        pcs_current_lsb_decimal = self.convert_hex_to_dec_values(
            pcs_current_lsb_hex)

        pcs_current_lsb_decimal_float = float(pcs_current_lsb_decimal)

        pcs_current_full_decimal_unscaled = (
            ((((2**8) * pcs_current_msb_decimal_float)+pcs_current_lsb_decimal_float)/32))

    # Laser Bias Control ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def laser_bias_enable(self):
        """Enables the laser bias"""

        hex_list = []
        hex_list.append("AA")
        hex_list.append("B0")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")

        tx_bytes = self.build_tx_bytes(hex_list)

        self.write_serial(tx_bytes)

    def laser_bias_disable(self):
        """Disables the laser bias"""

        hex_list = []
        hex_list.append("AA")
        hex_list.append("B1")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")

        tx_bytes = self.build_tx_bytes(hex_list)

        self.write_serial(tx_bytes)

    # Component values read ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def read_heatsink_temp(self):
        """Reads heatsink temperature value"""

        hex_list = []
        hex_list.append("AA")
        hex_list.append("C0")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")

        tx_bytes = self.build_tx_bytes(hex_list)

        heatsink_temps_bytes = self.write_serial(tx_bytes)

        split_hex_list = self.convert_hex_and_split_bytes(
            heatsink_temps_bytes)

        temp_heatsink_msb_hex = split_hex_list[8]

        temp_heatsink_lsb_hex = split_hex_list[9]

        temp_heatsink_msb_decimal = self.convert_hex_to_dec_values(
            temp_heatsink_msb_hex)

        temp_heatsink_msb_decimal_float = float(temp_heatsink_msb_decimal)

        temp_heatsink_lsb_decimal = self.convert_hex_to_dec_values(
            temp_heatsink_lsb_hex)

        temp_heatsink_lsb_decimal_float = float(temp_heatsink_lsb_decimal)

        temp_heatsink_full_decimal_unscaled = (
            (((((2**8) * temp_heatsink_msb_decimal_float)+temp_heatsink_lsb_decimal_float)/427.36)) - 35.13)

    def read_dsp_temp(self):
        """Reads dsp temperature value"""

        hex_list = []
        hex_list.append("AA")
        hex_list.append("C1")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")

        tx_bytes = self.build_tx_bytes(hex_list)

        dsp_temps_bytes = self.write_serial(tx_bytes)

        split_hex_list = self.convert_hex_and_split_bytes(
            dsp_temps_bytes)

        temp_dsp_msb_hex = split_hex_list[8]

        temp_dsp_lsb_hex = split_hex_list[9]

        temp_dsp_msb_decimal = self.convert_hex_to_dec_values(
            temp_dsp_msb_hex)

        temp_dsp_msb_decimal_float = float(temp_dsp_msb_decimal)

        temp_dsp_lsb_decimal = self.convert_hex_to_dec_values(
            temp_dsp_lsb_hex)

        temp_dsp_lsb_decimal_float = float(temp_dsp_lsb_decimal)

        temp_dsp_full_decimal_unscaled = (
            (((((2**8) * temp_dsp_msb_decimal_float)+temp_dsp_lsb_decimal_float)/427.36)) - 35.13)

    # Fan Control ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def fan_on_high(self):
        """Turns the fan on to high setting"""

        hex_list = []
        hex_list.append("AA")
        hex_list.append("C4")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("01")
        hex_list.append("01")

        tx_bytes = self.build_tx_bytes(hex_list)

        print("Turning fan on....")

        fan_state_and_speed_bytes = self.write_serial(tx_bytes)

        fan_state_and_speed_hex = self.convert_hex_and_split_bytes(
            fan_state_and_speed_bytes)

        fan_state_and_speed_decimal = self.convert_hex_to_dec(
            fan_state_and_speed_hex)

    def fan_on_low(self):
        """Turns the fan on to high setting"""

        hex_list = []
        hex_list.append("AA")
        hex_list.append("C4")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("01")

        tx_bytes = self.build_tx_bytes(hex_list)

        print("Turning fan on....")

        fan_state_and_speed_bytes = self.write_serial(tx_bytes)

        fan_state_and_speed_hex = self.convert_hex_and_split_bytes(
            fan_state_and_speed_bytes)

        fan_state_and_speed_decimal = self.convert_hex_to_dec(
            fan_state_and_speed_hex)

    def fan_off(self):
        """Turns the fan off"""

        hex_list = []
        hex_list.append("AA")
        hex_list.append("C4")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")

        tx_bytes = self.build_tx_bytes(hex_list)

        print("Turning fan off....")

        fan_state_and_speed_bytes = self.write_serial(tx_bytes)

        fan_state_and_speed_hex = self.convert_hex_and_split_bytes(
            fan_state_and_speed_bytes)

        fan_state_and_speed_decimal = self.convert_hex_to_dec(
            fan_state_and_speed_hex)

        fan_state_decimal = fan_state_and_speed_decimal[8]

        fan_speed_decimal = fan_state_and_speed_decimal[9]

    # LED control ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def LED_enable(self):
        """Enables the LED"""

        hex_list = []
        hex_list.append("AA")
        hex_list.append("C5")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("01")

        tx_bytes = self.build_tx_bytes(hex_list)

        LED_enable_command = self.write_serial(tx_bytes)

        print(LED_enable_command)

    def LED_disable(self):
        """Enables the LED"""

        hex_list = []
        hex_list.append("AA")
        hex_list.append("C5")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")

        tx_bytes = self.build_tx_bytes(hex_list)

        LED_disable_command = self.write_serial(tx_bytes)

        print(LED_disable_command)

    # Read Firmware Version ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def read_version(self):
        """reads firmware version installed"""

        hex_list = []
        hex_list.append("AA")
        hex_list.append("C6")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")

        tx_bytes = self.build_tx_bytes(hex_list)

        version_bytes = self.write_serial(tx_bytes)

        split_hex_list = self.convert_hex_and_split_bytes(version_bytes)

        converted_list = self.convert_hex_to_dec(split_hex_list)

        version_first_half = str(converted_list[8])

        version_second_half = str(converted_list[6])

        version_number = f"{version_first_half}.{version_second_half}"

        print("Firmware version number is: " + version_first_half +
              "." + version_second_half)

        return version_number

    # Lock-in on/off control ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def lockin_enable(self):
        """Enables Lock-in"""

        hex_list = []
        hex_list.append("AA")
        hex_list.append("C7")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("01")

        tx_bytes = self.build_tx_bytes(hex_list)

        lockin_enable_comm = self.write_serial(tx_bytes)

        lockin_enable_hex = lockin_enable_comm.hex()

        print("Lockin enabled")

    def lockin_disable(self):
        """Disables Lock-in"""

        hex_list = []
        hex_list.append("AA")
        hex_list.append("C7")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")

        tx_bytes = self.build_tx_bytes(hex_list)

        lockin_disable_comm = self.write_serial(tx_bytes)

        lockin_disable_hex = lockin_disable_comm.hex()

        lockin_disable_dec = self.convert_hex_to_dec_values(lockin_disable_hex)

        print("Lockin disabled")

    # Sleep timer control ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def start_sleep_timer_countdown(self, hours_delay, minutes_delay, seconds_delay):
        """Sets sleep timer countdown delay in hours, minutes and seconds"""

        hours_delay_hex = hex(hours_delay)

        minutes_delay_hex = hex(minutes_delay)

        seconds_delay_hex = hex(seconds_delay)

        hex_list = []
        hex_list.append("AA")
        hex_list.append("C8")
        hex_list.append("00")
        hex_list.append(hours_delay_hex)
        hex_list.append(minutes_delay_hex)
        hex_list.append(seconds_delay_hex)

        tx_bytes = self.build_tx_bytes(hex_list)

        echo_delay = self.write_serial(tx_bytes)

        split_hex_list = self.convert_hex_and_split_bytes(echo_delay)

        echo_hours_delay_hex = split_hex_list[7]

        echo_minutes_msb_hex = split_hex_list[8]

        echo_seconds_lsb_hex = split_hex_list[9]

        echo_delay_string = f"Time delay set to: {echo_hours_delay_hex} Hours, {echo_minutes_msb_hex} Minutes, {echo_seconds_lsb_hex}"

        print(
            f"Time delay set to: {echo_hours_delay_hex} Hours, {echo_minutes_msb_hex} Minutes, {echo_seconds_lsb_hex}")

        return echo_delay_string

    def stop_sleep_timer_countdown(self):
        """Stops sleep timer from running"""

        hex_list = []
        hex_list.append("AA")
        hex_list.append("C9")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")

        tx_bytes = self.build_tx_bytes(hex_list)

        self.write_serial(tx_bytes)
    # Read Laser Currents ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def read_laser_currents(self):
        """Reads LD0, LD1 Bias Current"""

        hex_list = []
        hex_list.append("AA")
        hex_list.append("CC")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")

        tx_bytes = self.build_tx_bytes(hex_list)

        lockin_and_temps_bytes = self.write_serial(tx_bytes)

        split_hex_list = self.convert_hex_and_split_bytes(
            lockin_and_temps_bytes)

        temp_1_msb_hex = split_hex_list[6]

        temp_1_lsb_hex = split_hex_list[7]

        temp_2_msb_hex = split_hex_list[8]

        temp_2_lsb_hex = split_hex_list[9]

        # laser 1

        temp_1_msb_decimal = self.convert_hex_to_dec_values(temp_1_msb_hex)

        temp_1_msb_decimal_float = float(temp_1_msb_decimal)

        temp_1_lsb_decimal = self.convert_hex_to_dec_values(temp_1_lsb_hex)

        temp_1_lsb_decimal_float = float(temp_1_lsb_decimal)

        temp_1_full_decimal_unscaled = (
            ((2**8) * temp_1_msb_decimal_float)+temp_1_lsb_decimal_float)

        if temp_1_full_decimal_unscaled < 32768:
            temp_1_full_decimal_unscaled = 0

        temp_1_full_decimal_scaled = (temp_1_full_decimal_unscaled/80)

        # laser 2

        temp_2_msb_decimal = self.convert_hex_to_dec_values(temp_2_msb_hex)

        temp_2_msb_decimal_float = float(temp_2_msb_decimal)

        temp_2_lsb_decimal = self.convert_hex_to_dec_values(temp_2_lsb_hex)

        temp_2_lsb_decimal_float = float(temp_2_lsb_decimal)

        temp_2_full_decimal_unscaled = (
            ((2**8) * temp_2_msb_decimal_float)+temp_2_lsb_decimal_float)

        if temp_2_full_decimal_unscaled < 32768:
            temp_2_full_decimal_unscaled = 0

        temp_2_full_decimal_scaled = (temp_2_full_decimal_unscaled/80)

    # Lock in time constant ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def set_lockin_time_constant(self, set_time):
        """Sets the lockin time constant"""

        #TIME_CONSTANT = 100

        time_scaled = int(set_time / 3)

        time_hex = hex(time_scaled)

        n = 2

        split_hex_list = [time_hex[i:i+n]
                          for i in range(0, len(time_hex), n)]

        time_msb = str("00")

        time_lsb = str(split_hex_list[1])

        hex_list = []
        hex_list.append("AA")
        hex_list.append("CB")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append(time_msb)
        hex_list.append(time_lsb)

        tx_bytes = self.build_tx_bytes(hex_list)

        echo_time = self.write_serial(tx_bytes)

        split_hex_list = self.convert_hex_and_split_bytes(echo_time)

        time_msb_hex = split_hex_list[8]

        time_lsb_hex = split_hex_list[9]

        time_msb_decimal = self.convert_hex_to_dec_values(time_msb_hex)

        time_msb_decimal_float = float(time_msb_decimal)

        time_lsb_decimal = self.convert_hex_to_dec_values(time_lsb_hex)

        time_lsb_decimal_float = float(time_lsb_decimal)

        time_full_decimal_unscaled = (
            (((2**8) * time_msb_decimal_float)+time_lsb_decimal_float)*3)

    # Set lock in gain ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def set_lockin_gain(self, gain):
        """Sets the lockin gain"""

        gain_formatted = f"0{gain}"

        hex_list = []
        hex_list.append("AA")
        hex_list.append("CE")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append("00")
        hex_list.append(gain_formatted)

        tx_bytes = self.build_tx_bytes(hex_list)

        lockin_gain_bytes = self.write_serial(tx_bytes)

        lockin_gain_hex = lockin_gain_bytes.hex()

        lockin_gain_dec = self.convert_hex_to_dec_values(lockin_gain_hex)

    def write_EEPROM(self, address, value):
        # Untested, should not use

        split_address = float(math.floor(address/256))
        modded_address = float(address % 256)

        hex_list = []
        hex_list.append("AA")
        hex_list.append("09")
        hex_list.append("4C")
        hex_list.append(split_address)
        hex_list.append(modded_address)
        hex_list.append(value)

        tx_bytes = self.build_tx_bytes(hex_list)

        self.write_serial(tx_bytes)

    def read_eeprom(self, address):
        """Reads the eemprom 1 memory address at a time and returns a char"""
        split_address = (math.floor(address/256))

        modded_address = (address % 256)

        # Separates address lsb msb, turns them into hex, capitalizes the chars, checks if theres only 1 char adds
        # a 0 in front to conform to byte format
        split1 = f'0{str.upper(hex(split_address).split("x")[1])}' if len(hex(
            split_address).split("x")[1]) == 1 else f'{str.upper(hex(split_address).split("x")[1])}'
        split2 = f'0{str.upper(hex(modded_address).split("x")[1])}' if len(hex(
            modded_address).split("x")[1]) == 1 else f'{str.upper(hex(modded_address).split("x")[1])}'

        hex_list = []
        hex_list.append("AA")
        hex_list.append("0A")
        hex_list.append("00")
        hex_list.append(split1)
        hex_list.append(split2)
        hex_list.append("00")

        tx_bytes = self.build_tx_bytes(hex_list)

        eeprom_data = self.write_serial(tx_bytes)

        # checks for integrity of byte array if not a list, rechecks the memory address until valid
        try:
            char = chr(eeprom_data[9])
        except TypeError as e:
            print(e)
            char = self.check_data(address)

        return char

    def check_data(self, address):
        value = self.read_eeprom(address)
        return value
    
    def shutdown(self):
        self.set_LD0_Temperature(25)
        self.set_LD1_Temperature(25)
        self.TEC_disable()
        self.fan_off()
        self.PCS_disable()
        self.laser_bias_disable()
        self.lockin_disable()