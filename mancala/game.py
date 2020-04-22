from mancala.board import Board
from mancala.exceptions import InvalidInput, EmptyPit
from random import randint
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from mancala.base import Base
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID

# Base = Base()


class Game(Base):
    __tablename__ = 'games'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    player_1 = Column(String)
    player_2 = Column(String)
    turn = Column(String)

    board = relationship("Board", uselist=False, back_populates="game")

    def __init__(self, player_1, player_2):
        self.board = Board()
        self.player_1 = player_1  # pits 0-5, store 1
        self.player_2 = player_2  # pits 6-11, store 2

    def validate_move(self, pit_so_start):
        try:
            pit_so_start = int(pit_so_start)
        except ValueError:
            raise InvalidInput
        if pit_so_start not in range(12):
            raise InvalidInput
        if self.board.get_pit_stones(pit_so_start) == 0:
            raise EmptyPit
        return pit_so_start

    def make_move(self, pit_to_start):
        pit_to_start = self.validate_move(pit_to_start)
        stones_in_pit = Board.remove_from_pit(self.board, pit_to_start)
        current_turn = self.turn
        self.turn = self.player_1 if current_turn != self.player_1 else self.player_2

        # # if player 1
        # if stones_in_pit + pit_to_start == 5:
        #     for steps, stone in enumerate(stones_in_pit):
        #         Board.add_to_pit(self.board, pit_to_start + steps + 1)
        #     Board.add_to_store(self.board, current_player_store)
        #
        # if stones_in_pit + pit_to_start == 11:
        #     for steps, stone in enumerate(stones_in_pit):
        #         Board.add_to_pit(self.board, pit_to_start + steps + 1)
        #     Board.add_to_store(self.board, current_player_store)
        current_pit = pit_to_start

        stones = stones_in_pit
        while stones > 0:
            current_pit = (current_pit + 1) % 12
            if current_pit == 6 and current_turn == self.player_1:
                Board.add_to_store(self.board, 1)
                stones -= 1

            if current_pit == 0 and current_turn == self.player_2:
                Board.add_to_store(self.board, 2)
                stones -= 1

            if stones == 0:
                self.turn = current_turn
                break

            Board.add_to_pit(self.board, current_pit)
            stones -= 1

        pit_in_front_current = None
        if current_pit <= 5 and Board.get_pit_stones(self.board, current_pit) == 1 and current_turn == self.player_1:
            pit_in_front_current = self.board.pits_pairs.get(current_pit)
            if Board.get_pit_stones(self.board, pit_in_front_current) > 0:
                self.take_from_in_front_pit(current_pit, pit_in_front_current, 1)

        if current_pit >= 6 and Board.get_pit_stones(self.board, current_pit) == 1 and current_turn == self.player_2:
            for key, val in self.board.pits_pairs.items():
                if val == current_pit:
                    pit_in_front_current = key
                    break
            if Board.get_pit_stones(self.board, pit_in_front_current) > 0:
                self.take_from_in_front_pit(current_pit, pit_in_front_current, 2)

    def take_from_in_front_pit(self, current_pit, pit_in_front_current, current_store):
        stones_in_front_of_current = Board.remove_from_pit(self.board, pit_in_front_current)
        Board.remove_from_pit(self.board, current_pit)
        for i in range(stones_in_front_of_current + 1):
            Board.add_to_store(self.board, current_store)

    def start_game(self):
        first_turn = randint(1, 3)

        self.turn = self.player_2 if first_turn == 2 else self.player_1

    def end_game(self):
        winner = self.player_1 if self.board.get_store_stones(1) >\
                                  self.board.get_store_stones(2) else self.player_2
        return winner
