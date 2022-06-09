from typing import Any
import json
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import scoped_session
from config.config import session_local, engine


@as_declarative()
class Base:
    uuid: Any
    __name__: str

    # Generate __tablename__ automatically

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def as_dict(self, include_fields=None, ignore_fields=None):
        return jsonable_encoder(self, include=include_fields, exclude=ignore_fields)

    def as_json(self, include_fields=None, ignore_fields=None):
        return json.dumps(self.as_dict(include_fields, ignore_fields))

    @staticmethod
    def to_dict(db_obj, include_fields=None, ignore_fields=None):
        return jsonable_encoder(db_obj, include=include_fields, exclude=ignore_fields)

    @staticmethod
    def to_json(db_obj, include_fields=None, ignore_fields=None):
        return Base.to_dict(db_obj, include_fields, ignore_fields)


Base.query = scoped_session(session_local).query_property()
