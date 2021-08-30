from modules.extractors.BaseFileExtractor import FileExtractor

class Sets(FileExtractor):
    def __init__(self):
        super().__init__(folder='sets')
 
    def get(self, removeAccents=True):
        clean = lambda setValues: list(set([self.cleanText(text, removeAccents=removeAccents) for text in setValues]))
        self.sets = {setName: clean(setValues) for (setName, setValues) in self.sets.items()}
        return self.sets