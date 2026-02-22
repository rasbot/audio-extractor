# Audio Extractor

Scripts in this repo can take a video file and extract the audio from the file to an mp3. The mp3 file can be normalized so the volume of the file is consistant. Ex: You have a handful of videos and extract the audio, they can all be normalized so the louder audio is less loud, and the quieter audio is less quiet. The mp3 files can also be tagged with the album, artist, and title so programs playing the files can use the tags to sort the files correctly.

## Prerequisites
You will need to have `ffmpeg` installed on your computer. Setup uses uv, so please install that as well.

## Installation
1. Clone this repo
```bash
git clone https://github.com/rasbot/audio-extractor.git
```
2. Install packages
```bash
uv sync
```

## Usage
The scripts and their usage will be described below.

### Audio Extraction
Audio extraction can be done on individual files or on a directory where all video files will be processed.
#### Individual file
The `audio_extractor.py` script can be ran on individual video files to extract audio from them. Point the script to the video path using the command line arg:
```bash
uv run .\src\audio_extractor.py --vid_path ".\some-directory\video_file.avi"
```
The resulting mp3 file will be in the `.\data\extracted_audio` directory in the repo directory.

#### Multiple files in a directory
The `extract_audios_from_dir.py` script will process all video files in a directory.
```bash
uv run .\src\extract_audios_from_dir.py --dir ".\some-directory-with-video-files-in-it"
```
The resulting mp3 files will be in the `.\data\extracted_audio` directory in the repo directory.

### Audio Normalization
mp3 files can be normalized, which can be useful if the video file is too loud or too quiet. The default value is -30 dBFS, and a less negative number will result in a louder file (-10 dBFS is louder than -20 dBFS).

#### Individual file
```bash
uv run .\src\audio_normalizer.py --audio_path ".\some-directory\audio_file.mp3" --dBFS -20
```
The resulting mp3 file will be in the `.\data\normalized_audio` directory in the repo directory.

#### Multiple files in a directory
```bash
uv run .\src\normalize_audios_from_dir.py --dir ".\some-directory-with-audio-files-in-it" --dBFS -20
```
The resulting mp3 file will be in the `.\data\normalized_audio` directory in the repo directory.

### mp3 Tagging
mp3 files can be tagged with the album, artist, and title. The title can be omitted, and the name of the mp3 file will be used instead.
The album and artist will default to "default album" and "default artist", respectively, if these flags are not passed to the script.

#### Individual file
```bash
uv run .\src\audio_tagger.py --audio_path ".\some-directory\audio_file.mp3" --artist "Darkthrone" --album "A Blaze in the Northern Sky" --title "Where the Cold Winds Blow"
```
The resulting mp3 file will have the tags applied.

#### Multiple files in a directory
```bash
uv run .\src\tag_audios_from_dir.py --dir ".\some-directory-with-audio-files-in-it" --artist "Wolves in the Throne Room" --album "Black Cascade"
```
The resulting mp3 files will have the album and artist tags, and the title tags will use the mp3 file names.

### Processing Pipeline
If you have a directory of audio files, they can all be processed without calling the individual scripts. The `files_processor.py` script can be used here.
```bash
uv run .\src\files_processor.py --extract --normalize --tag --artist "Taake" --album "Kveld"
```
This will process all video files in the `.\data\` directory. You can also pass a `--dir` flag to specify a directory. Subsets of these functions can be called as well. If you wanted to normalize and tag files you can use
```bash
uv run .\src\files_processor.py --dir ".\some-directory-with-audio-files-in-it" --normalize --tag --artist "Kampfar" --album "KVASS"
```
