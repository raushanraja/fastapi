import logging

from graphene import Boolean, DateTime, InputObjectType, List, String, relay
from graphene.types.generic import GenericScalar
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from sq.user import User as UserModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class User(SQLAlchemyObjectType):

    class Meta:
        model = UserModel
        interfaces = (relay.Node,)

class UserConnection(SQLAlchemyConnectionField):
    def __init__(self, args):
        super().__init__(User.connection, args=args)

    @classmethod
    def get_query(cls, model, info, sort=None, **args):
        if 'username' in args:
            return model.query.filter_by(username=args['username'])
        return model.query

class UserBase(InputObjectType):
    username = String(required=False)
    name = String(required=False)
    password = String(required=True)
    created_at = DateTime(required=False)
    is_superuser= Boolean(required=False)

class UserCreate(UserBase):
    username = String(required=True)
    password = String(required=True)

class UserUpdate(UserBase):
    id = String(required=True)

class UserDelete(InputObjectType):
    id = String(required=True)
