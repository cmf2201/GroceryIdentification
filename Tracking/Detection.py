class Detection:
    def __init__(self, class_name, confidence, xyxy):
        self.class_name = class_name
        self.confidence = confidence
        self.xyxy = xyxy
    def __str__(self):
        return f"Detection(class_name={self.class_name}, confidence={self.confidence}, xyxy={self.xyxy})"