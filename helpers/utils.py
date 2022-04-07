import cv2 
import numpy as np 

def normalize(image):
    return (image.astype("float32")-127.5)/127.5

def denormalize(image):
    return np.uint8(((image+1.0)/2.0)*255.0)

def convert_channel(image, code):
    return cv2.cvtColor(image, code) 

def resize(image, size):
    return cv2.resize(image, size[:2])