import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Player(_message.Message):
    __slots__ = ("id", "name", "is_active", "last_login", "login_time", "cur_ad", "status", "address", "previous_games", "inventory")
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NEW: _ClassVar[Player.Status]
        CONFIRMED: _ClassVar[Player.Status]
        DIED: _ClassVar[Player.Status]
    NEW: Player.Status
    CONFIRMED: Player.Status
    DIED: Player.Status
    class InventoryEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    LAST_LOGIN_FIELD_NUMBER: _ClassVar[int]
    LOGIN_TIME_FIELD_NUMBER: _ClassVar[int]
    CUR_AD_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_GAMES_FIELD_NUMBER: _ClassVar[int]
    INVENTORY_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    is_active: bool
    last_login: _timestamp_pb2.Timestamp
    login_time: int
    cur_ad: str
    status: Player.Status
    address: Address
    previous_games: _containers.RepeatedScalarFieldContainer[str]
    inventory: _containers.ScalarMap[str, int]
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., is_active: bool = ..., last_login: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., login_time: _Optional[int] = ..., cur_ad: _Optional[str] = ..., status: _Optional[_Union[Player.Status, str]] = ..., address: _Optional[_Union[Address, _Mapping]] = ..., previous_games: _Optional[_Iterable[str]] = ..., inventory: _Optional[_Mapping[str, int]] = ...) -> None: ...

class Address(_message.Message):
    __slots__ = ("street", "city")
    STREET_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    street: str
    city: str
    def __init__(self, street: _Optional[str] = ..., city: _Optional[str] = ...) -> None: ...

class PlayerID(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...
