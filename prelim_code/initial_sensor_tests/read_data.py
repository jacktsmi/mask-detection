import serial,time,csv,os
import numpy as np
import matplotlib.pyplot as plt

ser = serial.Serial('/dev/ttyACM0',
                    baudrate=115200)
ser.flush()
# overwrite file for saving data
datafile_name = 'test_data.csv'
if os.path.isfile(datafile_name):
    os.remove(datafile_name)
time_vec,dat_vec = [],[]
avg_samps = []
mov_avg = []
L = 35
s = 0
c = 0
while True:
    try:
        ser_bytes = ser.readline()
        try:
            decoded_bytes = (ser_bytes[0:len(ser_bytes)-2].decode("utf-8")).split(',')
        except:
            continue
        if len(decoded_bytes)!=2 or decoded_bytes[0]=='' or decoded_bytes[1]=='':
            continue
        print(decoded_bytes)
        time_vec.append(float(decoded_bytes[0]))
        dat_vec.append(float(decoded_bytes[1]))
        if len(avg_samps) < L:
            avg_samps.append(float(decoded_bytes[1]))
            s += float(decoded_bytes[1])
            c += 1
            mov_avg.append(s/c)
        else:
            s -= avg_samps.pop(0)
            avg_samps.append(float(decoded_bytes[1]))
            s += float(decoded_bytes[1])
            mov_avg.append(s/c)
        if mov_avg[-1] < 1000:
            print('PUT ON A MASK')
            break

    except KeyboardInterrupt:
        print('Keyboard Interrupt')
        break
# plotting the data and saving points with the first points as the
# temporal and distance zeros
time_min = np.min(time_vec)
dat_min = np.min(dat_vec)
with open(datafile_name,'a') as f:
    writer = csv.writer(f,delimiter=',')
    for t,x in zip(time_vec,dat_vec):
        writer.writerow([t-time_min,x-dat_min])
plt.scatter(np.arange(0,len(dat_vec)),dat_vec, label='Instantaneous Distance')
plt.plot(np.arange(0,len(dat_vec)),mov_avg, 'r-',label='Moving Average')
plt.title('Walking to the Sensor')
plt.xlabel('Sample')
plt.ylabel('Distance (mm)')
plt.legend()
plt.show()