from abc import ABC
import os
from unidecode import unidecode as remove_accents
import re, string

class FileExtractor(ABC):
    def __init__(self, folder='sets'):
        print(f'Extracting {folder}')
        read = lambda setname: open(f'{folder}/{setname}', 'r', encoding='utf-8').read().splitlines()
        setsname = list(os.walk(folder))[0][2]
        self.sets = {setname.replace('.txt', ''): read(setname) for setname in setsname}

    def cleanText(self, text, removeAccents=True):
        if text[:2] == '- ':
            text = text[2:]

        if removeAccents:
            text = remove_accents(text)

        text = re.sub(' +', ' ', text)
        text = text.lower()
        text = text.strip()
        text = text.translate(str.maketrans('', '', string.punctuation))
        return text