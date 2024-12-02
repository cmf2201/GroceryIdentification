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
video_path = os.path.join(script_dir, 'palace.mp4')
cap = cv2.VideoCapture(video_path)
# cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX

# Below VideoWriter object will create 
# a frame of above defined The output  
# is stored in 'filename.avi' file. 
frame_width = int(cap.get(3)) 
frame_height = int(cap.get(4)) 
size = (frame_width, frame_height)
video_output = cv2.VideoWriter('palace_demo.avi',  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         10, size) 

# Scott's ByteTrack
byteTrack = ByteTrack(0.6)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLO inference on the frame
        results: List[Results] = model.track(frame)
        
        detections = []
        for result in results:
            for box in result.boxes:
                class_name = model.names[int(box.cls)]
                confidence = box.conf
                xyxy = box.xyxy
                xywh = box.xywh
                detections.append(Detection(class_name, confidence, box.xywh))    
        byteTrack.updateTracks(detections)

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

        video_output.write(annotated_frame)

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
video_output.release()
cv2.destroyAllWindows()
