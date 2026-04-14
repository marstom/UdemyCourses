# TODO mutacje
from datetime import datetime

import graphene
from graphql import GraphQLError

import global_data
from graphql_types import NoteType, NoteStateType
from models import Note


class CreateNote(graphene.Mutation):
    success = graphene.Boolean(description="Whether the mutation was successful")
    note = graphene.Field(NoteType, description="The created note, can see all fields")

    class Arguments:
        title = graphene.String(description="Note title")
        content = graphene.String()
        due = graphene.DateTime(
            required=False, description="Indicates if note is expired"
        )

    def mutate(root, info, title, content, due=None):
        if due < datetime.now():
            raise GraphQLError(
                "Due date must be in the future",
                extensions={"code": "DUE_DATE_MUST_BE_IN_THE_FUTURE"},
            )
        note = Note(title=title, content=content, due=due)
        global_data.notes.append(note)
        return CreateNote(success=True, note=note, due=due)


class ChangeNoteState(graphene.Mutation):
    success = graphene.Boolean(description="Whether the mutation was successful")
    note = graphene.Field(NoteType, description="The updated note")

    class Arguments:
        idx = graphene.Int(required=True, description="Note ID")
        state = NoteStateType(required=True, description="New state")

    @staticmethod
    def mutate(root, info, idx, state):
        note = global_data.notes[idx]
        if not note:
            raise GraphQLError("Note not found", extensions={"code": "NOTE_NOT_FOUND"})
        note.state = state
        return ChangeNoteState(success=True, note=note)


class Mutation(graphene.ObjectType):
    create_note = CreateNote.Field(description="Create note")
    change_note_state = ChangeNoteState.Field(description="Change note state")
