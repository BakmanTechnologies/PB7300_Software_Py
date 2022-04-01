import math


def test_eeprom():
    address = 10

    split_address = (math.floor(address/256))

    print(hex(split_address))

    modded_address = (address % 256)

    print(hex(modded_address))

    print(hex(split_address).split("x"))
    print(hex(modded_address).split("x"))

    split1 = f'0{str.capitalize(hex(split_address).split("x")[1])}' if len(hex(split_address).split("x")[1]) == 1 else f'{str.capitalize(hex(split_address).split("x")[1])}'
    split2 = f'0{str.capitalize(hex(modded_address).split("x")[1])}' if len(hex(modded_address).split("x")[1]) == 1 else f'{str.capitalize(hex(modded_address).split("x")[1])}'

    print("split1",split1)
    print("split2",split2)

    hex_list = []
    hex_list.append("AA")
    hex_list.append("0A")
    hex_list.append("00")
    hex_list.append(split1)
    hex_list.append(split2)
    hex_list.append("00")

    print(hex_list)

    sync_byte = hex_list[0]
    command_byte = hex_list[1]
    third_byte = hex_list[2]
    fourth_byte = hex_list[3]
    fifth_byte = hex_list[4]
    sixth_byte = hex_list[5]

    tx_bytes_hex = f"{sync_byte} {command_byte} {third_byte} {fourth_byte} {fifth_byte} {sixth_byte}"

    print(tx_bytes_hex)

    tx_byte_array = bytearray.fromhex(tx_bytes_hex)

    #eeprom_data = self.write_serial(tx_byte_array)

    print(tx_byte_array)

    # return eeprom_data

test_eeprom()
