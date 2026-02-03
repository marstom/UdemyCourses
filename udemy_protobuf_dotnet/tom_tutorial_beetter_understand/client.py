import asyncio
from concurrent import futures

import grpc

from generated import my_pb2_grpc, my_pb2


async def unpack():
    # to jest unary
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub= my_pb2_grpc.BackpackManagerStub(channel)
        response = await stub.unpack(my_pb2.UnpackReqest(item_name="nooone"))
        print(response)



async def pack():
    # To jest unary
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub= my_pb2_grpc.BackpackManagerStub(channel)
        response = await stub.pack(my_pb2.BackpackItemRequest(item="tom", count=1))
        print(response)
        # print(response.message)

async def continous_pack_items():
    # client streaming

    async def continous_pack_items():



async def continous_unpack_items():
    # client streaming
    # serwer podaj diuuuuuużo itemków z placaka

async def main():
    await unpack()

if __name__ == "__main__":

    asyncio.run(main())
