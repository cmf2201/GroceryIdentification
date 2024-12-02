"""
This file is used to run a YOLO object detection model in real time on your webcam
To use this file:
1. Run the file
2. Enter the model name (default is 'yolo11s.pt')
3. The webcam will open and the YOLO model will run on the video frames
"""
import os
from typing import List
import cv2
import numpy as np
import requests
from ultralytics import YOLO
from ultralytics.engine.results import Results
from Tracking.ByteTrack import ByteTrack
from Tracking.Detection import Detection
import matplotlib.pyplot as plt
from list_manager.list_manager import ListManager

TRACKED_CLASSES = [46, 47, 48, 49, 50, 52, 53, 54, 55, 56]
current_tracks = []
# initialize the list manager with shopping list of 2 apples, 1 banana, 1 orange
list_manager = ListManager([2, 1, 0, 0, 1])
# class_names = {0: 'apples', 1: 'bananas', 2: 'carrots', 10: 'onions'}
class_names = {
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

model_name = input("Enter the model name (default is 'yolo11s.pt'): ").strip()
if not model_name:
    model_name = 'yolo11s.pt'
# Download the YOLO model
def find_model_file(directory: str, model_name: str) -> str:
    for root, _, files in os.walk(directory):
        if model_name in files:
            return os.path.join(root, model_name)
    return ""

model_path = find_model_file(os.getcwd(), model_name)
if model_path:
    model_name = model_path
if not os.path.isfile(model_name):
    print(f'{model_name} does not exist. Downloading...')
    download_url = 'https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt'

    response = requests.get(download_url)

    if response.status_code == 200:
        with open(model_name, 'wb') as file:
            file.write(response.content)
        print(f'Downloaded {model_name}')
    else:
        print(f'Failed to download {model_name}')

# Load the YOLO model
model: YOLO = YOLO(model_name)

# capture video
script_dir = os.path.dirname(os.path.abspath(__file__))
video_path = os.path.join(script_dir, 'Banana.MOV')
# video_path = os.path.join(script_dir, 'TwoBananasStill.MOV')
# video_path = os.path.join(script_dir, 'TwoBananasMoving.MOV')
# video_path = os.path.join(script_dir, 'palace.mp4')
cap = cv2.VideoCapture(video_path)
# cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX

# Below VideoWriter object will create 
# a frame of above defined The output  
# is stored in 'filename.avi' file. 
frame_width = int(cap.get(3)) 
frame_height = int(cap.get(4)) 
size = (frame_width, frame_height)
# video_output = cv2.VideoWriter('palace_demo.avi',  
#                          cv2.VideoWriter_fourcc(*'MJPG'), 
#                          10, size) 

# Scott's ByteTrack
byteTrack = ByteTrack(0.6)

# Loop through the video frames
frames = 0
frames_plot = []
track_x = []
track_y = []
track_w = []
track_h = []
while cap.isOpened() and frames < 500:
    frames += 1
    
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLO inference on the frame
        results = model.track(frame, persist=True, classes=TRACKED_CLASSES, tracker="bytetrack.yaml", conf=0.35)
        
        detections = []
        for result in results:
            for box in result.boxes:
                class_name = model.names[int(box.cls)]
                confidence = box.conf
                xyxy = box.xyxy
                xywh = box.xywh
                track_x.append(xywh[0,0].item())
                track_y.append(xywh[0,1].item())
                track_w.append(xywh[0,2].item())
                track_h.append(xywh[0,3].item())
                detections.append(Detection(class_name, confidence, box.xywh))
                frames_plot.append(frames)
        # byteTrack.updateTracks(detections)

        # Visualize the results on the frame
        # annotated_frame: np.ndarray = results[0].plot()
        annotated_frame = frame
        cv2.putText(annotated_frame, f"Number of Tracks: {len(byteTrack.tracks)}", (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 2)
        for object in byteTrack.tracks:
            top_left = object.box_corners[0]  # Convert top-left corner to tuple
            bottom_right = object.box_corners[2]  # Convert bottom-right corner to tuple
            cv2.rectangle(annotated_frame, top_left, bottom_right, object.color, thickness=3)
            
            # # I want to see the accuracy of the prediction
            # top_left_prediction = object.prediction[0]  # Convert top-left corner to tuple
            # bottom_right_prediction = object.prediction[2]  # Convert bottom-right corner to tuple
            # cv2.rectangle(annotated_frame, top_left_prediction, bottom_right_prediction, object.color, thickness=1)
            
            # Drawing the text on the box
            text = f"Class: {object.class_name}, ID: {object.id}, Confidence: {object.confidence}"
            font = cv2.FONT_HERSHEY_COMPLEX_SMALL
            size, _ = cv2.getTextSize(text, font, 1, 1)
            text_w, text_h = size
            pos = (top_left[0], top_left[1] - text_h)
            cv2.rectangle(annotated_frame, pos, (pos[0] + text_w, pos[1] + text_h), (0, 0, 0), -1)
            cv2.putText(annotated_frame, text, (top_left[0], top_left[1]),
                        font, 1, (200,200,200), thickness=1)

        # Add information to quit to frame
        cv2.putText(annotated_frame, text="Press 'q' to quit", org=(0, frame.shape[0] - 10), fontFace=font, fontScale=0.5, color=(0, 0, 255))

        # video_output.write(annotated_frame)

        # Display the annotated frame
        cv2.imshow("YOLO Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
# video_output.release()
cv2.destroyAllWindows()

# Number of indices (assuming 12 indices)
num_indices = 4

# Custom titles for each subplot (you can adjust this list)
custom_titles = [
    "Position X", "Position Y", "Width", "Height",
    "Velocity X", "Velocity Y", "Velocity Width", "Velocity Height",
    "Acceleration X", "Acceleration Y", "Acceleration Width", "Acceleration Height"
]

data = [track_x, track_y, track_w, track_h]

# Create a figure and axes with 3 rows and 4 columns
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Flatten the 2D array of axes for easier iteration
axes = axes.flatten()

# Loop over each object in byteTrack.tracks
for _ in range(0, 1):
    # Loop over the indices (0 to 11)
    for i in range(num_indices):
        # Get the state and prediction data for the i-th index
        # state = obj.filter.state_data[i]
        # prediction = obj.filter.prediction_data[i]
        
        # Plot state and prediction data on the corresponding subplot
        ax = axes[i]
        # ax.plot(obj.filter.steps, state, color='blue', label='State')
        # ax.plot(obj.filter.steps, prediction, color='red', label='Prediction')
        ax.plot(frames_plot, data[i], color='black', label='YOLOv11 ByteTrack')

        # Set the custom title and labels
        ax.set_title(custom_titles[i])
        ax.set_xlabel('Steps')
        ax.set_ylabel('Value')
        
        # Optionally, add a legend
        if i == 0:  # Only add legend once
            ax.legend()

    # Adjust layout for better spacing
    plt.tight_layout()

    # Show the plot
    plt.show()

