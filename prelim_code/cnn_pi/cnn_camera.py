import tflite_runtime.interpreter as tflite
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
from PIL import Image
import io
import cv2

def set_input_tensor(interpreter, image):
	tensor_index = interpreter.get_input_details()[0]['index']
	input_tensor = interpreter.tensor(tensor_index)()[0]
	input_tensor[:, :] = image

def classify_image(interpreter, image, top_k=1):
	set_input_tensor(interpreter, image)
	interpreter.invoke()
	output_details = interpreter.get_output_details()[0]
	output = np.squeeze(interpreter.get_tensor(output_details['index']))
	print(output)

	if output_details['dtype'] == np.uint8:
		scale, zero_point = output_details['quantization']
		output = scale * (output - zero_point)

	ordered = np.argpartition(-output, top_k)
	return [(i, output[i]) for i in ordered[:top_k]]

def main():
	model_filename = 'MobileNetV2.tflite'
	model_path = './models/' + model_filename

	interpreter = tflite.Interpreter(model_path=model_path)
	interpreter.allocate_tensors()
	_, image_h, image_w, _ = interpreter.get_input_details()[0]['shape']


	face_cascade = cv2.CascadeClassifier('haarcascade_frontal_face_default.xml')
	eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
	with PiCamera(resolution=(640, 480), framerate=15) as camera:
		raw_capture = PiRGBArray(camera, size=(640, 480))
		for frame in camera.capture_continuous(raw_capture, format="rgb", use_video_port=True):
			image = frame.array
			cv2.imshow("Raw image", image)

			key = cv2.waitKey(1)
			raw_capture.truncate(0)

			if key == ord("q"):
				break
			elif key == ord("c"):
				image_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
				#cv2.imshow("Before", image)
				image_v = image_hsv[:,:,2]
				image_v[image_v < (255. / 5.)] = 5 * image_v[image_v < (255. / 5.)] # np.minimum(np.floor(5 * image_hsv[:, :, 2]), 255).astype(np.uint8)
				image_hsv[:,:,2] = image_v
				image2 = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2RGB)
				#cv2.imshow("After", image2)
				#image_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
				#cv2.imshow("Gray", image_gray)
				#faces = face_cascade.detectMultiScale(image_gray, 1.1, 4)
				#print(faces)
				#for (x, y, w, h) in faces:
				#	cv2.rectangle(image2, (x, y), (x+w, y+h), (255, 255, 0), 2)

				#cv2.imshow("Face detection", image2)

				image2 = cv2.resize(image2, (image_h, image_w))
				#cv2.imshow("Input to CNN", image2)
				results = classify_image(interpreter, image2)
				print(results)

if __name__ == '__main__':
	main()
