import cv2
import json
import os
import numpy as np

drawing = False  # true if mouse is pressed
rectangle_type = "cart"
rectangle_color = (0, 255, 0)
polygons = {'cart': []}
current_polygon = []
ix, iy = -1, -1
close_threshold = 10  # pixels

# function for finding files
def find_file(directory: str, file_name: str) -> str:
    for root, _, files in os.walk(directory):
        if file_name in files:
            return os.path.join(root, file_name)
    return ""

# mouse callback function
def draw_polygon(event, x, y, flags, param):
    global ix, iy, drawing, img, original_img, rectangle_color, rectangle_type, current_polygon
    if rectangle_type == "cart":
        rectangle_color = (0, 255, 0)
    else:
        rectangle_color = (0, 0, 255)
    
    if event == cv2.EVENT_LBUTTONDOWN:
        if not drawing:
            drawing = True
            current_polygon = [(x, y)]
        else:
            # Check if the new point is close to the first point to close the polygon
            if np.linalg.norm(np.array(current_polygon[0]) - np.array((x, y))) < close_threshold:
                current_polygon.append(current_polygon[0])
                polygons['cart'].append(current_polygon)
                drawing = False
                current_polygon = []
            else:
                current_polygon.append((x, y))
    
    if drawing:
        img = img.copy()
        if len(current_polygon) > 1:
            cv2.polylines(img, [np.array(current_polygon, np.int32).reshape((-1, 1, 2))], isClosed=False, color=rectangle_color, thickness=2)
        for polygon in polygons['cart']:
            cv2.polylines(img, [np.array(polygon, np.int32).reshape((-1, 1, 2))], isClosed=True, color=(0, 255, 0), thickness=5)
        cv2.imshow("image", img)

# ask user if they should set up on webcam or a photo
print("Would you like to set up on a webcam or a photo or a frame?")
while True:
    setup_type = input("Enter 'webcam' or 'photo' or 'frame': ").strip().lower()
    if setup_type in ['webcam', 'photo', 'frame']:
        break
    else:
        print("Invalid input. Please enter 'webcam' or 'photo' or 'frame'")

# if setup is photo, ask for photo path
if setup_type == 'photo':
    # Path to the downloaded photo
    photo_name = input("Enter the name of the photo file (default is example_photo.png): ").strip()
    if not photo_name:
        photo_name = 'example_grocery.jpg'
    photo_path = find_file(os.getcwd(), photo_name)
    if photo_path:
        photo_name = photo_path
        print(f"Absolute photo path: {photo_name}")
        # get photo from path
        cap = cv2.VideoCapture(photo_path)
        ret, original_img = cap.read()
    if not os.path.isfile(photo_path):
        print(f"Could not find photo: {photo_path}")
        exit(1)
# if setup type is webcam capture a picture
if setup_type == 'webcam':
    # capture picture
    cap = cv2.VideoCapture(0)
    ret, original_img = cap.read()
    cap.release()

if setup_type == 'frame':
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
        ret, original_img = cap.read()
        cap.release()
    if not os.path.isfile(video_path):
        print(f"Could not find video: {video_path}")
        exit(1)
    
# Get the screen resolution
screen_width = 1920 
screen_height = 1080  

# Calculate the scaling factor
scale_width = screen_width / original_img.shape[1]
scale_height = (screen_height - 200) / original_img.shape[0]  # Subtract some pixels for the text
scale = min(scale_width, scale_height)

# Resize the image
original_img = cv2.resize(original_img, None, fx=scale, fy=scale)

font = cv2.FONT_HERSHEY_SIMPLEX
img = original_img.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", draw_polygon)
# get old polygons from file
try:
    with open('polygons.json', 'r') as f:
        old_polygons = json.load(f)
        print("Polygons loaded from polygons.json")
except FileNotFoundError:
    print("polygons.json not found, starting with empty polygons")
# display old polygons
if old_polygons is not None:  
    for polygon in old_polygons['cart']:
        # append old polygon to polygons
        polygons['cart'].append(polygon)

while True:
    img = original_img.copy()
    # display polygons
    for polygon in polygons['cart']:
        cv2.polylines(img, [np.array(polygon, np.int32).reshape((-1, 1, 2))], isClosed=True, color=(0, 255, 0), thickness=5)
        
    # Add information to quit to frame
    cv2.putText(img, text="Press 'q' to quit", org=(0, img.shape[0] - 10), fontFace=font, fontScale=0.5, color=(0, 0, 255))
    # add information on how to reset frame
    cv2.putText(img, text="Press 'r' to reset polygons", org=(0, img.shape[0] - 30), fontFace=font, fontScale=0.5, color=(0, 0, 255))
    # add information on how to change rectangle type

    cv2.imshow("image", img)
    
    key = cv2.waitKey(1) & 0xFF    
    # wait for r to reset polygons
    if key == ord("r"):
        polygons = {'cart': []}
        img = original_img.copy()
    # wait for q to end setup
    if key == ord("q"):
        # Save polygons to a file
        with open('polygons.json', 'w') as f:
            json.dump(polygons, f)
            print("Polygons saved to polygons.json")
        break

cv2.destroyAllWindows()