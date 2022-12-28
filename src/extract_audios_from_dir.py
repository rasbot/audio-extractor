import os
import argparse
from constants import VID_EXTS
from files_processor import process_all_files
from audio_extractor import AudioExtractor


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dir",
        type=str,
        default=os.getcwd(),
        help="Directory containing video files to extract audio from."
    )
    args = parser.parse_args()
    process_all_files(args.dir, VID_EXTS, AudioExtractor)
