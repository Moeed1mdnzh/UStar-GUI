#  Providing the simple graphical interface here

import cv2 
import time
import numpy as np 
from helpers import draw
from configs.gui_configs import *
from inference import Inference, Result
from configs.prediction_configs import *


class Draw:
    def __init__(self):
        self.screen = np.zeros((SH, SW, 3), np.uint8)
        self.canvas = np.zeros((CH, CW, 3), np.uint8)  
        self.paint_helper = draw.Paint()
        self.graphical_helper = draw.Graphics()
        self.screen = self.paint_helper.overlap(self.screen, self.canvas)
        self.pen_size = 10
        self.pen_color = (170, 170, 170)
        self.prev_color = self.pen_color
        
    def start_drawing(self):
        screen = self.paint_helper.show_pen(self.screen, self.pen_size, self.prev_color)
        screen = self.graphical_helper.connect_colors(screen)
        screen = self.graphical_helper.show_tools(screen)
        screen = self.paint_helper.generate_button(screen, gX, gY, gX2, gY2)
        return screen
    

class Interact:
    def __init__(self):
        self.drawing = False 
        self.color_click = False
        H1, W1 = self.screen.shape[:2] 
        H2, W2 = self.canvas.shape[:2]
        self.cW1, self.cH1 = int(W1 / 2), int(H1 / 2)
        self.cW2, self.cH2 = int(W2 / 2), int(H2 / 2)
        self.tools_boxes = [(0, 0, 0) for i in range(3)]
        self.tools_pts = []
        y = 133
        for i in range(3):
            self.tools_pts.append((0, y))
            y += 164
        self.tool_times = [None, None, None]
        self.erasing = False
        self.generation_box = (0, 0, 0)
        self.generation_time = None
        self.generator = Inference(GENERATOR_PATH,
                                   MAIN_SHAPE,
                                   INPUT_SHAPE)
        
    def sliders(self):
        cv2.setTrackbarMin("Pen Size: ", "UStar", 5)
        cv2.setTrackbarMax("Pen Size: ", "UStar", 20)
        return (cv2.getTrackbarPos("Pen Size: ", "UStar"),
                cv2.getTrackbarPos("R: ", "UStar"),
                cv2.getTrackbarPos("G: ", "UStar"),
                cv2.getTrackbarPos("B: ", "UStar"))
    
    def check_events(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.check_color_choice(x, y)
            self.check_tool_choice(x, y)
            if self.check_drawing(x, y):
                cv2.circle(self.screen, (x, y), self.pen_size, self.pen_color, -1)
            self.check_generation(x, y)

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing == True: 
                if self.check_drawing(x, y):
                    cv2.circle(self.screen, (x, y), self.pen_size, self.pen_color, -1)
                
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
        
    def check_color_choice(self, x, y):
        if x <= SW+70 and x >= SW:
            if y <= SH and y >= 0:
                self.pen_color = tuple([int(i) for i in self.main_screen[y, x]])
                self.prev_color = self.pen_color
                self.color_click = True

    def check_tool_choice(self, x, y):
        if x >= 0 and x <= 64:
            if y >= 133 and y < 133+164:
                self.pen_color = self.prev_color
                self.tools_boxes[0] = (0, 255, 255)
                self.tool_times[0] = time.time()
                self.erasing = False
                self.color_click = False
            
            elif y >= 297 and y < 297+164:
                self.pen_color = (0, 0, 0)
                self.tools_boxes[1] = (0, 255, 255)
                self.tool_times[1] = time.time()
                self.erasing = True
                self.color_click = False
            
            elif y >= 461 and y < 461+164:
                self.screen = self.paint_helper.overlap(self.screen, self.canvas)
                self.tools_boxes[2] = (0, 255, 255)
                self.tool_times[2] = time.time()
                self.erasing = False
                self.color_click = False
    
    def check_generation(self, x, y):
        if x >= gX and x <= gX2:
            if y >= gY and y <= gY2:
                self.generation_time = time.time() 
                self.generation_box = (0, 255, 255)
                sample = self.main_screen[self.cH1-self.cH2: self.cH1+self.cH2,
                                          self.cW1-self.cW2: self.cW1+self.cW2]
                self.generator.prepare(sample)
                self.generator.generate()
                res = self.generator.get_outcome()
                x, y, _, _ = cv2.getWindowImageRect("UStar")
                result_screen = Result(self.screen, res, 
                                       [self.cH1, self.cH2, self.cW1, self.cW2], x, y)
                cv2.destroyWindow("UStar")
                result_screen.start()
                gui = GUI() 
                gui.start()
                
    
    def check_drawing(self, x, y):
        if x <= self.cW1+self.cW2 and x >= self.cW1-self.cW2: 
            if y <= self.cH1+self.cH2 and y >= self.cH1-self.cH2: 
                self.drawing = True
                return True 
        return False
    
    def check_color_limit(self, color):
        if sum(color) < 170:
            for i, c in enumerate(color):
                if c < 170:
                    color[i] = 170
            return True, color 
        return False, color
    
class GUI(Draw, Interact):
    def __init__(self):
        Draw.__init__(self)
        Interact.__init__(self)
        self.wait_time = 1
        
    def start(self, x=812, y=668):
        cv2.namedWindow("UStar", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("UStar", x, y)
        x, y, _, _ = cv2.getWindowImageRect("UStar")
        cv2.moveWindow("UStar", x, 0)
        cv2.createTrackbar("Pen Size: ", "UStar", 5, 20, lambda x: None)
        cv2.createTrackbar("R: ", "UStar", 0, 255, lambda x: None)
        cv2.createTrackbar("G: ", "UStar", 0, 255, lambda x: None)
        cv2.createTrackbar("B: ", "UStar", 0, 255, lambda x: None)
        cv2.setTrackbarPos("R: ", "UStar", self.pen_color[-1])
        cv2.setTrackbarPos("G: ", "UStar", self.pen_color[1])
        cv2.setTrackbarPos("B: ", "UStar", self.pen_color[0])
        PB, PG, PR = 255, 255, 255
        while True:
            self.main_screen = self.start_drawing()
            self.pen_size, R, G, B = self.sliders()
            to_warn, (R, G, B) = self.check_color_limit([R, G, B])
            if to_warn:
                self.wait_time = 2000
                cv2.putText(self.main_screen, "Choose A Brighter Color", (250, 35), cv2.FONT_HERSHEY_COMPLEX,
                            1, (0, 0, 210), 2)
            else:
                if not self.erasing:
                    if (B, G, R) != (PB, PG, PR):
                        self.color_click = False
                    if not self.color_click:
                        self.pen_color = (B, G, R)
                        self.prev_color = self.pen_color
            cv2.setMouseCallback("UStar", self.check_events)
            self.main_screen = self.paint_helper.tool_alignment(self.main_screen,
                                                                self.tools_pts,
                                                                self.tools_boxes)
            self.main_screen = self.paint_helper.button_alignment(self.main_screen,
                                                                  [(gX, gY), (gX2, gY2)],
                                                                  self.generation_box)
            cv2.imshow("UStar", self.main_screen)
            if cv2.waitKey(self.wait_time) & 0xff == ord("q"):
                quit()
            self.tools_boxes, self.tool_times = self.paint_helper.update_boxes(self.tools_boxes,
                                                                               self.tool_times)
            self.generation_box, self.generation_time = self.paint_helper.update_generation(self.generation_box,
                                                                                            self.generation_time)
            if to_warn: 
                for value, name in zip((R, G, B), ("R: ", "G: ", "B: ")):
                    cv2.setTrackbarPos(name, "UStar", value)
                    to_warn = False
            PB, PG, PR = B, G, R
            self.wait_time = 1
         
def main():
    gui = GUI() 
    gui.start()
         
if __name__ == "__main__":
    main()       
        

