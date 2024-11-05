"""
This file is used to run a YOLO object detection model on any given .png photo file
To use this file:
1. Run the file
2. Enter the model name (default is 'yolo11s.pt')
3. Enter the name of the ohoto file
4. The photo will open and the YOLO model will run on the photo
"""
import os
from typing import List
import cv2
import numpy as np
import requests
from ultralytics import YOLO
from ultralytics.engine.results import Results


model_name = input("Enter the model name (default is 'yolo11s.pt'): ").strip()
if not model_name:
    model_name = 'yolo11s.pt'
# Download the YOLO model
def find_file(directory: str, file_name: str) -> str:
    for root, _, files in os.walk(directory):
        if file_name in files:
            return os.path.join(root, file_name)
    return ""

model_path = find_file(os.getcwd(), model_name)
if model_path:
    model_name = model_path
    print(f"Absolute model weights path: {model_name}")
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

# Path to the downloaded video
photo_name = input("Enter the name of the photo file: ").strip()
if not photo_name:
    photo_name = 'example_photo.png'
photo_path = find_file(os.getcwd(), photo_name)
if photo_path:
    photo_name = photo_path
    print(f"Absolute photo path: {photo_name}")
if not os.path.isfile(photo_path):
    print(f"Could not find photo: {photo_path}")
    exit(1)

# capture video
cap = cv2.VideoCapture(photo_path)
font = cv2.FONT_HERSHEY_SIMPLEX

# Read a frame from photo
success, frame = cap.read()
while True:
    if success:
        # Run YOLO inference on the frame
        results: List[Results] = model(frame)

        # Visualize the results on the frame
        annotated_frame: np.ndarray = results[0].plot()

        # Add information to quit to frame
        cv2.putText(annotated_frame, text="Press 'q' to quit", org=(0, frame.shape[0] - 10), fontFace=font, fontScale=0.5, color=(0, 0, 255))

        # Display the annotated frame
        cv2.imshow("YOLO Inference", annotated_frame)

        # Add information to quit to frame
        cv2.putText(annotated_frame, text="Press 'q' to quit", org=(0, frame.shape[0] - 10), fontFace=font, fontScale=0.5, color=(0, 0, 255))

        # Break stop displaying image if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            # Release the video capture object and close the display window
            cap.release()
            cv2.destroyAllWindows()
            break