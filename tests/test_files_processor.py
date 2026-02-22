import os

from files_processor import process_all_files


class TestProcessAllFiles:
    def test_calls_process_class_for_each_valid_file(self, mocker):
        mocker.patch("files_processor.os.listdir", return_value=["a.mp4", "b.mp4"])
        mocker.patch("files_processor.os.path.isfile", return_value=True)
        mock_process_class = mocker.MagicMock()

        process_all_files("/some/dir", ["mp4"], mock_process_class)

        assert mock_process_class.call_count == 2

    def test_skips_invalid_extensions(self, mocker):
        mocker.patch(
            "files_processor.os.listdir", return_value=["a.mp4", "b.txt", "c.mp4"]
        )
        mocker.patch("files_processor.os.path.isfile", return_value=True)
        mock_process_class = mocker.MagicMock()

        process_all_files("/some/dir", ["mp4"], mock_process_class)

        assert mock_process_class.call_count == 2

    def test_skips_non_file_entries(self, mocker):
        mocker.patch("files_processor.os.listdir", return_value=["subdir", "video.mp4"])

        def isfile_side_effect(path):
            return not path.endswith("subdir")

        mocker.patch("files_processor.os.path.isfile", side_effect=isfile_side_effect)
        mock_process_class = mocker.MagicMock()

        process_all_files("/some/dir", ["mp4"], mock_process_class)

        assert mock_process_class.call_count == 1

    def test_passes_correct_file_path(self, mocker):
        mocker.patch("files_processor.os.listdir", return_value=["video.mp4"])
        mocker.patch("files_processor.os.path.isfile", return_value=True)
        mock_process_class = mocker.MagicMock()

        process_all_files("/some/dir", ["mp4"], mock_process_class)

        expected_path = os.path.join("/some/dir", "video.mp4")
        mock_process_class.assert_called_once_with(expected_path)

    def test_passes_kwargs_to_process_class(self, mocker):
        mocker.patch("files_processor.os.listdir", return_value=["audio.mp3"])
        mocker.patch("files_processor.os.path.isfile", return_value=True)
        mock_process_class = mocker.MagicMock()

        process_all_files("/some/dir", ["mp3"], mock_process_class, target_dbfs=-20)

        expected_path = os.path.join("/some/dir", "audio.mp3")
        mock_process_class.assert_called_once_with(expected_path, target_dbfs=-20)

    def test_handles_empty_directory(self, mocker):
        mocker.patch("files_processor.os.listdir", return_value=[])
        mocker.patch("files_processor.os.path.isfile", return_value=True)
        mock_process_class = mocker.MagicMock()

        process_all_files("/some/dir", ["mp4"], mock_process_class)

        mock_process_class.assert_not_called()

    def test_handles_dir_with_no_valid_extensions(self, mocker):
        mocker.patch(
            "files_processor.os.listdir", return_value=["doc.pdf", "image.jpg"]
        )
        mocker.patch("files_processor.os.path.isfile", return_value=True)
        mock_process_class = mocker.MagicMock()

        process_all_files("/some/dir", ["mp4"], mock_process_class)

        mock_process_class.assert_not_called()
