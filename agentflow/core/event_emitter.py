import signal
import time
from typing import Dict, List, Type, Callable
import queue
import threading

from .abstract_event import AbstractEvent

class EventEmitter:
    def __init__(self, stop_at_exit=True):
        self._listeners: Dict[Type[AbstractEvent], List[Callable[[AbstractEvent], None]]] = {}
        self._universal_listeners: List[Callable[[AbstractEvent], None]] = []  # Listeners for all events
        self._event_queue = queue.Queue()  # Queue to hold events
        self._stop_event = threading.Event()  # Event to signal the worker to stop
        self._worker = threading.Thread(target=self._process_queue)  # Worker thread
        self._worker.start()

        if stop_at_exit:
            signal.signal(signal.SIGTERM, self._signal_handler)
            signal.signal(signal.SIGINT, self._signal_handler)

    # necessary to use as context
    def __enter__(self):
        return self

    # necessary to use as context
    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def _signal_handler(self, signum, frame):
        self.stop()

    def on(self, event_type: Type[AbstractEvent], listener: Callable[[AbstractEvent], None]):
        """Register a listener for a specific event type."""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)

    def on_all(self, listener: Callable[[AbstractEvent], None]):
        """Register a listener for all event types."""
        self._universal_listeners.append(listener)

    def emit(self, event: AbstractEvent):
        """Add an event to the queue for processing."""
        self._event_queue.put(event)

    def _process_queue(self):
        """Continuously process events from the queue in the order they were received."""
        while not self._stop_event.is_set():
            try:
                event = self._event_queue.get(timeout=1)  # Wait for an event
                self._notify_listeners(event)
                self._event_queue.task_done()
            except queue.Empty:
                pass

    def _notify_listeners(self, event: AbstractEvent):
        """Notify registered listeners for the given event."""
        event_type = type(event)

        # Notify the universal listeners
        for listener in self._universal_listeners:
            listener(event)

        if event_type in self._listeners:
            for listener in self._listeners[event_type]:
                listener(event)

    def is_queue_empty(self) -> bool:
        return self._event_queue.empty()

    def stop(self):
        while not self.is_queue_empty():
            time.sleep(0.2)  # Sleep for a short duration before checking again
        """Stop the worker thread."""
        self._stop_event.set()
        self._worker.join()
