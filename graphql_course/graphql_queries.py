import graphene
from icecream import ic

from graphql_types import NoteType, NotesFilter
import global_data


class Query(graphene.ObjectType):
    notes = graphene.List(NoteType, filters=graphene.Argument(NotesFilter))

    @staticmethod
    def resolve_notes(root, info, filters=None):
        print(info.context)

        ic(filters)
        if filters is None:
            return global_data.notes
        return [
            note for note in global_data.notes if filters.title_contains in note.title
        ]
