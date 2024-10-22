import os
from typing import List
import cv2
import numpy as np
import requests
from ultralytics import YOLO
from ultralytics.engine.results import Results
from Detection import Detection
from ByteTrack import ByteTrack

model_name = 'yolo11n.pt'
# Download the YOLO model
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
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX

# Start ByteTrack
byteTrack = ByteTrack(0.6)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLO inference on the frame
        results: List[Results] = model(frame)
               
        # Create detection classes for ByteTrack
        detections = []
        for box in results[0].boxes:
            class_name = model.names[int(box.cls)]
            confidence = box.conf
            xyxy = box.xyxy
            center = box.xywh
            detections.append(Detection(class_name, confidence, xyxy))
        byteTrack.updateTracks(detections)
        print(len(byteTrack.tracks))
        # display tracked objects on frame
        annotated_frame = frame
        for object in byteTrack.tracks:
            # arr = object.box
            # list_of_tuples = [tuple(row) for row in arr]
            # print(list_of_tuples)
            top_left = object.box[0]  # Convert top-left corner to tuple
            bottom_right = object.box[3]  # Convert bottom-right corner to tuple
            cv2.rectangle(annotated_frame, top_left, bottom_right, (0, 255, 0))
        
        # Visualize the results on the frame
        # annotated_frame: np.ndarray = results[0].plot()
        
        # Add information to quit to frame
        cv2.putText(annotated_frame, text="Press 'q' to quit", org=(0, frame.shape[0] - 10), fontFace=font, fontScale=0.5, color=(0, 0, 255))

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
cv2.destroyAllWindows()
