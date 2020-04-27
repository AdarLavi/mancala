from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from mancala.base import Base

DB_STRING = "postgresql://postgres:65266526@localhost/mancala"


def create_session():
    engine = create_engine(DB_STRING)
    Base.metadata.create_all(engine)
    Session = sessionmaker(engine, expire_on_commit=False)
    session = Session()
    return session
