"""Audio normalization module for adjusting mp3 volume levels."""

import os
import argparse
from pathlib import Path
from pydub import AudioSegment

from utils import get_file_strings
from process_class import ProcessClass
from constants import NORMALIZED_DIR


class FileNotSupported(Exception):
    """Raised when a file with an unsupported extension is processed."""


class AudioNormalizer(ProcessClass):
    """Normalizes the volume of an mp3 file to a target dBFS level."""

    def __init__(self, audio_path: str, target_dbfs: float) -> None:
        """Init method for the AudioNormalizer class.

        Args:
            audio_path: Path to audio file.
            target_dbfs: Target volume level in decibels relative to full scale.
        """
        self.audio_path = audio_path
        self.target_dbfs = target_dbfs
        self.audio_name, self.audio_ext = get_file_strings(self.audio_path)
        self.normalized_dir: Path = NORMALIZED_DIR

    def process_file(self) -> None:
        """Normalize the audio file to the target dBFS level and export it.

        Raises:
            FileNotSupported: If the file is not an mp3.
        """
        if self.audio_ext != "mp3":
            raise FileNotSupported(
                f"{self.audio_ext} files are not supported! Use mp3 for now!"
            )
        os.makedirs(self.normalized_dir, exist_ok=True)
        print(f"Normalizing {self.audio_name}...")
        sound = AudioSegment.from_mp3(self.audio_path)
        audio_diff = self.target_dbfs - sound.dBFS
        normalized_audio = sound.apply_gain(audio_diff)
        normalized_audio.export(
            self.normalized_dir / f"{self.audio_name}_norm.{self.audio_ext}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--audio_path", type=str, default=None, help="Path to audio file to normalize."
    )
    parser.add_argument(
        "--dBFS", type=float, default=-30, help="Target dBFS. Defaults to -30."
    )
    args = parser.parse_args()
    an = AudioNormalizer(args.audio_path, args.dBFS)
    an.process_file()
