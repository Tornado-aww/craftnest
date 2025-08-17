from sqlmodel import SQLModel, create_engine, Session
from contextlib import contextmanager
import os

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./craftnest.db")
connect_args = {"check_same_thread": False} if DB_URL.startswith("sqlite") else {}
engine = create_engine(DB_URL, echo=False, connect_args=connect_args)


def init_db():
    from models import Product  # noqa: F401 (регистрация моделей)
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session():
    with Session(engine) as session:
        yield session
