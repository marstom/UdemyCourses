
import queue

import groom_pb2

class MessagesQueue:
    def __init__(self):
        self.queue = queue.Queue()


    def add_news_to_queue(self, news_flash: groom_pb2.NewsFlash):
        msg = groom_pb2.ReceivedMessage(
            msg_time=news_flash.news_time,
            contents=news_flash.news_item,
            user="id__groom"
        )
        self.queue.put(msg)


        # self.queue.get()

    def received_message(self) -> groom_pb2.ReceivedMessage:
        return self.queue.get()

    def get_message_count(self) -> int:
        return self.queue.qsize()
