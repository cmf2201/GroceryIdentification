import cv2
import json
import os
import numpy as np
import sys

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
    global ix, iy, drawing, img, display_img, rectangle_color, rectangle_type, current_polygon
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
        display_img = img.copy()
        if len(current_polygon) > 1:
            cv2.polylines(display_img, [np.array(current_polygon, np.int32).reshape((-1, 1, 2))], isClosed=False, color=rectangle_color, thickness=2)
        for polygon in polygons['cart']:
            cv2.polylines(display_img, [np.array(polygon, np.int32).reshape((-1, 1, 2))], isClosed=True, color=(0, 255, 0), thickness=5)
        cv2.imshow("image", display_img)

# Check if an image path is provided as an argument
if len(sys.argv) != 2:
    print("Usage: python setup_assistant.py <image_path>")
    exit(1)

image_path = sys.argv[1]

if not os.path.isfile(image_path):
    print(f"Could not find image: {image_path}")
    exit(1)

# Load the image
original_img = cv2.imread(image_path)

# Get the screen resolution
screen_width = 1920 
screen_height = 1080  

# Calculate the scaling factor
scale_width = screen_width / original_img.shape[1]
scale_height = (screen_height - 200) / original_img.shape[0]  # Subtract some pixels for the text
scale = min(scale_width, scale_height)

# Resize the image for display
display_img = cv2.resize(original_img, None, fx=scale, fy=scale)

# Save the scaling factor
with open('scaling_factor.json', 'w') as f:
    json.dump({'scale': scale}, f)

font = cv2.FONT_HERSHEY_SIMPLEX
img = display_img.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", draw_polygon)

# get old polygons from file
try:
    with open('polygons.json', 'r') as f:
        content = f.read().strip()
        if content:
            old_polygons = json.loads(content)
            print("Polygons loaded from polygons.json")
        else:
            print("polygons.json is empty, starting with empty polygons")
            old_polygons = None
except (FileNotFoundError, json.JSONDecodeError):
    print("polygons.json not found or invalid, starting with empty polygons")
    old_polygons = None

# display old polygons
if old_polygons is not None:  
    for polygon in old_polygons['cart']:
        # append old polygon to polygons
        polygons['cart'].append(polygon)

while True:
    display_img = img.copy()
    # display polygons
    for polygon in polygons['cart']:
        cv2.polylines(display_img, [np.array(polygon, np.int32).reshape((-1, 1, 2))], isClosed=True, color=(0, 255, 0), thickness=5)
        
    # Add information to quit to frame
    cv2.putText(display_img, text="Press 'q' to quit", org=(0, display_img.shape[0] - 10), fontFace=font, fontScale=0.5, color=(0, 0, 255))
    # add information on how to reset frame
    cv2.putText(display_img, text="Press 'r' to reset polygons", org=(0, display_img.shape[0] - 30), fontFace=font, fontScale=0.5, color=(0, 0, 255))
    # add information on how to change rectangle type

    cv2.imshow("image", display_img)
    
    key = cv2.waitKey(1) & 0xFF    
    # wait for r to reset polygons
    if key == ord("r"):
        polygons = {'cart': []}
        img = display_img.copy()
    # wait for q to end setup
    if key == ord("q"):
        # Scale up the polygons before saving
        scaled_polygons = {'cart': []}
        for polygon in polygons['cart']:
            scaled_polygon = [(int(x / scale), int(y / scale)) for x, y in polygon]
            scaled_polygons['cart'].append(scaled_polygon)
        
        # Save polygons to a file
        with open('polygons.json', 'w') as f:
            json.dump(scaled_polygons, f)
            print("Polygons saved to polygons.json")
        break

cv2.destroyAllWindows()