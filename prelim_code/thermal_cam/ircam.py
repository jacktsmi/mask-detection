##########################################
# MLX90640 Thermal Camera w Raspberry Pi
# -- 2fps with Interpolation and Blitting
##########################################
#
import time,board,busio
import numpy as np
import adafruit_mlx90640
import matplotlib.pyplot as plt
from scipy import ndimage

import cv2
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)

relay = 17
red = 18
yellow = 27
green = 22
GPIO.output(relay,0)


GPIO.output(red,0)
GPIO.output(green,0)


i2c = busio.I2C(board.SCL, board.SDA, frequency=400000) # setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c) # begin MLX90640 with I2C comm
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_1_HZ # set refresh rate
mlx_shape = (24,32) # mlx90640 shape

mlx_interp_val = 1 # interpolate # on each dimension
mlx_interp_shape = (mlx_shape[0]*mlx_interp_val,
                    mlx_shape[1]*mlx_interp_val) # new shape

fig = plt.figure(figsize=(12,9)) # start figure
ax = fig.add_subplot(111) # add subplot
fig.subplots_adjust(0.05,0.05,0.95,0.95) # get rid of unnecessary padding
# therm1 = ax.imshow(np.zeros(mlx_interp_shape),interpolation='none',
#                    cmap=plt.cm.bwr,vmin=25,vmax=45) # preemptive image
therm1 = ax.imshow(np.zeros(mlx_interp_shape),interpolation='none',
                   cmap='gray',vmin=0,vmax=255) # preemptive image
cbar = fig.colorbar(therm1) # setup colorbar
cbar.set_label('Temperature [$^{\circ}$C]',fontsize=14) # colorbar label

fig.canvas.draw() # draw figure to copy background
ax_background = fig.canvas.copy_from_bbox(ax.bbox) # copy background
fig.show() # show the figure before blitting


frame = np.zeros(mlx_shape[0]*mlx_shape[1]) # 768 pts
def plot_update():
    fig.canvas.restore_region(ax_background) # restore background
    mlx.getFrame(frame) # read mlx90640
    data_array = np.fliplr(np.reshape(frame,mlx_shape)) # reshape, flip data
    data_array = ndimage.zoom(data_array,mlx_interp_val) # interpolate
    oldr = np.max(data_array) - np.min(data_array)
    newr = 255 - 0
    newval = (((data_array - np.min(data_array)) * newr) / oldr) + 0
    img = np.asarray(newval)
    img = img.astype(float)
    intimg = img.astype(int)
    horiz = np.array([[-1, 0, 1],[-2, 0, 2], [-1, 0, 1]])
    vert = np.array([[1, 2, 1],[0, 0, 0], [-1, -2, -1]])
    horizedge = np.convolve(intimg,horiz)
    #print(intimg)
    #edges = cv2.canny(intimg,100,50)
#     plt.figure(1)
#     ax.imshow(img, cmap = 'gray')
#     print(np.size(data_array[data_array>34]))
#     if(np.size(data_array[data_array>34])> 30000):
#         print("No Mask")
#         GPIO.output(red,1)
#         GPIO.output(green,0)
#     else:
#         print("Mask")
#         GPIO.output(red,0)
#         GPIO.output(green,1)
        # around 11k for mask and 18k for no mask
#     plt.figure(2)
#     img = np.asarray(edges)
#     plt.imshow(edges,cmap = 'gray',vmin = 0, vmax = 255)
#     plt.show()
    therm1.set_array(img) # set data
    therm1.set_clim(vmin=np.min(img),vmax=np.max(img)) # set bounds
    cbar.on_mappable_changed(therm1) # update colorbar range

    ax.draw_artist(therm1) # draw new thermal image
    fig.canvas.blit(ax.bbox) # draw background
    fig.canvas.flush_events() # show the new image
    return

#def BinaryThres():
    

t_array = []
while True:
    t1 = time.monotonic() # for determining frame rate
    try:
        plot_update() # update plot
    except:
        continue
    # approximating frame rate
    t_array.append(time.monotonic()-t1)
    if len(t_array)>10:
        t_array = t_array[1:] # recent times for frame rate approx
    print('Frame Rate: {0:2.1f}fps'.format(len(t_array)/np.sum(t_array)))