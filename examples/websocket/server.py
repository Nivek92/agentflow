from agentflow.utility.websocket_server import WebSocketServer
from examples.websocket.actors import SumActor
from examples.websocket.events import SumRequestEvent, SumResponseEvent


server = WebSocketServer(events=[SumRequestEvent, SumResponseEvent], actors=[SumActor])
server.start()