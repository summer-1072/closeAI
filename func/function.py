import os

from func.tools import *
from func.doc import *
from model.openai import *


class Media2Text:
    def __init__(self, prop, length, overlap, model_name, device):
        super().__init__()
        self.prop = prop
        self.length = length
        self.overlap = overlap
        self.media = Media()
        self.whisper = Whisper(model_name, device)

    def audio2text(self):
        pass

    def video2text(self, video_path):
        folder, video_file = os.path.split(video_path)
        video_name = os.path.splitext(video_file)[0]
        audio_path = os.path.join(folder, video_name, video_name + '.mp3')
        audio_folder = os.path.join(folder, video_name, video_name)
        os.makedirs(audio_folder, exist_ok=True)

        self.media.video2audio(video_path, audio_path)
        self.media.reduce_noise(audio_path, audio_path, self.prop)
        self.media.split_audio(audio_path, audio_folder, self.length, self.overlap)

        sentences = []
        for file in sorted(os.listdir(audio_folder)):
            if 'mp3' in file:
                language, fragments = self.whisper(os.path.join(audio_folder, file))
                cost = 0
                for fragment in fragments:
                    cost += fragment[0]
                    print(fragment, cost)
                    if cost <= self.length - self.overlap:
                        sentences.append(fragment[1])

        text = '，'.join(sentences) + '。'
        print(text)


data = Media2Text(0.75, 30000, 5000, 'small', 'cuda')
data.video2text('/D/project/data/mp4/demo.mp4')
