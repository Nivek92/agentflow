import asyncio
from typing import Type
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
import json

from ..core.abstract_event import AbstractEvent
from ..core.event_emitter import EventEmitter

class WebSocketServer:
    def __init__(self, events, actors):
        self._app = FastAPI()
        self._event_classes = {}
        self._actor_classes = actors
        self._sessions = {}


        for event in (events or []):
            self._register_event(event)

    def _register_event(self, event: Type[AbstractEvent]):
        event_name = event.__fields__['name'].default

        if type(event_name) is not str:
            print(f"Error: 'name' attribute for {event.__name__} is undefined!")
            return

        self._event_classes[event_name] = event

        @self._app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            
            # Create a session-specific EventEmitter
            event_emitter = EventEmitter()
            
            # Relay every event handled by the EventEmitter via WebSocket
            def relay_event(event: AbstractEvent):
                asyncio.create_task(websocket.send_text(event.to_json()))

            event_emitter.on_all(relay_event)
            
            # Initialize session-specific actors
            actor_instances = [actor(event_emitter=event_emitter) for actor in self._actor_classes]
            
            self._sessions[websocket] = {
                'event_emitter': event_emitter,
                'actors': actor_instances
            }

            try:
                while True:
                    await self._receive_data(websocket)
            except WebSocketDisconnect:
                del self._sessions[websocket]

    async def _receive_data(self, websocket: WebSocket):
        data_str = await websocket.receive_text()
        data = json.loads(data_str)
        event_name = data.get("name")
        
        if event_name in self._event_classes:
            event_instance = self._event_classes[event_name].from_json_str(data_str)
            event_emitter = self._sessions[websocket]['event_emitter']
            event_emitter.emit(event_instance)

    def start(self):
        uvicorn.run(self._app, host="0.0.0.0", port=8000)
