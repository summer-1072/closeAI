import re
import pdfplumber
from docx import Document


def load_stopwords(file_path):
    words = []
    with open(file_path, 'r') as f:
        for word in f:
            words.append(word.strip())

    return words


def read_pdf(file_path):
    text = ''

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    return text


def read_docx(file_path):
    text = ''

    doc = Document(file_path)
    for paragraph in doc.paragraphs:
        text += paragraph.text

    return text


def read_txt(file_path):
    with open(file_path, 'r') as file:
        text = file.read()

    return text


def filter_text(text, stopwords):
    pattern = f"[{re.escape(''.join(stopwords))}]"
    text = re.sub(pattern, '', text)
    text = text.replace('\n', '')

    return text