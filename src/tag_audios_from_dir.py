"""CLI entry point for batch mp3 tagging from a directory of audio files."""

import argparse
from pathlib import Path

from audio_tagger import AudioTagger
from constants import AUDIO_EXTS, DEFAULT_ALBUM, DEFAULT_ARTIST
from files_processor import process_all_files

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dir",
        type=str,
        default=str(Path.cwd()),
        help="Directory containing audio files to tag.",
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
    process_all_files(
        args.dir, AUDIO_EXTS, AudioTagger, artist_tag=args.artist, album_tag=args.album
    )
