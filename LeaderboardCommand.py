

import requests
import json
import re
from Framework.Commands.Option import Option
from Framework.Commands import SlashCommand
#TODO: Uploading this command is unsuccessful. See DiscordHandler_1726840941.606717.botlog @ line 12
class LeaderboardCommand(SlashCommand.SlashCommand):
    def __init__(self):
        option = Option(type=7, name="cytaty", description="Kanał z którego pobierane są cytaty", required=True)
        print(option.dict())
        (super(LeaderboardCommand, self)
         .__init__(
            name="Leaderboard",
            description="Pokazuje statystyki cytatów",
            options=[option]))
    @staticmethod
    def on_use(interactionToken: str, interactionID: str, token:str):
        callbackURL = f"https://discord.com/api/v10/interactions/{interactionID}/{interactionToken}/callback"
        channelMessages = requests.get("https://discord.com/api/v10/channels/1012458745248358461/messages", headers={"Authorization": f"Bot {token}"})
        userCount: dict[str, int] = {}
        message_content: str = ""
        for message in json.loads(channelMessages.text):
            message_content = message["content"]
            try:
                user: str = re.search(r'<@(\d+)>', message_content).group(0)
            except AttributeError:
                continue
            userCount[user] = userCount.get(user, 0) + 1
        print(userCount)
        outputMessage: str = "# Leaderboard cytatów:\n"
        for i in range(1, 5):
            index = max(userCount, key=userCount.get)
            outputMessage += f"- TOP{i}: {userCount[index]} - {index}\n"
            del userCount[index]



        r = requests.post(callbackURL, headers={"Content-Type": "application/json"}, json={
            "type":4,
            "data": {
                "content":outputMessage
            }
        })

