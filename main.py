from typing import List
from fastapi import FastAPI, Request, APIRouter
from config.config import session_local
from py.user import UserCreate, User
from crud.user import user
from gql import gql, gqlwui

app = FastAPI()
api_router = APIRouter()


@app.get('/user')
async def get_user(id: str):
    user_data = None
    with session_local() as session:
        user_data = user.get(db=session, id=id)
    return user_data


@app.post('/user', response_model=User)
async def create_user(new_user: UserCreate):
    user_data = None
    with session_local() as session:
        user_data = user.create(db=session, obj_in=new_user)
    return user_data


@app.get('/users', response_model=List[User])
async def get_users():
    with session_local() as session:
        user_data = user.get_by_filter(db=session)
    return user_data


@app.get('/usersf', response_model=List[User])
async def get_usersf():
    with session_local() as session:
        user_data = user.test_multiple_filter(db=session, filter_one={'username': 'raushan'}, filter_two={
                                              'name': 'raushan'}, filter_three={'password': 'password'})
    return user_data

app.mount('/graphiql', gql)
app.mount('/graphql', gqlwui)
