import os
from typing import List, Tuple
import argparse
import moviepy.editor as mp


def get_file_strings(file_path: str, full_path=False) -> Tuple[str, str]:
    """Split file path name into name / file extension.

    Args:
        file_path (str): Path to file.
        full_path (bool, optional): True if the full path
            will be used for the file name return string.
            Defaults to False.

    Returns:
        Tuple[str, str]: File name string and image
            extension string.
    """

    file_strings = file_path.rsplit(".", 1)
    file_name = file_strings[0]
    if not full_path:
        file_name = file_name.replace("\\", "/")
        file_name = file_name.rsplit("/", 1)[-1]
    file_ext = file_strings[-1]
    return file_name, file_ext


class AudioExtractor:
    """Args: vid_path, audio_path"""

    def __init__(self, vid_path: str, audio_name: str=None) -> None:
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
        self.audio_dir = "./data/extracted_audio"

    def get_clip(self):
        """Returns the clip of a video file.

        Returns:
            VideoClipFile: Video Clip File object.
        """
        #TODO: fix return type in docstring
        return mp.VideoFileClip(self.vid_path)


    def extract_audio(self):
        """Extracts audio of a single file as an mp3 into the audio path folder.

        Args:
            vid_file (str): Video file name and ext in vids_path
            audio_name (str): (optional) If passed, will override the audio name which
                        is the same as the video name. Defaults to None.
        """
        clip = self.get_clip()
        if not os.path.exists(self.audio_dir):
            os.mkdir(self.audio_dir)
        print(f"\nExtracting audio for {self.audio_name}...\n")
        clip.audio.write_audiofile(f"{self.audio_dir}/{self.audio_name}.mp3")
        print("\nFinished extracting audio!\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--vid_path",
        type=str,
        default=None,
        help="File path to video file that will have audio extracted from."
    )
    args = parser.parse_args()
    ae = AudioExtractor(args.vid_path)
    ae.extract_audio()