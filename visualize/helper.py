import matplotlib.pyplot as plt
import math
import cv2
import numpy as np


#inspired by https://gitlab.fit.cvut.cz/bi-svz/improutils_package/-/blob/master/improutils/visualisation/visualisation.py
def plot_images(*imgs, titles=[], title_size=32, width=30, height=30):
    """
    Display multiple images in a single matplotlib figure with optional titles.
    
    Parameters:
    - imgs (*args): Variable number of image arrays. Each image should be in the format expected by the 'channels' parameter.
    - titles (list of str, optional): Titles for each image. The length of 'titles' should match the number of images.
    - title_size (int, optional): Font size of the titles
    - width (int, optional): Desired width of each image in the grid. 
    - height (int, optional): Desired height of each image in the grid. 
    
    Raises:
    """
    width_def = width
    height_def = height

    width = math.ceil(math.sqrt(len(imgs)))
    height = math.ceil(len(imgs) / width)

    height_def = height_def / 5 * width

    f = plt.figure(figsize=(width_def, height_def))

    for i, img in enumerate(imgs, 1):
        ax = f.add_subplot(height, width, i)
        ax.axis('off')

        if len(titles) != 0:
            if len(imgs) != len(titles):
                print('WARNING titles length is not the same as images length!')
            try:
                ax.set_title(str(titles[i - 1]), fontdict={'fontsize': title_size, 'fontweight': 'medium'})
            except:
                pass

        ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

def plot_rectangle_on_image(image, cx, cy, w, h, color=(0, 255, 0), thickness=2):
    """
    Draws a rectangle on an image based on the center coordinates, width, and height.

    Parameters:
    - image: The image (numpy array) on which to draw.
    - cx, cy: The center coordinates of the rectangle.
    - w, h: The width and height of the rectangle.
    - color: The color of the rectangle (BGR format).
    - thickness: The thickness of the rectangle's outline. Use -1 for filled rectangle.
    """
    # Calculate the top-left corner of the rectangle
        
    top_left_x = int(cx - w / 2)
    top_left_y = int(cy - h / 2)

    # Calculate the bottom-right corner of the rectangle
    bottom_right_x = int(cx + w / 2)
    bottom_right_y = int(cy + h / 2)

    # Draw the rectangle on the image
    cv2.rectangle(image, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), color, thickness)

def draw_bounding_rect(image, bounding_rect, col=(0, 255, 0)):
    """
    Draws a rectangle on the image based on the bounding rectangle parameters.

    Parameters:
    - image: The image on which to draw the rectangle.
    - bounding_rect: A tuple of the form (x, y, w, h) representing the top-left corner coordinates,
                     width, and height of the bounding rectangle.
    """
    x, y, w, h = bounding_rect
    
    # Draw the rectangle on the image
    cv2.rectangle(image, (x, y), (x + w, y + h), col, 2)

def draw_circle(image, rel_x, rel_y, radius=10, color=(0, 0, 255), thickness=2):
    """
    Draw a small circle on the image at a relative position.

    Parameters:
    - image: The image on which to draw the circle (numpy array).
    - rel_x: The relative x coordinate (from 0 to 1) where to draw the circle.
    - rel_y: The relative y coordinate (from 0 to 1) where to draw the circle.
    - radius: The radius of the circle (in pixels).
    - color: The color of the circle (B, G, R) format.
    - thickness: The thickness of the circle's outline. Use a negative value for a filled circle.
    """
    # Calculate actual pixel coordinates
    center_x = int(rel_x)
    center_y = int(rel_y)

    # Draw the circle
    cv2.circle(image, (center_x, center_y), radius, color, thickness)


def plot_polygon_on_image(image, vertices, is_closed=True, color=(0, 255, 0), thickness=2):
    """
    Draws a polygon on an image based on a list of (x, y) tuples using OpenCV.

    Parameters:
    - image: The image (numpy array) on which to draw.
    - vertices: A list of tuples, where each tuple represents the x and y coordinates of a vertex.
    - is_closed: A boolean indicating whether the polygon should be closed (last vertex connected to the first).
    - color: The color of the polygon (BGR format).
    - thickness: The thickness of the polygon lines.
    """
    # Convert the list of tuples to a numpy array of shape (n, 1, 2)
    points = np.array(vertices, dtype=np.int32).reshape((-1, 1, 2))
    
    # Draw the polygon
    cv2.polylines(image, [points], isClosed=is_closed, color=color, thickness=thickness)


def downscale_image_by_2(input_image_path, output_image_path):
    # Read the input image using OpenCV
    input_image = cv2.imread(input_image_path)

    # Downscale the image by a factor of 2
    downscaled_image = cv2.resize(input_image, (0,0), fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

    # Save the downscaled image
    cv2.imwrite(output_image_path, downscaled_image)

