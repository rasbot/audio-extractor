"""Shared path constants and file extension sets for the audio-extractor pipeline."""

from pathlib import Path

__all__ = [
    "AUDIO_EXTS",
    "DATA_DIR",
    "DEFAULT_ALBUM",
    "DEFAULT_ARTIST",
    "DEFAULT_DBFS",
    "EXTRACTED_DIR",
    "NORMALIZED_DIR",
    "REPO_ROOT",
    "VID_EXTS",
]

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
NORMALIZED_DIR = DATA_DIR / "normalized_audio"
EXTRACTED_DIR = DATA_DIR / "extracted_audio"

VID_EXTS: frozenset[str] = frozenset({"mp4", "avi", "mov", "mkv"})
AUDIO_EXTS: frozenset[str] = frozenset({"mp3"})

DEFAULT_DBFS: float = -30.0
DEFAULT_ARTIST: str = "default artist"
DEFAULT_ALBUM: str = "default album"
