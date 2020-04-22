from mancala.board import Board
import pytest
import pandas as pd


@pytest.fixture
def board():
    board = Board()
    return board


def test_initial_pits(board):
    assert board.pits == [4] * 12


def test_initial_stores(board):
    assert board.stores == [0] * 2


def test_empty_pits(board):
    for pit in range(len(board.pits)):
        board.pits[pit] = 0

    assert board.all_pits_empty()


def test_get_pit_stones(board):
    for i in range(5):
        board.add_to_pit(3)
    assert board.get_pit_stones(3) == 9


def test_get_store_stones(board):
    for i in range(3):
        board.add_to_store(2)
    assert board.get_store_stones(2) == 3


def test_remove_from_pit(board):
    for stone in range(board.pits[2]):
        board.remove_from_pit(2)

    assert board.get_pit_stones(2) == 0


def test_add_to_pit(board):
    board.add_to_pit(3)
    assert board.pits[3] == 5


def test_add_to_store(board):
    board.add_to_store(2)
    assert board.stores[1] == 1


# def test_print_borad(board):
#     in_pit = board.remove_from_pit(2)
#     for i in range(1, in_pit):
#         board.add_to_pit(2+i)
#     board.add_to_store(1)
#     first_player_pits_and_store = [' '] + [4, 0] + [5]*3 + [1]
#
#     second_player_store_and_pits = [0] + [4]*6 + [' ']
#
#     columns_names = {x: 'pit' for x in range(1, 7)}
#     df = pd.DataFrame({"second": second_player_store_and_pits, "first": first_player_pits_and_store})
#     df = df.transpose()
#     df = df.rename(columns={0: 'store', 7: 'store'})
#     df = df.rename(columns=columns_names)
#
#     assert Board.print_board(board, "first", "second") ==
