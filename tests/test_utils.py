from utils import get_file_strings, is_valid_ext
from constants import VID_EXTS


class TestGetFileStrings:
    def test_simple_filename(self):
        name, ext = get_file_strings("video.mp4")
        assert name == "video"
        assert ext == "mp4"

    def test_path_stripping(self):
        name, ext = get_file_strings("/some/path/to/video.avi")
        assert name == "video"
        assert ext == "avi"

    def test_windows_backslash(self):
        name, ext = get_file_strings("C:\\Users\\user\\video.mkv")
        assert name == "video"
        assert ext == "mkv"

    def test_full_path_true(self):
        name, ext = get_file_strings("/some/path/to/video.mp4", full_path=True)
        assert name == "/some/path/to/video"
        assert ext == "mp4"

    def test_multiple_dots(self):
        name, ext = get_file_strings("my.video.file.mp4")
        assert name == "my.video.file"
        assert ext == "mp4"

    def test_audio_ext(self):
        name, ext = get_file_strings("audio_track.mp3")
        assert name == "audio_track"
        assert ext == "mp3"

    def test_path_with_directory(self):
        name, ext = get_file_strings("data/extracted_audio/clip.mp3")
        assert name == "clip"
        assert ext == "mp3"


class TestIsValidExt:
    def test_valid_ext(self):
        assert is_valid_ext("video.mp4", ["mp4", "avi"]) is True

    def test_invalid_ext(self):
        assert is_valid_ext("video.txt", ["mp4", "avi"]) is False

    def test_case_sensitivity(self):
        assert is_valid_ext("video.MP4", ["mp4", "avi"]) is False

    def test_empty_list(self):
        assert is_valid_ext("video.mp4", []) is False

    def test_vid_exts_integration(self):
        assert is_valid_ext("clip.mov", VID_EXTS) is True

    def test_vid_exts_invalid(self):
        assert is_valid_ext("clip.mp3", VID_EXTS) is False
