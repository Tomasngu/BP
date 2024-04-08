import os
import shutil
import numpy as np
import tqdm

def split_files(source_dir, dest_dir_label, dest_dir_blank):
    """
    Splits files from the source directory into two directories based on content

    Parameters:
    - source_dir: Path to the source directory containing the files to be split.
    - dest_dir_label: Path to the destination directory for files with image content.
    - dest_dir_blank: Path to the destination directory for files which are blank.
    """
    # Ensure destination directories exist
    os.makedirs(dest_dir_label, exist_ok=True)
    os.makedirs(dest_dir_blank, exist_ok=True)

    # Iterate over all files in the source directory
    for filename in tqdm.tqdm(os.listdir(source_dir)):
        # Build the full file path
        file_path = os.path.join(source_dir, filename)
        image_np = cv2.imread(file_path)
        zero_pixels_count = np.sum(np.all(image_np == 0, axis=-1))
        total_pixels = image_np.shape[0] * image_np.shape[1]
        # Skip directories, only process files
        if os.path.isfile(file_path):
            # Check if the filename has content
            if zero_pixels_count/total_pixels < 0.6:
                # Move the file to dest_dir_label
                shutil.move(file_path, os.path.join(dest_dir_label, filename))
            else:
                # Move the file to dest_dir_blank
                shutil.move(file_path, os.path.join(dest_dir_blank, filename))

# Example usage
def main(input_dir):
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get annotations from your data.')
    parser.add_argument("--input_dir", default=INPUT_DIR, help="Input your image directory.")
    args = parser.parse_args()
    main(args.dir)

