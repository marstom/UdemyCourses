from google.protobuf import empty_pb2

import grpc.aio
import groom_pb2_grpc

SERVER_ADDRESS = "localhost:50052"


def monitor():
    with grpc.insecure_channel(SERVER_ADDRESS) as channel:
        client = groom_pb2_grpc.GroomStub(channel)

        for msg in client.StartMonitoring(empty_pb2.Empty()):
            print(msg)


def main():
    monitor()


if __name__ == "__main__":
    main()
    # asyncio.run(main())
