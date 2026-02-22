"""CLI entry point for batch mp3 tagging from a directory of audio files."""

import argparse
import os

from audio_tagger import AudioTagger
from constants import AUDIO_EXTS
from files_processor import process_all_files

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dir",
        type=str,
        default=os.getcwd(),
        help="Directory containing audio files to tag.",
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
    process_all_files(
        args.dir, AUDIO_EXTS, AudioTagger, artist_tag=args.artist, album_tag=args.album
    )
