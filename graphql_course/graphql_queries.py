import graphene

from graphql_types import NoteType
import global_data


class Query(graphene.ObjectType):
    notes = graphene.List(NoteType)

    @staticmethod
    def resolve_notes(root, info):
        return global_data.notes

    # wyszukiwarka
