from collections import defaultdict
import json
import string
import cv2
import numpy as np
from ultralytics import YOLO
from list_manager.list_manager import ListManager
from raycasting import is_point_inside_polygon


class groceryAssistant:
    def __init__(self, model_path: string, TRACKED_CLASSES: list[int], setup_type: string, shopping_list: list[int]):
        # Load the YOLO11 model
        self.model = YOLO(model_path, verbose=True)
        self.TRACKED_CLASSES = TRACKED_CLASSES
        # setup cap based on setup_type
        if setup_type == 'video':
            video_path = 'C:\Users\bmanw\GroceryIdentification\yolo_custom_training\example_video.mp4'
            self.cap = cv2.VideoCapture(video_path)
        else: 
            #capture picture
            self.cap = cv2.VideoCapture(0)
        # Store the track history
        
        self.track_history = defaultdict(lambda: [])
        self.last_seen = {}
        self.current_tracks = []
        self.max_frames_missing = 30  # Number of frames to wait before removing a track
        
        # Load polygons from polygons.json
        try:
            with open('polygons.json', 'r') as f:
                self.polygons = json.load(f)
                print("Polygons loaded from polygons.json")
                # print(polygons)
        except FileNotFoundError:
            print("polygons.json not found, starting with empty polygons")
            
        self.list_manager = ListManager(shopping_list)
        
        self.class_names = {
                47: 'apples', 
                46: 'bananas', 
                49: 'oranges', 
                48: 'carrots', 
                50: 'broccoli', 
                52: 'pizza', 
                53: 'hot dog', 
                54: 'sandwich', 
                55: 'cake'
                }
    
    def run(self):
        # Loop through the video frames
        frame_count = 0
        while self.cap.isOpened():
            # Read a frame from the video
            success, frame = self.cap.read()
            if frame is None:
                break
            # Get the screen resolution
            screen_width = 1920 
            screen_height = 1080  

            # Calculate the scaling factor
            scale_width = screen_width / frame.shape[1]
            scale_height = (screen_height - 200) / frame.shape[0]  # Subtract some pixels for the text
            scale = min(scale_width, scale_height)

            # Resize the image
            frame = cv2.resize(frame, None, fx=scale, fy=scale)

            if success:
                # display polygon
                for polygon in self.polygons['cart']:
                    cv2.polylines(frame, [np.array(polygon, np.int32).reshape((-1, 1, 2))], isClosed=True, color=(0, 255, 0), thickness=5)
                # Run YOLO11 tracking on the frame, persisting tracks between frames
                results = self.model.track(frame, persist=True, classes=self.TRACKED_CLASSES, tracker="bytetrack.yaml", conf=0.35)
                # Get the boxes, track IDs, and class IDs
                boxes = results[0].boxes.xywh.cpu()
                track_ids = results[0].boxes.id
                class_ids = results[0].boxes.cls
                if track_ids is not None:
                    track_ids = track_ids.int().cpu().tolist()
                else:
                    track_ids = []
                if class_ids is not None:
                    class_ids = class_ids.int().cpu().tolist()
                else:
                    class_ids = []
                    
                # Visualize the results on the frame
                annotated_frame = results[0].plot()

                # Plot the tracks
                for box, track_id, class_id in zip(boxes, track_ids, class_ids):
                    x, y, w, h = box
                    track = self.track_history[track_id]
                    track.append((float(x), float(y)))  # x, y center point
                    if len(track) > 30:  # retain 30 tracks for 30 frames
                        track.pop(0)

                    # Draw the tracking lines
                    # points = np.array(track, dtype=np.int32).reshape((-1, 1, 2))
                    # cv2.polylines(annotated_frame, [points], isClosed=False, color=(230, 230, 230), thickness=2)

                    # Calculate the bounding box center
                    bbox_center = (x, y)

                    # Check if the bounding box center is inside any polygon
                    in_cart = False
                    for polygon in self.polygons['cart']:
                        in_cart = in_cart or is_point_inside_polygon(bbox_center, polygon)
                                    
                    if in_cart and (track_id not in self.current_tracks):
                            print("Adding item to cart: ", self.class_names[class_id])
                            self.list_manager.add_item_to_cart(self.class_names[class_id])
                    
                    if track_id not in self.current_tracks:
                        # print("adding", track_id, "To current tracks")
                        self.current_tracks.append(track_id)
                    
                    self.last_seen[track_id] = (frame_count, class_id)
                
                # Remove tracks that have not been seen for a while
                for track_id in list(self.last_seen.keys()):
                    if frame_count - self.last_seen[track_id][0] > self.max_frames_missing:
                        class_id = self.last_seen[track_id][1]
                        if class_id is not None:
                            print("Removing item from cart: ", self.class_names[class_id])
                            self.list_manager.remove_item_from_cart(self.class_names[class_id])
                        self.current_tracks.remove(track_id)
                        del self.last_seen[track_id]
                        
                # Add information to quit to frame
                cv2.putText(annotated_frame, text="Press 'q' to quit", org=(0, frame.shape[0] - 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 255))

                # Display the annotated frame
                cv2.imshow("YOLO11 Tracking", annotated_frame)
                
                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    # Release the video capture object and close the display window
                    self.cap.release()
                    cv2.destroyAllWindows()
                    break
            frame_count += 1
                