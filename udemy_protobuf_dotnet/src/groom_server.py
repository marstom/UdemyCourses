import time
from datetime import datetime

from google.protobuf.internal import well_known_types

import groom_pb2
import groom_pb2_grpc   
import grpc
from concurrent import futures

# from google.protobuf.internal.well_known_types import Empty


# TODO: Implement the GroomService class
class GroomService(groom_pb2_grpc.GroomServicer):
    def RegisterToRoom(self, request, context):
        print("Get a room")
        return groom_pb2.RoomRegistrationResponse(room_id=f"Room {request.room_name}")



    # def GetGroom(self, request, context):
        # return groom_pb2.GetGroomResponse(room_name=request.room_name)

    def SendNewsFlash(self, request_iterator, context):
        """ Client side streaming """
        try:
            for request in request_iterator:
                print(f"News flash: {request.news_item} at {request.news_time}")
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
        for cnt in range(10):
            yield groom_pb2.ReceivedMessage(msg_time=datetime.now(), contents=f"The test message started {cnt}", user="id__groom")
            time.sleep(0.5)

def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    groom_pb2_grpc.add_GroomServicer_to_server(GroomService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    main()