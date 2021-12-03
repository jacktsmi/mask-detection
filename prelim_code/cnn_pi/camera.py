from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import cv2
from matplotlib import pyplot as plt

def capture_images(filename):
	# Initialize objects for continuous image capture
	camera = PiCamera()
	image_size = (640, 480)
	camera.resolution = image_size
	camera.framerate = 32
	raw_capture = PiRGBArray(camera, size=image_size)

	# Continuous camera capture; only take a picture and plot image when "c" is pressed
	sleep(0.1)
	filename_num = 1
	for frame in camera.capture_continuous(raw_capture, format="rgb", use_video_port=True):
		image = frame.array # Get image from frame
		cv2.imshow("Raw Image", image)

		key = cv2.waitKey(1) & 0xFF # Press key
		raw_capture.truncate(0) # Clear buffer

		if key == ord("q"):
			break
		elif key == ord("c"):
			camera.capture(filename + '_' + str(filename_num) + '.jpg')
			plt.imshow(image)
			plt.show()
			filename_num = filename_num + 1


def main():
	filename = 'with_mask'
	dir = 'images/' + filename + '/'
	capture_images(dir + filename)

if __name__ == '__main__':
	main()
