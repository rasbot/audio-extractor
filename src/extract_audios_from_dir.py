import os
import argparse
from typing import List
from constants import VID_EXTS
from utils import get_file_strings
from audio_extractor import AudioExtractor


def is_video_ext(file_path:str, ext_list: List[str]) -> bool:
    """Check if file has a valid video extension.

    Args:
        file_path (str): File path (ex: mydir/my_file.txt)

    Returns:
        bool: Bool indicating if the file is a
            valid video file based on the extension.
    """
    _, file_ext = get_file_strings(file_path)
    return file_ext in ext_list


def extract_all_audios(file_dir: str, ext_list: List[str]) -> None:
    """Extract audio from all files in specified directory. Will extract
    files if they match an extension in the ext_list variable.

    Args:
        file_dir (str): Directory containing files.
        ext_list (List[str]): List of valid extensions to check against.
    """
    file_names = os.listdir(file_dir)

    file_paths = []
    for file_name in file_names:
        file_path = os.path.join(file_dir, file_name)
        if os.path.isfile(file_path):
            if is_video_ext(file_path, ext_list):
                file_paths.append(file_path)
            else:
                print(f"{file_path} might not be a video file, not processing it for now.")

    for file_path in file_paths:
        AudioExtractor(file_path).extract_audio()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dir",
        type=str,
        default=os.getcwd(),
        help="Directory containing video files to extract audio from."
    )
    args = parser.parse_args()
    extract_all_audios(args.dir, VID_EXTS, AudioExtractor)
