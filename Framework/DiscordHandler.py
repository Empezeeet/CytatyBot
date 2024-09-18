import websocket
import json

from Framework.PacketFactory import PacketFactory
from Framework.Logger import Logger, LogType
from Framework.Bot import Bot
from Framework.HeartbeatManager import HeartbeatManager

class DiscordHandler:



    def __init__(self, bot: Bot):

        self._websocket: websocket.WebSocket = websocket.WebSocket()
        self._bot: Bot = bot
        self._logger: Logger = Logger("DiscordHandler")

        self._lastSequence = None
        self.event: str = ""
        self.heartbeatIntervalMiliseconds: int = 0
        self.sessionID = ""
        self.resumeURL = ""




        self._logger.print("Initializing DiscordHandler")
        # Connect to Discord and receive Hello Event
        self._connectToGateway()
        # Start heart beating thread.
        self._startHeartbeat(self.heartbeatIntervalMiliseconds)
        # Send Identify
        self._identify()

        # Upload Commands.



    # function handles identifying and receiving Ready event.
    def _identify(self):
        self._logger.print("[Identify] Sent Identify Packet")
        self._websocket.send(json.dumps(PacketFactory.identifyPacket(self._bot.getToken(), self._lastSequence)))
        # Receive READY event
        self._logger.print("[Identify] Receiving READY event")
        self.handleResponse()

    def _startHeartbeat(self, intervalMiliseconds):
        self._heartBeatManager: HeartbeatManager = HeartbeatManager(intervalMiliseconds, self._websocket, self._logger)

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
        waitForPacket: bool = True
        while waitForPacket:
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
                        self.heartbeatIntervalMiliseconds = response.get("d").get("heartbeat_interval")
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




