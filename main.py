from Framework import DiscordHandler as discord
from Framework import Bot as app
import PingCommand
import LeaderboardCommand
from GameCommand import GameCommand

# TODO: Remove token on public release!
TOKEN = "MTI4NjEzNDQyNzg1MTgxNzAzMg.GWsWE0.JnxYw5Yr7b3cC7tbWEHiOC9SpxoD9cfVK_Mavo" # NOQA
# TODO: bot crashes after a while. Maybe create support for resume packet!

pingCommand: PingCommand = PingCommand.PingCommand()
leaderboardCommand: LeaderboardCommand = LeaderboardCommand.LeaderboardCommand()
gameCommand: GameCommand = GameCommand()
handler: discord.DiscordHandler = discord.DiscordHandler(
    app.Bot(
        TOKEN,
        1286134427851817032,"Cytatów",
        {leaderboardCommand.name: leaderboardCommand,
                    pingCommand.name: pingCommand,
                    gameCommand.name: gameCommand
        }
    )
)
