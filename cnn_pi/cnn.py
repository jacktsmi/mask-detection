import tflite_runtime.interpreter as tflite
from PIL import Image
import glob
import numpy as np
import cv2

# Define directory paths
data_path = "./images/"
model_path = "./models/"
model_file = "custom_model.tflite"

interpreter = tflite.Interpreter(model_path=model_path + model_file)
interpreter.allocate_tensors()

print("Model loaded successfully.")

# Load test images
_, image_h, image_w, _ = interpreter.get_input_details()[0]['shape']
image_size = (image_h, image_w)

with_mask_images = []
without_mask_images = []

for filename in glob.glob('./images/with_mask/*.jpg'):
	im = Image.open(filename).resize(image_size)
	im = np.array(im, dtype=np.uint8)
	with_mask_images.append(im)

for filename in glob.glob('./images/without_mask/*.jpg'):
	im = Image.open(filename).resize(image_size)
	im = np.array(im, dtype=np.uint8)
	without_mask_images.append(im)

with_mask_images = np.array(with_mask_images)
without_mask_images = np.array(without_mask_images)

#cv2.imshow("with mask image", with_mask_images[0, :, :, :])
#cv2.waitKey(0)
#cv2.imshow("without mask image", without_mask_images[0, :, :, :])
#cv2.waitKey(0)

# Classify images
def set_input_tensor(interpreter, image):
	tensor_index = interpreter.get_input_details()[0]['index']
	input_tensor = interpreter.tensor(tensor_index)()[0]
	input_tensor[:, :] = image

def classify_image(interpreter, image, top_k=1):
	set_input_tensor(interpreter, image)
	interpreter.invoke()
	output_details = interpreter.get_output_details()[0]
	output = np.squeeze(interpreter.get_tensor(output_details['index']))

	ordered = np.argpartition(-output, top_k)
	return [(i, output[i]) for i in ordered[:top_k]]

for with_mask_image, without_mask_image in zip(with_mask_images, without_mask_images):
	with_mask_results = classify_image(interpreter, with_mask_image)
	without_mask_results = classify_image(interpreter, without_mask_image)
	print("With mask image: ", with_mask_results)
	print("Without mask image: ", without_mask_results, "\n")

