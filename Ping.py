from Framework.Commands import SlashCommand


class Ping(SlashCommand):
    def __init__(self, name: str, description: str):
        super().__init__(name, description)
    @staticmethod
    def on_use():
        ...