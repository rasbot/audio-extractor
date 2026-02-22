from pathlib import Path

import pytest

from audio_normalizer import AudioNormalizer, FileNotSupportedError
from constants import NORMALIZED_DIR


class TestAudioNormalizerInit:
    def test_stores_audio_path(self):
        an = AudioNormalizer("/some/path/audio.mp3", target_dbfs=-20.0)
        assert an.audio_path == "/some/path/audio.mp3"

    def test_stores_target_dbfs(self):
        an = AudioNormalizer("/some/path/audio.mp3", target_dbfs=-20.0)
        assert an.target_dbfs == -20.0

    def test_parses_name(self):
        an = AudioNormalizer("/some/path/my_audio.mp3", target_dbfs=-30.0)
        assert an.audio_name == "my_audio"

    def test_parses_ext(self):
        an = AudioNormalizer("/some/path/my_audio.mp3", target_dbfs=-30.0)
        assert an.audio_ext == "mp3"

    def test_normalized_dir_uses_constant(self):
        an = AudioNormalizer("/some/path/audio.mp3", target_dbfs=-20.0)
        assert an.normalized_dir == NORMALIZED_DIR


class TestAudioNormalizerProcessFile:
    def test_raises_file_not_supported_for_non_mp3(self):
        an = AudioNormalizer("/some/path/audio.wav", target_dbfs=-20.0)
        with pytest.raises(FileNotSupportedError):
            an.process_file()

    def test_creates_output_directory(self, mocker):
        mock_mkdir = mocker.patch.object(Path, "mkdir")
        mock_sound = mocker.MagicMock()
        mock_sound.dBFS = -40.0
        mocker.patch("audio_normalizer.AudioSegment.from_mp3", return_value=mock_sound)

        an = AudioNormalizer("/some/path/audio.mp3", target_dbfs=-20.0)
        an.process_file()

        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

    def test_computes_correct_gain_delta(self, mocker):
        mocker.patch.object(Path, "mkdir")
        mock_sound = mocker.MagicMock()
        mock_sound.dBFS = -40.0
        mocker.patch("audio_normalizer.AudioSegment.from_mp3", return_value=mock_sound)

        an = AudioNormalizer("/some/path/audio.mp3", target_dbfs=-20.0)
        an.process_file()

        mock_sound.apply_gain.assert_called_once_with(20.0)

    def test_exports_to_correct_path(self, mocker):
        mocker.patch.object(Path, "mkdir")
        mock_sound = mocker.MagicMock()
        mock_sound.dBFS = -40.0
        mock_normalized = mocker.MagicMock()
        mock_sound.apply_gain.return_value = mock_normalized
        mocker.patch("audio_normalizer.AudioSegment.from_mp3", return_value=mock_sound)

        an = AudioNormalizer("/some/path/my_audio.mp3", target_dbfs=-20.0)
        an.process_file()

        expected_path = an.normalized_dir / "my_audio_norm.mp3"
        mock_normalized.export.assert_called_once_with(expected_path)

    def test_loads_from_correct_audio_path(self, mocker):
        mocker.patch.object(Path, "mkdir")
        mock_sound = mocker.MagicMock()
        mock_sound.dBFS = -30.0
        mock_from_mp3 = mocker.patch(
            "audio_normalizer.AudioSegment.from_mp3", return_value=mock_sound
        )

        an = AudioNormalizer("/some/path/audio.mp3", target_dbfs=-20.0)
        an.process_file()

        mock_from_mp3.assert_called_once_with("/some/path/audio.mp3")
