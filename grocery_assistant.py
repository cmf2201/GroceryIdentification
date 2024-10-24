import os
from typing import List
import cv2
import numpy as np
import requests
from ultralytics import YOLO
from ultralytics.engine.results import Results
import yt_dlp as youtube_dl

model_name = 'best.pt'
# model_name = 'Yolo_Custom_Training/runs/detect/train8/weights/best.pt'
# Download the YOLO model
if not os.path.isfile(model_name):
    print(f'{model_name} does not exist. Downloading...')
    download_url = f'https://github.com/ultralytics/assets/releases/download/v8.3.0/{model_name}'

    response = requests.get(download_url)

    if response.status_code == 200:
        with open(model_name, 'wb') as file:
            file.write(response.content)
        print(f'Downloaded {model_name}')
    else:
        print(f'Failed to download {model_name}')

# Load the YOLO model
model: YOLO = YOLO(model_name)

# URL of the YouTube video
youtube_url = 'https://www.youtube.com/watch/Ie_aQqez9qo'
video_path = 'downloaded_video.mp4'

# Check if the video already exists
if not os.path.isfile(video_path):
    print(f'{video_path} does not exist. Downloading...')
    
    # Download the YouTube video using yt-dlp
    ydl_opts = {
        'format': 'best',
        'outtmpl': video_path,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    
    print(f'Downloaded {video_path}')
else:
    print(f'{video_path} already exists.')

# capture video
cap = cv2.VideoCapture(video_path)
font = cv2.FONT_HERSHEY_SIMPLEX

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLO inference on the frame
        results = model.track(frame, show=False, tracker="bytetrack.yaml")  

        # Visualize the results on the frame
        annotated_frame: np.ndarray = results[0].plot()
        
        # Calculate and display FPS
        fps = cap.get(cv2.CAP_PROP_FPS)
        cv2.putText(annotated_frame, f'FPS: {fps:.2f}', (10, 30), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
        
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