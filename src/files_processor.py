"""Batch file processing module for running processors across directories."""

import argparse
from collections.abc import Callable, Collection
from pathlib import Path
from typing import Any

from audio_extractor import AudioExtractor
from audio_normalizer import AudioNormalizer
from audio_tagger import AudioTagger
from constants import (
    AUDIO_EXTS,
    DEFAULT_ALBUM,
    DEFAULT_ARTIST,
    DEFAULT_DBFS,
    EXTRACTED_DIR,
    NORMALIZED_DIR,
    VID_EXTS,
)
from utils import is_valid_ext

__all__ = ["process_all_files"]


def process_all_files(
    file_dir: str | Path,
    ext_list: Collection[str],
    process_class: Callable[..., Any],
    **kwargs: Any,
) -> None:
    """Process all matching files in a directory using the given processor.

    Args:
        file_dir: Directory containing files to process.
        ext_list: Collection of valid file extensions to match against.
        process_class: Processor class to instantiate and call for each file.
        **kwargs: Additional keyword arguments forwarded to process_class.
    """
    dir_path = Path(file_dir)
    file_paths: list[str] = []
    for entry in dir_path.iterdir():
        if entry.is_file() and is_valid_ext(str(entry), ext_list):
            file_paths.append(str(entry))

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
        "--dBFS",
        type=float,
        default=DEFAULT_DBFS,
        help=f"Target dBFS. Defaults to {DEFAULT_DBFS}.",
    )
    parser.add_argument(
        "--artist",
        type=str,
        default=DEFAULT_ARTIST,
        help=f"artist tag for mp3 file - Defaults to {DEFAULT_ARTIST!r}.",
    )
    parser.add_argument(
        "--album",
        type=str,
        default=DEFAULT_ALBUM,
        help=f"album tag for mp3 file - Defaults to {DEFAULT_ALBUM!r}.",
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
