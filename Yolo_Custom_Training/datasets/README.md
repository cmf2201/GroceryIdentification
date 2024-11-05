# Datasets Directory

Use this directory to place datasets you wish to train a custom YOLO model on.

## YOLO Dataset Format

The YOLO dataset format consists of:

1. **Images**: The images you want to train your model on.
2. **Annotations**: Corresponding annotation files for each image, typically in `.txt` format. Each line in the annotation file represents one object in the image with the following format:
    ```
    <object-class> <x_center> <y_center> <width> <height>
    ```
    - `object-class`: Integer representing the class of the object.
    - `x_center`: Float representing the x-coordinate of the center of the object (relative to the width of the image).
    - `y_center`: Float representing the y-coordinate of the center of the object (relative to the height of the image).
    - `width`: Float representing the width of the object (relative to the width of the image).
    - `height`: Float representing the height of the object (relative to the height of the image).
Ensure that your dataset follows this format for successful training.

## Roboflow custom dataset
1. On roboflow find the dataset version you want to use
2. Click download dataset
3. Select YOLO11 as the format
4. Update roboflow_dataset.py with your API key and project