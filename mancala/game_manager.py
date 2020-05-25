import os

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from mancala.base import Base
from mancala.game import Game

DB_STRING = os.environ['DATABASE_URL']


def create_session():
    engine = create_engine(DB_STRING)
    Base.metadata.create_all(engine)
    Session = sessionmaker(engine, expire_on_commit=False)
    session = Session()
    return session


def retrieve_game(session, game_id):
    return session.query(Game).filter_by(id=game_id).first()
