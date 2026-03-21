from concurrent import futures
import signal
from typing import AsyncIterator

from grpc_reflection.v1alpha import reflection

import grpc
import asyncio

import groom_pb2
import groom_pb2_grpc
from utils.message_queue import MessagesQueue

from utils.user_queue import Rooms
from loguru import logger
import sys

# Remove default handler
logger.remove()

# Add colorful console output
logger.add(
    sys.stdout,
    level="DEBUG",
    format="<green>{time:HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>\n"
    "<level>{message}</level>\n"
    "",
    colorize=True,
)


class GroomService(groom_pb2_grpc.GroomServicer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mq = MessagesQueue()
        # self.rooms: dict[str, dict[str, asyncio.Queue]] = {}

        self.rooms = Rooms()

    async def RegisterToRoom(self, request, context):
        """Client side streaming to server"""
        logger.debug("Get a room")
        return groom_pb2.RoomRegistrationResponse(joined=True)

    async def SendNewsFlash(
        self,
        request_iterator: AsyncIterator[groom_pb2.NewsFlash],
        context: grpc.aio.ServicerContext,
    ) -> groom_pb2.NewsStreamStatus:
        """Client side streaming"""
        try:
            async for news_flash in request_iterator:
                print(f"News flash: {news_flash.news_item} at {news_flash.news_time}")
                self.mq.add_news_to_queue(news_flash)
            return groom_pb2.NewsStreamStatus(success=True)
        except grpc.RpcError as e:
            # Typical when client cancels/aborts mid-stream; gRPC logs this as
            # "Exception iterating requests" if not handled.
            print(f"SendNewsFlash stream aborted: {e.code()} {e.details()}")
            return groom_pb2.NewsStreamStatus(success=False)

    async def StartMonitoring(
        self, request: "Empty", context
    ) -> AsyncIterator[groom_pb2.ReceivedMessage]:
        """Server side streaming"""
        print(f"Monitoring: {request}, {context}")
        while True:
            mc = self.mq.get_message_count()
            print(mc)
            if mc > 0:
                received_message = self.mq.received_message()
                print(received_message)
                yield received_message
            await asyncio.sleep(0.5)

    async def StartChat(
        self,
        incoming_stream: AsyncIterator[groom_pb2.ChatMessage],
        context: grpc.aio.ServicerContext,
    ) -> AsyncIterator[groom_pb2.ChatMessage]:
        """Bi-directional streaming: receive ChatMessages, broadcast to room, yield ChatMessages for this user."""
        logger.debug("Toms chat impl")
        first_message = await anext(incoming_stream)
        # room = first_message.room
        user_name = first_message.user
        logger.debug(f"First message: {first_message}")
        self.rooms.add_user_to_room(first_message.room, user_name)
        # if room not in self.rooms:
        # self.rooms[room] = {}
        # user_queue = asyncio.Queue()
        # self.rooms[room][user] = user_queue

        # Broadcast join message
        # await self._broadcast(room, first_message)
        room = self.rooms.get_room(first_message.room)
        await room.boradcast_to_room(first_message)

        async def receive_room_message():
            async for msg in incoming_stream:
                logger.debug(f"Received message: {msg}")
                if msg.contents == "EXIT":
                    logger.info("Quitting....")
                    break
                # await self._broadcast(room, msg)
                room = self.rooms.get_room(msg.room)
                await room.boradcast_to_room(msg)

        # Start background receive task
        asyncio.create_task(receive_room_message())

        while True:
            # message = await self.rooms[room][user].get()
            message = await room.get_user_message(user_name)

            if message is None:
                break
            yield message

    async def _broadcast(self, room, message):
        for queue in self.rooms[room].values():
            await queue.put(message)


async def main():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))

    groom_pb2_grpc.add_GroomServicer_to_server(GroomService(), server)

    SERVICE_NAMES = (
        groom_pb2.DESCRIPTOR.services_by_name["Groom"].full_name,
        reflection.SERVICE_NAME,
    )

    logger.debug(SERVICE_NAMES)
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    listen_addr = "[::]:50052"
    server.add_insecure_port(listen_addr)
    await server.start()
    logger.info(f"Server started on {listen_addr}")

    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()

    def shutdown():
        logger.info("Shutdown signal received.")
        stop_event.set()

    loop.add_signal_handler(signal.SIGTERM, shutdown)
    loop.add_signal_handler(signal.SIGINT, shutdown)
    await stop_event.wait()
    logger.info("Stopping GRPC server...")
    logger.info("Server stopped.")


if __name__ == "__main__":
    asyncio.run(main())
