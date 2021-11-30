import serial

"""
This is the initial simple code to read values from the Arduino. The Arduino sends a string with 2 values: 
0 or 1, and running average so far
This script decodes this string, and prints 'No person' or 'Person' based on 0 or 1 input

"""
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
