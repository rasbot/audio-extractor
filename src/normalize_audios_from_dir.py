"""CLI entry point for batch audio normalization from a directory of mp3 files."""

import argparse
from pathlib import Path

from audio_normalizer import AudioNormalizer
from constants import AUDIO_EXTS, DEFAULT_DBFS
from files_processor import process_all_files

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dir",
        type=str,
        default=str(Path.cwd()),
        help="Directory containing audio files to normalize.",
    )
    parser.add_argument(
        "--dBFS",
        type=float,
        default=DEFAULT_DBFS,
        help=f"Target dBFS. Defaults to {DEFAULT_DBFS}.",
    )
    args = parser.parse_args()
    process_all_files(args.dir, AUDIO_EXTS, AudioNormalizer, target_dbfs=args.dBFS)
