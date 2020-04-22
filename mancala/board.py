import pandas as pd
import uuid
from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ARRAY, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.attributes import flag_dirty, flag_modified

from mancala.base import Base

# Base = Base


class Board(Base):
    __tablename__ = "boards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    pits = Column(ARRAY(Integer))
    stores = Column(ARRAY(Integer))
    game_id = Column(UUID(as_uuid=True), ForeignKey('games.id'))

    game = relationship("Game", back_populates="board")

    def __init__(self):
        self.pits = [4] * 12
        self.stores = [0] * 2
        self.pits_pairs = {0: 11,
                           1: 10,
                           2: 9,
                           3: 8,
                           4: 7,
                           5: 6}

    def get_store_stones(self, store_num):
        return self.stores[store_num - 1]

    def get_pit_stones(self, pit_num):
        return self.pits[pit_num]

    def all_pits_empty(self):
        for pit in self.pits:
            if pit != 0:
                return False
        return True

    def remove_from_pit(self, pit_num):
        in_pit = self.pits[pit_num]
        self.pits[pit_num] = 0
        flag_modified(self, 'pits')
        return in_pit

    def add_to_pit(self, pit_num):
        self.pits[pit_num] += 1
        flag_modified(self, 'pits')

    def add_to_store(self, player_store):
        self.stores[player_store-1] += 1
        flag_modified(self, 'stores')

    @staticmethod
    def print_board(board, player_1, player_2):
        player_1_arr = board.pits[:6]
        player_1_arr.append(board.stores[0])
        player_1_arr = [' '] + player_1_arr

        player_2_arr = [board.stores[1]]
        pits_reverse = board.pits[6:]
        pits_reverse.reverse()
        player_2_arr += pits_reverse
        player_2_arr += [' ']

        columns_names = {x: 'pit' for x in range(1,7)}
        df = pd.DataFrame({player_2: player_2_arr, player_1: player_1_arr})
        df = df.transpose()
        df = df.rename(columns={0: 'store', 7: 'store'})
        df = df.rename(columns=columns_names)
        print(df)
