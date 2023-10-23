from typing import Type
from ..core.abstract_event import AbstractEvent
from ..core.event_emitter import EventEmitter

class TerminalClient:
    def __init__(self, event_emitter: EventEmitter, event: Type[AbstractEvent]):
        self._event_emitter = event_emitter
        self._event = event

    def run(self):

        event_name = event_name = self._event.__fields__['name'].default

        # Gather parameters for the event
        params = {}
        for attr, attr_type in self._event.__annotations__.items():
            # Skip predefined attributes
            if attr in ["name", "description"]:
                continue

            user_input = input(f"Enter value for {event_name}.{attr} ({attr_type.__name__}) or 'q' to quit: ")

            if user_input.lower() == 'q':
                return

            try:
                # Convert the input to the correct type
                params[attr] = attr_type(user_input)
            except ValueError:
                print(f"Invalid input. Please enter a valid {attr_type.__name__}.")
                continue

        # Emit the event with the gathered parameters
        event_instance = self._event(**params)
        self._event_emitter.emit(event_instance)