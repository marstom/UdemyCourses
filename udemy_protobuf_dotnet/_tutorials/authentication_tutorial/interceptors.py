import grpc
from grpc import aio


class AuthInterceptor(aio.ServerInterceptor):
    async def intercept_service(self, continuation, handler_call_details):
        metadata = dict(handler_call_details.invocation_metadata or [])
        auth_header = metadata.get("authorization")

        if auth_header != "Bearer abc123":
            async def deny(request, context):
                await context.abort(
                    grpc.StatusCode.UNAUTHENTICATED,
                    "Invalid token",
                )

            return grpc.unary_unary_rpc_method_handler(deny)

        return await continuation(handler_call_details)