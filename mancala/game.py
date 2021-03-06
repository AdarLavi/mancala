import uuid
from random import randint

from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from mancala.base import Base
from mancala.board import Board, pits_pairs
from mancala.exceptions import InvalidInput, EmptyPit


class Game(Base):

    __tablename__ = 'games'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    player_1 = Column(String)
    player_2 = Column(String)
    turn = Column(String)
    is_over = Column(Boolean)

    board = relationship("Board", uselist=False, back_populates="game")

    def __init__(self, player_1, player_2):
        self.board = Board()
        self.player_1 = player_1  # pits 0-5, store 1
        self.player_2 = player_2  # pits 6-11, store 2
        self.turn = self.start_game()
        self.is_over = False

    def start_game(self):
        first_turn = randint(1, 3)

        turn = self.player_2 if first_turn == 2 else self.player_1
        return turn

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
        stones_in_pit = self.board.remove_from_pit(pit_to_start)
        current_turn = self.turn
        self.turn = self.player_1 if current_turn != self.player_1 else self.player_2
        current_pit = pit_to_start

        stones = stones_in_pit
        while stones > 0:
            current_pit = (current_pit + 1) % 12
            if current_pit == 6 and current_turn == self.player_1:
                self.board.add_to_store(1)
                stones -= 1

            if current_pit == 0 and current_turn == self.player_2:
                self.board.add_to_store(2)
                stones -= 1

            if stones == 0:
                self.turn = current_turn
                break

            self.board.add_to_pit(current_pit)
            stones -= 1

        pit_in_front_current = None
        if current_pit <= 5 and self.board.get_pit_stones(current_pit) == 1 and current_turn == self.player_1:
            pit_in_front_current = pits_pairs.get(current_pit)
            if self.board.get_pit_stones(pit_in_front_current) > 0:
                self.take_from_in_front_pit(current_pit, pit_in_front_current, 1)

        if current_pit >= 6 and self.board.get_pit_stones(current_pit) == 1 and current_turn == self.player_2:
            for key, val in pits_pairs.items():
                if val == current_pit:
                    pit_in_front_current = key
                    break
            if self.board.get_pit_stones(pit_in_front_current) > 0:
                self.take_from_in_front_pit(current_pit, pit_in_front_current, 2)

    def take_from_in_front_pit(self, current_pit, pit_in_front_current, current_store):
        stones_in_front_of_current = self.board.remove_from_pit(pit_in_front_current)
        self.board.remove_from_pit(current_pit)
        for i in range(stones_in_front_of_current + 1):
            self.board.add_to_store(current_store)

    def end_game(self):
        player_1_in_store = self.board.get_store_stones(1)
        player_2_in_store = self.board.get_store_stones(2)
        if player_1_in_store == player_2_in_store:
            winner = 'No one, it\'s a tie!'
        elif player_1_in_store > player_2_in_store:
            winner = self.player_1
        else:
            winner = self.player_2
        self.is_over = True
        return winner
