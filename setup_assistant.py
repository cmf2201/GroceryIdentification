import cv2
import json
import os

drawing = False  # true if mouse is pressed
rectangle_type = "entry"
rectangle_color = (0, 255, 0)
polygons = {'entry': [], 'exit': []}
ix, iy = -1, -1

# function for finding files
def find_file(directory: str, file_name: str) -> str:
    for root, _, files in os.walk(directory):
        if file_name in files:
            return os.path.join(root, file_name)
    return ""

# mouse callback function
def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, img, original_img, rectangle_color, rectangle_type
    if rectangle_type == "entry":
        rectangle_color = (0, 255, 0)
    else:
        rectangle_color = (0, 0, 255)
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img = original_img.copy()
            cv2.rectangle(img, (ix, iy), (x, y), rectangle_color, 1)
            cv2.imshow("image", img)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        # Record rectangle
        if rectangle_type == "entry":
            polygons['entry'].append((ix, iy, x, y))
        else:
            polygons['exit'].append((ix, iy, x, y))
        img = original_img.copy()
        for polygon in polygons['entry']:
            cv2.rectangle(img, polygon[:2], polygon[2:], (0, 255, 0), 5)
        for polygon in polygons['exit']:
            cv2.rectangle(img, polygon[:2], polygon[2:], (0, 0, 255), 5)
        cv2.imshow("image", img)

# ask user if they should set up on webcam or a photo
print("Would you like to set up on a webcam or a photo?")
while True:
    setup_type = input("Enter 'webcam' or 'photo': ").strip().lower()
    if setup_type in ['webcam', 'photo']:
        break
    else:
        print("Invalid input. Please enter 'webcam' or 'photo'")

# if setup is photo, ask for photo path
if setup_type == 'photo':
    # Path to the downloaded photo
    photo_name = input("Enter the name of the photo file (default is example_photo.png): ").strip()
    if not photo_name:
        photo_name = 'example_photo.png'
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
    
font = cv2.FONT_HERSHEY_SIMPLEX
img = original_img.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", draw_rectangle)
# get old polygons from file
try:
    with open('polygons.json', 'r') as f:
        old_polygons = json.load(f)
        print("Polygons loaded from polygons.json")
except FileNotFoundError:
    print("polygons.json not found, starting with empty polygons")
# display old polygons
if old_polygons is not None:  
    for polygon in old_polygons['entry']:
        # append old polygon to polygons
        polygons['entry'].append(polygon)
    for polygon in old_polygons['exit']:
        # append old polygon to polygons
        polygons['exit'].append(polygon)

while True:
    img = original_img.copy()
    # display polygons
    for polygon in polygons['entry']:
        cv2.rectangle(img, polygon[:2], polygon[2:], (0, 255, 0), 5)
    for polygon in polygons['exit']:
        cv2.rectangle(img, polygon[:2], polygon[2:], (0, 0, 255), 5)
        
    # Add information to quit to frame
    cv2.putText(img, text="Press 'q' to quit", org=(0, img.shape[0] - 10), fontFace=font, fontScale=0.5, color=(0, 0, 255))
    # add information on how to reset frame
    cv2.putText(img, text="Press 'r' to reset polygons", org=(0, img.shape[0] - 30), fontFace=font, fontScale=0.5, color=(0, 0, 255))
    # add information on how to change rectangle type
    cv2.putText(img, text="Press 'space bar' to change between 'entry' and 'exit' rectangles", org=(0, img.shape[0] - 50), fontFace=font, fontScale=0.5, color=(0, 0, 255))

    cv2.imshow("image", img)
    
    key = cv2.waitKey(1) & 0xFF
    # wait for space to change rectangle type
    if key == ord(" "):
        if rectangle_type == "entry":
            rectangle_type = "exit"
        else:
            rectangle_type = "entry"
    
    # wait for r to reset polygons
    if key == ord("r"):
        polygons = {'entry': [], 'exit': []}
        img = original_img.copy()
    # wait for q to end setup
    if key == ord("q"):
        # Save polygons to a file
        with open('polygons.json', 'w') as f:
            json.dump(polygons, f)
            print("Polygons saved to polygons.json")
        break

cv2.destroyAllWindows()