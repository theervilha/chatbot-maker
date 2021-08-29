from abc import ABC
import os
import  unicodedata

class FileExtractor(ABC):
    def __init__(self, folder='sets'):
        print(folder)
        read = lambda setname: open(f'{folder}/{setname}', 'r', encoding='utf-8').read().splitlines()
        setsname = list(os.walk(folder))[0][2]
        self.sets = {setname.replace('.txt', ''): read(setname) for setname in setsname}

    def cleanText(self, text, removeAccents=True):
        if text[2:] == '- ':
            text = text[2:]

        text = text.replace('ç', '@@c')
        if removeAccents:
            removeAccentsAndÇ = lambda text: unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
            text = removeAccentsAndÇ(text)
        text = text.replace('@@c', 'ç')
        
        text = text.lower()
        return text