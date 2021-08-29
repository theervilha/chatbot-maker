from modules.extractors.BaseFileExtractor import FileExtractor

class Entities(FileExtractor):
    def __init__(self):
        super().__init__(folder='entities')

    def get(self, removeAccents=True):
        self.entities = {}
        variationsOfValue = []
        for topic, setContent in self.sets.items():
            self.entities[topic] = {}

            for setItem in setContent:
                if setItem != '':
                    if setItem[0] != '-':
                        value = setItem
                    else:
                        variationsOfValue.append(self.cleanText(setItem, removeAccents=removeAccents))
                else:
                    variationsOfValue = list(set(variationsOfValue))
                    self.entities[topic][value] = variationsOfValue
                    variationsOfValue = []
        
        return self.entities