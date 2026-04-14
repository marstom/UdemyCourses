import graphene

from graphql_mutations import Mutation
from graphql_queries import Query
from graphql_types import AddressInfoTypeInter, ContactInfoTypeInter


# interfaces trzeba podać explicite w types
schema = graphene.Schema(
    query=Query, mutation=Mutation, types=[AddressInfoTypeInter, ContactInfoTypeInter]
)
