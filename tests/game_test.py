from mancala.game import Game
from mancala.exceptions import InvalidInput, EmptyPit
import pytest


@pytest.fixture
def game():
    game = Game("first", "second")
    game.start_game()
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
    game.make_move(0)
    assert game.board.get_store_stones(1) == 0


def test_finishing_in_empty_pit_with_empty_pit_in_front_player_2(game):
    game.board.pits = [0]*6 + [2]*2 + [0]*4
    game.turn = "second"
    game.make_move(7)
    assert game.board.get_store_stones(2) == 0


def test_whole_round(game):
    game.board.pits = [0]*11 + [14]
    game.make_move(11)
    player_1_store_has_one = True if game.board.get_store_stones(1) == 1 else False
    pits = True if game.board.pits == [2] + [1]*11 else False
    player_2_store_has_none = True if game.board.get_store_stones(2) == 0 else False
    assert player_1_store_has_one and player_2_store_has_none and pits


def test_string_input(game):
    with pytest.raises(InvalidInput):
        game.validate_move('randomstring')


def test_invalid_number_pit(game):
    with pytest.raises(InvalidInput):
        game.validate_move(13)


def test_empty_pit_input(game):
    game.board.pits[2] = 0
    with pytest.raises(EmptyPit):
        game.validate_move(2)


def test_winning(game):
    game.board.pits = [0]*11 + [1]
    game.turn = "second"
    game.make_move(11)
    assert game.end_game() == "second"
