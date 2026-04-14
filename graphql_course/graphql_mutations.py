# TODO mutacje
import graphene

import global_data
from models import Note


class CreateNote(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        title = graphene.String()
        content = graphene.String()

    def mutate(root, info, title, content):
        global_data.notes.append(Note(title=title, content=content))
        return CreateNote(success=True)


class Mutation(graphene.ObjectType):
    create_note = CreateNote.Field()

