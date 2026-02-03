import asyncio
from concurrent import futures

import grpc

# import typer
import async_typer
from generated import my_pb2_grpc, my_pb2

cli = async_typer.AsyncTyper()


@cli.async_command()
async def unpack():
    """
    to jest unary rozpakowanie
    """
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = my_pb2_grpc.BackpackManagerStub(channel)
        response = await stub.unpack(my_pb2.UnpackReqest(item_name="nooone"))
        print(response)


@cli.async_command()
async def pack():
    """
    To jest unary pakowanie
    """
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = my_pb2_grpc.BackpackManagerStub(channel)
        response = await stub.pack(my_pb2.BackpackItemRequest(item="tom", count=1))
        print(response)
        # print(response.message)


def create_requests():
    for i in range(5):
        yield my_pb2.PackReqest(item_name=f"ajtem {i}")

@cli.async_command()
async def continous_pack_items():
    """
    client streaming
    """
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = my_pb2_grpc.BackpackManagerStub(channel)
        requests_iterator = create_requests()
        summary = await stub.pack_continously(requests_iterator)
        print(summary)
    ...


@cli.async_command()
async def continous_unpack_items():
    """
    client streaming
    serwer podaj diuuuuuużo itemków z placaka
    """
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = my_pb2_grpc.BackpackManagerStub(channel)
        response_iter = stub.unpack_continously(my_pb2.UnpackReqest(item_name="ANY"))
        # print(response_iter)
        async for item in response_iter:
            print(item)
            # print(item.status)
        # for el in response_iter:
        #     print(el)


async def main():
    await unpack()


if __name__ == "__main__":
    # asyncio.run(main())
    cli()
