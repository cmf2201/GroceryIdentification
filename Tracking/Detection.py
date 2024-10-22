from torch import Tensor
class Detection:
    def __init__(self, class_name, confidence, xyxy: Tensor, id=None):
        self.id = id
        self.class_name = class_name
        self.confidence = confidence
        # adapt xyxy to be a box of list 4x2 representing the corners
        self.box = self.makeBox(xyxy)
        self.previous = self
        self.prediction = self
        self.vel_x = 0 # store in pixels / frame (assuming it is recorded each frame)
        self.vel_y = 0 # store in pixels / frame (assuming it is recorded each frame)
    
    def __str__(self):
        return f"Detection(class_name={self.class_name}, confidence={self.confidence}, xyxy={self.xyxy})"

    def makeBox(self, xyxy: Tensor):
        xyxy_np = xyxy.numpy()[0]
        top_left = (int(xyxy_np[0]), int(xyxy_np[1]))  # top-left corner (x1, y1)
        top_right = (int(xyxy_np[2]), int(xyxy_np[1]))  # top-right corner (x2, y1)
        bottom_right = (int(xyxy_np[2]), int(xyxy_np[3]))  # bottom-right corner (x2, y2)
        bottom_left = (int(xyxy_np[0]), int(xyxy_np[3]))  # bottom-left corner (x1, y2)
        return top_left, top_right, bottom_right, bottom_left
    
    def predictNextLocation(self):
        new_x1 = self.box[0][0] + self.vel_x
        new_y1 = self.box[0][1] + self.vel_y
        new_x2 = self.box[2][0] + self.vel_x
        new_y2 = self.box[2][1] + self.vel_y
        new_xyxy = Tensor([[new_x1, new_y1, new_x2, new_y2]])
        self.prediction = Detection(class_name=self.class_name, confidence=self.confidence, xyxy=new_xyxy,id=self.id)
    
    def calculateVel(self):
        # Check differences in x locations
        # May need to consider FPS in the future
        x_difference = self.box[0][0] - self.previous.box[0][0]
        y_difference = self.box[0][1] - self.previous.box[0][1]
        return [x_difference, y_difference]
        
    
    def updateInfo(self, new_detection: 'Detection'):
        self.previous = self
        vel = self.calculateVel()
        self.vel_x = vel[0]
        self.vel_y = vel[1]
        self.class_name = new_detection.class_name
        self.confidence = new_detection.confidence
        self.box = new_detection.box
