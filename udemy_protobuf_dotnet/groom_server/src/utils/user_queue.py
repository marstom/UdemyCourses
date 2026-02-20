
import queue

import groom_pb2

class UserQueue:
    def __init__(self):
        self.queue = queue.Queue()


    def add_user_to_queue(self, msg: groom_pb2.ReceivedMessage, room_name: str):
        msg = groom_pb2.ReceivedMessage(
            msg_time=u,
            contents=news_flash.news_item,
            user="id__groom"
        )
        self.queue.put(msg)


        # self.queue.get()

    def received_message(self) -> groom_pb2.ReceivedMessage:
        return self.queue.get()

    def get_message_count(self) -> int:
        return self.queue.qsize()
