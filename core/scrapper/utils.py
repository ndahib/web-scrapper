import os
from ..constants import DEFAULT_PATH


def create_directory(path=DEFAULT_PATH):
    if not os.path.exists(path):
        print(f"Creating directory: {path}")
        os.makedirs(path)
    elif not os.path.isdir(path):
        raise NotADirectoryError(f"The path {path} is not a directory.")
    elif not os.access(path, os.W_OK) or not os.access(path, os.X_OK):
        raise PermissionError(f"The directory {path} is not writable or executable.")
    return path
