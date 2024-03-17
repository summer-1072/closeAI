import re
import pdfplumber
from docx import Document
from moviepy.editor import *
from pydub import AudioSegment
from opencc import OpenCC


class Text:
    def __init__(self, stop_word_path):
        super().__init__()

        self.stop_words = []
        with open(stop_word_path, 'r') as file:
            for word in file:
                self.stop_words.append(word.strip())

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

    def filter_text(self, text):
        pattern = f"[{re.escape(''.join(self.stop_words))}]"
        text = re.sub(pattern, '', text)
        text = text.replace('\n', '')

        return text

    def tradition2simplicity(self, text):
        return OpenCC('t2s').convert(text)


class Media:
    def __init__(self):
        super().__init__()

    def video2audio(self, in_path, out_path):
        video = VideoFileClip(in_path)
        audio = video.audio
        audio.write_audiofile(out_path)

        audio.close()
        video.close()

    def split_audio(self, in_path, out_path, length, overlap):
        audio = AudioSegment.from_file(in_path)
        size = length - overlap
        chunks = []

        for i in range(0, len(audio), size):
            chunk = audio[i:i + length]
            chunks.append(chunk)

        for i, chunk in enumerate(chunks):
            chunk.export(os.path.join(out_path, f"chunk_{i}.{'mp3'}"))
