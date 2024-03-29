from datetime import datetime
from uuid import uuid4

from crud.base_class import Base, OutputMixin
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import column_mapped_collection

from .posts import Post


class User(Base, OutputMixin):
    RELATIONSHIPS_TO_DICT = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_superuser = Column(Boolean, default=False)
    address = relationship('Address', back_populates='user', uselist=False)
    post = relationship("Post", backref="user", uselist=False)
