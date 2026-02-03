import asyncio
import logging
import time
from concurrent import futures

import grpc

from generated import my_pb2_grpc, my_pb2

from faker import Faker

ff = Faker()

class BackpackManager(my_pb2_grpc.BackpackManagerServicer):

    def __init__(self):

        self.items = [ff.text()[:10] for a in range(3)]
    def pack(self, request, context):
        # Echo back the packed item.
        self.items.append(request.item)
        print(request.item)
        return my_pb2.BackpackItemResponse(item=request.item)

    def unpack(self, request, context):
        # In a real app you'd track state; here we just return an empty response.
        print("00000000")
        return my_pb2.BackpackItemResponse(item=self.items.pop())

    def unpack_continously(self, request, context):
        """ Server streaming"""
        print("UUPPP")
        ...
        # for request in request_iterator:
        print(request)
        while len(self.items) > 0:
                fetched_item = self.items.pop()
                print(f"---1---> {fetched_item}")
                yield my_pb2.UnpackContinouslyResponse(fetched_item=fetched_item)
                time.sleep(0.7)
                # yield 1

    def pack_continously(self, request_iter, context):
        for request in request_iter:
            print("Pack item...")
            print(request)
            self.items.append(request.item_name)
            time.sleep(0.5)
        return my_pb2.PackResponse(added=f"OK!")



if __name__ == "__main__":
    logging.basicConfig()
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # add servicer to server
    my_pb2_grpc.add_BackpackManagerServicer_to_server(BackpackManager(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()