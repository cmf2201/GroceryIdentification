from collections import defaultdict
import cv2
import numpy as np
from ultralytics import YOLO
import os
import json
from shapely.geometry import Polygon, Point
from raycasting import is_point_inside_polygon
from list_manager.list_manager import ListManager

os.environ['YOLO_VERBOSE'] = 'False'
model_path = r'yolo_custom_training\runs\trainv2\weights\best.pt'
# model_path = 'yolo11s.pt'
print(model_path)
# Load the YOLO11 model
model = YOLO(model_path, verbose=True)
# track apples, bananas, oranges, carrot, broccoli, donut, pizza, hot dog, sandwich, cake
# TRACKED_CLASSES = [46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56]
TRACKED_CLASSES = [0, 1]
# Ask user if it should use a video file or webcam
print("Would you like to track on webcam or video file?")
while True:
    setup_type = input("Enter 'webcam' or 'video': ").strip().lower()
    if setup_type in ['webcam', 'video']:
        break
    else:
        print("Invalid input. Please enter 'webcam' or 'video'")

def find_file(directory: str, file_name: str) -> str:
    for root, _, files in os.walk(directory):
        if file_name in files:
            return os.path.join(root, file_name)
    return ""

# if setup is video, ask for video path
if setup_type == 'video':
    # Path to the downloaded video
    video_name = input("Enter the name of the video file (default is example_video.mp4): ").strip()
    if not video_name:
        video_name = 'example_video.mp4'
    video_path = find_file(os.getcwd(), video_name)
    if video_path:
        video_name = video_path
        print(f"Absolute video path: {video_name}")
        # get video from path
        cap = cv2.VideoCapture(video_path)
    if not os.path.isfile(video_path):
        print(f"Could not find video: {video_path}")
        exit(1)

# if setup type is webcam capture a picture
if setup_type == 'webcam':
    # capture picture
    cap = cv2.VideoCapture(0)

# Store the track history
track_history = defaultdict(lambda: [])

# Load polygons from polygons.json
try:
    with open('polygons.json', 'r') as f:
        polygons = json.load(f)
        print("Polygons loaded from polygons.json")
        # print(polygons)
except FileNotFoundError:
    print("polygons.json not found, starting with empty polygons")

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # initialize the list manager with no items
        list_manager = ListManager([1, 1, 0, 0, 0])
        class_names = {0: 'apples', 1: 'bananas', 2: 'carrots', 3: 'onions', 4: 'tomatoes'}
        current_tracks = []
        # display polygon
        for polygon in polygons['cart']:
            cv2.polylines(frame, [np.array(polygon, np.int32).reshape((-1, 1, 2))], isClosed=True, color=(0, 255, 0), thickness=5)
        # Run YOLO11 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True, classes=TRACKED_CLASSES, tracker="bytetrack.yaml")
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
            track = track_history[track_id]
            track.append((float(x), float(y)))  # x, y center point
            if len(track) > 30:  # retain 30 tracks for 30 frames
                track.pop(0)

            # Draw the tracking lines
            points = np.array(track, dtype=np.int32).reshape((-1, 1, 2))
            cv2.polylines(annotated_frame, [points], isClosed=False, color=(230, 230, 230), thickness=2)

            # Calculate the bounding box center
            bbox_center = (x, y)

            # Check if the bounding box center is inside any polygon
            in_cart = False
            for polygon in polygons['cart']:
                in_cart = in_cart or is_point_inside_polygon(bbox_center, polygon)
                
            if in_cart and (track_id not in current_tracks):
                    print("Adding item to cart: ", class_names[class_id])
                    list_manager.add_item_to_cart(class_names[class_id])
            
            if track_id not in current_tracks:
                current_tracks.append(track_id)
                    

        # Display the annotated frame
        cv2.imshow("YOLO11 Tracking", annotated_frame)
        
        # Clear the terminal screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Print the cart items from listmanager
        list_manager.list_status()
        
        # Add information to quit to frame
        cv2.putText(annotated_frame, text="Press 'q' to quit", org=(0, frame.shape[0] - 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 255))

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()