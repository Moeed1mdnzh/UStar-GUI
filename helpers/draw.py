import os
import cv2
import time
import numpy as np 

class Paint:
        
    def overlap(self, screen_1, screen_2, size=10):
        H1, W1 = screen_1.shape[:2] 
        H2, W2 = screen_2.shape[:2]
        cW1, cH1 = int(W1 / 2), int(H1 / 2)
        cW2, cH2 = int(W2 / 2), int(H2 / 2)
        clone = screen_1.copy()
        clone[cH1-cH2: cH1+cH2, cW1-cW2: cW1+cW2] = screen_2
        return cv2.rectangle(clone, 
                      (cW1-cW2-size, cH1-cH2-size),
                      (cW1+cW2+size, cH1+cH2+size), 
                      (255, 255, 255), 2)
        
    def show_pen(self, screen, size, color):
        clone = screen.copy()
        return cv2.circle(clone, (30, 45), size, color, -1)
    
    def generate_button(self, screen, x, y, x2, y2):
        clone = screen.copy()
        cv2.rectangle(clone, (x, y), (x2, y2), (0, 255, 255), 3)
        cv2.putText(clone, "Generate", (x+18, y+45), cv2.FONT_HERSHEY_SIMPLEX,
                    1.1, (255, 255, 255), 2)
        return clone
    
    def tool_alignment(self, screen, pts, colors):
        clone = screen.copy()
        for pt, color in zip(pts, colors):
            if color != (0, 0, 0):
                cv2.rectangle(clone, pt, (pt[0]+64, pt[1]+64), color, 2)
        return clone
    
    def update_boxes(self, boxes, times):
        for i, t in enumerate(times):
            if t is not None:
                if 0.1 <= time.time()-t:
                    boxes[i] = (0, 0, 0)
                    times[i] = None 
        return boxes, times
    
    def generation_alignment(self, screen, pt, color):
        clone = screen.copy()
        if color != (0, 0, 0):
            cv2.rectangle(clone, pt[0], pt[1], color, -1)
        return clone
    
    def update_generation(self, box, t):
        if t is not None:
            if 0.1 <= time.time()-t:
                box = (0, 0, 0)
                t = None
        return box, t
                 
        

class Graphics:
    def __init__(self):
        self.rgb_path = os.sep.join(["helpers", "colors2.jpg"])
        self.tool_images = []
        for name in ["brush", "eraser"]:
            image = cv2.imread(os.sep.join(["helpers", name])+".jpg")
            self.tool_images.append(image)
        self.tool_images.append(None)
        
    def connect_colors(self, screen):
        colors = cv2.imread(self.rgb_path)
        return np.hstack([screen, colors])
    
    def show_tools(self, screen_1):
        clone = screen_1.copy()
        y = 133
        for image in self.tool_images:
            if y != 461:
                clone[y: y+64, 0: 64] = image 
            else:
                cv2.putText(clone, "C", (16, y+45), cv2.FONT_HERSHEY_TRIPLEX, 1.2, (215, 215, 0))
            y += 164
        return clone
