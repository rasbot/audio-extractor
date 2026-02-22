"""Tests for the process_all_files batch processing function."""

from pathlib import Path

from files_processor import process_all_files


class _FakeEntry:
    """Minimal stand-in for a pathlib.Path entry returned by Path.iterdir()."""

    def __init__(self, path_str: str, is_file_val: bool = True) -> None:
        self._path_str = path_str
        self._is_file_val = is_file_val

    def is_file(self) -> bool:
        """Return whether this entry represents a file."""
        return self._is_file_val

    def __str__(self) -> str:
        return self._path_str


class TestProcessAllFiles:
    """Verifies directory traversal, extension filtering, and processor dispatch."""

    def test_calls_process_class_for_each_valid_file(self, mocker):
        entries = [
            _FakeEntry("/some/dir/a.mp4"),
            _FakeEntry("/some/dir/b.mp4"),
        ]
        mocker.patch.object(Path, "iterdir", return_value=entries)
        mock_process_class = mocker.MagicMock()

        process_all_files("/some/dir", ["mp4"], mock_process_class)

        assert mock_process_class.call_count == 2

    def test_skips_invalid_extensions(self, mocker):
        entries = [
            _FakeEntry("/some/dir/a.mp4"),
            _FakeEntry("/some/dir/b.txt"),
            _FakeEntry("/some/dir/c.mp4"),
        ]
        mocker.patch.object(Path, "iterdir", return_value=entries)
        mock_process_class = mocker.MagicMock()

        process_all_files("/some/dir", ["mp4"], mock_process_class)

        assert mock_process_class.call_count == 2

    def test_skips_non_file_entries(self, mocker):
        entries = [
            _FakeEntry("/some/dir/subdir", is_file_val=False),
            _FakeEntry("/some/dir/video.mp4"),
        ]
        mocker.patch.object(Path, "iterdir", return_value=entries)
        mock_process_class = mocker.MagicMock()

        process_all_files("/some/dir", ["mp4"], mock_process_class)

        assert mock_process_class.call_count == 1

    def test_passes_correct_file_path(self, mocker):
        entries = [_FakeEntry("/some/dir/video.mp4")]
        mocker.patch.object(Path, "iterdir", return_value=entries)
        mock_process_class = mocker.MagicMock()

        process_all_files("/some/dir", ["mp4"], mock_process_class)

        mock_process_class.assert_called_once_with("/some/dir/video.mp4")

    def test_passes_kwargs_to_process_class(self, mocker):
        entries = [_FakeEntry("/some/dir/audio.mp3")]
        mocker.patch.object(Path, "iterdir", return_value=entries)
        mock_process_class = mocker.MagicMock()

        process_all_files("/some/dir", ["mp3"], mock_process_class, target_dbfs=-20)

        mock_process_class.assert_called_once_with(
            "/some/dir/audio.mp3", target_dbfs=-20
        )

    def test_handles_empty_directory(self, mocker):
        mocker.patch.object(Path, "iterdir", return_value=[])
        mock_process_class = mocker.MagicMock()

        process_all_files("/some/dir", ["mp4"], mock_process_class)

        mock_process_class.assert_not_called()

    def test_handles_dir_with_no_valid_extensions(self, mocker):
        entries = [
            _FakeEntry("/some/dir/doc.pdf"),
            _FakeEntry("/some/dir/image.jpg"),
        ]
        mocker.patch.object(Path, "iterdir", return_value=entries)
        mock_process_class = mocker.MagicMock()

        process_all_files("/some/dir", ["mp4"], mock_process_class)

        mock_process_class.assert_not_called()
