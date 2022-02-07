from typing import List
from fastapi import FastAPI, Request, Depends
from config.config import session_local
from py.user import UserCreate, User
from crud.user import user

app = FastAPI()


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