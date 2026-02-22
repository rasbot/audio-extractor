"""Utility functions for file path parsing and extension validation."""

from collections.abc import Collection
from pathlib import Path

__all__ = ["get_file_strings", "is_valid_ext"]


def get_file_strings(file_path: str | Path, full_path: bool = False) -> tuple[str, str]:
    """Split a file path into name and file extension.

    Args:
        file_path: Path to file.
        full_path: If True, the full path is used as the file name rather
            than just the base name. Defaults to False.

    Returns:
        A tuple of (file_name, file_extension). If the path has no extension,
        file_extension is an empty string.
    """
    path_str = str(file_path)
    parts = path_str.rsplit(".", 1)
    if len(parts) == 1:
        file_name = parts[0]
        if not full_path:
            file_name = file_name.replace("\\", "/").rsplit("/", 1)[-1]
        return file_name, ""
    file_name = parts[0]
    if not full_path:
        file_name = file_name.replace("\\", "/").rsplit("/", 1)[-1]
    file_ext = parts[1]
    return file_name, file_ext


def is_valid_ext(file_path: str | Path, ext_list: Collection[str]) -> bool:
    """Check if a file has a valid extension.

    Args:
        file_path: File path (ex: mydir/my_file.txt).
        ext_list: Collection of valid extensions to check against.

    Returns:
        True if the file extension is in ext_list, False otherwise.
    """
    _, file_ext = get_file_strings(file_path)
    return file_ext in ext_list
