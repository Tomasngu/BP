import cv2
import numpy as np

def transform_row2(M, x, y, width, height):

    def transform_point(M, x, y):
        points = np.array([[x, y]], dtype='float32')  
        points_reshaped = np.array([points])
        pointsOut = cv2.perspectiveTransform(points_reshaped, M)
        return pointsOut[0,0,0], pointsOut[0,0,1]

    x_proj, y_proj = transform_point(M, x, y)
    
    left, right = x - width/2, x + width/2
    up, down = y - height/2, y + height/2

    upper_left_proj = transform_point(M, left, up)
    upper_right_proj = transform_point(M, right, up)
    lower_left_proj = transform_point(M, left, down)
    lower_right_proj = transform_point(M, right, down)        
    return x_proj, y_proj, [upper_left_proj, upper_right_proj, lower_right_proj, lower_left_proj]

def shift(x, y, width, height):
    y += height/3
    return x, y, width, height

def calculate_iou(boxA, boxB):
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes.

    Parameters:
    - boxA: The first bounding box as a tuple (x, y, width, height)
    - boxB: The second bounding box as a tuple (x, y, width, height)

    Returns:
    - The IoU as a float. This will be 0 if the boxes do not intersect.
    """
    # Determine the coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[0] + boxA[2], boxB[0] + boxB[2])
    yB = min(boxA[1] + boxA[3], boxB[1] + boxB[3])

    # Compute the area of intersection rectangle
    interArea = max(0, xB - xA) * max(0, yB - yA)

    # Compute the area of both the bounding boxes
    boxAArea = boxA[2] * boxA[3]
    boxBArea = boxB[2] * boxB[3]

    # Compute the union area by adding both areas and subtracting the intersection area
    unionArea = boxAArea + boxBArea - interArea

    # Compute the IoU
    iou = interArea / unionArea

    return iou