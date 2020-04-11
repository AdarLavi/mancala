from board import Board
from random import randint


class Game:
    def __init__(self):
        self.board = Board()
        self.turn = None
        self.player_1 = None  # pits 0-5, store 1
        self.player_2 = None  # pits 6-11, store 2

    def make_move(self, pit_to_start):
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

        current_pit = (pit_to_start + 1) % 12

        stones = stones_in_pit
        while stones > 0:
            if current_pit == 6 and current_turn == self.player_1:
                Board.add_to_store(self.board, 1)
                stones -= 1

            if current_pit == 11 and current_turn == self.player_2:
                Board.add_to_store(self.board, 2)
                stones -= 1

            if stones == 0:
                self.turn = current_turn
                break

            Board.add_to_pit(self.board, current_pit)
            stones -= 1
            current_pit = (current_pit + 1) % 12

        pit_in_front_current = None
        if current_pit <= 5 and Board.get_pit_stones(self.board, current_pit) == 1 and current_turn == self.player_1:
            pit_in_front_current = self.board.pits_pairs.get(current_pit)
            self.take_from_in_front_pit(current_pit, pit_in_front_current, 1)

        if current_pit >= 6 and Board.get_pit_stones(self.board, current_pit) == 1 and current_turn == self.player_2:
            for key, val in self.board.pits_pairs.items():
                if val == current_pit:
                    pit_in_front_current = key
                    break
            self.take_from_in_front_pit(current_pit, pit_in_front_current, 2)

    def take_from_in_front_pit(self, current_pit, pit_in_front_current, current_store):
        stones_in_front_of_current = Board.remove_from_pit(self.board, pit_in_front_current)
        Board.remove_from_pit(self.board, current_pit)
        for i in range(stones_in_front_of_current + 1):
            Board.add_to_store(self.board, current_store)

    def start_game(self, first_player_name, second_player_name):
        self.player_1 = first_player_name
        self.player_2 = second_player_name
        first_turn = randint(1, 3)

        self.turn = self.player_2 if first_turn == 2 else self.player_1
