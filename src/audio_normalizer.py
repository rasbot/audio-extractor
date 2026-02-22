"""Audio normalization module for adjusting mp3 volume levels."""

import argparse
from pathlib import Path

from pydub import AudioSegment

from constants import DEFAULT_DBFS, NORMALIZED_DIR
from process_class import ProcessClass
from utils import get_file_strings

__all__ = ["AudioNormalizer", "FileNotSupportedError"]


class FileNotSupportedError(Exception):
    """Raised when a file with an unsupported extension is processed."""


class AudioNormalizer(ProcessClass):
    """Normalizes the volume of an mp3 file to a target dBFS level."""

    def __init__(self, audio_path: str, target_dbfs: float) -> None:
        """Init method for the AudioNormalizer class.

        Args:
            audio_path: Path to audio file.
            target_dbfs: Target volume level in decibels relative to full scale.

        Raises:
            FileNotFoundError: If audio_path does not point to a valid file.
        """
        if not Path(audio_path).is_file():
            raise FileNotFoundError(f"{audio_path} does not point to a valid file!")
        self.audio_path = audio_path
        self.target_dbfs = target_dbfs
        self.audio_name, self.audio_ext = get_file_strings(self.audio_path)
        self.normalized_dir: Path = NORMALIZED_DIR

    def process_file(self) -> None:
        """Normalize the audio file to the target dBFS level and export it.

        Raises:
            FileNotSupportedError: If the file is not an mp3.
        """
        if self.audio_ext != "mp3":
            raise FileNotSupportedError(
                f"{self.audio_ext} files are not supported! Use mp3 for now!"
            )
        self.normalized_dir.mkdir(parents=True, exist_ok=True)
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
        "--audio_path",
        type=str,
        required=True,
        help="Path to audio file to normalize.",
    )
    parser.add_argument(
        "--dBFS",
        type=float,
        default=DEFAULT_DBFS,
        help=f"Target dBFS. Defaults to {DEFAULT_DBFS}.",
    )
    args = parser.parse_args()
    an = AudioNormalizer(args.audio_path, args.dBFS)
    an.process_file()
