from typing import Any
import json
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import scoped_session
from config.config import session_local
from sqlalchemy.orm import class_mapper

@as_declarative()
class Base:
    uuid: Any
    __name__: str

    # Generate __tablename__ automatically

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @staticmethod
    def object_to_dict(obj, found=None):
        if found is None:
            found = set()
        mapper = class_mapper(obj.__class__)
        columns = [column.key for column in mapper.columns]
        get_key_value = lambda c: (c, getattr(obj, c).isoformat()) if isinstance(getattr(obj, c), datetime) else (c, getattr(obj, c))
        out = dict(map(get_key_value, columns))
        for name, relation in mapper.relationships.items():
            if relation not in found:
                found.add(relation)
                related_obj = getattr(obj, name)
                if related_obj is not None:
                    if relation.uselist:
                        out[name] = [Base.object_to_dict(child, found) for child in related_obj]
                    else:
                        out[name] = Base.object_to_dict(related_obj, found)
        return out


    # def as_dict(self, include_fields=None, ignore_fields=None):
    #     return jsonable_encoder(self, include=include_fields, exclude=ignore_fields)

    # def as_json(self, include_fields=None, ignore_fields=None):
    #     return json.dumps(self.as_dict(include_fields, ignore_fields))
    
    # def to_dict(self, ignore_fields=None, include_fields=None):
    #     obj_dict= {c.name: getattr(self, c.name) for c in self.__table__.columns}  
    #     for c in inspect(self).mapper.column_attrs:
    #         print(c.key, getattr(self, c.key))


    #     if ignore_fields is not None:
    #         for column in ignore_fields:
    #             if column in obj_dict:
    #                 del obj_dict[column]
    #     # return obj_dict

    # @staticmethod
    # def to_json(db_obj, include_fields=None, ignore_fields=None):
    #     return Base.to_dict(db_obj, include_fields, ignore_fields)


Base.query = scoped_session(session_local).query_property()

import json
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.declarative import DeclarativeMeta


class OutputMixin(object):
    RELATIONSHIPS_TO_DICT = False

    # def __iter__(self):
    #     return self.to_dict().iteritems()

    def to_dict(self, rel=None, back=None):
        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        res = {column.key: getattr(self, attr)
               for attr, column in self.__mapper__.c.items()}
        if rel:
            for attr, relation in self.__mapper__.relationships.items():
                # Avoid recursive loop between to tables.
                if back == attr:
                    continue
                value = getattr(self, attr)
                if value is None:
                    res[relation.key] = None
                elif isinstance(value.__class__, DeclarativeMeta):
                    res[relation.key] = value.to_dict(back=self.__table__)
                else:
                    res[relation.key] = [i.to_dict(back=self.__table__)
                                         for i in value]
        return res



    def to_json(self, rel=None):
        def extended_encoder(x):
            if isinstance(x, datetime):
                return x.isoformat()
            if isinstance(x, UUID):
                return str(x)
        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        return json.dumps(self.to_dict(rel), default=extended_encoder)
