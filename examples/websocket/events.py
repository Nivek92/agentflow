from agentflow.core.abstract_event import AbstractEvent


class SumRequestEvent(AbstractEvent):
    name: str = "sum_request_event"
    description: str ="Request the sum of numbers"

    a: int
    b: int

class SumResponseEvent(AbstractEvent):
    name: str = "sum_response_event"
    description: str ="Result of an addition"

    sum: int