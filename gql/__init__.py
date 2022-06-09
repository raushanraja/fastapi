from datetime import datetime
import graphene
from fastapi import APIRouter, Request
from graphene import ObjectType, Schema, Mutation
from graphene_sqlalchemy import SQLAlchemyConnectionField
from starlette.applications import Starlette
from starlette_graphene3 import GraphQLApp,  make_playground_handler

from .user import User, UserConnection, UserCreate
from crud.user import user as crud_user
from config.config import SessionLocal


class CreateUser(Mutation):
    user = graphene.Field(User)

    class Arguments:
        user = UserCreate()

    @staticmethod
    def mutate(root, info, user):
        with SessionLocal() as db:
            crud_user.create(db, obj_in=user)
        return CreateUser(user=User(**user))


class AA(graphene.Argument):
    username = graphene.String


class Query(ObjectType):
    users = SQLAlchemyConnectionField(User.connection)
    user = graphene.relay.Node.Field(User)
    users_with_filter = UserConnection(args={'username': graphene.Argument(
        graphene.String), 'name': graphene.Argument(graphene.String)})


class Mutations(ObjectType):
    create_user = CreateUser.Field()


class Subscription(ObjectType):
    pass


schema = Schema(query=Query, mutation=Mutations)
gql = GraphQLApp(schema, on_get=make_playground_handler())
gqlwui = GraphQLApp(schema)
