import time
from concurrent import futures

import grpc

from generated import groom_pb2
from generated import groom_pb2_grpc
from src.utils.message_queue import MessagesQueue


# from google.protobuf.internal.well_known_types import Empty


# TODO: Implement the GroomService class
class GroomService(groom_pb2_grpc.GroomServicer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mq = MessagesQueue()

    def RegisterToRoom(self, request, context):
        """Client side streaming to server"""
        print("Get a room")
        return groom_pb2.RoomRegistrationResponse(room_id=f"Room {request.room_name}")



    # def GetGroom(self, request, context):
        # return groom_pb2.GetGroomResponse(room_name=request.room_name)

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

    def StartMonitoring(self, request, context):
        """ Server side streaming """
        print(f"Monitoring: {request}, {context}")


        # for request in request:
        #     print(f"Monitoring: {request}")
        # for cnt in range(10):
        #     yield groom_pb2.ReceivedMessage(msg_time=datetime.now(), contents=f"The test message started {cnt}", user="id__groom")
        #     time.sleep(0.5)

        while True:
            if self.mq.get_message_count() > 0:
                received_message = self.mq.received_message()
                print(received_message)
                yield received_message
            time.sleep(0.5)

def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    groom_pb2_grpc.add_GroomServicer_to_server(GroomService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    main()