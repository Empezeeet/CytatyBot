from Framework import DiscordHandler as discord
from Framework import Bot as app
import PingCommand

# TODO: Remove token on public release!
TOKEN = "MTI4NjEzNDQyNzg1MTgxNzAzMg.GWsWE0.JnxYw5Yr7b3cC7tbWEHiOC9SpxoD9cfVK_Mavo"


pingCommand: PingCommand = PingCommand.PingCommand()

handler: discord.DiscordHandler = discord.DiscordHandler(
    app.Bot(
        TOKEN,
        1286134427851817032,
        [pingCommand]
    )
)