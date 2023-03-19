from datetime import datetime
from sq.user import User
from sq.address import Address
from sq.posts import Post
from crud.user import user as crud_user
from crud import crud_address, crud_post
from config.config import SessionLocal
from fastapi.encoders import jsonable_encoder


def get_post(user_id: str = None):
    if user_id is None:
        return Post(title='Hello World', content='This is my first post')
    return Post(title='Hello World', content='This is my first post', user_id=user_id)


def get_user(post: Post = None):
    if post is not None:
        return User(name='John', username='john', password='123456', post=post)
    return User(name='John', username='john', password='123456')


def get_address(user_id: str = None):
    if user_id is None:
        return Address(address='123 Main St')
    return Address(address='123 Main St', user_id=user_id)


def add_user_with_data(user):
    with SessionLocal() as db:
        user_obj = crud_user.create(db=db, obj_in=user)
        return str(user_obj.id)


def add_user():
    with SessionLocal() as db:
        user = User(name='John', username='john', password='123456')
        user_obj = crud_user.create(db=db, obj_in=user)
        return str(user_obj.id)


def add_address(user_id: str):
    with SessionLocal() as db:
        user = crud_user.get(db=db, id=user_id)
        address = Address(user_id=user.id, address='123 Main St')
        address_obj = crud_address.create(db=db, obj_in=address)
        print(jsonable_encoder(address_obj))


def get_all_user():
    with SessionLocal() as db:
        users = crud_user.get_by_filter(db=db, filters={'username': 'john'})
        for user in users:
            print((jsonable_encoder(user.post)))


def add_post(user_id: str = None):
    with SessionLocal() as db:
        post = Post(title='Hello World',
                    content='This is my first post', user_id=user_id)
        post_obj = crud_post.create(db=db, obj_in=post)
        print(str(post_obj.id))


def add_user_post_dict():
    post_dict = {'title': 'Hello World', 'content': 'This is my first post'}
    user_dict = {'name': 'John', 'username': 'John',
                 'post': post_dict, 'password': 'passowrd'}
    with SessionLocal() as db:
        user_obj = crud_user.create(db=db, obj_in=user_dict)
        print(str(user_obj.__dict__))
        if hasattr(user_obj, 'post'):
            print(str(user_obj.post.__dict__))
        return str(user_obj.id)


def add_user_attr():
    with SessionLocal() as db:
        user = User(name='John')
        user.username = 'John'
        user.password = 'Password'
        user.post = Post()
        user.post.title = 'Hello World'
        user.post.content = 'The post by post for the post.'
        user = crud_user.create(db=db, obj_in=user)
        print(user)
        print(user.object_to_dict(user))


def main():
    add_user_attr()
    # add_user_post_dict()
    # user_id: str = add_user()
    # add_address(user_id=user_id)
    # add_address(user_id='a6af623b-010a-4464-b764-5dc1e64d2638')
    # post = get_post(user_id='ad0d7b81-cf8a-4a8e-9177-94b74792e057')
    # post_obj = add_post(user_id='ad0d7b81-cf8a-4a8e-9177-94b74792e057')
    # print(post_obj)
    # get_all_user()
    # post = get_post()
    # user = get_user(post=post)
    # print(get_user(post=Post(title='John', content='John')).__dict__)
    # print(jsonable_encoder(User(post=Post(title='John', content='John'))))
    # print(add_user_with_data(user))
    # get_all_user()


if __name__ == '__main__':
    main()


# print(User.__table__.columns)  # get column name using column.name
# user_dict = {'name':"raushan", 'username':"raushan",'password':"password", 'is_superuser':False}
# print(User(**user_dict).__dict__)
