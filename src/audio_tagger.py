import argparse

import eyed3

from utils import get_file_strings
from process_class import ProcessClass


class AudioTagger(ProcessClass):
    """AudioTagger class to tag mp3 files.
    """
    def __init__(
        self,
        sound_file_path: str,
        artist_tag: str,
        album_tag: str,
        title_tag: str = None,
    ) -> None:
        """Init method for `AudioTagger` class.

        Args:
            sound_file_path (str): Path to audio file.
            artist_tag (str): Artist name.
            album_tag (str): Album name.
            title_tag (str, optional): Title of mp3.
                If None, will use the name of the mp3 file.
                Defaults to None.
        """
        self.sound_file_path = sound_file_path
        self.artist_tag = artist_tag
        self.album_tag = album_tag
        if not title_tag:
            self.title_tag, _ = get_file_strings(self.sound_file_path)
        else:
            self.title_tag = title_tag
        self.mp3_file = None

    def get_mp3(self) -> None:
        """Loads a mp3 file as a eyed3.mp3.Mp3AudioFile object."""
        self.mp3_file = eyed3.load(self.sound_file_path)

    def process_file(self) -> None:
        """Loads mp3 file and tags it with album/artist/title tags.
        Saves mp3 file with tags.
        """
        print(f"\nTagging {self.title_tag}...\n")
        self.get_mp3()
        self.mp3_file.tag.album = self.album_tag
        self.mp3_file.tag.artist = self.artist_tag
        self.mp3_file.tag.title = self.title_tag
        self.mp3_file.tag.save(version=eyed3.id3.ID3_V2_3)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--audio_path", type=str, default=None, help="Path to audio file to tag"
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
    parser.add_argument(
        "--title",
        type=str,
        default=None,
        help="title tag for mp3 file - Defaults to mp3 file name.",
    )
    args = parser.parse_args()
    tagger = AudioTagger(
        args.audio_path,
        args.artist,
        args.album,
        args.title,
    )
    tagger.process_file()
