import os
from typing import List
import cv2
import numpy as np
import requests
import time
import matplotlib.pyplot as plt
from ultralytics import YOLO
from ultralytics.engine.results import Results
from Detection import Detection
from ByteTrack import ByteTrack

model_name = 'yolo11s.pt'
# Download the YOLO model
if not os.path.isfile(model_name):
    print(f'{model_name} does not exist. Downloading...')
    download_url = 'https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11s.pt'

    response = requests.get(download_url)

    if response.status_code == 200:
        with open(model_name, 'wb') as file:
            file.write(response.content)
        print(f'Downloaded {model_name}')
    else:
        print(f'Failed to download {model_name}')

# Load the YOLO model
model: YOLO = YOLO(model_name)

# These are some test videos Scott used while developing and troubleshooting ByteTrack
script_dir = os.path.dirname(os.path.abspath(__file__))
video_path = os.path.join(script_dir, 'Banana.MOV')
# video_path = os.path.join(script_dir, 'TwoBananasStill.MOV')
# video_path = os.path.join(script_dir, 'TwoBananasMoving.MOV')
# video_path = os.path.join(script_dir, 'palace.mp4')
cap = cv2.VideoCapture(video_path)

frame_width = int(cap.get(3)) 
frame_height = int(cap.get(4)) 
   
size = (frame_width, frame_height)
# Below VideoWriter object will create 
# a frame of above defined The output  
# is stored in 'filename.avi' file. 
# video_output = cv2.VideoWriter('palace_demo.avi',  
#                          cv2.VideoWriter_fourcc(*'MJPG'), 
#                          10, size) 

font = cv2.FONT_HERSHEY_SIMPLEX

# Start ByteTrack
bytetrack_confidence_threshold = 0.6
byteTrack = ByteTrack(bytetrack_confidence_threshold)

# Frame count to help with troubleshooting
frame_count = 0
curr_time = time.time()
prev_time = curr_time
fps_count = 0
fps = 0

# Loop through the video frames
steps = []
while cap.isOpened() and frame_count < 600:
    # Read a frame from the video
    success, frame = cap.read()
    
    fps_count += 1
    curr_time = time.time()
    if curr_time - prev_time >= 1:
        fps = fps_count / (curr_time - prev_time)
        prev_time = curr_time
        fps_count = 0
    if success:
        # Run YOLO inference on the frame
        results: List[Results] = model(frame)
               
        # Create detection classes for ByteTrack
        detections = []
        print(f"Number of Detections: {len(results[0].boxes)}")
        for result in results:
            for box in result.boxes:
                class_name = model.names[int(box.cls)]
                confidence = box.conf
                xyxy = box.xyxy
                xywh = box.xywh
                detections.append(Detection(class_name, confidence, box.xywh))    
        byteTrack.updateTracks(detections)
        
        # display tracked objects on frame
        annotated_frame = frame
        cv2.putText(annotated_frame, f"Number of Tracks: {len(byteTrack.tracks)}", (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 2)
        for object in byteTrack.tracks:
            top_left = object.box_corners[0]  # Convert top-left corner to tuple
            bottom_right = object.box_corners[2]  # Convert bottom-right corner to tuple
            cv2.rectangle(annotated_frame, top_left, bottom_right, object.color, thickness=3)
            
            # I want to see the accuracy of the prediction
            top_left_prediction = object.prediction[0]  # Convert top-left corner to tuple
            bottom_right_prediction = object.prediction[2]  # Convert bottom-right corner to tuple
            cv2.rectangle(annotated_frame, top_left_prediction, bottom_right_prediction, object.color, thickness=1)
            
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

        # Add frame count to frame
        cv2.putText(annotated_frame, text=f"{frame_count}", org=(frame.shape[1] - 40, frame.shape[0] - 10), fontFace=font, fontScale=0.75, color=(0, 0, 255))
        frame_count += 1
        
        # Add fps to display
        cv2.putText(annotated_frame, f"{fps}", org=(frame.shape[1] - 40, frame.shape[0] - 40), fontFace=font, fontScale=0.75, color=(0, 0, 255))
        
        # Display the annotated frame
        cv2.imshow("YOLO Inference", annotated_frame)
        
        # video_output.write(annotated_frame)

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


## BELOW is for graphing the accuracy of the Kalman Filter. I (Scott) use it for troubleshooting
## and will include it in the presentation.

width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float
# fourcc = cv2.VideoWriter_fourcc(*'MP4V')
# output = cv2.VideoWriter("output.mp4", fourcc, fps,(int(width),int(height)))

# Number of indices (assuming 12 indices)
num_indices = 4

# Custom titles for each subplot (you can adjust this list)
custom_titles = [
    "Position X", "Position Y", "Width", "Height",
    "Velocity X", "Velocity Y", "Velocity Width", "Velocity Height",
    "Acceleration X", "Acceleration Y", "Acceleration Width", "Acceleration Height"
]

# Create a figure and axes with 3 rows and 4 columns
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Flatten the 2D array of axes for easier iteration
axes = axes.flatten()

# Loop over each object in byteTrack.tracks
for obj in byteTrack.tracks:
    # Loop over the indices (0 to 11)
    for i in range(num_indices):
        # Get the state and prediction data for the i-th index
        state = obj.filter.state_data[i]
        prediction = obj.filter.prediction_data[i]
        
        # Plot state and prediction data on the corresponding subplot
        ax = axes[i]
        ax.plot(obj.filter.steps, state, color='blue', label='State')
        ax.plot(obj.filter.steps, prediction, color='red', label='Prediction')

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
