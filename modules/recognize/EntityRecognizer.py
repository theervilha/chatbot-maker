from modules.recognize.BaseRecognizer import BaseRecognizer

class EntityRecognizer(BaseRecognizer):
    def __init__(self, entities):
        self.entities = entities

    def get_entities_by_equal(self, user_message):
        [print({topic: {item: item_content}})
                    for topic, entity_items in self.entities.items() 
                    for item, item_content in entity_items.items()
        ]
        return {
            topic: {item: self.get_equals(item_content, user_message)}
                    for topic, entity_items in self.entities.items() 
                    for item, item_content in entity_items.items() if self.get_equals(item_content, user_message)
        }
        
    def get_entities_by_contains(self, user_message):
        [print({topic: {item: item_content}})
            for topic, entity_items in self.entities.items() 
            for item, item_content in entity_items.items()
        ]

        return {
            topic: {item: self.get_contains(item_content, user_message)}
                    for topic, entity_items in self.entities.items() 
                    for item, item_content in entity_items.items() if self.get_contains(item_content, user_message)
        }
