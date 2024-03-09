import os
import shutil
from glob import glob
import numpy as np
import random
import tqdm
import argparse
import re
from sklearn.model_selection import train_test_split

RATIOS = [0.7, 0.15, 0.15]
IMAGE_EXTENSION = 'png'
LABEL_EXTENSION = 'txt'
PATTERN = re.compile(r'screenshot(\d+)_(\d{2})_(\d{2})__(\d{2})_(\d{2})\.(txt|png)')
DEFAULT_PATH_DIR = '../test_data'
DEFAULT_TARGET = './target'
                
def calc_keep_ratio(len_images, len_labels, target_ratio=0.1):
    """
    Calculate the ratio of images without labels to keep, in order to achieve a specified target ratio of unlabeled images.

    Parameters:
    - len_images (int): The total number of images in the dataset.
    - len_labels (int): The number of images in the dataset that have corresponding labels.
    - target_ratio (float, optional): The desired ratio of unlabeled images to total images in the dataset. Default is 0.1.

    Returns:
    - float: The calculated keep ratio for images without labels. This ratio ensures that, after potentially discarding some
      unlabeled images, the proportion of unlabeled images in the dataset is close to the target_ratio.
    """
    assert len_images >= len_labels
    len_no_label = len_images - len_labels
    if(len_no_label/len_images <= target_ratio):
        return 1
    target_num = (1/(1-target_ratio))*len_labels
    keep_ratio = (target_num-len_labels)/len_no_label
    return keep_ratio
    
def data_split(path_dir, target, create_new=True, keep_empty=False):
    """
    Split a dataset into training, validation, and test sets, and copy the respective images and labels into target directories.

    Parameters:
    - path_dir (str): The directory path where the original dataset is located. This directory should contain 'images' and 'labels' subdirectories.
    - target (str): The target directory path where the split datasets will be stored. This function will create 'train', 'val', and 'test' subdirectories within 'images' and 'labels' directories at this location.
    - create_new (bool, optional): Flag to indicate whether add new files to the possibly existing target or rewrite it. Default is True.
    - keep_empty (bool, optional): A flag to indicate whether to keep images without corresponding labels in the split datasets. Default is False.
    
    """
    image_dir = os.path.join(path_dir, 'images')
    label_dir = os.path.join(path_dir, 'labels')

    # List all image files, assuming JPEG format for images
    image_files = [os.path.splitext(img)[0] for img in os.listdir(image_dir) if PATTERN.match(img)]
    len_images = len(image_files)
    # print(f'len = {len(image_files)}')

    train_files, rest_files = train_test_split(image_files, test_size=RATIOS[1]+RATIOS[2], random_state=42)
    val_files, test_files = train_test_split(rest_files, test_size=RATIOS[1]/(RATIOS[1] + RATIOS[2]), random_state=42)

    # print(f'len = {len(train_files)}')
    # print(f'len = {len(val_files)}, len = {len(test_files)} ')
    # print(f'sum = {len(train_files) + len(val_files) + len(test_files)}')
    # print(set(val_files).intersection(set(test_files)))
    len_labels = len([os.path.splitext(label)[0] for label in os.listdir(label_dir) if PATTERN.match(label)])
    keep_ratio = calc_keep_ratio(len_images, len_labels)
    # print(keep_ratio)
    

    def copy_files(file_list, image_dir, label_dir, target_image_dir, target_label_dir):
        for filename in tqdm.tqdm(file_list):
            image_filename = f"{filename}.{IMAGE_EXTENSION}"
            label_filename = f"{filename}.{LABEL_EXTENSION}"

            image_path = os.path.join(image_dir, image_filename)
            label_path = os.path.join(label_dir, label_filename)
            image_target_path = os.path.join(target_image_dir, image_filename)
            label_target_path = os.path.join(target_label_dir, label_filename)
            if os.path.exists(label_path):
                shutil.copy(image_path, image_target_path)
                shutil.copy(label_path, label_target_path)
            else:
                if keep_empty and random.random() < keep_ratio:
                    shutil.copy(image_path, image_target_path)

                
    # Directories for the split datasets
    train_img_dir = os.path.join(target, 'images/train')
    train_label_dir = os.path.join(target, 'labels/train')
    val_img_dir = os.path.join(target, 'images/val')
    val_label_dir = os.path.join(target, 'labels/val')
    test_img_dir = os.path.join(target, 'images/test')
    test_label_dir = os.path.join(target, 'labels/test')

    if create_new and os.path.exists(target):
        shutil.rmtree(target)
    directories = [train_img_dir, train_label_dir, val_img_dir, val_label_dir, test_img_dir, test_label_dir]

    for dir in directories:
        os.makedirs(dir, exist_ok=not create_new)


    # Copy files for each set
    copy_files(train_files, image_dir, label_dir, train_img_dir, train_label_dir)
    copy_files(val_files, image_dir, label_dir, val_img_dir, val_label_dir)
    copy_files(test_files, image_dir, label_dir, test_img_dir, test_label_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split dataset into training, validation, and test sets.")
    parser.add_argument("--path_dir", type=str, default=DEFAULT_PATH_DIR, help="Path to the directory containing 'images' and 'labels' folders.")
    parser.add_argument("--target", type=str, default=DEFAULT_TARGET, help="Target directory where the split datasets will be stored.")
    parser.add_argument("--create_new", action='store_true', help="Flag to indicate whether add new files to the possibly existing target or rewrite it", default=False)
    parser.add_argument("--keep_empty", action='store_true', help="Flag to indicate whether to keep images without corresponding labels in the dataset.", default=False)    

    args = parser.parse_args()
    data_split(args.path_dir, args.target, args.keep_empty)
    
