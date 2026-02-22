import os
import argparse
from moviepy import VideoFileClip

from utils import get_file_strings
from process_class import ProcessClass
from constants import EXTRACTED_DIR


class AudioExtractor(ProcessClass):
    """AudioExtractor class to process a video file and extract audio
    to mp3 format.
    """

    def __init__(self, vid_path: str, audio_name: str = None) -> None:
        """Init method for the `AudioExtractor` class.

        Args:
            vid_path (str): Path to video file.
            audio_name (str): String used to name audio file. If None, the name
                of the video file will be used. Defaults to None.

        Raises:
            AttributeError: If the file_path is not a file, raise exception.
        """

        if not os.path.isfile(vid_path):
            raise AttributeError(f"{vid_path} does not point to a valid file!")
        self.vid_path = vid_path
        if not audio_name:
            self.audio_name, _ = get_file_strings(self.vid_path)
        else:
            self.audio_name = audio_name
        self.audio_dir = str(EXTRACTED_DIR)

    def get_clip(self) -> VideoFileClip:
        """Returns the clip of a video file.

        Returns:
            VideoFileClip: Video file clip object.
        """
        return VideoFileClip(self.vid_path)

    def process_file(self):
        """Extracts audio of a single file as an mp3 into the audio path folder.

        Args:
            vid_file (str): Video file name and ext in vids_path
            audio_name (str): (optional) If passed, will override the audio name which
                        is the same as the video name. Defaults to None.
        """
        clip = self.get_clip()
        try:
            os.makedirs(self.audio_dir, exist_ok=True)
            print(f"\nExtracting audio for {self.audio_name}...\n")
            clip.audio.write_audiofile(f"{self.audio_dir}/{self.audio_name}.mp3")
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
