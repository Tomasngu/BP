import os

def rewrite_classes(directory_path, old_class=0, new_class=20):
    """
    Rewrite class indices in YOLO format annotation files from old_class to new_class.

    Parameters:
    directory_path (str): The path to the directory containing YOLO format txt files.
    old_class (int): The class index to replace.
    new_class (int): The new class index to use instead.
    """
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r') as file:
                lines = file.readlines()
            modified_lines = []
            for line in lines:
                parts = line.strip().split()
                if len(parts) > 1 and int(parts[0]) == old_class:
                    parts[0] = str(new_class)
                modified_lines.append(" ".join(parts))
            with open(file_path, 'w') as file:
                for line in modified_lines:
                    file.write(line + '\n')
