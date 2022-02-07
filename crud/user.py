from crud.crud_base import CRUDBase
from sq.user import User
from py.user import UserCreate, UserUpdate, User as UserSchema


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    pass


user = CRUDUser(User, UserSchema)
