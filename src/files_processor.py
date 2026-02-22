"""Batch file processing module for running processors across directories."""

import argparse
import os
from collections.abc import Callable, Collection
from pathlib import Path

from audio_extractor import AudioExtractor
from audio_normalizer import AudioNormalizer
from audio_tagger import AudioTagger
from constants import AUDIO_EXTS, EXTRACTED_DIR, NORMALIZED_DIR, VID_EXTS
from utils import is_valid_ext


def process_all_files(
    file_dir: str | Path, ext_list: Collection[str], process_class: Callable, **kwargs
) -> None:
    """Process all matching files in a directory using the given processor.

    Args:
        file_dir: Directory containing files to process.
        ext_list: Collection of valid file extensions to match against.
        process_class: Processor class to instantiate and call for each file.
        **kwargs: Additional keyword arguments forwarded to process_class.
    """
    file_names = os.listdir(file_dir)

    file_paths: list[str] = []
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dir", type=str, default="./data", help="Directory with files to process."
    )
    parser.add_argument(
        "--extract",
        action="store_true",
        help="Extract flag - extracts audio from videos in directory.",
    )
    parser.add_argument(
        "--normalize",
        action="store_true",
        help="Normalize flag - normalize audio of files in directory.",
    )
    parser.add_argument(
        "--tag",
        action="store_true",
        help="Tag flag - tag audio from files in directory.",
    )
    parser.add_argument(
        "--dBFS", type=float, default=-30, help="Target dBFS. Defaults to -30."
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
        audio_dir = EXTRACTED_DIR if args.extract else args.dir
        process_all_files(audio_dir, AUDIO_EXTS, AudioNormalizer, target_dbfs=args.dBFS)
    if args.tag:
        if args.normalize:
            audio_dir = NORMALIZED_DIR
        elif args.extract:
            audio_dir = EXTRACTED_DIR
        else:
            audio_dir = args.dir
        process_all_files(
            audio_dir,
            AUDIO_EXTS,
            AudioTagger,
            artist_tag=args.artist,
            album_tag=args.album,
        )
