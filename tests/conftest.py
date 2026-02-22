"""Shared pytest fixtures for the audio-extractor test suite."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture


@pytest.fixture
def mock_path_is_file(mocker: MockerFixture) -> MagicMock:
    """Patch Path.is_file to return True for all instances.

    Use this fixture in tests that construct objects requiring a valid file path
    without needing an actual file on disk.

    Args:
        mocker: The pytest-mock fixture.

    Returns:
        The patch mock object for Path.is_file.
    """
    return mocker.patch.object(Path, "is_file", return_value=True)
