#  Creating predictions for the drawings here

import os
import cv2 
import numpy as np 
import tensorflow as tf 
from helpers.utils import *

class Inference:
    def __init__(self, generator_path, original_shape, sample_shape):
        self.original_shape = original_shape
        self.sample_shape = sample_shape
        self.sample = None
        self.pred = None
        self.generator = tf.keras.models.load_model(generator_path)
        
    def prepare(self, sample):
        sample = resize(sample, self.sample_shape)
        sample = convert_channel(sample, cv2.COLOR_BGR2RGB)
        sample = normalize(sample.reshape(-1, *self.sample_shape))
        self.sample = sample.copy()
    
    def generate(self):
        pred = self.generator.predict(self.sample)
        self.sample = None 
        self.pred = pred
    
    def get_outcome(self, auto_resize=True):
        pred = denormalize(self.pred.squeeze())
        pred = convert_channel(pred, cv2.COLOR_RGB2BGR)
        if auto_resize:
            pred = resize(pred, self.original_shape)
        return pred
