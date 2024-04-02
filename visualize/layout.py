import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

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

    outline_thickness = 2
    separator_height = 20
    horizontal_separator_outline = np.zeros((separator_height, final_width, 3), dtype=np.uint8)  # Black outline
    cv2.rectangle(horizontal_separator_outline, (0, 0), (final_width, separator_height), (128, 128, 128), thickness=-1)  # Fill with grey
    cv2.rectangle(horizontal_separator_outline, (0, 0), (final_width-1, separator_height-1), (0, 0, 0), thickness=outline_thickness)  # Black outline
    
    # Vertically stack the rescaled top part, the outlined horizontal separator, and the bottom part
    final_layout = np.vstack((top_part, horizontal_separator_outline, overlayed_img4, horizontal_separator_outline, overlayed_img6))
    return final_layout


def add_colorbar(image, min_val, max_val, title=None, show=False):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 10),
                                   gridspec_kw={'width_ratios': [20, 1], 'wspace': 0.05})
    if title is not None:
        fig.suptitle(title, fontsize=16)
        
    # Display the image in the first subplot
    ax1.imshow(image[..., ::-1]) 
    ax1.axis('off')  # Turn off axis for image
    
    # Create a colormap and normalization instance
    cmap = mpl.cm.jet
    norm = mpl.colors.Normalize(vmin=min_val, vmax=max_val)
    
    # Create the colorbar in the second subplot
    cb1 = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, orientation='vertical')
    cb1.set_label('Average # Elephants per day')
    # Set custom ticks if needed (here just showing min and max)
    tick_values = np.linspace(min_val, max_val, num=11)
    cb1.set_ticks(tick_values)
    cb1.set_ticks(tick_values)
    # cb1.set_ticklabels([f'{min_val}', f'{max_val}'])
    cb1.set_ticklabels([f'{val.round(1)}' for val in tick_values])
    if not show:
        plt.close()
    #fig.tight_layout()
    fig.subplots_adjust(top=0.95)
    return fig

def add_colorbar_image(image, min_val, max_val, title=None, show=False):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 4),
                                   gridspec_kw={'width_ratios': [20, 1], 'wspace': 0.05})
    if title is not None:
        fig.suptitle(title, fontsize=16)
        
    # Display the image in the first subplot
    ax1.imshow(image[..., ::-1]) 
    ax1.axis('off')  # Turn off axis for image
    
    # Create a colormap and normalization instance
    cmap = mpl.cm.jet
    norm = mpl.colors.Normalize(vmin=min_val, vmax=max_val)
    
    # Create the colorbar in the second subplot
    cb1 = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, orientation='vertical')
    cb1.set_label('Average # Elephants per day')
    # Set custom ticks if needed (here just showing min and max)
    tick_values = np.linspace(min_val, max_val, num=11)
    cb1.set_ticks(tick_values)
    cb1.set_ticks(tick_values)
    # cb1.set_ticklabels([f'{min_val}', f'{max_val}'])
    cb1.set_ticklabels([f'{val.round(1)}' for val in tick_values])
    if not show:
        plt.close()
    #fig.tight_layout()
    fig.subplots_adjust(top=0.90)
    return fig