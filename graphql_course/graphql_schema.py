import graphene

from graphql_queries import Query

schema = graphene.Schema(query=Query)