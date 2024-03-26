import cv2
import numpy as np
from image_points import ELEPHANT_SIZE, MAP_WIDTH_12

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

def transform_row(M, x, y):

    def transform_point(M, x, y):
        points = np.array([[x, y]], dtype='float32')  
        points_reshaped = np.array([points])
        pointsOut = cv2.perspectiveTransform(points_reshaped, M)
        return pointsOut[0,0,0], pointsOut[0,0,1]

    x_proj, y_proj = transform_point(M, x, y)
    return x_proj, y_proj


def get_size(map_width_px, map_height_px, map_width_real):
    ratio = ELEPHANT_SIZE/map_width_real
    return ratio, ratio*map_width_px/map_height_px

def shift(x, y, width, height, camera):
    if camera in [1, 2, 6]:
        y += height/3
    else:
        y += height/2
    return x, y, width, height

def remove_duplicate_elephants(df, threshold=0.1):
    def calculate_distance(row1, row2):
        """Calculate the Euclidean distance between two points."""
        return np.linalg.norm(np.array([row1['X_center'], row1['Y_center']]) - np.array([row2['X_center'], row2['Y_center']]))

    # Prepare a list to track indices to remove
    indices_to_remove = []

    # Iterate through each unique timestamp
    for timestamp in df['Date'].unique():
        # Filter entries for this specific timestamp for both cameras
        cam1_entries = df[(df['Camera'] == 1) & (df['Date'] == timestamp)]
        cam2_entries = df[(df['Camera'] == 2) & (df['Date'] == timestamp)]
        
        # Nested loop to calculate distances between all cam1 and cam2 entries
        for index1, row1 in cam1_entries.iterrows():
            for index2, row2 in cam2_entries.iterrows():
                distance = calculate_distance(row1, row2)
                
                # If distance is within threshold, check mutual closeness
                if distance < threshold:
                    # Find closest cam2 entry to current cam1 entry
                    
                    closest_to_cam1 = cam2_entries.apply(lambda row: calculate_distance(row, row1), axis=1).idxmin()
                    # Find closest cam1 entry to current cam2 entry
                    closest_to_cam2 = cam1_entries.apply(lambda row: calculate_distance(row, row2), axis=1).idxmin()
                    # Check mutual closeness
                    if closest_to_cam1 == index2 and closest_to_cam2 == index1:
                        assert index2 not in indices_to_remove
                        indices_to_remove.append(index2)  # Add cam2 entry to removal list
                        # c1 = (row1['X_center'], row1['Y_center'])
                        # c2 = (row2['X_center'], row2['Y_center'])
                        # # print(distance)
                        # c1 = (c1[0]*MAP_WIDTH_12, c1[1]*MAP_HEIGHT_12)
                        # c2 = (c2[0]*MAP_WIDTH_12, c2[1]*MAP_HEIGHT_12)
    # Drop the entries from the original DataFrame
    df_cleaned = df.drop(indices_to_remove)
    
    return df_cleaned