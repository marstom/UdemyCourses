from datetime import datetime
import graphene

from models import NoteState, AddressInfo, ContactInfo

NoteStateType = graphene.Enum.from_enum(NoteState)


class AddressInfoType(graphene.ObjectType):
    street = graphene.String()
    city = graphene.String()


class ContactInfoType(graphene.ObjectType):
    name = graphene.String()
    phone = graphene.String()


class InfoType(graphene.Union):
    class Meta:
        types = (AddressInfoType, ContactInfoType)

    @classmethod
    def resolve_type(cls, instance, info):
        if isinstance(instance, AddressInfo):
            return AddressInfoType
        elif isinstance(instance, ContactInfo):
            return ContactInfoType
        else:
            return None


class NoteType(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()
    created = graphene.DateTime()
    due = graphene.DateTime()
    content_short = graphene.String()

    state = NoteStateType()
    info = InfoType()

    @staticmethod
    def resolve_title(root, info):
        return root.title.upper()

    @staticmethod
    def resolve_content_short(root, info):
        return root.content[:5] + "..." if len(root.content) > 5 else root.content


class NotesFilter(graphene.InputObjectType):
    title_contains = graphene.String(default_value="")
    # content_contains = graphene.String(default_value="")
    created_after = graphene.DateTime(default_value=datetime.min)
    created_before = graphene.DateTime(default_value=datetime.max)
