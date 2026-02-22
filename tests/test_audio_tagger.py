import pytest
import eyed3
import eyed3.id3
from audio_tagger import AudioTagger


class TestAudioTaggerInit:
    def test_stores_sound_file_path(self):
        at = AudioTagger("/some/path/track.mp3", "Artist", "Album")
        assert at.sound_file_path == "/some/path/track.mp3"

    def test_stores_artist_tag(self):
        at = AudioTagger("/some/path/track.mp3", "My Artist", "My Album")
        assert at.artist_tag == "My Artist"

    def test_stores_album_tag(self):
        at = AudioTagger("/some/path/track.mp3", "My Artist", "My Album")
        assert at.album_tag == "My Album"

    def test_defaults_title_to_filename(self):
        at = AudioTagger("/some/path/my_track.mp3", "Artist", "Album")
        assert at.title_tag == "my_track"

    def test_stores_custom_title_tag(self):
        at = AudioTagger("/some/path/track.mp3", "Artist", "Album", title_tag="Custom Title")
        assert at.title_tag == "Custom Title"

    def test_mp3_file_is_none_before_get_mp3(self):
        at = AudioTagger("/some/path/track.mp3", "Artist", "Album")
        assert at.mp3_file is None


class TestAudioTaggerGetMp3:
    def test_get_mp3_calls_eyed3_load(self, mocker):
        mock_mp3 = mocker.MagicMock()
        mock_load = mocker.patch("audio_tagger.eyed3.load", return_value=mock_mp3)

        at = AudioTagger("/some/path/track.mp3", "Artist", "Album")
        at.get_mp3()

        mock_load.assert_called_once_with("/some/path/track.mp3")
        assert at.mp3_file is mock_mp3

    def test_get_mp3_raises_when_eyed3_returns_none(self, mocker):
        mocker.patch("audio_tagger.eyed3.load", return_value=None)

        at = AudioTagger("/some/path/track.mp3", "Artist", "Album")
        with pytest.raises(ValueError, match="Failed to load"):
            at.get_mp3()


class TestAudioTaggerProcessFile:
    def _make_mock_mp3(self, mocker, tag=None):
        mock_mp3 = mocker.MagicMock()
        mock_mp3.tag = tag if tag is not None else mocker.MagicMock()
        mocker.patch("audio_tagger.eyed3.load", return_value=mock_mp3)
        return mock_mp3

    def test_process_file_calls_get_mp3(self, mocker):
        self._make_mock_mp3(mocker)
        at = AudioTagger("/some/path/track.mp3", "Artist", "Album")
        spy = mocker.spy(at, "get_mp3")
        at.process_file()

        spy.assert_called_once()

    def test_process_file_sets_artist(self, mocker):
        mock_mp3 = self._make_mock_mp3(mocker)
        at = AudioTagger("/some/path/track.mp3", "My Artist", "My Album")
        at.process_file()

        assert mock_mp3.tag.artist == "My Artist"

    def test_process_file_sets_album(self, mocker):
        mock_mp3 = self._make_mock_mp3(mocker)
        at = AudioTagger("/some/path/track.mp3", "My Artist", "My Album")
        at.process_file()

        assert mock_mp3.tag.album == "My Album"

    def test_process_file_sets_title(self, mocker):
        mock_mp3 = self._make_mock_mp3(mocker)
        at = AudioTagger("/some/path/track.mp3", "Artist", "Album", title_tag="My Title")
        at.process_file()

        assert mock_mp3.tag.title == "My Title"

    def test_process_file_calls_init_tag_when_tag_is_none(self, mocker):
        mock_mp3 = mocker.MagicMock()
        mock_tag = mocker.MagicMock()
        mock_mp3.tag = None

        def init_tag_side_effect():
            mock_mp3.tag = mock_tag

        mock_mp3.initTag.side_effect = init_tag_side_effect
        mocker.patch("audio_tagger.eyed3.load", return_value=mock_mp3)
        at = AudioTagger("/some/path/track.mp3", "Artist", "Album")
        at.process_file()

        mock_mp3.initTag.assert_called_once()

    def test_process_file_skips_init_tag_when_tag_exists(self, mocker):
        mock_mp3 = self._make_mock_mp3(mocker)
        at = AudioTagger("/some/path/track.mp3", "Artist", "Album")
        at.process_file()

        mock_mp3.initTag.assert_not_called()

    def test_process_file_saves_with_id3_v2_3(self, mocker):
        mock_mp3 = self._make_mock_mp3(mocker)
        at = AudioTagger("/some/path/track.mp3", "Artist", "Album")
        at.process_file()

        mock_mp3.tag.save.assert_called_once_with(version=eyed3.id3.ID3_V2_3)
