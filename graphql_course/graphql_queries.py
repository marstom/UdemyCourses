import graphene
from icecream import ic

from graphql_types import NoteType, NotesFilter
import global_data


class Query(graphene.ObjectType):
    notes = graphene.List(
        NoteType,
        filters=graphene.Argument(NotesFilter)
    )

    @staticmethod
    def resolve_notes(root, info, filters=None):
        print(info.context)
        # if title_contains is not None:
        #     return [note for note in global_data.notes if title_contains in note.title]
        # return global_data.notes

        ic(filters)
        if filters is None:
            return global_data.notes
        return [note for note in global_data.notes if filters.title_contains in note.title]
        if title_contains is not None:
            return [note for note in global_data.notes if title_contains in note.title]
        return global_data.notes

