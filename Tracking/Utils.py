import numpy as np

def calculateArea(pixels: np.array):
    """Calculates the area of a square from the pixel corners provided.

    Args:
        pixels (array): List of int tuples that represent each corner in the square.

    Returns:
        float: The area of the defined square.
    """
    
    # I convert the input list to a numpy array for easier manipulation
    pixel_array = np.array(pixels)
    
    x_coords = pixel_array[:, 0]
    y_coords = pixel_array[:, 1]

    width = np.max(x_coords) - np.min(x_coords)
    height = np.max(y_coords) - np.min(y_coords)

    area = width * height
    return area

def computeIoU(box1: np.array, box2: np.array):
    """Calcuated the IoU between two detection boxes

    Args:
        box1 (array): XYWH Array of box corners from box1
        box2 (array): XYWH Array of box corners from box2
    """
    
    x_left = max(box1[0][0], box2[0][0])
    y_top = max(box1[0][1], box2[0][1])
    x_right = min(box1[2][0], box2[2][0])
    y_bottom = min(box1[2][1], box2[2][1])
    
    # Calculate intersection area
    if x_right < x_left or y_bottom < y_top:
        intersection_area = 0
    else:
        intersection_area = (x_right - x_left) * (y_bottom - y_top)

    union_area = calculateArea(box1) + calculateArea(box2) - intersection_area
    
    # If boxes do not overlap at all, then the union will be zero. To avoid dividing by zero, 
    # we just return an IoU of 0.0, meaning the boxes are completely seperate.
    if union_area == 0:
        return 0.0
    
    # Calculate IoU
    return intersection_area / union_area

def detectionToMeasurement(detection):
    state = np.array([
        detection.x,
        detection.y,
        detection.width,
        detection.height,
        ]).T
    return state

def detectionToState(detection):
    state = np.array([
        detection.x,
        detection.y,
        detection.width,
        detection.height,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        ]).T
    return state
