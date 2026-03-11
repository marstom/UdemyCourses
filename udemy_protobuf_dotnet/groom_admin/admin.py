import asyncio
from datetime import datetime
from google.protobuf import empty_pb2

import grpc.aio
import groom_pb2_grpc

# Match C#: http://localhost:5054 (use 50052 if your groom server runs there)
SERVER_ADDRESS = "localhost:50052"


#
# async def monitor():
#     async with grpc.aio.insecure_channel(SERVER_ADDRESS) as channel:
#         client = groom_pb2_grpc.GroomStub(channel)
#
#         async for msg in client.StartMonitoring(empty_pb2.Empty()):
#             print(msg)
#
# async def main():
#     await monitor()  # IMPORTANT: await, don't fire-and-forget
#
def monitor():
    with grpc.insecure_channel(SERVER_ADDRESS) as channel:
        client = groom_pb2_grpc.GroomStub(channel)

        for msg in client.StartMonitoring(empty_pb2.Empty()):
            print(msg)


def main():
    monitor()  # IMPORTANT: await, don't fire-and-forget


# async def main():
#     print("*** Admin Console started ***")
#     print("Listening...")
#
#
#     async with grpc.aio.insecure_channel(SERVER_ADDRESS) as channel:
#         client = groom_pb2_grpc.GroomStub(channel)
#         async for msg in client.StartMonitoring(empty_pb2.Empty()):
#             ts = msg.msg_time
#             if ts:
#                 dt = datetime.fromtimestamp(ts.seconds + ts.nanos / 1e9)
#                 time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
#             else:
#                 time_str = "?"
#             print(f"[{time_str}] {msg.user}: {msg.contents}")


if __name__ == "__main__":
    main()
    # asyncio.run(main())
