from datetime import datetime
from dataclasses import dataclass


@dataclass
class Note:
    title: str
    content: str | None = None
    created: datetime = ""
    edited: datetime = ""
    due: datetime = ""
