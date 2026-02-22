"""Audio tagging module for writing ID3 tags to mp3 files."""

import argparse

import eyed3
import eyed3.id3
import eyed3.mp3

from process_class import ProcessClass
from utils import get_file_strings


class AudioTagger(ProcessClass):
    """Tags an mp3 file with album, artist, and title metadata."""

    def __init__(
        self,
        sound_file_path: str,
        artist_tag: str,
        album_tag: str,
        title_tag: str | None = None,
    ) -> None:
        """Init method for AudioTagger class.

        Args:
            sound_file_path: Path to audio file.
            artist_tag: Artist name.
            album_tag: Album name.
            title_tag: Title of the mp3. If None, the filename is used.
                Defaults to None.
        """
        self.sound_file_path = sound_file_path
        self.artist_tag = artist_tag
        self.album_tag = album_tag
        if not title_tag:
            self.title_tag, _ = get_file_strings(self.sound_file_path)
        else:
            self.title_tag = title_tag
        self.mp3_file: eyed3.mp3.Mp3AudioFile | None = None

    def get_mp3(self) -> None:
        """Load the mp3 file into self.mp3_file.

        Raises:
            ValueError: If eyed3 cannot load the file (corrupt or not a valid mp3).
        """
        self.mp3_file = eyed3.load(self.sound_file_path)
        if self.mp3_file is None:
            raise ValueError(
                f"Failed to load MP3 file: {self.sound_file_path!r}. "
                "The file may be corrupt or is not a valid MP3."
            )

    def process_file(self) -> None:
        """Load the mp3 and write album, artist, and title tags to it."""
        print(f"Tagging {self.title_tag}...")
        self.get_mp3()
        assert self.mp3_file is not None
        if self.mp3_file.tag is None:
            self.mp3_file.initTag()
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
