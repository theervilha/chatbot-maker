from modules.extractors.BaseFileExtractor import FileExtractor

class Sets(FileExtractor):
    def __init__(self):
        super().__init__(folder='sets')
 
    def get(self, removeAccents=True):
        clean = lambda setValues: list(set([self.cleanText(text, removeAccents=removeAccents) for text in setValues]))
        self.sets = {setName: clean(setValues) for (setName, setValues) in self.sets.items()}
        return self.sets
    
    
    ''' def readSets(self):
        read = lambda setname: open(f'sets/{setname}', 'r', encoding='utf-8').read().splitlines()
        self.sets = {setname.replace('.txt', ''): read(setname) for setname in self.setsname}
        self.sets = self.clearSets(self.sets)

        self.setsOnlyTokens = {setName: set for setName, set in self.sets.items if "only_tokens" in setName}
        self.sets = {setName: set for setName, set in self.sets.items if "only_tokens" not in setName}

    def recognize(self, message, context):
        self.message = message
        self.context = context

        self.setsRecognizeds = []
        for setName, set in sets.items():
            itemsInMsg = [setItem for setItem in set if self.setItemInMsg(setItem)]
            if itemsInMsg != []:
                self.setsRecognizeds.append(setName)
        
        # special - token
        # *não consigo* *comprar* algo

        # special - structure
        # *não consigo* mas *quero comprar*

    def setItemInMsg(self, setItem):
        if setItem in self.message:
            return setItem'''