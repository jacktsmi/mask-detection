##########################################
# MLX90640 Thermal Camera w Raspberry Pi
# -- 2Hz Sampling with Simple Routine
##########################################
#
import time,board,busio
import numpy as np
import adafruit_mlx90640
import matplotlib.pyplot as plt
import cv2
import RPi.GPIO as GPIO
import serial
#if __name__ == '__main__':
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
ser.flush()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)

relay = 17
red = 18
green = 22
GPIO.output(relay,0)
GPIO.output(red,0)
GPIO.output(green,0)

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000) # setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c) # begin MLX90640 with I2C comm
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_4_HZ # set refresh rate
mlx_shape = (24,32)

mlx_interp_val = 1 # interpolate # on each dimension
mlx_interp_shape = (mlx_shape[0]*mlx_interp_val,
                    mlx_shape[1]*mlx_interp_val) # new shape



frame = np.zeros((24*32,)) # setup array for storing all 768 temperatures
t_array = []
tests = []
while True:
    if ser.in_waiting > 0:
    #readline receives unicode encoded string
    #ASCII encoding is a subset of unicode encoding; it has the same encoding as the first 128 characters of unicode.
    #But we may have a string that goes beyond ASCII so we use unicde escape decoding
        line = ser.readline().decode("utf-8").rstrip()
        ser.reset_input_buffer()
        print(line)
        line = line.split(',')
        if len(line)<3:
            continue
        if line[0] == '0': # while someone is not there
        #print(line)
            #time.sleep(0.1)
            print('No person')
            GPIO.output(red,1)
            GPIO.output(green,1)
            GPIO.output(relay,0)
            print(line)
            continue
        print('PERSON')
        #camera capture, run through a model, and unlock- maybe once it enters this, tell the arduino to..
        #..stop measuring. Then when it's done, start measuring from arduino again
        #That way we don't have data waiting while this part is being run
        #print('Put your face here')
        time.sleep(1)
        ser.reset_input_buffer()
        print(line)
        t1 = time.monotonic()
        try:
            mlx.getFrame(frame) # read MLX temperatures into frame var
        except:
            print("some nonsense")
            continue
        data_array = (np.reshape(frame,mlx_interp_shape)) # reshape to 24x32
        oldr = np.max(data_array) - np.min(data_array)
        newr = 255 - 0
        newval = (((data_array - np.min(data_array)) * newr) / oldr) + 0
        img = np.asarray(newval)
        intimg = img.astype(np.uint8)
        intimg[intimg < 200] = 0
        
        #Canny edge detection
        edges = cv2.Canny(intimg,100,200)
        
        #finding bounds
        indices = np.where(edges == 255)
        left_col = np.min(indices[1])
        right_col = np.max(indices[1])
        nred = np.sum(data_array[10:20,left_col:right_col+1]>32)
        tests.append(nred)
        print(np.mean(tests))
        print(len(tests))
        GPIO.output(red,1)
        if(nred>60):
            GPIO.output(red,1)
            GPIO.output(green,0)
            GPIO.output(relay,0)
        else:
            GPIO.output(red,0)
            GPIO.output(green,1)
            GPIO.output(relay,1)
        
        
        t_array.append(time.monotonic()-t1)
        print('Sample Rate: {0:2.1f}fps'.format(len(t_array)/np.sum(t_array)))