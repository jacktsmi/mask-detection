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

"""
This script reads serial data from the Arduino to determine if a person is present. If so, it takes a picture using the MLX90640 thermal camera,...
...calculates average difference between forehead and mouth region temperatures, and accordingly sets the output LED's and lock. 
There are two main commented out sections that could be uncommented if you would like to visualize the thermal camera image. 
- RK

"""

# First, set up the serial port to arduino and all GPIO pins to relay/lock and LED's
# if __name__ == '__main__':
ser = serial.Serial('/dev/ard', 115200, timeout=1)
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

# Setup I2C between thermal camera and Pi 
i2c = busio.I2C(board.SCL, board.SDA, frequency=400000) # setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c) # begin MLX90640 with I2C comm
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_4_HZ # set refresh rate
mlx_shape = (24,32)
# IF you would like to interpolate differently by 'zooming in' to the existing thermal resolution of 24x32, change the below values
mlx_interp_val = 1 # interpolate on each dimension
mlx_interp_shape = (mlx_shape[0]*mlx_interp_val,
                    mlx_shape[1]*mlx_interp_val) # new shape


# -------Code to display live thermal image, might lag/crash program after-------
# -----a bit but is useful for calibrating thermal and real camera positions-----

# Create figure, axis, and set parameter for plotting thermal image later
# plt.ion()
# fig2,ax2 = plt.subplots(figsize=(12,7))
# therm2 = ax2.imshow(np.zeros(mlx_interp_shape),cmap = plt.cm.bwr,vmin=25,vmax=45)
# cbar2 = fig2.colorbar(therm2)
# cbar2.set_label('Temperature [$^{\circ}$C]',fontsize=14) # colorbar label

# fig2.canvas.draw() # draw figure to copy background
# ax_background = fig2.canvas.copy_from_bbox(ax2.bbox) # copy background
# fig2.show() # show the figure before blitting

# ------------------------------------------------------------------------------

frame = np.zeros((24*32,)) # setup array for storing all 768 temperatures
# t_array = [] # To keep track of runtime and frame rate

try:
    while True:
        if ser.in_waiting > 0:
        # readline receives unicode encoded string
        # ASCII encoding is a subset of unicode encoding; it has the same encoding as the first 128 characters of unicode.
        # But we may have a string that goes beyond ASCII so we use unicde utf-8 decoding
            line = ser.readline().decode("utf-8").rstrip()
            ser.reset_input_buffer()
            line = line.split(',')
            if len(line)<3:
                continue
            if line[0] == '0': # while someone is not there
                GPIO.output(red,1)
                GPIO.output(green,1)
                GPIO.output(relay,0)
                continue
            print('PERSON')

            # Camera capture, run through algorithm, and unlock
            time.sleep(1)
            ser.reset_input_buffer()
            t1 = time.monotonic()
            try:
                mlx.getFrame(frame) # read MLX temperatures into frame var
            except:
		print('Unable to get frame from thermal camera')
                continue
            data_array = (np.reshape(frame,mlx_interp_shape)) # reshape to 24x32
            # Note: Because MLX camera reads it in opposite from imshow, 'origin' is top right and we need to flip if plotting later

            top = data_array[6,12:18]  # Forehead pixels
            bottom = data_array[15,12:18] # Mouth region pixels
            avg = np.mean(np.abs(top-bottom)) # Average of absolute difference between forehead and mouth temperatures 
            #GPIO.output(red,1) ###IS THIS NEEDED HERE??
            if(avg<2): # If difference is < 2 degrees celsius if they're not wearing mask
                GPIO.output(red,1)
                GPIO.output(green,0)
                GPIO.output(relay,0)
            else:
                GPIO.output(red,0)
                GPIO.output(green,1)
                GPIO.output(relay,1)
            
            # -------Code to display live thermal image, might lag/crash program after-------
	    # -----a bit but is useful for calibrating thermal and real camera positions-----

            #therm2.set_data(np.fliplr(data_array))#[10:20,left_col:right_col+1])) # flip left to right
            #therm2.set_clim(vmin=np.min(data_array),vmax=np.max(data_array)) # set bounds
            #cbar2.on_mappable_changed(therm2) # update colorbar range
            #plt.pause(0.001) # required

            # -------------------------------------------------------------------------------

            # Calculate time to get frame and perform calculations, and print frame rate
            # t_array.append(time.monotonic()-t1) 
            # print('Sample Rate: {0:2.1f}fps'.format(len(t_array)/np.sum(t_array)))
finally:
    ser.close()
