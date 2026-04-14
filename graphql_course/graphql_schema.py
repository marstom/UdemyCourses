import graphene

from graphql_mutations import Mutation
from graphql_queries import Query

schema = graphene.Schema(query=Query, mutation=Mutation)
