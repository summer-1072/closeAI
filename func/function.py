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
        for i, file in enumerate(files):
            language, fragments = self.whisper(os.path.join(audio_folder, file))

            if i == 0:
                sentences.extend([fragment[1] for fragment in fragments][:-1])
            else:
                sentences.extend([fragment[1] for fragment in fragments][1:])

        sentences = [self.Htext.prep_text(sen) for sen in sentences]
        sentences = [self.Htext.split_text(sen) for sen in sentences]
        sentences = [self.Htext.clean_mark(sen) for sentence in sentences for sen in sentence]
        sentences = [sen for sen in sentences if sen]

        idx, idxs = 0, []
        num = len(sentences)
        while idx < num:
            sen_front = sentences[idx]
            sen_front = re.findall(r'[A-Za-z]+|[\u4e00-\u9fff]', sen_front)
            for inc, sen_back in enumerate(sentences[idx + 1:idx + 10]):
                sen_back = re.findall(r'[A-Za-z]+|[\u4e00-\u9fff]', sen_back)

                inter = [idx, idx + inc + 1] if len(sen_front) <= len(sen_back) else [idx + 1, idx + 1 + inc + 1]
                sen_min, sen_max = (sen_front, sen_back) if len(sen_front) <= len(sen_back) else (sen_back, sen_front)

                if max([[sen_min[j] == sen_max[i + j] for j in range(len(sen_min))].count(True) for i in
                        range(len(sen_max) - len(sen_min) + 1)]) / len(sen_min) > 0.8:
                    idxs.extend([i for i in range(inter[0], inter[1])])
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
        text = self.Htext.prep_text(text)
        sentences = self.Htext.split_text(text)
        sentences = [self.Htext.clean_mark(sentence) for sentence in sentences]
        sentences = [sentence for sentence in sentences if sentence]

        return ', '.join(sentences) + '.'