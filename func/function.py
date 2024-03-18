import os
import re
from func.tools import *
from func.doc import *
from model.openai import *


class Media2Text:
    def __init__(self, slice, overlap, media, text, model_size, device):
        super().__init__()
        self.slice = slice
        self.overlap = overlap
        self.media = media
        self.text = text
        self.whisper = Whisper(model_size, device)

    def audio2text(self, audio_path):
        folder, audio = os.path.split(audio_path)
        audio_name = os.path.splitext(audio)[0]
        dec_audio_path = os.path.join(folder, audio_name + '_dec.mp3')
        audio_folder = os.path.join(folder, audio_name)
        os.makedirs(audio_folder, exist_ok=True)

        self.media.reduce_noise(audio_path, dec_audio_path)
        self.media.slice_audio(dec_audio_path, audio_folder, self.slice, self.overlap)

        sentences = []
        files = sorted([x for x in os.listdir(audio_folder) if x.endswith('.mp3')])
        for i in range(len(files)):
            language, fragments = self.whisper(os.path.join(audio_folder, files[i]))
            if i == 0:
                sentences.extend(fragments[:-1])

            else:
                sentences.extend(fragments[1:])

        sentences = [sen.lower() for sen in sentences]
        sentences = [self.text.tradition2simplicity(sen) for sen in sentences]
        sentences = [re.sub(re.compile(r'[^\w\s]+|[\u3000-\u303f\ufb00-\ufffd]'), '', sen) for sen in sentences]

        idxs = []
        size = len(sentences)
        for i in range(size):
            sen_i = sentences[i]
            for j in range(i + 1, min(i + 10, size)):
                sen_j = sentences[j]
                if len(set(sen_i) & set(sen_j)) / min(len(set(sen_i)), len(set(sen_j))) > 0.8:
                    idx = [i, j][[len(sen_i), len(sen_j)].index(min([len(sen_i), len(sen_j)]))]
                    idxs.append(idx)

        for idx in sorted(idxs, reverse=True):
            sentences.pop(idx)

        text = ', '.join(sentences) + '.'

        return text

    def video2text(self, video_path):
        folder, video = os.path.split(video_path)
        video_name = os.path.splitext(video)[0]
        audio_path = os.path.join(folder, video_name + '.mp3')
        self.media.video2audio(video_path, audio_path)

        return self.audio2text(audio_path)