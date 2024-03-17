import os

import whisper
from base.document import Media


class Whisper:
    def __init__(self, name, device):
        self.model = whisper.load_model(name, device)

    def __call__(self, file_path):
        return self.model.transcribe(file_path)['text']


# model = Whisper('large', 'cpu')


def transcribe_audio(audio_path):
    # 加载模型
    model = whisper.load_model("base")  # 你可以根据需要选择不同大小的模型

    # 处理音频并获取结果
    result = model.transcribe(audio_path, verbose=True)

    # 打印识别的语言
    print("Detected language:", result["language"])

    # 打印按秒分割的转录文本
    # Whisper 自动提供包含时间戳的segments
    for segment in result["segments"]:
        start = segment["start"]
        end = segment["end"]
        text = segment["text"]
        print(f"{start}-{end} seconds: {text}")

# media = Media()
# media.video2audio('/Users/kaiwang/Downloads/demo/video/demo.mp4',
#                   '/Users/kaiwang/Downloads/demo/mp3/demo.mp3')
# media.split_audio('/Users/kaiwang/Downloads/demo/mp3/demo.mp3',
#                   '/Users/kaiwang/Downloads/demo/paragraph', 30000, 5000)

for file in sorted(os.listdir('/Users/kaiwang/Downloads/demo/paragraph')):
    if 'mp3' in file:
        print(file)
        transcribe_audio(os.path.join('/Users/kaiwang/Downloads/demo/paragraph', file))
        # text = model(os.path.join('/Users/kaiwang/Downloads/demo/paragraph', file))