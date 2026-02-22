import pytest
from constants import EXTRACTED_DIR
from audio_extractor import AudioExtractor


@pytest.fixture
def mock_clip_env(mocker):
    """Patch isfile, VideoFileClip, and makedirs for AudioExtractor process_file tests."""
    mocker.patch("audio_extractor.os.path.isfile", return_value=True)
    mock_clip = mocker.MagicMock()
    mocker.patch("audio_extractor.VideoFileClip", return_value=mock_clip)
    mock_makedirs = mocker.patch("audio_extractor.os.makedirs")
    return mock_clip, mock_makedirs


class TestAudioExtractorInit:
    def test_raises_when_file_not_found(self, mocker):
        mocker.patch("audio_extractor.os.path.isfile", return_value=False)

        with pytest.raises(FileNotFoundError):
            AudioExtractor("/nonexistent/path/video.mp4")

    def test_defaults_audio_name_to_filename(self, mocker):
        mocker.patch("audio_extractor.os.path.isfile", return_value=True)

        ae = AudioExtractor("/some/path/my_video.mp4")
        assert ae.audio_name == "my_video"

    def test_stores_custom_audio_name(self, mocker):
        mocker.patch("audio_extractor.os.path.isfile", return_value=True)

        ae = AudioExtractor("/some/path/my_video.mp4", audio_name="custom_name")
        assert ae.audio_name == "custom_name"

    def test_audio_dir_uses_extracted_dir_constant(self, mocker):
        mocker.patch("audio_extractor.os.path.isfile", return_value=True)

        ae = AudioExtractor("/some/path/my_video.mp4")
        assert ae.audio_dir == EXTRACTED_DIR


class TestAudioExtractorGetClip:
    def test_get_clip_calls_video_file_clip(self, mocker):
        mocker.patch("audio_extractor.os.path.isfile", return_value=True)
        mock_clip = mocker.MagicMock()
        mock_vfc = mocker.patch("audio_extractor.VideoFileClip", return_value=mock_clip)

        ae = AudioExtractor("/some/path/my_video.mp4")
        result = ae.get_clip()

        mock_vfc.assert_called_once_with("/some/path/my_video.mp4")
        assert result is mock_clip


class TestAudioExtractorProcessFile:
    def test_process_file_calls_makedirs_with_exist_ok(self, mock_clip_env):
        mock_clip, mock_makedirs = mock_clip_env
        ae = AudioExtractor("/some/path/my_video.mp4")
        ae.process_file()

        mock_makedirs.assert_called_once_with(ae.audio_dir, exist_ok=True)

    def test_process_file_calls_write_audiofile_with_correct_path(self, mock_clip_env):
        mock_clip, _ = mock_clip_env
        ae = AudioExtractor("/some/path/my_video.mp4")
        ae.process_file()

        expected_path = ae.audio_dir / "my_video.mp3"
        mock_clip.audio.write_audiofile.assert_called_once_with(expected_path)

    def test_process_file_uses_custom_name_in_path(self, mock_clip_env):
        mock_clip, _ = mock_clip_env
        ae = AudioExtractor("/some/path/my_video.mp4", audio_name="custom_name")
        ae.process_file()

        expected_path = ae.audio_dir / "custom_name.mp3"
        mock_clip.audio.write_audiofile.assert_called_once_with(expected_path)

    def test_process_file_closes_clip_on_success(self, mock_clip_env):
        mock_clip, _ = mock_clip_env
        ae = AudioExtractor("/some/path/my_video.mp4")
        ae.process_file()

        mock_clip.close.assert_called_once()

    def test_process_file_closes_clip_on_error(self, mock_clip_env):
        mock_clip, _ = mock_clip_env
        mock_clip.audio.write_audiofile.side_effect = RuntimeError("write failed")
        ae = AudioExtractor("/some/path/my_video.mp4")

        with pytest.raises(RuntimeError):
            ae.process_file()

        mock_clip.close.assert_called_once()

    def test_process_file_raises_when_no_audio_track(self, mock_clip_env):
        mock_clip, _ = mock_clip_env
        mock_clip.audio = None
        ae = AudioExtractor("/some/path/my_video.mp4")

        with pytest.raises(ValueError, match="no audio track"):
            ae.process_file()

        mock_clip.close.assert_called_once()
