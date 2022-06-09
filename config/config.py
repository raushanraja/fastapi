from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from pydantic import PostgresDsn
from config.setting import settings

postgres_url = PostgresDsn.build(scheme=settings.SCHEMA, user=settings.POSTUSER, password=settings.POSTPASSWORD,
                                 host=settings.POSTHOST, path=f"/{settings.POSTPATH}", port=settings.POSTPORT)
print(postgres_url)
engine = create_engine(postgres_url, pool_pre_ping=True, pool_size=50)
session_local = sessionmaker(autocommit=False, bind=engine)
SessionLocal = scoped_session(session_factory=session_local)
