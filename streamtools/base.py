import enum
from dataclasses import asdict, dataclass


class EventType(enum.Enum):
    READY = "ready"
    MESSAGE = "message"


@dataclass
class ChatEvent:
    type: EventType
    source: str
    author: str = None
    content: str = None

    def asdata(self):
        data = asdict(self)
        data["type"] = self.type.value
        return data

    def __str__(self):
        return f"{self.source}/{self.type.value} @{self.author} {self.content}"
