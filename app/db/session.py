from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)

Base = declarative_base()

def SessionLocal(bind=None):
    if bind is None:
        bind = engine
    session = sessionmaker(autocommit=False, autoflush=False, bind=bind)
    return session()

