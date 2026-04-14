from datetime import datetime
import graphene

from models import NoteState


class NoteType(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()
    created = graphene.DateTime()
    # no edited
    due = graphene.DateTime()

    ####
    content_short = graphene.String()

    state = graphene.Enum.from_enum(NoteState)()

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
