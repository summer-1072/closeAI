import os
import whisper
from openai import OpenAI


class Whisper:
    def __init__(self, model_name, device):
        super().__init__()
        self.model = whisper.load_model(model_name, device)

    def __call__(self, file_path):
        result = self.model.transcribe(file_path)
        language, segments = result['language'], result['segments']

        fragments = []
        for segment in segments:
            fragments.append([[segment['start'], segment['end']], segment['text']])

        return language, fragments


class GPT:
    def __init__(self, license):
        super().__init__()
        self.license = license
        self.client = OpenAI()

    def __call__(self, model_name, prompt, text):
        response = self.client.completions.create(
            model=model_name,
            prompt=prompt,
        )
