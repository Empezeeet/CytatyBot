import json
import time

from Framework.Commands import SlashCommand
import requests
import random
import re
class GameCommand(SlashCommand.SlashCommand):
    def __init__(self):
        super(GameCommand, self).__init__("Graj", "Rozpocznij grę w cytaty!")
    @staticmethod
    def on_use(interactionToken: str, interactionID: str, token: str):
        callbackURL = f"https://discord.com/api/v10/interactions/{interactionID}/{interactionToken}/callback"
        channelMessages = requests.get("https://discord.com/api/v10/channels/1012458745248358461/messages",
                                       headers={"Authorization": f"Bot {token}"})

        channelMessages = json.loads(channelMessages.text)
        message: str = ""
        while True:
            message = random.choice(channelMessages)["content"]
            if message.count("~") == 2:
                break
        user: str = re.search(r'<@(\d+)>', message).group(0)
        idx1 = message.index("~")
        idx2 = message.rindex("~")
        extractedMessage: str = ""
        for idx in range(idx1+1, idx2):
            extractedMessage += message[idx]
        r = requests.post(callbackURL, headers={"Content-Type": "application/json"}, json={
            "type":4,
            "data": {
                "content": f"Kto to powiedział?\n\"***{extractedMessage.strip()}***\"\nOdpowiedź to: ||{user}||"
            }
        })
