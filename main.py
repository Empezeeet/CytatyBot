from disintegration import DiscordHandler as discord
from disintegration import Bot as app
import PingCommand
import LeaderboardCommand
from GameCommand import GameCommand


TOKEN = "secret token" # NOQA
# TODO: bot crashes  a while. Maybe create support for resume packet!

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
