import os
import shutil

def copy_files(src_dir, target_dir):
    """
    Copy files from the source directory to the destination if they do not exist.

    Parameters:
    - src_dir (str): The path to the source directory.
    - target_dir (str): The path to the destination directory.
    """

    source_files = os.listdir(src_dir)
    destination_files = os.listdir(target_dir)

    for filename in source_files:
        source_file_path = os.path.join(src_dir, filename)
        destination_file_path = os.path.join(target_dir, filename)
        if filename not in destination_files:
            shutil.copy2(source_file_path, destination_file_path)


def count_lines(directory):
    """
    Count the number of lines in all text files within the specified directory.

    Parameters:
    - directory (str): The path to the directory whose files will be counted for lines.
    """
    total_lines = 0
    file_line_counts = {}
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    for file in files:
        file_path = os.path.join(directory, file)
        with open(file_path, 'r') as f:
            line_count = sum(1 for line in f)
            file_line_counts[file] = line_count
            total_lines += line_count
    
    return total_lines, file_line_counts