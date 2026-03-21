import asyncio

import groom_pb2



class Room:
    def __init__(self, room: str):
        self.room = room
        self.users: dict[str, asyncio.Queue] = {}
        self.messages: list[groom_pb2.ReceivedMessage] = []

    def add_user(self, user: str):
        self.users[user] = asyncio.Queue()

    async def add_message(self, message: groom_pb2.ReceivedMessage):
        for user in self.users.values():
            await user.put(message)

    async def boradcast_to_room(self, message: groom_pb2.ReceivedMessage):
        for user in self.users.values():
            await user.put(message)

    async def get_all_users_messages(self) -> list[groom_pb2.ReceivedMessage]:
        messages = []
        for user in self.users.values():
            messages.append(await user.get())
        return messages

    async def get_user_message(self, user_name: str) -> groom_pb2.ReceivedMessage:
        return await self.users[user_name].get()


class Rooms:
    def __init__(self):
        self.rooms: dict[str, Room] = {}

    def _add_room(self, room: str):
        if room not in self.rooms:
            self.rooms[room] = Room(room)

    def add_user_to_room(self, room: str, user: str):
        self._add_room(room)
        self.rooms[room].add_user(user)

    # def add_message_to_room(self, room: str, message: groom_pb2.ReceivedMessage):
    # self.rooms[room].add_message(message)

    def get_room(self, room: str) -> Room:
        return self.rooms[room]
