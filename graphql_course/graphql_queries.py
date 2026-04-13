import graphene

from graphql_types import NoteType
import global_data


class Query(graphene.ObjectType):
    notes = graphene.List(NoteType, title_contains=graphene.String())

    @staticmethod
    def resolve_notes(root, info, title_contains=None):
        print(info.context)
        if title_contains is not None:
            return [note for note in global_data.notes if title_contains in note.title]
        return global_data.notes

    # rozdz 4.8
