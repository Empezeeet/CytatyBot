import requests
import websocket
import json

from Framework.PacketFactory import PacketFactory
from Framework.Logger import Logger, LogType
from Framework.Bot import Bot
from Framework.HeartbeatManager import HeartbeatManager
from Framework.Commands.SlashCommand import SlashCommand

class DiscordHandler:



    def __init__(self, bot: Bot):

        self._websocket: websocket.WebSocket = websocket.WebSocket()
        self._bot: Bot = bot
        self._logger: Logger = Logger("DiscordHandler")

        self._lastSequence = None
        self.event: str = ""
        self.heartbeatIntervalMilliseconds: int = 0
        self.sessionID = ""
        self.resumeURL = ""
        self.commands: list[SlashCommand] = []



        self._logger.print("Initializing DiscordHandler")
        # Connect to Discord and receive Hello Event
        self._connectToGateway()
        # Start heart beating thread.
        self._startHeartbeat(self.heartbeatIntervalMilliseconds)
        # Send Identify
        self._identify()

        # Upload Commands.
        self._setupCommands()

        # Start autohandler loop.
    def _autohandler(self):
        while True:
            packet = self.receiveResponse()
            # try to auto handle response
            # if handler couldn't handle

    # loads commands and sends them off to discord
    def _setupCommands(self):
        url: str = f"https://discord.com/api/v10/applications/{self._bot.appid}/commands"
        headers: dict = {"Authorization": f"Bot {self._bot.getToken()}"}
        command: SlashCommand
        for command in self._bot.commands:
            r = requests.post(url, headers=headers, json=command.setupPacket)
            self._logger.print(f"Loaded Command {command.name} with status: {r.status_code}\n {r.json()}")
            if r.status_code == 201:
                self.commands.append(command)

    # function handles identifying and receiving Ready event.
    def _identify(self):
        self._logger.print("[Identify] Sent Identify Packet")
        self._websocket.send(json.dumps(PacketFactory.identifyPacket(self._bot.getToken(), self._lastSequence)))
        # Receive READY event
        self._logger.print("[Identify] Receiving READY event")
        self.handleResponse()

    def _startHeartbeat(self, intervalMilliseconds: int):
        self._heartBeatManager: HeartbeatManager = HeartbeatManager(intervalMilliseconds, self._websocket, self._logger)

    # function handles connecting to gateway and receiving Hello Packet.
    def _connectToGateway(self):
        self._logger.print("Connecting to Discord's Gateway")
        self._websocket.connect('wss://gateway.discord.gg/?v=6&encoding=json')

        if not self.handleResponse()[0]:
            self._logger.print("[eventConnect To Gateway] Error occurred when handling Hello Event", logType=LogType.ERROR)
            breakpoint()
        self._logger.print("[Connect To Gateway] Successfully connected to Discord's Gateway")

    # Returns TRUE if response was handled automatically
    # Returns FALSE if program couldn't handle response.
    def handleResponse(self) -> [bool, dict]:
        response: dict = self.receiveResponse()
        match response.get('op', -1):
            case -1:
                # program occurred error so return false
                self._logger.print(f"[Handler Error] Couldn't auto-handle response!\n Response:\n{response}\n----")
                breakpoint()
                return [False, response]
            case 7:
                # TODO OP 07
                self._logger.print(f"[Handler] Gateway requested connection resume")
                self._websocket.connect('wss://gateway.discord.gg/?v=6&encoding=json')
                self._websocket.send(
                    json.dumps(
                        PacketFactory.resumePacket(self._bot.getToken(), self.sessionID, self._lastSequence)
                    )
                )
                raise NotImplementedError()
            case 10:
                self._logger.print("Received HELLO event.")
                # Hello Event
                try:
                    self.heartbeatIntervalMilliseconds = response.get("d").get("heartbeat_interval")
                    return [True, {}]
                except AttributeError as e:
                    self._logger.print("chuj mniue jasny strzeli\n" + str(e))
                    breakpoint()
                    return [False, response]

            case 0:
                self._logger.print("Received READY event.")
                # Ready event
                try:
                    self.sessionID = response.get("d").get("session_id")
                    self.resumeURL = response.get("d").get("resume_url")
                except AttributeError as e:
                    self._logger.print("AT READY: chuj mniue jasny strzeli\n" + str(e))
                    breakpoint()
                    return [False, response]
                self._logger.print("Sucessfully parsed READY event")
                return [True, {}]
            case 11:
                self._logger.print("Heartbeat received")

        match response.get("t", "nula"):
            case "nula":
                self._logger.print("Error occurred while trying to parse type event response!", logType=LogType.ERROR)
            ### TODO: write command handler!
            case "INTERACTION_CREATE":
                self._handleCommand(response)

    def _handleCommand(self, response: dict):
        ...
    def receiveResponse(self) -> dict:
        response = None
        try:
            response = self._websocket.recv()
        except websocket.WebSocketConnectionClosedException as e:
            self._logger.print("[Gateway] Connection closed")
            self._logger.print(f"An error occurred!\n {e}")
            self._websocket.close()
            breakpoint()
        self._lastSequence = json.loads(response)['s']
        return json.loads(response)




