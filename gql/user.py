import logging
import enum
from graphene import Boolean, DateTime, InputObjectType, List, String, relay
from graphene.types.generic import GenericScalar
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from sq.user import User as UserModel
from graphene_sqlalchemy.utils import EnumValue

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class User(SQLAlchemyObjectType):

    class Meta:
        model = UserModel
        interfaces = (relay.Node,)


def sort_by(obj,sort):
    if sort is not None:
        if not isinstance(sort, list):
            sort = [sort]
        sort_args = []
        for item in sort:
            if isinstance(item, enum.Enum):
                sort_args.append(item.value.value)
            elif isinstance(item, EnumValue):
                sort_args.append(item.value)
            else:
                sort_args.append(item)
    return obj.order_by(*sort_args)

class UserConnection(SQLAlchemyConnectionField):
    def __init__(self, args=None):
        super().__init__(User.connection, args=args)

    @classmethod
    def get_query(cls, model, info, sort=None, **args):
        filter_dict = dict([(key, val) for key, val in 
           args.items() if key not in ['after', 'before', 'last', 'first']])
        filters={}
        for key, value in filter_dict.items():
            if value is not None:
                filters[key] = value
        db_obj= model.query.filter_by(**filters)
        db_obj= sort_by(db_obj,sort)
        return db_obj

class UserBase(InputObjectType):
    username = String(required=False)
    name = String(required=False)
    created_at = DateTime(required=False)
    is_superuser = Boolean(required=False)


class UserCreate(UserBase):
    username = String(required=True)
    password = String(required=True)


class UserUpdate(UserBase):
    id = String(required=True)
    password = String(required=False)


class UserDelete(InputObjectType):
    id = String(required=True)
