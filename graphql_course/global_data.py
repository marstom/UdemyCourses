from datetime import datetime


from models import Note, AddressInfo, ContactInfo

notes = [
    Note(
        title="Call my parents",
        content="Call them",
        created=datetime(2021, 1, 1),
        edited=datetime(2021, 1, 1),
        due=datetime(2021, 1, 1),
        info=ContactInfo(name="Tom", phone="123456789"),
    ),
    Note(
        title="Second Note",
        content="Something",
        created=datetime(2021, 1, 2),
        edited=datetime(2021, 1, 2),
        due=datetime(2021, 1, 2),
        info=ContactInfo(name="Tom", phone="123456789"),
    ),
    Note(
        title="Third Note",
        content="Empty content",
        created=datetime(2021, 1, 3),
        edited=datetime(2021, 1, 3),
        due=datetime(2021, 1, 3),
    ),
    Note(
        title="Buy a bread",
        content="Need fresh bread",
        created=datetime(2021, 1, 4),
        edited=datetime(2021, 1, 4),
        due=datetime(2021, 1, 4),
    ),
    Note(
        title="Buy a milk",
        content="Milk for cereal",
        created=datetime(2021, 1, 5),
        edited=datetime(2021, 1, 5),
        due=datetime(2021, 1, 5),
    ),
    Note(
        title="Buy a cheese",
        content="Cheese for sandwich",
        created=datetime(2021, 1, 6),
        edited=datetime(2021, 1, 6),
        due=datetime(2021, 1, 6),
    ),
    Note(
        title="Buy a butter",
        content="Butter for bread",
        created=datetime(2021, 1, 7),
        edited=datetime(2021, 1, 7),
        due=datetime(2021, 1, 7),
    ),
    Note(
        title="Buy an eggs",
        content="Eggs for breakfast",
        created=datetime(2021, 1, 8),
        edited=datetime(2021, 1, 8),
        due=datetime(2021, 1, 8),
        info=AddressInfo(street="Eggs address info", city="Wegs"),
    ),
]
