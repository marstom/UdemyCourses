# TODO mutacje
from datetime import datetime

import graphene
from graphql import GraphQLError

import global_data
from graphql_types import NoteType
from models import Note


class CreateNote(graphene.Mutation):
    success = graphene.Boolean()
    note = graphene.Field(NoteType)

    class Arguments:
        title = graphene.String()
        content = graphene.String()
        due = graphene.DateTime(required=False)

    def mutate(root, info, title, content, due=None):
        if due < datetime.now():
            raise GraphQLError(
                "Due date must be in the future",
                extensions={"code": "DUE_DATE_MUST_BE_IN_THE_FUTURE"},
            )
        note = Note(title=title, content=content, due=due)
        global_data.notes.append(note)
        return CreateNote(success=True, note=note, due=due)


class Mutation(graphene.ObjectType):
    create_note = CreateNote.Field()
