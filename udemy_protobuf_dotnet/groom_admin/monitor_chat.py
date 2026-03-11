import asyncio
from datetime import datetime

import grpc
from google.protobuf import empty_pb2

import groom_pb2_grpc

SERVER_ADDRESS = "localhost:50052"


async def keepalive_requests():
    """Send empty messages periodically to keep stream open"""
    while True:
        await asyncio.sleep(5)
        yield empty_pb2.Empty()


async def monitor():
    print("*** Admin Console started ***")
    print("Listening for messages...\n")

    async with grpc.aio.insecure_channel(SERVER_ADDRESS) as channel:
        stub = groom_pb2_grpc.GroomStub(channel)

        try:
            stream = stub.StartMonitoring(keepalive_requests())

            async for msg in stream:
                ts = msg.msg_time
                if ts and ts.seconds:
                    dt = datetime.fromtimestamp(ts.seconds + ts.nanos / 1e9)
                    time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    time_str = "?"

                print(f"[{time_str}] {msg.user}: {msg.contents}")

        except asyncio.CancelledError:
            print("\nMonitoring stopped.")
            raise

        except grpc.aio.AioRpcError as e:
            print(f"\nStream ended: {e.code().name} – {e.details()}")


if __name__ == "__main__":
    try:
        asyncio.run(monitor())
    except KeyboardInterrupt:
        print("\nAdmin console closed.")
