import mongomock
from mongoengine import connect, disconnect 
from mongoengine import Document, StringField


connect('mongoenginetest', host='mongodb://localhost', mongo_client_class=mongomock.MongoClient)


class Person(Document):
    name= StringField()

