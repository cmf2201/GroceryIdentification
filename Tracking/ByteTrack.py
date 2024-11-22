from Detection import Detection
import Utils
import copy
from KalmanFilter import KalmanFilter
class ByteTrack:
    def __init__(self, confidence_threshold: float):
        self.confidence_threshold = confidence_threshold
        self.velocity_threshold = 1.0
        self.tracks: list[Detection] = []
        self.id_count = 0
        
    def updateTracks(self, detections: list[Detection]) -> None:
        """Updates the list of tracks within the ByteTrack object.

        Args:
            detections (Detections): List of detections from a single frame provided by camera.
        """
        high_confidence_detections: list[Detection] = list()
        low_confidence_detections: list[Detection] = list()
        for detection in detections:
            if detection.confidence >= self.confidence_threshold:
                high_confidence_detections.append(detection)
            else:
                low_confidence_detections.append(detection)
        
        matched_tracks: list[Detection] = []
        unmatched_tracks = copy.copy(self.tracks)
        
        ## Association #1 with high confidence detections ##
        for track in unmatched_tracks:
            # Set the prediction of the track to compare with new detections.
            track.filter.predict()
            track.prediction = track.makeBox(track.filter.predict_x[0:4])
            # predicted_xywh = track.filter.x[0:4]
            # predicted_box_corners = track.makeBox(predicted_xywh)
            
            best_detection_match = None
            best_iou = 0.0
            for detection in high_confidence_detections:
                iou_value = Utils.computeIoU(track.prediction, detection.box_corners)
                if iou_value > best_iou:
                    best_iou = iou_value
                    best_detection_match = detection
            if best_detection_match is None:
                continue
            
            # We want to keep track of all tracks that had good match. We temporarily remove the 
            # matched track from self.tracks to prevent it from attempting to match with
            # the low confidence matches. matched_tracks will become self.tracks at the end of
            # this method.
            track.updateInfo(best_detection_match)
            matched_tracks.append(track)
            
            # We remove this from the high detections to prevent the matched detection from
            # attempting to match with other tracks.
            high_confidence_detections.remove(best_detection_match)
        unmatched_tracks = [track for track in unmatched_tracks if track not in matched_tracks]
        
        ## Association #2 with low confidence detections ##
        for track in unmatched_tracks:
            best_detection_match = None
            best_iou = 0.0
            for detection in low_confidence_detections:
                iou_value = Utils.computeIoU(track.prediction, detection.box_corners)
                if iou_value > best_iou:
                    best_iou = iou_value
                    best_detection_match = detection
            
            if best_detection_match is None:
                continue
            
            track.updateInfo(best_detection_match)
            matched_tracks.append(track)
            low_confidence_detections.remove(best_detection_match)
            
        unmatched_tracks = [track for track in unmatched_tracks if track not in matched_tracks]
        
        # Add remaining self.high_confidence_detections to tracks as new tracked objects.
        # If a new track is added, lets add a Kalman Filter to start running predictions
        for remaining_detection in high_confidence_detections:
            self.id_count += 1
            remaining_detection.id = self.id_count
            state = Utils.detectionToState(remaining_detection)
            remaining_detection.filter = KalmanFilter(state)
            matched_tracks.append(remaining_detection)
        
        for track in unmatched_tracks:
            if track.frames_since_previous_detection <= 10:
                track.frames_since_previous_detection += 1
                matched_tracks.append(track)
                
        
        # After everything has found a match from IoU, make the matched_tracks the list of tracks.
        self.tracks = matched_tracks
        
