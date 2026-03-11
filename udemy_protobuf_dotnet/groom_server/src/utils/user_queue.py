import asyncio
import queue

import groom_pb2

from loguru import logger


class UsersQueues:
    def __init__(self):
        self._queues: list[UserQueue] = []
        self._admin_queue = asyncio.Queue()
        # self._admin_queue: list[groom_pb2.ReceivedMessage] = []

    def create_user_queue(self, room: str, user: str):

        for q in self._queues:
            if q.room == room:
                return
        self._queues.append(UserQueue(room=room, user=user))

    # def _get_room_queue(self, room: str):
    #     for q in self._queues:
    #         if q.room == room:
    #             return q
    #     return None

    async def add_message_to_room(self, room: str, msg: str):
        for q in self._queues:
            if q.room == room:
                await q.add_message_to_queue(msg)

        logger.debug(self._queues)

    async def get_message_for_user(self, user: str) -> groom_pb2.ReceivedMessage | None:
        for q in self._queues:
            if q.user == user:
                return await q.next_message()
        else:
            return None

    async def get_admin_message(self):
        if self._admin_queue.qsize() == 0:
            return None
        return await self._admin_queue.get()


class UserQueue:
    def __init__(self, *, room: str, user: str):
        self.room = room
        self.user = user
        self.queue = asyncio.Queue()

    async def add_message_to_queue(self, msg: groom_pb2.ReceivedMessage):
        await self.queue.put(msg)

    async def next_message(self) -> groom_pb2.ReceivedMessage:
        return await self.queue.get()

    def messages_count(self) -> int:
        return self.queue.qsize()
