from collections.abc import Collection


def get_file_strings(file_path: str, full_path: bool = False) -> tuple[str, str]:
    """Split file path name into name / file extension.

    Args:
        file_path (str): Path to file.
        full_path (bool, optional): True if the full path
            will be used for the file name return string.
            Defaults to False.

    Returns:
        tuple[str, str]: File name string and file
            extension string.
    """

    file_strings = file_path.rsplit(".", 1)
    file_name = file_strings[0]
    if not full_path:
        file_name = file_name.replace("\\", "/")
        file_name = file_name.rsplit("/", 1)[-1]
    file_ext = file_strings[-1]
    return file_name, file_ext


def is_valid_ext(file_path: str, ext_list: Collection[str]) -> bool:
    """Check if file has a valid extension.

    Args:
        file_path (str): File path (ex: mydir/my_file.txt)
        ext_list (Collection[str]): Collection of valid extensions to check against.

    Returns:
        bool: Bool indicating if the file is a
            valid file based on the extension.
    """
    _, file_ext = get_file_strings(file_path)
    return file_ext in ext_list
