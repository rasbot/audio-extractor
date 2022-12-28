import argparse
from pydub import AudioSegment

from utils import get_file_strings


class FileNotSupported(Exception):
    """Exception to throw if file is not a supported extension."""


class AudioNormalizer:
    """AudioNormalizer class to normalize audio of mp3 file."""

    def __init__(self, audio_path: str, target_dbfs: int) -> None:
        """Init method for the `AudioNormalizer` class.

        Args:
            audio_path (str): Path to audio file.
            target_dbfs (int): Decibels relative to full scale target value.
        """
        self.audio_path = audio_path
        self.target_dbfs = target_dbfs
        self.audio_name, self.audio_ext = get_file_strings(self.audio_path)

    def process_file(self):
        """Normalize audio of an mp3 file based on a target dBFS value.

        Raises:
            FileNotSupported: Throw an exception if the file is not an mp3.
        """
        if self.audio_ext != "mp3":
            raise FileNotSupported(
                f"{self.audio_ext} files are not supported! Use mp3 for now!"
            )
        print(f"\nNormalizing {self.audio_name}...\n")
        sound = AudioSegment.from_mp3(self.audio_path)
        audio_diff = self.target_dbfs - sound.dBFS
        normalized_audio = sound.apply_gain(audio_diff)
        normalized_audio.export(
            f"data/extracted_audio/{self.audio_name}_norm.{self.audio_ext}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--audio_path", type=str, default=None, help="Path to audio file to normalize."
    )
    parser.add_argument(
        "--dBFS", type=int, default=-30, help="Target dBFS. Defaults to -30."
    )
    args = parser.parse_args()
    an = AudioNormalizer(args.audio_path, args.dBFS)
    an.process_file()
