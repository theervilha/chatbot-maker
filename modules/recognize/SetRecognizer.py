from modules.recognize.BaseRecognizer import BaseRecognizer

class SetRecognizer(BaseRecognizer):
    def __init__(self, sets):
        self.sets = sets
        
    def get_sets_by_equal(self, user_message):
        equals = {set: self.get_equals(setvalues, user_message) for set, setvalues in self.sets.items()}
        return {set: found_values for set, found_values in equals.items() if found_values}

    def get_sets_by_contains(self, user_message):
        contains = {set: self.get_contains(setvalues, user_message) for set, setvalues in self.sets.items()}
        return {set: found_values for set, found_values in contains.items() if found_values}

    def get_sets_by_words_equal(self, user_message):
        equals = {set: self.get_words_equals(setvalues, user_message) for set, setvalues in self.sets.items()}
        return {set: found_values for set, found_values in equals.items() if found_values}

    def get_sets_by_words_contains(self, user_message):
        contains = {set: self.get_words_contains(setvalues, user_message) for set, setvalues in self.sets.items()}
        return {set: found_values for set, found_values in contains.items() if found_values}