from Framework.Commands import SlashCommand


class Bot:
    def __init__(self, token, appid, commands: list[SlashCommand] = None):
        self._token = token
        self.appid = appid
        if commands is None:
            self.commands = []
        else:
            self.commands = commands

    def getToken(self) -> str:
        return self._token