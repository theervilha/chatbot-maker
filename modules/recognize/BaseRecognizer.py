from abc import ABC

class BaseRecognizer(ABC):
    def get_equals(self, setvalues, user_message):
        # "I cannot purchase that" == "I cannot purchase that"
        print('getting equals: ',setvalues)
        return [v for v in setvalues if v == user_message]

    def get_contains(self, setvalues, user_message):
        # "I cannot purchase" in "Well, I cannot purchase that"
        print('getting contains:', setvalues)
        return [v for v in setvalues if v in user_message]

    def get_words_equals(self, setvalues, user_message):
        # values = ['cannot', 'purchase']
        # user_message = "Well, I cannot purchase that"
        # in the words of the user_message... "cannot" == "cannot" AND "purchase" == "purchase"
        # returns the ones who the values found was the same length than expected.
        all_words_equals = []
        for values in setvalues:
            values = values.split()
            min_length_values = len(values)
            words_equals = [set_word for set_word in values for word_message in user_message.split() if set_word == word_message]
            if len(words_equals) == min_length_values:
                all_words_equals.append(words_equals)
        
        return all_words_equals

    def get_words_contains(self, setvalues, user_message):
        # values = ['canno', 'purch']
        # user_message = "Well, I cannot purchase that"
        # in the words of the user_message... "canno" in "cannot" AND "purch" in "purchase"
        # returns the ones who the values found was the same length than expected.
        all_words_equals = []
        for values in setvalues:
            values = values.split()
            min_length_values = len(values)
            words_equals = [set_word for set_word in values for word_message in user_message.split() if set_word in word_message]
            if len(words_equals) == min_length_values:
                all_words_equals.append(words_equals)
        
        return all_words_equals