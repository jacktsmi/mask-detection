import serial

ser = serial.Serial('/dev/ttyACM0', baudrate=9600)
ser.flush()

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('unicode_escape').rstrip()
        print(line)
        if line[0] == '0':
           print('No person')
        elif line[0] == '1':
            print('PERSON')
