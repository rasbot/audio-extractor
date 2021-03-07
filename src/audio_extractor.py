import os
import eyed3
import moviepy.editor as mp

"""Look...a module docstring..."""

class AudioExtract:
    """Args: vid_path, audio_path"""

    def __init__(self, vid_path, audio_path, mp3_tag_d):
        self.vid_path = vid_path
        self.audio_path = audio_path
        self.audio_name = None
        self.mp3_tag_d = mp3_tag_d
        self.file_names = [f for f in os.listdir(vid_path) if os.path.isfile(os.path.join(vid_path, f))]

    def get_clip(self, vid_file):
        """Returns the clip of a video file
        args: vid_file (str): video file name and ext in vid_path
        return: video clip object"""
        return mp.VideoFileClip(r"{}/{}".format(self.vid_path, vid_file))

    def get_mp3(self):
        """Gets audiofile object from path/name"""
        return eyed3.load(self.audio_path + "/" + self.audio_name + ".mp3")

    def tag_mp3(self):
        """Tags an audiofile with values of dictionary with 'album' or 'artist'
           keys and updates the audiofile title with self.audio_name"""
        audiofile = self.get_mp3()
        k = self.mp3_tag_d.keys()
        if 'album' in k:
            audiofile.tag.album = self.mp3_tag_d['album']
        if 'artist' in k:
            audiofile.tag.artist = self.mp3_tag_d['artist']
        audiofile.tag.title = self.audio_name
        audiofile.tag.save(version=eyed3.id3.ID3_V2_3)

    def tag_all_mp3(self):
        """For all files in folder, tag them"""
        for file in self.file_names:
            try:
                self.audio_name = file[:-4]
                self.tag_mp3()
            except Exception as e:
                print(e)

    def extract_audio(self, vid_file, audio_name=None):
        """Extracts audio of a single file as an mp3 into the audio path folder
        args: vid_file (str): video file name and ext in vid_path
              audio_name (str): (optional) if passed, will override the audio name
              which is the same as the video name
        return: None"""
        self.audio_name = audio_name
        try:
            if audio_name is None:
                self.audio_name = vid_file[:-4]
            clip = self.get_clip(vid_file)
            if not os.path.exists(self.audio_path):
                os.mkdir(self.audio_path)
            print("Extracting audio...")
            clip.audio.write_audiofile(r"{}/{}.mp3".format(self.audio_path, self.audio_name))
            print("Finished extracting audio!")
        except Exception as e:
            print(e)

    def extract_all_audio(self):
        """Extracts audio from all video files in vid_path and writes them to audio_path
        args: None
        returns: None"""
        for file in self.file_names:
            try:
                self.extract_audio(file)
            except Exception as e:
                print(e)

    def extract_and_tag(self):
        """Extract and tag all files"""
        self.extract_all_audio()
        self.tag_all_mp3()