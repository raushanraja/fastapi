from datetime import datetime
from uuid import uuid4

from crud.base_class import Base, OutputMixin
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref


# create a sqlalchemy table name post
class Post(Base, OutputMixin):
    RELATIONSHIPS_TO_DICT = False
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), unique=True)
    title = Column(String)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

