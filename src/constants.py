from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
NORMALIZED_DIR = DATA_DIR / "normalized_audio"
EXTRACTED_DIR = DATA_DIR / "extracted_audio"

VID_EXTS = [
    "mp4",
    "avi",
    "mov",
    "mkv",
]
AUDIO_EXTS = [
    "mp3",
]
