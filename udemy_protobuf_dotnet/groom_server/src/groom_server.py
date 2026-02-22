import time
from concurrent import futures
from typing import Iterator

from grpc_reflection.v1alpha import reflection
# from grpc_reflection.v1alpha import reflection
# from google.protobuf import reflection
from icecream import ic

import grpc

import groom_pb2
import groom_pb2_grpc
from utils.message_queue import MessagesQueue
from utils.user_queue import UsersQueues

from loguru import logger
import sys

# Remove default handler
logger.remove()

# Add colorful console output
logger.add(
    sys.stdout,
    level="DEBUG",
    format="<green>{time:HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>\n"
           "<level>{message}</level>\n"
           "",
    colorize=True,
)

class GroomService(groom_pb2_grpc.GroomServicer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mq = MessagesQueue()
        self.user_queues = UsersQueues()

    def RegisterToRoom(self, request, context):
        """Client side streaming to server"""
        print("Get a room")
        return groom_pb2.RoomRegistrationResponse(room_id=f"Room {request.room_name}")

    def SendNewsFlash(self, request_iterator, context):
        """ Client side streaming """
        try:
            for news_flash in request_iterator:
                print(f"News flash: {news_flash.news_item} at {news_flash.news_time}")
                self.mq.add_news_to_queue(news_flash)
            return groom_pb2.NewsStreamStatus(success=True)
        except grpc.RpcError as e:
            # Typical when client cancels/aborts mid-stream; gRPC logs this as
            # "Exception iterating requests" if not handled.
            print(f"SendNewsFlash stream aborted: {e.code()} {e.details()}")
            return groom_pb2.NewsStreamStatus(success=False)

    def StartMonitoring(self, request: "Empty", context):
        """ Server side streaming """
        print(f"Monitoring: {request}, {context}")
        while True:
            if self.mq.get_message_count() > 0:
                received_message = self.mq.received_message()
                print(received_message)
                yield received_message
            time.sleep(0.5)

    def StartChat(self, incoming_stream: Iterator[groom_pb2.ChatMessage], context: grpc.ServicerContext) -> Iterator[groom_pb2.ChatMessage]:
        """Bi-directional streaming: receive ChatMessages, broadcast to room, yield ChatMessages for this user."""
        logger.debug("CONNNECETED")
        first_message = next(incoming_stream)
        logger.debug(f"First message: {first_message}")
        self.user_queues.create_user_queue(first_message.room, first_message.user)
        # on connect
        for chat_message in incoming_stream:
            self.user_queues.add_message_to_room(chat_message.room, chat_message)
            # on chat message send
            logger.debug(chat_message)
            # self.user_queues.create_user_queue(chat_message.room, chat_message.user)
            # self.user_queues.get_message_for_user(chat_message.user)
            # chat_message.room
            # chat_message.user
            # chat_message.contents
            # chat_message.msg_time

            # yield groom_pb2.ChatMessage(msg_time=chat_message.msg_time, contents=chat_message.contents, user=chat_message.user, room=chat_message.room)
            # yield groom_pb2.ChatMessage(msg_time=chat_message.msg_time, contents=chat_message.contents, user=chat_message.user, room=chat_message.room)
            # yield groom_pb2.ChatMessage(msg_time=chat_message.msg_time, contents=chat_message.contents, user=chat_message.user, room=chat_message.room)
        yield groom_pb2.ChatMessage(msg_time=chat_message.msg_time, contents="NONO", user=chat_message.user, room=chat_message.room)
        # print(first_msg)
        # yield first_msg
        # first_msg = next(incoming_stream)
        # self.user_queues.create_user_queue(first_msg.room, first_msg.user)
        # for chat_message in incoming_stream:
        #     print(f"Chat message: {chat_message.contents} at {chat_message.msg_time}")
        #     self.user_queues.add_message_to_room(chat_message.room, chat_message.contents)
        #     msg = self.user_queues.get_message_for_user(chat_message.user)
        #     if msg is not None:
        #         yield groom_pb2.ChatMessage(
        #             msg_time=msg.msg_time,
        #             contents=msg,
        #             user=msg.user,
        #             room=chat_message.room,
        #         )

def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    groom_pb2_grpc.add_GroomServicer_to_server(GroomService(), server)

    SERVICE_NAMES = (groom_pb2.DESCRIPTOR.services_by_name['Groom'].full_name, )
    logger.debug(SERVICE_NAMES)
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    main()