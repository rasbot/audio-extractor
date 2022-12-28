import os
import argparse
from typing import List
from constants import AUDIO_EXTS
from utils import get_file_strings
from audio_tagger import AudioTagger


def is_audio_ext(file_path:str, ext_list: List[str]) -> bool:
    """Check if file has a valid video extension.

    Args:
        file_path (str): File path (ex: mydir/my_file.txt)

    Returns:
        bool: Bool indicating if the file is a
            valid video file based on the extension.
    """
    _, file_ext = get_file_strings(file_path)
    return file_ext in ext_list


def tag_all_audios(file_dir: str, ext_list: List[str]) -> None:
    """Tag audio files in specified directory. Will tag
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
            if is_audio_ext(file_path, ext_list):
                file_paths.append(file_path)
            else:
                print(f"{file_path} might not be a video file, not processing it for now.")

    for file_path in file_paths:
        AudioTagger(file_path).tag_audio()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dir",
        type=str,
        default=os.getcwd(),
        help="Directory containing audio files to tag."
    )
    parser.add_argument(
        "--artist",
        type=str,
        default="default artist",
        help="artist tag for mp3 file - Defaults to 'default artist'."
    )
    parser.add_argument(
        "--album",
        type=str,
        default="default album",
        help="album tag for mp3 file - Defaults to 'default album'."
    )
    args = parser.parse_args()
    tagger = AudioTagger(
    args.audio_path,
    args.artist,
    args.album,
    args.title,
    )
    tag_all_audios(args.dir, AUDIO_EXTS, artist_tag=args.artist, album_tag=args.album)
