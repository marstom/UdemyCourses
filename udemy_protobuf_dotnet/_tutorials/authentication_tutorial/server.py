import asyncio

import grpc
from grpc import ServerInterceptor
import messages_pb2
import messages_pb2_grpc
from grpc_reflection.v1alpha import reflection
from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, level="DEBUG")
logger.level("DEBUG")

class AuthServerInterceptor(ServerInterceptor):
    ...


class Door(messages_pb2_grpc.DoorServicer):

    def SendCommandToDoor(self, request, context):
        auth = request.WhichOneof("auth")
        logger.debug(auth)
        logger.debug("Invoke command doorfefssaf {door} {context}", door=request, context=context)

        # Print the pass field if it exists
        if auth == "pass":
            logger.debug("ASDASD")
        elif auth  == "token":
            logger.debug(request.token)
            # print(f"Pass: {request.pass}")

        return messages_pb2.DoorLockResponse(ans="Locked")

async def serve():
    server = grpc.aio.server()
    messages_pb2_grpc.add_DoorServicer_to_server(Door(), server)

    # 👇 THIS IS THE MAGIC
    SERVICE_NAMES = (
        messages_pb2.DESCRIPTOR.services_by_name["Door"].full_name,
        reflection.SERVICE_NAME,  # required
    )
    # Remember! Refresh reflection in postman after ANY change
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port("0.0.0.0:50055")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())