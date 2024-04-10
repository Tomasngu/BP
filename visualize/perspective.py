import cv2
import numpy as np
from visualize.image_points import *
import pandas as pd

def transform_row(M, x, y):
    """
    Transforms a single point (x, y) using a given transformation matrix.

    Parameters:
    - M (numpy.ndarray): The transformation matrix.
    - x (float): The x-coordinate of the point.
    - y (float): The y-coordinate of the point.

    Returns:
    - tuple: The transformed (x, y) coordinates.
    """
    

    def transform_point(M, x, y):
        """
        Apply projective transformation.
        """
        points = np.array([[x, y]], dtype='float32')  
        points_reshaped = np.array([points])
        pointsOut = cv2.perspectiveTransform(points_reshaped, M)
        return pointsOut[0,0,0], pointsOut[0,0,1]

    x_proj, y_proj = transform_point(M, x, y)
    return x_proj, y_proj


def get_size(map_width_px, map_height_px, map_width_real):
    """
    Calculates the size ratio between the real world and the map dimensions.

    Parameters:
    - map_width_px (int): Width of the map in pixels.
    - map_height_px (int): Height of the map in pixels.
    - map_width_real (float): Real world width corresponding to the map width.

    Returns:
    - tuple: The width and height ratio.
    """
    ratio = ELEPHANT_SIZE/map_width_real
    return ratio, ratio*map_width_px/map_height_px

def remove_duplicate_elephants(df, threshold=0.1):
    """
    Removes duplicate elephant detections overlapping in camera 1 and 2 based on a distance threshold.

    Parameters:
    - df (pandas.DataFrame): The dataframe containing elephant detections.
    - threshold (float, optional): The distance threshold for considering detections as duplicates.

    Returns:
    - pandas.DataFrame: The cleaned dataframe with duplicates removed.
    """
    def calculate_distance(row1, row2):
        """Calculate the Euclidean distance between two points."""
        return np.linalg.norm(np.array([row1['X_center'], row1['Y_center']]) - np.array([row2['X_center'], row2['Y_center']]))

    # Prepare a list to track indices to remove
    indices_to_remove = []

    for timestamp in df['Date'].unique():
        cam1_entries = df[(df['Camera'] == 1) & (df['Date'] == timestamp)]
        cam2_entries = df[(df['Camera'] == 2) & (df['Date'] == timestamp)]
        
        for index1, row1 in cam1_entries.iterrows():
            for index2, row2 in cam2_entries.iterrows():
                distance = calculate_distance(row1, row2)
                
                # If distance is within threshold, check mutual closeness
                if distance < threshold:
                    
                    closest_to_cam1 = cam2_entries.apply(lambda row: calculate_distance(row, row1), axis=1).idxmin()
                    # Find closest cam1 entry to current cam2 entry
                    closest_to_cam2 = cam1_entries.apply(lambda row: calculate_distance(row, row2), axis=1).idxmin()
                    # Check mutual closeness
                    if closest_to_cam1 == index2 and closest_to_cam2 == index1:
                        assert index2 not in indices_to_remove
                        indices_to_remove.append(index2) 
    df_cleaned = df.drop(indices_to_remove)
    
    return df_cleaned

def project_df(df):
    """
    Projects data points from image coordinates to map coordinates.

    Parameters:
    - df (pandas.DataFrame): Dataframe containing the detection data with elephant coordinates.

    Returns:
    - pandas.DataFrame: New dataframe with projected map coordinates.
    """
    df_proj = pd.DataFrame(columns=['Camera', 'Date', 'X_center', 'Y_center', 'Width', 'Height'])
    for index, row in df.iterrows():
        data = {}
        data['Camera'] = row['Camera']
        map_width, map_height = CAMERA_to_MAP[data['Camera']]
        H = CAMERA_to_H[data['Camera']]
        width_real = CAMERA_to_REAL[data['Camera']]
        # print(width_real)
        data['Date'] = row['Date']
        x, y, width, height = row['X_center'], row['Y_center'], row['Width'], row['Height']
        
        x, y = x*IMG_WIDTH, y*IMG_HEIGHT
        width, height = width*IMG_WIDTH, height*IMG_HEIGHT
        # print(f'x, y, w, h = {x, y, width, height}')
        x, y, width, height = shift(x, y, width, height, data['Camera'])
            
        x_proj, y_proj = transform_row(H, x, y)
        # print(polygon)  
        data['X_center'], data['Y_center'] = x_proj/map_width, y_proj/map_height
        data['Width'], data['Height'] = get_size(map_width, map_height, width_real)
        
        df_proj = pd.concat([df_proj, pd.DataFrame([data])], ignore_index=True)
    return df_proj

def get_heatmap_new(df, camera, size):
    """
    Generates a heatmap for specified cameras within a dataframe.

    Parameters:
    - df (pandas.DataFrame): The dataframe containing detection data.
    - camera (list): List of camera IDs for which to generate the heatmap.
    - size (tuple): The dimensions (width, height) for the heatmap.

    Returns:
    - numpy.ndarray: The generated heatmap as a 2D numpy array.
    """
    df = df[df['Camera'].isin(camera)]

    heatmap_width, heatmap_height = size

    heatmap_img = np.zeros((heatmap_height, heatmap_width), dtype=np.float32)

    # Function to apply intensity within the bounding box area
    def apply_bounded_gaussian_heatmap(cx, cy, w, h, heatmap):
        # Calculate the bounding box in pixel coordinates
        left = int(max(0, cx - w/2))
        right = int(min(heatmap_width-1, cx + w/2))
        top = int(max(0, cy - h/2))
        bottom = int(min(heatmap_height-1, cy + h/2))

        if(left >= heatmap_width or right < 0) or (top >= heatmap_height or bottom < 0):
            return
        
        value = 1
        heatmap[top:bottom, left:right] += value

    for _, row in df.iterrows():
        cx, cy, w, h = row['X_center'] * heatmap_width, row['Y_center'] * heatmap_height, row['Width'] * heatmap_width, row['Height'] * heatmap_height
        apply_bounded_gaussian_heatmap(cx, cy, w, h, heatmap_img)
        
    return heatmap_img
