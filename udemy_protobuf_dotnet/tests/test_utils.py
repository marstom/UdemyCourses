from datetime import datetime

from icecream import ic

from src.utils.message_queue import MessagesQueue

import groom_pb2

def test_messages_queue():
    mq = MessagesQueue()
    nf = groom_pb2.NewsFlash(news_time=datetime.now(), news_item="test")
    mq.add_news_to_queue(nf)


    received = mq.received_message()
    ic()
    ic(received.contents)

    assert received.contents == nf.news_item