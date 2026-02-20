from datetime import datetime

import grpc

import groom_pb2
import groom_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp

# def get_groom():
#     # this is to try client
#     with grpc.insecure_channel('localhost:50051') as channel:
#         stub = groom_pb2_grpc.GroomStub(channel)
#         # stub = groom_pb2_grpc.GroomServiceStub(channel)

#         response = stub.GetGroom(groom_pb2.GetGroomRequest(room_name="Blue"))
#         print(response.room_name)
    

def register_to_room():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = groom_pb2_grpc.GroomStub(channel)
        # stub = groom_pb2_grpc.GroomServiceStub(channel)

        response = stub.RegisterToRoom(groom_pb2.RoomRegistrationRequest(room_name="Blue hall room."))
        print(response.room_id)

def send_news_flash():
    """
    Or use BloomRPC it's like postman but dedicated for RPC.
    """
    def news_flash_requests():
        ts = Timestamp()
        ts.FromDatetime(datetime.utcnow())
        yield groom_pb2.NewsFlash(
            news_item="News flash: Blue hall room is on fire.",
            news_time=ts,
        )

    with grpc.insecure_channel('localhost:50052') as channel:
        stub = groom_pb2_grpc.GroomStub(channel)
        # stub = groom_pb2_grpc.GroomServiceStub(channel)

        response = stub.SendNewsFlash(news_flash_requests())
        print(response.success)

def client():
    # register_to_room()
    send_news_flash()

if __name__ =="__main__":
    client()