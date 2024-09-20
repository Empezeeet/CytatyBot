import requests
import json
import re

from Framework.Commands import SlashCommand

class LeaderboardCommand(SlashCommand.SlashCommand):
    def __init__(self):
        (super(LeaderboardCommand, self)
             .__init__(
                name="Leaderboard",
                description="Pokazuje statystyki cytatów",
                options=[]
            )
        )
    @staticmethod
    def on_use(interactionToken: str, interactionID: str, token:str):
        callbackURL = f"https://discord.com/api/v10/interactions/{interactionID}/{interactionToken}/callback"
        channelMessages = requests.get("https://discord.com/api/v10/channels/1012458745248358461/messages", headers={"Authorization": f"Bot {token}"})
        userCount: dict[str, int] = {}
        message_content: str = ""
        for message in json.loads(channelMessages.text):
            # get actual message
            message_content = message["content"]
            try:
                user: str = re.search(r'<@(\d+)>', message_content).group(0)
            except AttributeError:
                continue
            # add one to user's cytaty count or set to zero if none were previously detected.
            userCount[user] = userCount.get(user, 0) + 1
        # preparing message to be sent to user
        outputMessage: str = "# Leaderboard cytatów:\n"
        for i in range(1, 5):
            index = max(userCount, key=userCount.get)
            outputMessage += f"- TOP{i}: {userCount[index]} - {index}\n"
            del userCount[index]


        # sending message to user
        r = requests.post(callbackURL, headers={"Content-Type": "application/json"}, json={
            "type":4,
            "data": {
                "content":outputMessage
            }
        })
        print("Command success: " + str(r.status_code))