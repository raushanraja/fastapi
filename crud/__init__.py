from .crud_base import CRUDBase
from sq.address import Address
from py.address import AddressCreate, AddressUpdate, Address as AddressSchema
from sq.posts import Post
from py.posts import PostCreate, PostUpdate, Post as PostSchema

crud_address = CRUDBase[Address, AddressCreate, AddressUpdate](Address, AddressSchema)
crud_post = CRUDBase[Post, PostCreate, PostUpdate](Post, PostSchema)