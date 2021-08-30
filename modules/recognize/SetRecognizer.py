from modules.recognize.BaseRecognizer import BaseRecognizer

class SetRecognizer(BaseRecognizer):
    def __init__(self, sets):
        self.sets = sets
        
    def get_sets_by_equal(self, user_message):
        return {set: self.get_equals(values, user_message) for set, values in self.sets.items() if self.get_equals(values, user_message)}

    def get_sets_by_contains(self, user_message):
        return {set: self.get_contains(values, user_message) for set, values in self.sets.items() if self.get_contains(values, user_message)}
