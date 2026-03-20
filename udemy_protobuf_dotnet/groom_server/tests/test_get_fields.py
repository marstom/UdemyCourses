from pathlib import Path
import my_pb2
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.json_format import MessageToJson, MessageToDict, ParseDict, Parse
import json
from datetime import datetime


def main():
    print("=" * 60)
    print("1. CREATING A PLAYER")
    print("=" * 60)
    player = my_pb2.Player(
        id=1,
        name="John Doe",
        is_active=True,
        last_login=Timestamp(seconds=1716153600),
        cur_ad="123 Main St, Anytown, USA",
        status=my_pb2.Player.Status.NEW,
        address=my_pb2.Address(street="123 Main St", city="Anytown"),
    )
    print(player)
    print()

    print("=" * 60)
    print("2. ACCESSING FIELDS")
    print("=" * 60)
    print(f"Player ID: {player.id}")
    print(f"Player Name: {player.name}")
    print(f"Is Active: {player.is_active}")
    print(f"Status: {player.status} ({my_pb2.Player.Status.Name(player.status)})")
    print(f"Last Login (seconds): {player.last_login.seconds}")
    print()

    print("=" * 60)
    print("3. MODIFYING FIELDS")
    print("=" * 60)
    player.name = "Jane Smith"
    player.id = 42
    player.status = my_pb2.Player.Status.CONFIRMED
    player.is_active = False
    print(
        f"Updated player: {player.name}, ID: {player.id}, Status: {my_pb2.Player.Status.Name(player.status)}"
    )
    print()

    print("=" * 60)
    print("4. SERIALIZATION - Converting to Bytes (Binary Format)")
    print("=" * 60)
    # Serialize to binary (for network transfer, file storage, etc.)
    serialized_bytes = player.SerializeToString()
    print(f"Serialized size: {len(serialized_bytes)} bytes")
    print(f"First 20 bytes (hex): {serialized_bytes[:20].hex()}")
    print()

    print("=" * 60)
    print("5. DESERIALIZATION - Creating from Bytes")
    print("=" * 60)
    # Deserialize from binary
    new_player = my_pb2.Player()
    new_player.ParseFromString(serialized_bytes)
    print(f"Deserialized player: {new_player.name}, ID: {new_player.id}")
    print()

    print("=" * 60)
    print("6. JSON SERIALIZATION")
    print("=" * 60)
    # Convert to JSON (human-readable format)
    json_str = MessageToJson(player)
    print("JSON representation:")
    print(json_str)
    print()

    print("=" * 60)
    print("7. JSON DESERIALIZATION")
    print("=" * 60)
    # Create from JSON
    json_data = {
        "id": 100,
        "name": "Alice Wonder",
        "isActive": True,
        "lastLogin": "2024-05-20T10:30:00Z",
        "curAd": "456 Oak Ave",
        "status": "CONFIRMED",
    }
    player_from_json = Parse(json.dumps(json_data), my_pb2.Player())
    print(f"Player from JSON: {player_from_json.name}, ID: {player_from_json.id}")
    print()

    print("=" * 60)
    print("8. DICTIONARY CONVERSION")
    print("=" * 60)
    # Convert to dictionary
    player_dict = MessageToDict(player)
    print("As dictionary:")
    print(json.dumps(player_dict, indent=2))
    print()

    # Create from dictionary
    dict_data = {"id": 200, "name": "Bob Builder", "is_active": True, "status": "NEW"}
    player_from_dict = ParseDict(dict_data, my_pb2.Player())
    print(f"Player from dict: {player_from_dict.name}, ID: {player_from_dict.id}")
    print()

    print("=" * 60)
    print("9. COPYING MESSAGES")
    print("=" * 60)
    # Create a copy
    player_copy = my_pb2.Player()
    player_copy.CopyFrom(player)
    player_copy.name = "Copy of " + player.name
    print(f"Original: {player.name}")
    print(f"Copy: {player_copy.name}")
    print()

    print("=" * 60)
    print("10. MERGING MESSAGES")
    print("=" * 60)
    # Merge two messages (fields from source overwrite destination)
    player1 = my_pb2.Player(id=1, name="Player One", is_active=True)
    player2 = my_pb2.Player(
        id=2, name="Player Two", status=my_pb2.Player.Status.CONFIRMED
    )
    player1.MergeFrom(player2)
    print(
        f"Merged player: ID={player1.id}, Name={player1.name}, Status={my_pb2.Player.Status.Name(player1.status)}"
    )
    print("Note: All fields from player2 overwrote player1's fields (ID, name, status)")
    print()

    print("=" * 60)
    print("11. CLEARING FIELDS")
    print("=" * 60)
    player_to_clear = my_pb2.Player(id=999, name="To Be Cleared", is_active=True)
    print(f"Before clear: {player_to_clear}")
    player_to_clear.Clear()
    print(f"After clear: {player_to_clear}")
    print()

    print("=" * 60)
    print("12. CHECKING FIELD PRESENCE (Proto3)")
    print("=" * 60)
    # In proto3, you can't distinguish between unset and default values
    # But you can check if a message field is set
    empty_player = my_pb2.Player()
    print(f"Has last_login? {empty_player.HasField('last_login')}")
    print(f"Player with last_login: {player.HasField('last_login')}")
    print()

    print("=" * 60)
    print("13. WORKING WITH TIMESTAMPS")
    print("=" * 60)
    # Create timestamp from datetime
    now = datetime.now()
    timestamp_now = Timestamp()
    timestamp_now.FromDatetime(now)

    player_with_now = my_pb2.Player(
        id=300, name="Time Traveler", last_login=timestamp_now
    )
    print(f"Player created at: {player_with_now.last_login.ToDatetime()}")
    print(f"Seconds since epoch: {player_with_now.last_login.seconds}")
    print()

    print("=" * 60)
    print("14. ENUM OPERATIONS")
    print("=" * 60)
    # Access enum values
    print(f"Status enum values: {list(my_pb2.Player.Status.keys())}")
    print(f"Status enum names: {list(my_pb2.Player.Status.keys())}")
    print(f"NEW = {my_pb2.Player.Status.NEW}")
    print(f"CONFIRMED = {my_pb2.Player.Status.CONFIRMED}")
    print(f"DIED = {my_pb2.Player.Status.DIED}")
    # Convert enum value to name
    print(
        f"Current status value {player.status} = {my_pb2.Player.Status.Name(player.status)}"
    )
    print()

    print("=" * 60)
    print("15. SAVING TO FILE")
    print("=" * 60)
    # Save to binary file
    output_file = Path("player.bin")
    output_file.write_bytes(player.SerializeToString())
    print(f"Saved player to {output_file} ({output_file.stat().st_size} bytes)")

    # Load from file
    loaded_player = my_pb2.Player()
    loaded_player.ParseFromString(output_file.read_bytes())
    print(f"Loaded player: {loaded_player.name}, ID: {loaded_player.id}")
    print()


if __name__ == "__main__":
    main()
