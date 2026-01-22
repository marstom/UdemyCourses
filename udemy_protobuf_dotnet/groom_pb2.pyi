from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RoomRegistrationRequest(_message.Message):
    __slots__ = ("room_name",)
    ROOM_NAME_FIELD_NUMBER: _ClassVar[int]
    room_name: str
    def __init__(self, room_name: _Optional[str] = ...) -> None: ...

class RoomRegistrationResponse(_message.Message):
    __slots__ = ("room_id",)
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    room_id: str
    def __init__(self, room_id: _Optional[str] = ...) -> None: ...

class GetGroomRequest(_message.Message):
    __slots__ = ("room_name",)
    ROOM_NAME_FIELD_NUMBER: _ClassVar[int]
    room_name: str
    def __init__(self, room_name: _Optional[str] = ...) -> None: ...

class GetGroomResponse(_message.Message):
    __slots__ = ("room_name",)
    ROOM_NAME_FIELD_NUMBER: _ClassVar[int]
    room_name: str
    def __init__(self, room_name: _Optional[str] = ...) -> None: ...
