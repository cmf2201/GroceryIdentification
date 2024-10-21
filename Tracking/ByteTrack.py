from KalmanFilter import KalmanFilter
class ByteTrack:
    def __init__(self, confidence_threshold: float, filter: KalmanFilter):
        self.confidence_threshold = confidence_threshold
        self.tracks = list()
        self.filter = filter
        self.high_confidence_detections = list()
        self.low_confidence_detections = list()
        
    def updateTracks(self, detections) -> None:
        """Updates the list of tracks within the ByteTrack object.

        Args:
            detections (Detections): List of detections from a single frame provided by camera.
        """
        
        self.sortDetections(detections)
        
        # TODO: Send each object in tracks through KalmanFilter to get predictions
        # TODO: Associate predictions with self.high_confidence_detections via IoU (see Utils.py)
        # TODO: Associate remaining predictions with self.low_confidence_detections via IoU
    
    def sortDetections(self, detections) -> None:
        for detection in detections:
            # TODO: Make detections class (or similar) that houses this information and update this appropriately.
            if detection.boxes.conf >= self.confidence_threshold:
                self.high_confidence_detections.append(detection)
            else:
                self.low_confidence_detections.append(detection)

