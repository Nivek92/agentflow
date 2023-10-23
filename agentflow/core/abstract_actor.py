from abc import ABC, abstractmethod
from typing import Type, TypeVar

from .abstract_event import AbstractEvent
from .event_emitter import EventEmitter

TEvent= TypeVar('TEvent', bound=AbstractEvent)

class AbstractActor(ABC):

    name: str
    trigger_event: Type[TEvent]

    def __init__(self, event_emitter: EventEmitter):
        self._event_emitter = event_emitter
        self._event_emitter.on(self.trigger_event, self._handle_event)

    @property
    def name(self):
        return self._name

    @abstractmethod
    def _handle_event(self, event: TEvent):
        pass