import os

def get_file_tree(start_path=".", exclude_dirs=[".git", "__pycache__", "venv", ".venv", "node_modules"]):
    """
    Generates a string representation of the file directory tree.
    
    Args:
        start_path (str): The directory to start the tree from. Defaults to ".".
        exclude_dirs (list): List of directory names to exclude from the tree.
        
    Returns:
        str: A string representing the file tree.
    """
    tree_str = ""
    for root, dirs, files in os.walk(start_path):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        level = root.replace(start_path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        tree_str += '{}{}/\n'.format(indent, os.path.basename(root))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            tree_str += '{}{}\n'.format(subindent, f)
            
    return tree_str
