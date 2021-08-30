from abc import ABC

class BaseRecognizer(ABC):
    def get_equals(self, values, user_message):
        print('getting equals: ',values)
        return [v for v in values if v == user_message]

    def get_contains(self, values, user_message):
        print('getting contains:', values)
        return [v for v in values if v in user_message]