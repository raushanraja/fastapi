import json
from operator import mod
from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union
from sqlalchemy.orm import Session
from pydantic import BaseModel
from crud.base_class import Base
from fastapi.encoders import jsonable_encoder

ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
DeleteSchemaType = TypeVar("DeleteSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], schema: Type[SchemaType]):
        """
        CRUD Object with default methods to create, read, update, delete 
        **parameters**
        *`model`: A SqlAlchemy Model class`
        *`schema`: A Pydantic Model (schema) class
        """
        self.model = model
        self.schema = schema

    def get(self, db: Session, id: str) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).one_or_none()

    def get_by_filter(self, db: Session, filters: dict = None, limit: int = None) -> Optional[ModelType]:
        if filters:
            if limit:
                return db.query(self.model).filter_by(**filters).limit(limit).all()
            else:
                return db.query(self.model).filter_by(**filters).all()
        else:
            if limit:
                return db.query(self.model).limit(limit).all()
            else:
                return db.query(self.model).all()


    def create(self, db: Session, obj_in: CreateSchemaType) -> Optional[ModelType]:
        obj_in = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> Optional[ModelType]:
        db_obj_data = jsonable_encoder(db_obj.__dict__)
        if not isinstance(obj_in, dict):
            obj_in = obj_in.dict
        for field in db_obj_data:
            if field in obj_in:
                setattr(db_obj, field, obj_in[field])
        db.add(db_obj)
        db.refresh(db_obj)
        return db_obj

    def test_multiple_filter(self, db: Session, filter_one:dict = None, filter_two:dict = None, filter_three:dict = None) -> Optional[ModelType]:
        return db.query(self.model).filter_by(**filter_one).filter_by(**filter_two).filter_by(**filter_three).all()


    def remove(self, db: Session, id: str):
        db_obj = self.get(db, id)
        if db_obj:
            db.delete(db_obj)
            return True
        return False
