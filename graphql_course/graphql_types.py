import graphene


class NoteType(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()
    created = graphene.DateTime()
    # no edited
    due = graphene.DateTime()

    ####
    content_short = graphene.String()

    @staticmethod
    def resolve_title(root, info):
        return root.title.upper()

    @staticmethod
    def resolve_content_short(root, info):
        return root.content[:5] + "..." if len(root.content) > 5 else root.content
