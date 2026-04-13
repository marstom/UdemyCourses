import graphene


class Notetype(graphene.ObjectType):
    title = graphene.String()
