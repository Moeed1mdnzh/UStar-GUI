#  Creating predictions for the drawings here

import os
import cv2 
import time
import logging
import numpy as np 
import tensorflow as tf 
from helpers import draw
from helpers.utils import *
from configs.gui_configs import *

tf.get_logger().setLevel(logging.ERROR)

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
    
class Result:
    def __init__(self, screen, original, result, pts, wX, wY):
        self.screen = screen.copy()
        self.screen[pts[0]-pts[1]: pts[0]+pts[1],
                    pts[2]-pts[3]: pts[2]+pts[3]] = result
        self.original = original
        self.result = result
        self.wX, self.wY = wX, wY
        self.paint_helper = draw.Paint()
        self.color = [0, 0, 0]
        self.switch_color = False
        self.indices = [0, 1, 2]
        self.button_boxes = [(0, 0, 0) for _  in range(2)]
        self.button_times = [None, None]
        self.choice_made = False
        
    def gradient_title(self):
        if not self.switch_color:
            if self.color[self.indices[0]] != 255:
                self.color[self.indices[0]] += 5
            else:
                if self.color[self.indices[1]] != 255:
                    self.color[self.indices[1]] += 5
                else:
                    if self.color[self.indices[2]] != 255:
                        self.color[self.indices[2]] += 5
                    else: 
                        self.switch_color = True 
                        np.random.shuffle(self.indices)
        else:
            if self.color[self.indices[0]] != 0:
                self.color[self.indices[0]] -= 5
            else:
                if self.color[self.indices[1]] != 0:
                    self.color[self.indices[1]] -= 5
                else:
                    if self.color[self.indices[2]] != 0:
                        self.color[self.indices[2]] -= 5
                    else: 
                        self.switch_color = False
                        np.random.shuffle(self.indices)
    
    def check_events(self, event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                self.check_return_choice(x, y)
                self.check_save_choice(x, y)
                
    def check_return_choice(self, x, y):
        if x <= gX2+60 and x >= gX+110:
            if y <= gY2-10 and y >= gY+20:
                self.button_boxes[1] = (200, 0, 200)
                self.button_times[1] = time.time()
                self.choice_made = True
    
    def check_save_choice(self, x, y):
        if x <= gX2-110 and x >= gX-60:
            if y <= gY2-10 and y >= gY+20:
                self.button_boxes[0] = (0, 200, 0)
                self.button_times[0] = time.time()
                os.system("mkdir result")
                cv2.imwrite(os.sep.join(["result", "result.jpg"]), self.result)
                cv2.imwrite(os.sep.join(["result", "input.jpg"]), self.original)
            
    def start(self):
        cv2.namedWindow("UStar", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("UStar", 812, 478)
        cv2.moveWindow("UStar", self.wX, self.wY-95)
        while not self.choice_made:
            screen = self.paint_helper.save_button(self.screen, gX-60, gY+20, gX2-110, gY2-10)
            screen = self.paint_helper.return_button(screen, gX+110, gY+20, gX2+60, gY2-10)
            self.gradient_title()
            cv2.setMouseCallback("UStar", self.check_events)
            cv2.putText(screen, "Your Imaginary Star", (270, 70), cv2.FONT_HERSHEY_TRIPLEX,
                        1.0, self.color, 2)
            screen = self.paint_helper.button_alignment(screen,
                                                             [(gX-60, gY+20), (gX2-110, gY2-10)],
                                                             self.button_boxes[0])
            screen = self.paint_helper.button_alignment(screen,
                                                             [(gX+110, gY+20), (gX2+60, gY2-10)],
                                                             self.button_boxes[1])
            cv2.imshow("UStar", screen)
            if cv2.waitKey(1) == ord("q"):
                quit()
            self.button_boxes[0], self.button_times[0] = self.paint_helper.update_button(self.button_boxes[0],
                                                                                         self.button_times[0])
            self.button_boxes[1], self.button_times[1] = self.paint_helper.update_button(self.button_boxes[1],
                                                                                         self.button_times[1])
        cv2.destroyWindow("UStar")
        
