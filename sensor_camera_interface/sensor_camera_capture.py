import serial, csv, os
import numpy as np
import matplotlib.pyplot as plt
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera


time_vec, data_vec = [],[]
moving_avg = []
datafile_name = 'test_data.csv'
if os.path.isfile(datafile_name):
    os.remove(datafile_name)


ser = serial.Serial('/dev/ttyACM0', baudrate=115200)
ser.flush()

# Initialize objects for continuous image capture
camera = PiCamera()
image_size = (640, 480)
camera.resolution = image_size
camera.framerate = 30

# Continuously capture images fom camera, pause when person is detected
while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode("utf-8").rstrip()
        print(line)
        line = line.split(',')
        #info = ser.readline()
        #print(info)
        #line = (info[0:len(info)-4].decode("utf-8")).split(',')
        print(line)

        if np.size(line) == 1:
            continue;
        if line[0] == '0':
            #time_vec.append(float(line[3]))
            data_vec.append(float(line[2]))
            moving_avg.append(float(line[1]))
            print('No person')
        elif line[0] == '1':
            #time_vec.append(float(line[3]))
            data_vec.append(float(line[2]))
            moving_avg.append(float(line[1]))
            
            # Display image
            image = np.zeros((480, 640, 3), dtype=np.uint8)
            camera.capture(image, 'rgb') # Get image from frame
            plt.imshow(image)
            plt.show()
            print('PERSON')    
            
            break

#time_min = np.min(time_vec)
#dat_min = np.min(data_vec)
# with open(datafile_name,'a') as f:
#     writer = csv.writer(f,delimiter=',')
# plt.scatter(np.arange(0,len(data_vec)),data_vec,label = 'Instantaneous Distance')
# plt.plot(np.arange(0,len(data_vec)),moving_avg,label = 'Moving avg')
# plt.title('Walking perpendicular to sensor')
# plt.xlabel('Sample')
# plt.ylabel('Distance(mm)')
# plt.legend()
# plt.show()
