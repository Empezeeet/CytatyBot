import requests
from requests import options

from Framework.Commands import SlashCommand as slashCommand
class PingCommand(slashCommand.SlashCommand):
    def __init__(self):
        super(PingCommand, self).__init__("Ping", "Responds wih Pong!", options=[])
    @staticmethod
    def on_use(interactionToken: str, interactionID: str, applicationToken: str):
        # respond with pong
        r = requests.post(
            url=f"https://discord.com/api/v10/webhooks/{interactionID}/{interactionToken}",
            headers={"Content-Type": "application/json"},
            json={
                "type":4,
                "data": {
                    "content":"Pong!"
                }
            }
        )
        print("COMMAND STATUS: " + str(r.status_code))
