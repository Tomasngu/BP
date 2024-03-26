import cv2
import numpy as np

def create_layout(overlayed_img1, overlayed_img4 , overlayed_img6, overlayed_img7):
    top_part = np.hstack((overlayed_img7, overlayed_img1))
    final_width = top_part.shape[1]

    def widen(img, target_width):
        original_height, original_width = img.shape[:2]
        aspect_ratio = original_height / original_width
        target_height = int(target_width * aspect_ratio)
        resized = cv2.resize(img, (target_width, target_height))
        return resized

    overlayed_img4 = widen(overlayed_img4, final_width)
    overlayed_img6 = widen(overlayed_img6, final_width)

    # Create a horizontal separator with a black outline and a grey center
    outline_thickness = 2
    separator_height = 20
    horizontal_separator_outline = np.zeros((separator_height, final_width, 3), dtype=np.uint8)  # Black outline
    cv2.rectangle(horizontal_separator_outline, (0, 0), (final_width, separator_height), (128, 128, 128), thickness=-1)  # Fill with grey
    cv2.rectangle(horizontal_separator_outline, (0, 0), (final_width-1, separator_height-1), (0, 0, 0), thickness=outline_thickness)  # Black outline
    
    # Vertically stack the rescaled top part, the outlined horizontal separator, and the bottom part
    final_layout = np.vstack((top_part, horizontal_separator_outline, overlayed_img4, horizontal_separator_outline, overlayed_img6))
    return final_layout


