import graphene


class NoteType(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()
    created = graphene.DateTime()
    # no edited
    due = graphene.DateTime()

