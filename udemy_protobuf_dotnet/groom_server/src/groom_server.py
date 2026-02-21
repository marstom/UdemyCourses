import time
from concurrent import futures
from typing import Iterator

import grpc

import groom_pb2
import groom_pb2_grpc
from utils.message_queue import MessagesQueue
from utils.user_queue import UsersQueues


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
        """ Bi-directional streaming """
        print("ST")
        while True:
            # Wait for message...
            first_msg = next(incoming_stream)
            self.user_queues.create_user_queue(first_msg.room, first_msg.user)
            # Wait for message...
            for chat_message in incoming_stream:
                print(f"Chat message: {chat_message.contents} at {chat_message.msg_time}")
                self.user_queues.add_message_to_room(chat_message.room, chat_message.contents)

                yield self.user_queues.get_message_for_user(chat_message.user)
                    # yield msg
                # yield groom_pb2.ChatMessage(msg_time=chat_message.msg_time, contents="success", user="groom")
            # return groom_pb2.ChatStreamStatus(success=True)

def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    groom_pb2_grpc.add_GroomServicer_to_server(GroomService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    main()
