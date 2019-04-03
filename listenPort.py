import serial

ser = serial.Serial('/dev/cu.wchusbserial14320', 9600)

while True:
    data = ser.readline()
    if data:
        print(data)