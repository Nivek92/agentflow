import datetime

from ..core.abstract_event import AbstractEvent

class Logger:
    @staticmethod
    def log_event(event: AbstractEvent):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] Received event: {event}")