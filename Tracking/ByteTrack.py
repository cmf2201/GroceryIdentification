from Detection import Detection
import Utils
class ByteTrack:
    def __init__(self, confidence_threshold: float):
        self.confidence_threshold = confidence_threshold
        self.velocity_threshold = 1.0
        self.tracks: list[Detection] = []
        self.high_confidence_detections = list()
        self.low_confidence_detections = list()
        
    def updateTracks(self, detections: list[Detection]) -> None:
        """Updates the list of tracks within the ByteTrack object.

        Args:
            detections (Detections): List of detections from a single frame provided by camera.
        """
        self.sortDetections(detections)
        matched_tracks: list[Detection] = []
        
        ## Association #1 with high confidence detections ##
        for track in self.tracks:
            # Set the prediction of the track to compare with new detections.
            track.predictNextLocation()
            
            best_detection_match = None
            best_iou = 0.0
            for detection in self.high_confidence_detections:
                iou_value = Utils.computeIoU(track.prediction.box, detection.box)
                if iou_value > best_iou:
                    best_iou = iou_value
                    best_detection_match = detection
            if best_detection_match is None:
                continue
            
            # We want to keep track of all tracks that had good match. We temporarily remove the 
            # matched track from self.tracks to prevent it from attempting to match with
            # the low confidence matches. matched_tracks will become self.tracks at the end of
            # this method.
            self.tracks.remove(track)
            track.updateInfo(best_detection_match)
            matched_tracks.append(track)
            
            # We remove this from the high detections to prevent the matched detection from
            # attempting to match with other tracks.
            self.high_confidence_detections.remove(best_detection_match)
        
        ## Association #2 with low confidence detections ##
        for track in self.tracks:
            best_detection_match = None
            best_iou = 0.0
            for detection in self.low_confidence_detections:
                # TODO: Update with proper types
                iou_value = Utils.computeIoU(track.prediction.box, detection.box)
                if iou_value > best_iou:
                    best_iou = iou_value
                    best_detection_match = detection
            if best_detection_match is None:
                continue
            self.tracks.remove(track)
            track.updateInfo(best_detection_match)
            matched_tracks.append(track)
            self.low_confidence_detections.remove(best_detection_match)
        
        # These are all the remaining tracks that did not find a match. This could be due to
        # occlusion or the object being removed from the camera's frame.
        remaining_tracks = self.tracks
        
        # After everything has found a match from IoU, make the matched_tracks the list of tracks.
        self.tracks = matched_tracks
        
        # Add remaining self.high_confidence_detections to tracks as new tracked objects.
        for remaining_detection in self.high_confidence_detections:
            self.tracks.append(remaining_detection)
        
        # If a previous track wasn't matched, but has a low velocity, then we assume that the track was
        # just fully occluded, so we should still know about it. If it had a higher velocity, then we 
        # assume that a person removed the object from the cart.
        for track in remaining_tracks:
            if track.vel_x <= self.velocity_threshold and track.vel_y <= self.velocity_threshold:
                self.tracks.append(track)
    
    def sortDetections(self, detections: list[Detection]) -> None:
        for detection in detections:
            # TODO: Make detections class (or similar) that houses this information and update this appropriately.
            if detection.confidence >= self.confidence_threshold:
                self.high_confidence_detections.append(detection)
            else:
                self.low_confidence_detections.append(detection)
