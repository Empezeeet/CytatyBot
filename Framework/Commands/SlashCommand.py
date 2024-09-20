from abc import abstractmethod
from Framework.Commands import Option

class SlashCommand:
    def __init__(self, name: str, description: str, options: list[Option] = None):
        if options is None:
            options = []
        self.name = name
        self.description = description
        self.setupPacket = {
            "name":name.lower(),
            "type":1,
            "description":description,
            "options": options
        }
    @staticmethod
    @abstractmethod
    def on_use(interactionToken: str, interactionID: str, applicationToken: str):
        pass
