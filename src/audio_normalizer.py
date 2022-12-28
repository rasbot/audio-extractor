import os
import argparse
from pydub import AudioSegment

from utils import get_file_strings


class FileNotSupported(Exception):
    pass


class AudioNormalizer:
    def __init__(self, audio_path: str, target_dBFS: int) -> None:
        self.audio_path = audio_path
        self.target_dBFS = target_dBFS
        self.audio_name, self.audio_ext = get_file_strings(self.audio_path)

    def process_file(self):
        if self.audio_ext != 'mp3':
            raise FileNotSupported(f"{self.audio_ext} files are not supported! Use mp3 for now!")
        print(f"\nNormalizing {self.audio_name}...\n")
        sound = AudioSegment.from_mp3(self.audio_path)
        audio_diff = self.target_dBFS - sound.dBFS
        normalized_audio = sound.apply_gain(audio_diff)
        normalized_audio.export(f"data/extracted_audio/{self.audio_name}_norm.{self.audio_ext}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--audio_path",
        type=str,
        default=None,
        help="Path to audio file to normalize."
    )
    parser.add_argument(
        "--dBFS",
        type=int,
        default=-30,
        help="Target dBFS. Defaults to -30."
    )
    args = parser.parse_args()
    an = AudioNormalizer(args.audio_path, args.dBFS)
    an.process_file()
