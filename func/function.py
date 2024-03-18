import os
from func.tools import *
from func.doc import *
from model.openai import *


class Media2Text:
    def __init__(self, slice, overlap, noise_reduce_ratio, media, text, model_size, device):
        super().__init__()
        self.slice = slice
        self.overlap = overlap
        self.noise_reduce_ratio = noise_reduce_ratio
        self.media = media
        self.text = text
        self.whisper = Whisper(model_size, device)

    def clean_text(self, sentences):
        set_sentences = list(set(sentences))
        set_sentences.sort(key=sentences.index)
        text = ', '.join(set_sentences).lower()
        text = self.text.tradition2simplicity(text)

        print(text)

    def audio2text(self):
        pass

    def video2text(self, video_path):
        folder, video = os.path.split(video_path)
        video_name = os.path.splitext(video)[0]
        audio_path = os.path.join(folder, video_name, video_name + '.mp3')
        audio_folder = os.path.join(folder, video_name, video_name)
        os.makedirs(audio_folder, exist_ok=True)

        self.media.video2audio(video_path, audio_path)
        self.media.reduce_noise(audio_path, audio_path, self.noise_reduce_ratio)
        self.media.slice_audio(audio_path, audio_folder, self.slice, self.overlap)

        sentences = []
        files = sorted([x for x in os.listdir(audio_folder) if x.endswith('.mp3')])
        for i in range(len(files)):
            language, fragments = self.whisper(os.path.join(audio_folder, files[i]))
            if i == 0:
                sentences.extend(fragments[:-1])

            else:
                sentences.extend(fragments[1:])

        text = self.clean_text(sentences)

        return text


import time

start = time.time()
media = Media()
text = Text('../config/stop_word.txt')

data = Media2Text(30000, 6000, 0.6, media, text, 'medium', 'cuda')
data.video2text('/home/uto/demo/飞书20240314-120801.mp4')
end = time.time()
print(end - start)
