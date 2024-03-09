import os
import shutil
from .JSON2YOLO.general_json2yolo import convert_coco_json

DEFAULT_DIR = 'new_dir'

def reorganize_files(images_dir, json_file, new_base_dir):
    """
    Moves a directory of images and a JSON file into structured subdirectories within 'data'.
    
    Parameters:
    - images_dir (str): Source directory for images.
    - json_file (str): Filename of the JSON to relocate.
    - new_base_dir (str): Base path for creating 'images' and 'labels' subdirectories.
    
    The 'images' are moved to 'data/images' and the JSON file to 'data/labels/{name}'.
    """
    # Define new directory paths
    labels_dir = os.path.join('new_dir', 'labels', os.path.splitext(json_file)[0])
    new_images_dir = os.path.join(new_base_dir, 'images')
    new_labels_dir = os.path.join(new_base_dir, 'labels')

    # Create the new directories
    if os.path.exists(new_base_dir):
        shutil.rmtree(new_base_dir)
    os.makedirs(new_base_dir, exist_ok=False)

    # Move the JSON file to the new directory
    shutil.move(images_dir, new_images_dir)
    shutil.move(labels_dir, new_labels_dir)

    print(f"All images moved to {new_images_dir}")
    print(f"All labels moved to {new_labels_dir}")

def convert_json(images_dir, json_file, new_base_dir):
    
    if os.path.exists(DEFAULT_DIR):
        shutil.rmtree(DEFAULT_DIR)
    convert_coco_json(json_dir=os.path.dirname(json_file), use_segments=False, cls91to80=False)
    labels_dir = os.path.join('new_dir', 'labels', os.path.splitext(json_file)[0])
    files = [label for label in os.listdir(labels_dir)]
    print(f'Converted {len(files)} labels from {json_file}')
    reorganize_files(images_dir, json_file, new_base_dir)
    if os.path.exists(DEFAULT_DIR):
        shutil.rmtree(DEFAULT_DIR)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert COCO JSON annotations to YOLO format and reorganize files.")
    parser.add_argument("images_dir", type=str, help="Directory containing images.")
    parser.add_argument("json_file", type=str, help="Path to the COCO JSON file.")
    parser.add_argument("new_base_dir", type=str, help="The base directory to store the converted dataset.")

    args = parser.parse_args()

    convert_json(args.images_dir, args.json_file, args.new_base_dir)