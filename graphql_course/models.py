import enum
from datetime import datetime
from dataclasses import dataclass


class NoteState(enum.StrEnum):
    pending = enum.auto()
    done = enum.auto()


@dataclass
class Note:
    title: str
    content: str | None = None
    created: datetime = ""
    edited: datetime = ""
    due: datetime = ""
    state: NoteState = NoteState.pending
