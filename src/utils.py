import os
from typing import Tuple, List, Callable


def get_file_strings(file_path: str, full_path=False) -> Tuple[str, str]:
    """Split file path name into name / file extension.

    Args:
        file_path (str): Path to file.
        full_path (bool, optional): True if the full path
            will be used for the file name return string.
            Defaults to False.

    Returns:
        Tuple[str, str]: File name string and image
            extension string.
    """

    file_strings = file_path.rsplit(".", 1)
    file_name = file_strings[0]
    if not full_path:
        file_name = file_name.replace("\\", "/")
        file_name = file_name.rsplit("/", 1)[-1]
    file_ext = file_strings[-1]
    return file_name, file_ext


def is_valid_ext(file_path:str, ext_list: List[str]) -> bool:
    """Check if file has a valid extension.

    Args:
        file_path (str): File path (ex: mydir/my_file.txt)

    Returns:
        bool: Bool indicating if the file is a
            valid file based on the extension.
    """
    _, file_ext = get_file_strings(file_path)
    return file_ext in ext_list


def process_all_files(file_dir: str, ext_list: List[str], process_class: Callable, **kwargs) -> None:
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
                print(f"{file_path} might not be a video file, not processing it for now.")

    for file_path in file_paths:
        process_class(file_path, **kwargs).process_file()