from modules.recognize.BaseRecognizer import BaseRecognizer

class EntityRecognizer(BaseRecognizer):
    def __init__(self, entities):
        self.entities = entities

    def get_entities_by_equal(self, user_message):
        equals = {
            topic: {item: self.get_equals(item_content, user_message)}
                    for topic, entity_items in self.entities.items() 
                    for item, item_content in entity_items.items()
        }
        return {topic: {item: found_values} for topic, found_values in equals.items() 
                                            for item, item_content in found_values.items() if item_content}
    
    def get_entities_by_contains(self, user_message):
        contains = {
            topic: {item: self.get_contains(item_content, user_message)}
                    for topic, entity_items in self.entities.items() 
                    for item, item_content in entity_items.items()
        }
        return {topic: {item: found_values} for topic, found_values in contains.items() 
                                            for item, item_content in found_values.items() if item_content}

    def get_entities_by_words_equal(self, user_message):
        equal = {
            topic: {item: self.get_words_equals(item_content, user_message)}
                    for topic, entity_items in self.entities.items() 
                    for item, item_content in entity_items.items()
        }
        return {topic: {item: found_values} for topic, found_values in equal.items() 
                                            for item, item_content in found_values.items() if item_content}

    def get_entities_by_words_contains(self, user_message):   
        contains = {
            topic: {item: self.get_words_contains(item_content, user_message)}
                    for topic, entity_items in self.entities.items() 
                    for item, item_content in entity_items.items()
        }
        return {topic: {item: found_values} for topic, found_values in contains.items() 
                                            for item, item_content in found_values.items() if item_content}