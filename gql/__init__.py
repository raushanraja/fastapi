from datetime import datetime
import graphene
from fastapi import APIRouter, Request
from graphene import ObjectType, Mutation, Schema
from starlette.applications import Starlette
from starlette_graphene3 import GraphQLApp, make_graphiql_handler
from py.user import UserCreate

from .user import User, UserConnection


class CreateUser(Mutation):
    user = graphene.Field(User)

    class Arguments:
        user = UserCreate(username='raushan', name='raushan',
                          password='raushan', created_at=datetime.now())

    @staticmethod
    def mutate(self, info, **kwargs):
        return CreateUser(username='raushan', name='raushan',
                          password='raushan', created_at=datetime.now())


class Query(ObjectType):
    user = UserConnection(
        args={"username": graphene.Argument(graphene.String)})


class Mutation(ObjectType):
    user = graphene.Field(User)

    class Arguments:
        user = UserCreate(username='raushan', name='raushan',
                          password='raushan', created_at=datetime.now())

    @staticmethod
    def mutate(self, info, **kwargs):
        return CreateUser(None)

class Subscription(ObjectType):
    pass


schema = Schema(query=Query, mutation=Mutation)
gql = GraphQLApp(schema, on_get=make_graphiql_handler())
