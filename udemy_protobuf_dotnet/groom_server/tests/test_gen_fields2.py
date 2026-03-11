# from google.protobuf.internal.well_known_types import Timestamp
from datetime import datetime

# from google.protobuf.timestamp_pb2 import Timestamp

from google.protobuf.internal.well_known_types import Timestamp


def main():

    # Timestamp

    player = my_pb2.Player(
        id=1,
        name="John Doe",
        is_active=True,
        # last_login=datetime.now(), # union like and below V
        login_time=321,
        cur_ad="123 Main St, Anytown, USA",
        status=my_pb2.Player.Status.NEW,
        address=my_pb2.Address(street="123 Main St", city="Anytown"),
        previous_games=["Game 1", "Game 2", "Game 3"],
        inventory={"sword": 1, "shield": 1, "coins": 3223, "potion": 6},
    )
    # print(player)

    player.previous_games.append("Game 4")
    print(player)
    print(player.status == my_pb2.Player.Status.NEW)

    adr = my_pb2.Address
    adr.street = "123 Main St"

    player.inventory["gem"] = 2
    print(adr)


if __name__ == "__main__":
    main()
