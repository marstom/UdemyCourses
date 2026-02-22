
import queue

import groom_pb2

from loguru import logger


class UsersQueues:
    def __init__(self):
        self._queues: list[UserQueue] = []
        self._admin_queue: list[groom_pb2.ReceivedMessage] = []

    def create_user_queue(self, room: str, user: str):
        self._queues.append(UserQueue(room=room, user=user))

    def add_message_to_room(self, room: str, msg: str):
        for q in self._queues:
            if q.room == room:
                q.add_message_to_queue(msg)

        logger.debug(self._queues)
        # self._queues[room].add_message_to_queue(msg)

    def get_message_for_user(self, user: str) -> groom_pb2.ReceivedMessage | None:
        for q in self._queues:
            if q.user == user:
                return q.next_message()
        else:
            return None

    def get_admin_message(self):
        if len(self._admin_queue) == 0:
            return None
        return self._admin_queue.pop(0)


class UserQueue:
    def __init__(self, *, room: str, user: str):
        self.room = room
        self.user = user
        self.queue = queue.Queue()

    def add_message_to_queue(self, msg: groom_pb2.ReceivedMessage):
        self.queue.put(msg)

    def next_message(self) -> groom_pb2.ReceivedMessage:
        return self.queue.get()

    def messages_count(self) -> int:
        return self.queue.qsize()
