import os
from typing import List, Callable
from utils import is_valid_ext


def process_all_files(
    file_dir: str, ext_list: List[str], process_class: Callable, **kwargs
) -> None:
    """Process all files in specified directory. Will process
    files if they match an extension in the ext_list variable.

    Args:
        file_dir (str): Directory containing files.
        ext_list (List[str]): List of valid extensions to check against.
        process_class (Callable): Specific processing class to use.
    """
    file_names = os.listdir(file_dir)

    file_paths = []
    for file_name in file_names:
        file_path = os.path.join(file_dir, file_name)
        if os.path.isfile(file_path):
            if is_valid_ext(file_path, ext_list):
                file_paths.append(file_path)
            else:
                print(
                    f"{file_path} might not be a video file, not processing it for now."
                )

    for file_path in file_paths:
        process_class(file_path, **kwargs).process_file()
