import serial


class serial_data():
    TX_BYTE = [5]
    RX_BYTE = [9]
    COM_Port = ""
    PB7200COM = serial.Serial()
    is_COM_Open = False

    
