from collections import defaultdict
import cv2
import numpy as np
from ultralytics import YOLO
import os

# Load the YOLO11 model
model = YOLO("yolo11n.pt")
# track apples, bananas, oranges, carrot, broccoli, donut, pizza, hot dog, sandwich, cake
TRACKED_CLASSES = [46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56]

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

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLO11 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True, classes=TRACKED_CLASSES, tracker="bytetrack.yaml")
        # Get the boxes and track IDs
        boxes = results[0].boxes.xywh.cpu()
        track_ids = results[0].boxes.id
        if track_ids is not None:
            track_ids = track_ids.int().cpu().tolist()
        else:
            track_ids = []
            
            
        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Plot the tracks
        for box, track_id in zip(boxes, track_ids):
            x, y, w, h = box
            track = track_history[track_id]
            track.append((float(x), float(y)))  # x, y center point
            if len(track) > 30:  # retain 30 tracks for 30 frames
                track.pop(0)

            # Draw the tracking lines
            points = np.array(track, dtype=np.int32).reshape((-1, 1, 2))
            cv2.polylines(annotated_frame, [points], isClosed=False, color=(230, 230, 230), thickness=2)

        # Display the annotated frame
        cv2.imshow("YOLO11 Tracking", annotated_frame)
        
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