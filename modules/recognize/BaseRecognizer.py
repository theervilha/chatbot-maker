from abc import ABC

class BaseRecognizer(ABC):
    def __init__(self, sets, entities):
        self.sets = sets
        self.entities = entities

    def contains(self):
        pass