"""CLI entry point for batch audio extraction from a directory of video files."""

import argparse
from pathlib import Path

from audio_extractor import AudioExtractor
from constants import VID_EXTS
from files_processor import process_all_files

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dir",
        type=str,
        default=str(Path.cwd()),
        help="Directory containing video files to extract audio from.",
    )
    args = parser.parse_args()
    process_all_files(args.dir, VID_EXTS, AudioExtractor)
