from typing import Type
from agentflow.core.abstract_actor import AbstractActor
from agentflow.core.abstract_event import AbstractEvent
from agentflow.core.event_emitter import EventEmitter

from agentflow.utility.logger import Logger
from agentflow.utility.terminal_client import TerminalClient

class SumRequestEvent(AbstractEvent):

    name: str = "sum_request_event"
    description: str ="Request the sum of numbers"

    a: int
    b: int

class SumResponseEvent(AbstractEvent):

    name: str = "sum_response_event"
    description: str ="Result of an addition"

    sum: int

class SumActor(AbstractActor):

    name: str = "sum_actor"
    trigger_event: Type[AbstractEvent] = SumRequestEvent

    def _handle_event(self, event: SumRequestEvent):
        # Extract numbers from the event payload
        result = event.a + event.b
        
        # Create and emit a response event
        response_event = SumResponseEvent(sum=result)
        self._event_emitter.emit(response_event)

def return_response_to_user(event: SumResponseEvent):
    print(event.sum)

if __name__ == "__main__":

    event_emitter = EventEmitter()

    event_emitter.on_all(Logger.log_event)

    event_emitter.on(SumResponseEvent, return_response_to_user)

    sum_actor = SumActor(event_emitter=event_emitter)
    
    try:
        user_client = TerminalClient(event_emitter=event_emitter, event=SumRequestEvent)
        user_client.run()
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        event_emitter.stop()