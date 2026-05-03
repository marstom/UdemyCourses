import asyncio
import grpc
import messages_pb2
import messages_pb2_grpc
from google.protobuf import empty_pb2
from loguru import logger


async def test_with_password():
    """Test authentication with password"""
    print("=== Testing with Password ===")

    async with grpc.aio.insecure_channel('localhost:50055') as channel:
        stub = messages_pb2_grpc.DoorStub(channel)

        # Create request with password
        request = messages_pb2.DoorLockRequest(msg="suppellex", token="1234")

        try:
            response = await stub.SendCommandToDoor(request)
            print(f"Response: {response.ans}")
        except grpc.RpcError as e:
            print(f"Error: {e.code()} - {e.details()}")


async def test_with_token():
    """Test authentication with token"""
    print("\n=== Testing with Token ===")
    
    async with grpc.aio.insecure_channel('localhost:50055') as channel:
        stub = messages_pb2_grpc.DoorStub(channel)
        
        # Create request with token
        request = messages_pb2.DoorLockRequest(
            msg="suppellex",
            token="mytoken123"
        )
        
        try:
            response = await stub.SendCommandToDoor(request)
            print(f"Response: {response.ans}")
        except grpc.RpcError as e:
            print(f"Error: {e.code()} - {e.details()}")


async def test_with_icode():
    """Test authentication with integer code"""
    print("\n=== Testing with Integer Code ===")
    
    async with grpc.aio.insecure_channel('localhost:50055') as channel:
        stub = messages_pb2_grpc.DoorStub(channel)
        
        # Create request with integer code
        request = messages_pb2.DoorLockRequest(
            msg="suppellex",
            icode=5678
        )
        
        try:
            response = await stub.SendCommandToDoor(request)
            print(f"Response: {response.ans}")
        except grpc.RpcError as e:
            print(f"Error: {e.code()} - {e.details()}")


async def test_with_rrr():
    """Test authentication with rrr field"""
    print("\n=== Testing with RRR Field ===")
    
    async with grpc.aio.insecure_channel('localhost:50055') as channel:
        stub = messages_pb2_grpc.DoorStub(channel)
        
        # Create request with rrr
        request = messages_pb2.DoorLockRequest(
            msg="suppellex",
            rrr="custom_value"
        )
        
        try:
            response = await stub.SendCommandToDoor(request)
            print(f"Response: {response.ans}")
        except grpc.RpcError as e:
            print(f"Error: {e.code()} - {e.details()}")


async def test_with_valid_auth_header():
    """Test with valid authorization header for interceptor"""
    print("\n=== Testing with Valid Auth Header ===")

    # Create metadata with valid token
    metadata = [('authorization', 'Bearer abc123')]

    async with grpc.aio.insecure_channel('localhost:50055') as channel:
        stub = messages_pb2_grpc.DoorStub(channel)

        # Create request
        request = messages_pb2.DoorLockRequest(
            msg="suppellex",
            token="1234"
        )

        try:
            response = await stub.SendCommandToDoor(request, metadata=metadata)
            print(f"Response: {response.ans}")
        except grpc.RpcError as e:
            print(f"Error: {e.code()} - {e.details()}")


async def test_with_invalid_auth_header():
    """Test with invalid authorization header for interceptor"""
    print("\n=== Testing with Invalid Auth Header ===")

    # Create metadata with invalid token
    metadata = [('authorization', 'Bearer wrongtoken')]

    async with grpc.aio.insecure_channel('localhost:50055') as channel:
        stub = messages_pb2_grpc.DoorStub(channel)

        # Create request
        request = messages_pb2.DoorLockRequest(
            msg="suppellex",
            token="1234"
        )

        try:
            response = await stub.SendCommandToDoor(request, metadata=metadata)
            print(f"Response: {response.ans}")
        except grpc.RpcError as e:
            print(f"Error: {e.code()} - {e.details()}")


async def test_show_metadata():
    """Test the showMetadata method"""
    print("\n=== Testing Show Metadata ===")
    
    # Create custom metadata
    metadata = [
        ('authorization', 'Bearer abc123'),
        ('user-agent', 'test-client'),
        ('custom-header', 'test-value')
    ]
    
    async with grpc.aio.insecure_channel('localhost:50055') as channel:
        stub = messages_pb2_grpc.DoorStub(channel)
        
        try:
            response = await stub.showMetadata(empty_pb2.Empty(), metadata=metadata)
            print("Metadata sent successfully - check server logs")
        except grpc.RpcError as e:
            print(f"Error: {e.code()} - {e.details()}")


async def main():
    """Run all tests"""
    print("Starting gRPC Client Tests...\n")
    
    # Test different auth methods in request
    await test_with_password()
    await test_with_token()
    await test_with_icode()
    await test_with_rrr()
    
    # Test with auth headers (interceptor)
    await test_with_valid_auth_header()
    await test_with_invalid_auth_header()
    
    # Test metadata display
    await test_show_metadata()
    
    print("\nAll tests completed!")


if __name__ == "__main__":
    asyncio.run(main())