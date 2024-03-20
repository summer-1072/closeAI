import re
import librosa
import soundfile
import pdfplumber
import noisereduce
from docx import Document
from opencc import OpenCC
from moviepy.editor import *
from pydub import AudioSegment


class HandleText:
    def __init__(self):
        super().__init__()

    def read_text(self, file_path):
        text = ''

        if file_path.endswith('pdf'):
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text()

        elif file_path.endswith('doc') or file_path.endswith('docx'):
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text

        elif file_path.endswith('txt'):
            with open(file_path, 'r') as file:
                text = file.read()

        else:
            raise Exception('file type is not supported')

        return text

    def prep_text(self, text):
        text = text.lower()

        text = OpenCC('t2s').convert(text)

        web_pattern = r'\b(?:https?://)?(?:www\.)?[-a-zA-Z0-9.]+(?:\.[a-zA-Z]+)+(?:/[-a-zA-Z0-9_/]*)?\b'
        text = re.sub(web_pattern, '', text)

        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z0-9]+\b'
        text = re.sub(email_pattern, '', text)

        return text

    def split_text(self, text):
        pattern = ',|\.|;|:|\?|!|，|。|；|：|？|！|、|——|\.\.\.|\.\.\.\.\.\.'

        return re.split(pattern, text)

    def clean_mark(self, text):
        pattern = r'[\.\,\;\:\"\'\?\!\(\)\[\]\{\}\\\/\|\+\-\=\_\*\&\%\#\<\>\~\$\·\r?\n]|[，。、？！；：“”‘’（）【】《》…～—｜]'
        text = re.sub(pattern, '', text)

        return text


class HandleMedia:
    def __init__(self):
        super().__init__()

    def video2audio(self, in_path, out_path):
        video = VideoFileClip(in_path)
        audio = video.audio
        audio.write_audiofile(out_path)

        audio.close()
        video.close()

    def slice_audio(self, in_path, out_path, slice, overlap):
        audio = AudioSegment.from_file(in_path)
        step = slice - overlap
        chunks = []
        for i in range(0, len(audio), step):
            chunk = audio[i:i + slice]
            chunks.append(chunk)

        for i, chunk in enumerate(chunks):
            chunk.export(os.path.join(out_path, f"chunk_{i}.{'mp3'}"))

    def reduce_noise(self, in_path, out_path):
        audio, sample_ratio = librosa.load(in_path, sr=None)
        audio = noisereduce.reduce_noise(audio, sample_ratio, prop_decrease=0.6)
        soundfile.write(out_path, audio, sample_ratio)
