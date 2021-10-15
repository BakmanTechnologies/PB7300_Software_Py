

temperature_m = 427.36
temperature_b = 35.13

TEST_TEMP = 25

temp_scaled = int((TEST_TEMP + temperature_b)*temperature_m)

temp_hex = hex(temp_scaled)

n = 2

split_hex = [temp_hex[i:i+n]
             for i in range(0, len(temp_hex), n)]

temp_msb = str(split_hex[1])

temp_lsb = str(split_hex[2])

hex_list = []
hex_list.append("AA")
hex_list.append("10")
hex_list.append(temp_msb)
hex_list.append(temp_lsb)
hex_list.append("00")
hex_list.append("00")


print(hex_list)
