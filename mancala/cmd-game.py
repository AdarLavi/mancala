from mancala.game import Game
from mancala.board import Board


def run():
    game = Game()
    player_1 = input("First player, enter your name: ")
    player_2 = input("Second player, enter your name: ")
    game.start_game(player_1, player_2)

    Board.print_board(game.board, player_1, player_2)
    print(game.turn + ", the first move is yours")

    while not Board.all_pits_empty(game.board):
        move = int(input("pit number to start the move from: "))
        game.validate_move(move)
        game.make_move(move)
        Board.print_board(game.board, player_1, player_2)
        print(game.turn + " your turn")


if __name__ == "__main__":
    run()
