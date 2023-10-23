from typing import Type
from agentflow.core.abstract_actor import AbstractActor
from agentflow.core.abstract_event import AbstractEvent
from examples.websocket.events import SumRequestEvent, SumResponseEvent

class SumActor(AbstractActor):

    name: str = "sum_actor"
    trigger_event: Type[AbstractEvent] = SumRequestEvent

    def _handle_event(self, event: SumRequestEvent):
        # Extract numbers from the event payload
        result = event.a + event.b
        
        # Create and emit a response event
        response_event = SumResponseEvent(sum=result)
        self._event_emitter.emit(response_event)