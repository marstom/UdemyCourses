from concurrent import futures

import grpc

from generated import my_pb2_grpc, my_pb2


class BackpackManager(my_pb2_grpc.BackpackManagerServicer):

    def __init__(self):
        self.items = []
    def pack(self, request, context):
        # Echo back the packed item.
        self.items.append(request.item)
        print(request.item)
        return my_pb2.BackpackItemResponse(item=request.item)

    def unpack(self, request, context):
        # In a real app you'd track state; here we just return an empty response.
        print("00000000")
        return my_pb2.BackpackItemResponse(item=self.items.pop())


if __name__ == "__main__":
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    my_pb2_grpc.add_BackpackManagerServicer_to_server(BackpackManager(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()