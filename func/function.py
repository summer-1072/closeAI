import os
import re
from func.document import HandleText, HandleMedia
from model.openai import Whisper, GPT


class Media2Text:
    def __init__(self, slice, overlap, model_size, device):
        super().__init__()
        self.slice = slice
        self.overlap = overlap

        self.Htext = HandleText()
        self.Hmedia = HandleMedia()
        self.whisper = Whisper(model_size, device)

    def audio2text(self, audio_path):
        folder, audio = os.path.split(audio_path)
        audio_name = os.path.splitext(audio)[0]
        dec_audio_path = os.path.join(folder, audio_name + '_dec.mp3')
        audio_folder = os.path.join(folder, audio_name)
        os.makedirs(audio_folder, exist_ok=True)

        self.Hmedia.reduce_noise(audio_path, dec_audio_path)
        self.Hmedia.slice_audio(dec_audio_path, audio_folder, self.slice, self.overlap)

        sentences = []
        files = sorted([x for x in os.listdir(audio_folder) if x.endswith('.mp3')])
        for i in range(len(files)):
            language, fragments = self.whisper(os.path.join(audio_folder, files[i]))
            if i == 0:
                sentences.extend(fragments[:-1])

            else:
                sentences.extend(fragments[1:])

        sentences = [self.Htext.clean_text(sen) for sen in sentences]
        sentences = [sen for sen in sentences if sen]

        idxs = []
        idx = 0
        num = len(sentences)
        while idx < num:
            sen_front = sentences[idx]
            sen_front = re.findall(r'[A-Za-z]+|[\u4e00-\u9fff]', sen_front)
            for inc, sen_back in enumerate(sentences[idx + 1:idx + 10]):
                sen_back = re.findall(r'[A-Za-z]+|[\u4e00-\u9fff]', sen_back)

                if len(sen_front) > len(sen_back):
                    if max([[sen_front[i + j] == sen_back[j] for j in range(len(sen_back))].count(True) for i in
                            range(len(sen_front) - len(sen_back) + 1)]) / len(sen_back) > 0.8:
                        idxs.extend([i for i in range(idx + 1, idx + 1 + inc + 1)])
                        idx += inc + 1

                else:
                    if max([[sen_front[j] == sen_back[i + j] for j in range(len(sen_front))].count(True) for i in
                            range(len(sen_back) - len(sen_front) + 1)]) / len(sen_front) > 0.8:
                        idxs.extend([i for i in range(idx, idx + inc + 1)])
                        idx += inc + 1

            idx += 1
        for idx in sorted(idxs, reverse=True):
            sentences.pop(idx)

        return ', '.join(sentences) + '.'

    def video2text(self, video_path):
        folder, video = os.path.split(video_path)
        video_name = os.path.splitext(video)[0]
        audio_path = os.path.join(folder, video_name + '.mp3')
        self.Hmedia.video2audio(video_path, audio_path)

        return self.audio2text(audio_path)


class Doc2Text:
    def __init__(self):
        super().__init__()
        self.Htext = HandleText()

    def __call__(self, file_path):
        text = self.Htext.read_text(file_path)
        sentences = self.Htext.split_text(text)
        sentences = [self.Htext.clean_text(sen) for sen in sentences]
        sentences = [sen for sen in sentences if sen]

        return ', '.join(sentences) + '.'


import time

start = time.time()
media2text = Media2Text(30000, 6000, 'medium', 'cuda')
text = media2text.video2text('/D/project/data/mp4/demo.mp4')
end = time.time()

print(end - start)
print(text)
