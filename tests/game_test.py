from mancala.game import Game
import pytest


@pytest.fixture
def game():
    game = Game()
    game.start_game("first", "second")
    game.turn = "first"
    return game


def test_single_move_change_turns_first_to_second(game):
    game.make_move(4)
    assert game.turn == "second"


def test_single_move_change_turns_second_to_first(game):
    game.turn = "second"
    game.make_move(6)
    assert game.turn == "first"


def test_finishing_in_store_getting_another_turn_player_1(game):
    game.make_move(2)
    assert game.turn == "first"


def test_finishing_in_store_getting_another_turn_player_2(game):
    game.turn = "second"
    game.make_move(8)
    assert game.turn == "second"


def test_finishing_in_empty_pit_getting_stones_from_pit_in_front_player_1(game):
    game.make_move(2)
    game.make_move(10)
    assert game.board.get_store_stones(1) == 1 + 4 + 1


def test_finishing_in_empty_pit_getting_stones_from_pit_in_front_player_2(game):
    game.turn = "second"
    game.make_move(8)
    game.make_move(4)
    assert game.board.get_store_stones(2) == 1 + 4 + 1


def test_finishing_in_empty_pit_with_empty_pit_in_front_player_1(game):
    game.board.pits = [4]*2 + [0]*10
    game.make_move(11)
    assert game.board.get_store_stones(1) == 0


def test_finishing_in_empty_pit_with_empty_pit_in_front_player_2(game):
    game.board.pits = [0]*6 + [2]*2 + [0]*4
    game.turn = "second"
    game.make_move(7)
    assert game.board.get_store_stones(2) == 0

