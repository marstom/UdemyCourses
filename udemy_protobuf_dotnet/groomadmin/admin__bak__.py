import asyncio
from datetime import datetime
from google.protobuf import empty_pb2

import grpc.aio
import groom_pb2_grpc

# Match C#: http://localhost:5054 (use 50052 if your groom server runs there)
SERVER_ADDRESS = "localhost:5054"


async def empty_stream():
    """Yield Empty messages periodically to keep the monitoring stream open."""
    while True:
        yield empty_pb2.Empty()
        await asyncio.sleep(1)


async def main():
    print("*** Admin Console started ***")
    print("Listening...")

    async with grpc.aio.insecure_channel(SERVER_ADDRESS) as channel:
        stub = groom_pb2_grpc.GroomStub(channel)
        try:
            async for msg in stub.StartMonitoring(empty_stream()):
                ts = msg.msg_time
                if ts:
                    dt = datetime.fromtimestamp(ts.seconds + ts.nanos / 1e9)
                    time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    time_str = "?"
                print(f"[{time_str}] {msg.user}: {msg.contents}")
        except asyncio.CancelledError:
            pass
        except grpc.RpcError as e:
            print(f"Monitoring error: {e.code()} - {e.details()}")


if __name__ == "__main__":
    asyncio.run(main())