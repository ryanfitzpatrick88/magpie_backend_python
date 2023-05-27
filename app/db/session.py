from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(
    f'{settings.DATABASE_URL}/users', echo=True
)

Base = declarative_base()

def SessionLocal(bind=None):
    if bind is None:
        bind = engine
    session = sessionmaker(autocommit=False, autoflush=False, bind=bind)
    return session()

