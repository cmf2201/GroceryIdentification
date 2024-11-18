import cv2
import numpy as np
import numpy.typing as npt
from typing import Annotated, Optional, List

def intersect(ray_origin: np.ndarray, ray_direction: np.ndarray, segment_start: np.ndarray, segment_end: np.ndarray) -> Optional[np.ndarray]:
    """
    Calculates intersection between a ray and polygon segment
    
    Args:
        ray_origin (np.ndarray): Start of ray
        ray_direction (np.ndarray): direction of ray
        segment_start (np.ndarray): start of polygon segment
        segment_end (np.ndarray): end of polygon segment
    
    Returns:
        Optional[np.ndarray]: Intersection point if ray intersects segment
    """
    segment_start = np.array(segment_start)
    segment_end = np.array(segment_end)
    v1 = ray_origin - segment_start
    v2 = segment_end - segment_start
    # perpendicular vector to the ray's direction
    v3 = np.array([-ray_direction[1], ray_direction[0]])
    
    dot = np.dot(v2, v3)
    if abs(dot) < 1e-6:
        return None
    t1 = np.cross(v2, v1) / dot
    t2 = np.dot(v1, v3) / dot
    
    if t1 >= 0 and 0 <= t2 <= 1:
        return ray_origin + t1 * ray_direction
    return None

def is_point_inside_polygon(point: np.ndarray, polygon_points: np.ndarray) -> np.ndarray:
    # init intersections
    intersections: List[np.ndarray] = []
    
    # loop through polygon points to find every intersection
    for i in range(len(polygon_points)):
        segment_start = polygon_points[i]
        segment_end = polygon_points[(i+1) % len(polygon_points)]
        ray_direction = polygon_points[i] - np.array(point)
        intersection = intersect(point, ray_direction, segment_start, segment_end)
        if intersection is not None:
            intersections.append(intersection)
    return len(intersections) % 2 == 1