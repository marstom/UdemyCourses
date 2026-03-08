import asyncio
import time

import aioconsole
import grpc
from google.protobuf.timestamp_pb2 import Timestamp
from loguru import logger

import groom_pb2
import groom_pb2_grpc

async def main():
    logger.debug("MAIN")
    user = await aioconsole.ainput(f"Tell user name> ")
    room = await aioconsole.ainput(f"Tell the room> ")
    async with grpc.aio.insecure_channel("localhost:50052") as channel:
        stub = groom_pb2_grpc.GroomStub(channel)
        # user = "Tom"
        # room = "misc"
        call = stub.StartChat()  # ← NO iterator here
        # send first message to start stream
        await call.write(
            groom_pb2.ChatMessage(
                contents="join",
                user=user,
                room=room,
                msg_time=Timestamp(seconds=int(time.time())),
            )
        )
        async def send_messages():
            await call.write(
                groom_pb2.ChatMessage(
                    contents="Hello!",
                    user=user,
                    room=room,
                    msg_time=Timestamp(seconds=int(time.time())),
                )
            )

            message_in = ""
            while message_in != "q":
                message_in = await aioconsole.ainput(f"{user}:{room}> ")
                await call.write(
                    groom_pb2.ChatMessage(
                        contents=f"Message: {message_in}",
                        user=user,
                        room=room,
                        msg_time=Timestamp(seconds=int(time.time())),
                    )
                )
            await call.done_writing()

        async def receive_messages():
            async for response in call:
                print(f"📨 Received: {response.user} {response.contents}")

        await asyncio.gather(send_messages(), receive_messages())



if __name__ == "__main__":
    asyncio.run(main())
