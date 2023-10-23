from abc import ABC
from pydantic import BaseModel, Field
from datetime import datetime

class AbstractEvent(ABC, BaseModel):

    name: str
    description: str
    created_at: datetime = Field(default_factory=datetime.now)

    def to_json(self) -> str:
        return self.json()

    @classmethod
    def from_json_str(cls, json_str: str) -> 'AbstractEvent':
        return cls.parse_raw(json_str)