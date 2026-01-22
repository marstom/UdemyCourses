import grpc

import groom_pb2
import groom_pb2_grpc

def get_groom():
    # this is to try client
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = groom_pb2_grpc.GroomStub(channel)
        # stub = groom_pb2_grpc.GroomServiceStub(channel)

        response = stub.GetGroom(groom_pb2.GetGroomRequest(room_name="Blue"))
        print(response.room_name)
    

def register_to_room():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = groom_pb2_grpc.GroomStub(channel)
        # stub = groom_pb2_grpc.GroomServiceStub(channel)

        response = stub.RegisterToRoom(groom_pb2.RoomRegistrationRequest(room_name="Blue hall room."))
        print(response.room_id)

def client():
    register_to_room()
    

if __name__ =="__main__":
    client()