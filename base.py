from dataclasses import dataclass


@dataclass
class ChatMessage:
    source: str
    author: str
    content: str
