import requests
from disintegration.Commands import SlashCommand

class PingCommand(SlashCommand.SlashCommand):
    def __init__(self):
        super(PingCommand, self).__init__("Ping", "Responds wih Pong!", options=[])
    @staticmethod
    def on_use(interactionToken: str, interactionID: str, token: str):
        # respond with pong
        r = requests.post(
            url=f"https://discord.com/api/v10/interactions/{interactionID}/{interactionToken}/callback",
            headers={"Content-Type": "application/json"},
            json={
                "type":4,
                "data": {
                    "content":"Pong!"
                }
            }
        )
        print("COMMAND STATUS: " + str(r.status_code))
