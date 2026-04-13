# this is first query
import graphene


def resolve_string_query(root, info):
    return "OK"


def resolve_some(root, info):
    return 42


class Query(graphene.ObjectType):
    string_query = graphene.String(resolver=resolve_string_query)
    some = graphene.Int(resolver=resolve_some)

    # def resolve_string_query(root, info):
    #     return "OK"


schema = graphene.Schema(query=Query)

query = """
query {
    stringQuery,
    some
}
"""

if __name__ == "__main__":
    result = schema.execute(query)
    print(result)
