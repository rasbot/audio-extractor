import os
import argparse
from constants import AUDIO_EXTS
from files_processor import process_all_files
from audio_normalizer import AudioNormalizer


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dir",
        type=str,
        default=os.getcwd(),
        help="Directory containing audio files to normalize.",
    )
    parser.add_argument(
        "--dBFS", type=int, default=-30, help="Target dBFS. Defaults to -30."
    )
    args = parser.parse_args()
    process_all_files(args.dir, AUDIO_EXTS, AudioNormalizer, target_dbfs=args.dBFS)
