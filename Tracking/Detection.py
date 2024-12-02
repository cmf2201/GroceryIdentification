from torch import Tensor
import numpy as np
from functools import singledispatchmethod
from Tracking.KalmanFilter import KalmanFilter
import random
import Tracking.Utils as Utils
class Detection:
    def __init__(self, class_name, confidence:Tensor, xywh: Tensor, id=None):
        self.id = id
        self.class_name = class_name
        self.confidence = confidence.item()
        xywh_np = xywh.numpy()[0]
        self.x = int(xywh_np[0])
        self.y = int(xywh_np[1])
        self.width = int(xywh_np[2])
        self.height = int(xywh_np[3])
        self.box_corners = self.makeBox(xywh)
        self.previous = self
        self.frames_since_previous_detection = 0
        self.prediction = [(0,0), (1,1), (2,2), (3,3)]
        self.filter: KalmanFilter = None
        self.vel_x = 0 # store in pixels / frame (assuming it is recorded each frame)
        self.vel_y = 0 # store in pixels / frame (assuming it is recorded each frame)
        self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    
    def __str__(self):
        return f"Detection(class_name={self.class_name}, confidence={self.confidence}, xywh={(self.x, self.y, self.width, self.height)})"
    
    def __eq__(self, other: 'Detection'):
        return self.x == other.x and self.y == other.y and self.class_name == other.class_name

    # def makeBox(self, xywh):
    #     xywh_np = xywh.numpy()[0]
    #     top_left = (int(xywh_np[0]-xywh_np[2]/2), int(xywh_np[1]-xywh_np[3]/2))  # top-left corner (x1, y1)
    #     top_right = (int(xywh_np[0]+xywh_np[2]/2), int(xywh_np[1]-xywh_np[3]/2))   # top-right corner (x2, y1)
    #     bottom_right = (int(xywh_np[0]+xywh_np[2]/2), int(xywh_np[1]+xywh_np[3]/2))   # bottom-right corner (x2, y2)
    #     bottom_left = (int(xywh_np[0]-xywh_np[2]/2), int(xywh_np[1]+xywh_np[3]/2))   # bottom-left corner (x1, y2)
    #     return top_left, top_right, bottom_right, bottom_left
    
    def makeBox(self, xywh):
        if isinstance(xywh, Tensor):
            xywh = xywh.numpy()[0]
        top_left = (int(xywh[0]-xywh[2]/2), int(xywh[1]-xywh[3]/2))  # top-left corner (x1, y1)
        top_right = (int(xywh[0]+xywh[2]/2), int(xywh[1]-xywh[3]/2))   # top-right corner (x2, y1)
        bottom_right = (int(xywh[0]+xywh[2]/2), int(xywh[1]+xywh[3]/2))   # bottom-right corner (x2, y2)
        bottom_left = (int(xywh[0]-xywh[2]/2), int(xywh[1]+xywh[3]/2))   # bottom-left corner (x1, y2)
        return top_left, top_right, bottom_right, bottom_left
    
    def predictNextLocation(self):
        new_x1 = self.box_corners[0][0] + self.vel_x
        new_y1 = self.box_corners[0][1] + self.vel_y
        new_x2 = self.box_corners[2][0] + self.vel_x
        new_y2 = self.box_corners[2][1] + self.vel_y
        new_xyxy = Tensor([[new_x1, new_y1, new_x2, new_y2]])
        # self.prediction = Detection(class_name=self.class_name, confidence=self.confidence, xyxy=new_xyxy,id=self.id)
        self.prediction = self
    
    def calculateVel(self):
        # Check differences in x locations
        # May need to consider FPS in the future
        x_difference = self.box_corners[0][0] - self.previous.box_corners[0][0]
        y_difference = self.box_corners[0][1] - self.previous.box_corners[0][1]
        return [x_difference, y_difference]
        
    
    def updateInfo(self, new_detection: 'Detection'):
        self.previous = self
        vel = self.calculateVel()
        self.vel_x = vel[0]
        self.vel_y = vel[1]
        self.class_name = new_detection.class_name
        self.confidence = new_detection.confidence
        self.box_corners = new_detection.box_corners
        self.x = new_detection.x
        self.y = new_detection.y
        self.width = new_detection.width
        self.height = new_detection.height
        measurement = Utils.detectionToMeasurement(new_detection)
        self.filter.update(measurement)
