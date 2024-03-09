import os
import argparse

def print_structure_tree(dataset_path):
    """
    Reports the number of files in each specified subdirectory within the dataset using ASCII art for the directory tree.

    Parameters:
    - dataset_path (str): The base path of the dataset, which contains 'images' and 'labels' directories.
    """

    def count_files(dir_path):
        """Helper function to count files in a given directory."""
        return len([name for name in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, name))])

    # Define the structure of directories to report
    dirs_structure = {
        'images': ['train', 'val', 'test'],
        'labels': ['train', 'val', 'test'],
    }
    print(dataset_path)
    for main_dir, sub_dirs in dirs_structure.items():
        if main_dir == 'images':
            print(f"├── {main_dir}")
        else:
            print(f"└── {main_dir}")
        for i, sub_dir in enumerate(sub_dirs):
            branch = "└──" if i == len(sub_dirs) - 1 else "├──"
            full_dir_path = os.path.join(dataset_path, main_dir, sub_dir)
            if os.path.exists(full_dir_path):
                num_files = count_files(full_dir_path)
                if main_dir == 'images':
                    print(f"│   {branch} {sub_dir}: {num_files} files")
                else:
                    print(f"    {branch} {sub_dir}: {num_files} files")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Show counts of files in directories of YOLO format directory.")
    parser.add_argument("--path_dir", type=str, help="Path to the directory containing YOLO format directory.")
    
    args = parser.parse_args()
    print_structure_tree(args.path_dir)