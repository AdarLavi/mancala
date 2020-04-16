from mancala.game import Game
from mancala.board import Board
from mancala.exceptions import InvalidInput, EmptyPit


def run():
    game = Game()
    player_1 = input("First player, enter your name: ")
    player_2 = input("Second player, enter your name: ")
    game.start_game(player_1, player_2)

    Board.print_board(game.board, player_1, player_2)
    print(game.turn + ", the first move is yours")

    while not Board.all_pits_empty(game.board):
        print(game.turn + ", it\'s your turn")
        while True:
            move = input("pit number to start the move from: ")
            try:
                game.make_move(move)
                Board.print_board(game.board, player_1, player_2)
                break
            except EmptyPit:
                print("Choose a non empty pit, genius")
            except InvalidInput:
                print("Choose valid pit number, 0-11")

    winner = str(game.end_game()).upper()
    print(winner + " WON")

    return


if __name__ == "__main__":
    run()
