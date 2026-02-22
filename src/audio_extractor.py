"""Audio extraction module for converting video files to mp3 format."""

import os
import argparse
from pathlib import Path
from moviepy import VideoFileClip

from utils import get_file_strings
from process_class import ProcessClass
from constants import EXTRACTED_DIR


class AudioExtractor(ProcessClass):
    """Processes a video file and extracts its audio as an mp3."""

    def __init__(self, vid_path: str, audio_name: str | None = None) -> None:
        """Init method for the AudioExtractor class.

        Args:
            vid_path: Path to video file.
            audio_name: Name for the output audio file. If None, the video
                filename is used. Defaults to None.

        Raises:
            FileNotFoundError: If vid_path does not point to a valid file.
        """
        if not os.path.isfile(vid_path):
            raise FileNotFoundError(f"{vid_path} does not point to a valid file!")
        self.vid_path = vid_path
        if not audio_name:
            self.audio_name, _ = get_file_strings(self.vid_path)
        else:
            self.audio_name = audio_name
        self.audio_dir: Path = EXTRACTED_DIR

    def get_clip(self) -> VideoFileClip:
        """Load the video file as a clip.

        Returns:
            The loaded video file clip.
        """
        return VideoFileClip(self.vid_path)

    def process_file(self) -> None:
        """Extract audio from the video file and write it as an mp3.

        Raises:
            ValueError: If the video file has no audio track.
        """
        clip = self.get_clip()
        try:
            if clip.audio is None:
                raise ValueError(
                    f"Video file {self.vid_path!r} has no audio track."
                )
            os.makedirs(self.audio_dir, exist_ok=True)
            print(f"\nExtracting audio for {self.audio_name}...\n")
            clip.audio.write_audiofile(self.audio_dir / f"{self.audio_name}.mp3")
            print("\nFinished extracting audio!\n")
        finally:
            clip.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--vid_path",
        type=str,
        default=None,
        help="File path to video file that will have audio extracted from.",
    )
    args = parser.parse_args()
    ae = AudioExtractor(args.vid_path)
    ae.process_file()
