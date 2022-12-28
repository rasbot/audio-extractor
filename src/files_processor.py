import os
import argparse
from typing import List, Callable
from constants import VID_EXTS, AUDIO_EXTS
from utils import is_valid_ext
from audio_extractor import AudioExtractor
from audio_tagger import AudioTagger
from audio_normalizer import AudioNormalizer


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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dir",
        type=str,
        default='./data',
        help="Directory with files to process."
    )
    parser.add_argument(
        "--extract",
        action="store_true",
        help="Extract flag - extracts audio from videos in directory."
    )
    parser.add_argument(
        "--normalize",
        action="store_true",
        help="Normalize flag - normalize audio of files in directory."
    )
    parser.add_argument(
        "--tag",
        action="store_true",
        help="Tag flag - tag audio from files in directory."
    )
    parser.add_argument(
        "--dBFS",
        type=int,
        default=-30,
        help="Target dBFS. Defaults to -30."
    )
    parser.add_argument(
        "--artist",
        type=str,
        default="default artist",
        help="artist tag for mp3 file - Defaults to 'default artist'.",
    )
    parser.add_argument(
        "--album",
        type=str,
        default="default album",
        help="album tag for mp3 file - Defaults to 'default album'.",
    )
    args = parser.parse_args()
    if args.extract:
        process_all_files(args.dir, VID_EXTS, AudioExtractor)
    if args.normalize:
        if args.extract:
            audio_dir = './data/extracted_audio'
        else:
            audio_dir = args.dir
        process_all_files(audio_dir, AUDIO_EXTS, AudioNormalizer, target_dbfs=args.dBFS)
    if args.tag:
        if args.normalize:
            audio_dir = './data/normalized_audio'
        elif args.extract:
            audio_dir = './data/extracted_audio'
        else:
            audio_dir = args.dir
        process_all_files(
            audio_dir, AUDIO_EXTS, AudioTagger, artist_tag=args.artist, album_tag=args.album
        )
