import cv2
import numpy as np
from visualize.perspective import *
from visualize.layout import *
from visualize.image_points import *
from datetime import datetime, timedelta



def create_full_heatmap(df, save_path, days_interval=10, min_scale=20, title=None):
    """
    Creates and saves a full heatmap combining multiple camera views with color normalization.

    Parameters:
    - df (DataFrame): Data containing coordinates and camera information for heatmap generation.
    - save_path (str): Path to save the resulting heatmap image.
    - days_interval (int, optional): The number of days over which the data spans. Used for scaling.
    - min_scale (int, optional): Minimum scale for heatmap intensity.
    - title (str, optional): Title for the heatmap, displayed via the colorbar.
    """
    camera_ids = [2, 4, 6, 7]
    raw_heatmaps = []
    heatmap_1 = get_heatmap_new(df, [1,2], CAMERA_to_MAP[1])
    raw_heatmaps.append(heatmap_1)
    for camera in camera_ids[1:]:
        raw_heatmaps.append(get_heatmap_new(df, [camera], CAMERA_to_MAP[camera]))
    global_max = np.max([np.max(heatmap) for heatmap in raw_heatmaps])

    def normalize_and_apply_colormap(heatmap, global_max, min_scale=min_scale):
        # Scale heatmap values based on global_max directly
        heatmap_scaled = (heatmap / global_max) * 255 
        heatmap_scaled = np.clip(heatmap_scaled, 0, 255).astype(np.uint8)  
        zero_mask = (heatmap_scaled < 255/min_scale)

        heatmap_color = cv2.applyColorMap(heatmap_scaled, cv2.COLORMAP_JET)
        heatmap_color[zero_mask] = (0,0,0)
        return heatmap_color

    normalized_heatmaps = [normalize_and_apply_colormap(heatmap, global_max) for heatmap in raw_heatmaps]

    
    original_img = cv2.imread(CAMERA_to_PATH[1])
    # plot_images(original_img)
    heatmap_color = normalized_heatmaps[0]
    overlayed_img1 = cv2.addWeighted(original_img, 0.8, heatmap_color, 1, 0)
    
    original_img = cv2.imread(CAMERA_to_PATH[7])
    heatmap_color = normalized_heatmaps[3]
    overlayed_img7 = cv2.addWeighted(original_img, 0.8, heatmap_color, 1, 0)
    
    original_img = cv2.imread(CAMERA_to_PATH[6])
    heatmap_color = normalized_heatmaps[2]
    overlayed_img6 = cv2.addWeighted(original_img, 0.8, heatmap_color, 1, 0)
    
    original_img = cv2.imread(CAMERA_to_PATH[4])
    heatmap_color = normalized_heatmaps[1]
    overlayed_img4 = cv2.addWeighted(original_img, 0.8, heatmap_color, 1, 0)

    final_layout = create_layout(overlayed_img1, overlayed_img4, overlayed_img6, overlayed_img7)

    max_per_day = global_max/days_interval
    
    fig = add_colorbar(final_layout, max_per_day/min_scale, max_per_day, title)
    fig.savefig(save_path, bbox_inches='tight')

def one_heatmap(df, camera, min_scale=20):
    """
    Generates a heatmap for a single camera.

    Parameters:
    - df (DataFrame): Data containing coordinates for heatmap generation.
    - camera (list): List containing the camera number for which the heatmap is generated.
    - min_scale (int, optional): Minimum scale for heatmap intensity.
    
    Returns:
    - overlayed_img (ndarray): The original camera image overlayed with the heatmap.
    """
    heatmap = get_heatmap_new(df, camera, CAMERA_to_MAP[camera[0]])
    global_max = np.max(heatmap)
    heatmap_scaled = (heatmap / global_max) * 255 
    heatmap_scaled = np.clip(heatmap_scaled, 0, 255).astype(np.uint8) 
    zero_mask = (heatmap_scaled < 255/min_scale)

    heatmap_color = cv2.applyColorMap(heatmap_scaled, cv2.COLORMAP_JET)
    heatmap_color[zero_mask] = (0,0,0)
    
    original_img = cv2.imread(CAMERA_to_PATH[camera[0]])
    overlayed_img = cv2.addWeighted(original_img, 0.8, heatmap_color, 1, 0)
    # plt.figure()
    # plt.imshow(overlayed_img[..., ::-1]) 
    # plt.show()
    return overlayed_img

def one_heatmap_background(df, camera, background_img, min_scale=3):
    """
    Generates a heatmap for a single camera over a specified background image.

    Parameters:
    - df (DataFrame): Data containing coordinates for heatmap generation.
    - camera (list): List containing the camera number for which the heatmap is generated.
    - background_img (ndarray): Background image over which the heatmap is overlayed.
    - min_scale (int, optional): Minimum scale for heatmap intensity.
    
    Returns:
    - overlayed_img (ndarray): The background image overlayed with the heatmap.
    """
    heatmap = get_heatmap_new(df, camera, (IMG_WIDTH, IMG_HEIGHT))
    global_max = np.max(heatmap)
    heatmap_scaled = (heatmap / global_max) * 255 
    heatmap_scaled = np.clip(heatmap_scaled, 0, 255).astype(np.uint8)  
    zero_mask = (heatmap_scaled < 255/min_scale)

    heatmap_color = cv2.applyColorMap(heatmap_scaled, cv2.COLORMAP_JET)
    heatmap_color[zero_mask] = (0,0,0)
    
    original_img = background_img
    overlayed_img = cv2.addWeighted(original_img, 1, heatmap_color, 0.5, 0)
    return overlayed_img

def is_within_time_window(row_time, current_time, delta=timedelta(minutes=15)):
    """
    Checks if a given time is within a specified window around the current time.

    Parameters:
    - row_time (datetime.time): Time to check.
    - current_time (datetime.time): Current system time.
    - delta (timedelta, optional): Time window around the current time.
    
    Returns:
    - (bool): True if row_time is within the time window, otherwise False.
    """
    today = datetime.now().date()
    row_datetime = datetime.combine(today, row_time)
    current_datetime = datetime.combine(today, current_time)
    return current_datetime - delta <= row_datetime <= current_datetime + delta


def heatmap_by_hour(df_proj, hour_sampling, days_interval):
    """
    Generates and saves heatmaps for different time windows within a day.

    Parameters:
    - df_proj (DataFrame): Projected data containing coordinates and timestamps for heatmap generation.
    - hour_sampling (int): The interval in hours to divide the day for separate heatmaps.
    - days_interval (int): The number of days over which the data spans, used for scaling.
    """
    df_proj['Hour'] = df_proj['Date'].dt.hour
    def map_to_time_window(hour):
        return f'{int(np.floor(hour / hour_sampling) * hour_sampling):02d}-{int(np.floor(hour / hour_sampling) * hour_sampling + hour_sampling):02d}'
        
    df_proj['Time_Window'] = df_proj['Hour'].apply(map_to_time_window)
    df_proj[['Hour', 'Time_Window']]
    time_windows = df_proj['Time_Window'].unique().tolist()
    time_windows.sort()
    def all_heatmaps_exist(time_windows):
        for tw in time_windows:
            save_path = f'tmp_heatmaps/he{tw}.png'
            if not os.path.exists(save_path):
                return False  
        return True 
    if not all_heatmaps_exist(time_windows):
        for tw in time_windows:
            df = df_proj[df_proj['Time_Window'] == tw]
            create_full_heatmap(df=df, save_path=f'tmp_heatmaps/he{tw}.png', title=tw, days_interval=days_interval)
    else:
        print('Heatmaps already cached.')
    image_paths = [f"tmp_heatmaps/he{x}.png" for x in time_windows]
    images = [cv2.imread(path) for path in image_paths]
    rows = [cv2.hconcat(images[i:i+int(24/hour_sampling/4)]) for i in range(0, 24//hour_sampling, int(24/hour_sampling/4))]
    # Vertically concatenate the rows to form the final grid
    stacked_image = cv2.vconcat(rows)
    plot_images(stacked_image, height=200, width=200)
    cv2.imwrite('he_all.png', stacked_image)
