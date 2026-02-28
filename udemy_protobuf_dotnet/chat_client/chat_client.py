import asyncio
import time

import grpc
from google.protobuf.timestamp_pb2 import Timestamp
from loguru import logger

import groom_pb2
import groom_pb2_grpc

# TODO to implement


async def main():
    async with grpc.aio.insecure_channel("localhost:50052") as channel:
        stub = groom_pb2_grpc.GroomStub(channel)

        call = stub.StartChat()  # ← NO iterator here

        async def send_messages():
            # First message (join)
            logger.debug("First message")
            await call.write(
                groom_pb2.ChatMessage(
                    contents="Hello!",
                    user="Tom",
                    room="r",
                    msg_time=Timestamp(seconds=int(time.time())),
                )
            )
            logger.debug("Next message")

            # Keep sending messages
            for i in range(5):
                logger.debug(f"Next message {i}")
                await asyncio.sleep(2)
                await call.write(
                    groom_pb2.ChatMessage(
                        contents=f"Message {i}",
                        user="Tom",
                        room="r",
                        msg_time=Timestamp(seconds=int(time.time())),
                    )
                )

            await call.done_writing()

        async def receive_messages():
            async for response in call:
                logger.debug(f"📨 Received: {response.user} {response.contents}")

        await asyncio.gather(send_messages(), receive_messages())



if __name__ == "__main__":
    asyncio.run(main())