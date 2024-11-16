import cv2
import json
import os
from ultralytics import YOLO
from ultralytics.solutions import ObjectCounter
from ultralytics import solutions

TRACKED_CLASSES = [46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56]

# Function to find files
def find_file(directory: str, file_name: str) -> str:
    for root, _, files in os.walk(directory):
        if file_name in files:
            return os.path.join(root, file_name)
    return ""

# Path to the downloaded video
video_name = input("Enter the name of the video file (default is example_video.mp4): ").strip()
if not video_name:
    video_name = 'example_reversed.mp4'
video_path = find_file(os.getcwd(), video_name)
if video_path:
    video_name = video_path
    print(f"Absolute video path: {video_path}")
if not os.path.isfile(video_path):
    print(f"Could not find video: {video_path}")
    exit(1)

# Capture video
cap = cv2.VideoCapture(video_path)
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# Load region points from polygons.json
with open('polygons.json', 'r') as file:
    data = json.load(file)
    polygons = {
        'entry': data.get('entry', []),
        'exit': data.get('exit', [])
    }
# Define region points
region_points =  polygons['entry'][0] # For polygon region counting
print

# Video writer
video_writer = cv2.VideoWriter("object_counting_output.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

# Init Object Counter
counter = solutions.ObjectCounter(
    show=True,  # Display the output
    region=region_points,  # Pass region points
    model="yolo11n.pt",  # model="yolo11n-obb.pt" for object counting using YOLO11 OBB model.
    classes=TRACKED_CLASSES,  # If you want to count specific classes i.e person and car with COCO pretrained model.
    # show_in=True,  # Display in counts
    # show_out=True,  # Display out counts
    # line_width=2,  # Adjust the line width for bounding boxes and text display
)

# Process video
while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break
    im0 = counter.count(im0)
    video_writer.write(im0)

cap.release()
video_writer.release()
cv2.destroyAllWindows()