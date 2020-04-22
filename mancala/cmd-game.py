from mancala.game import Game, Base
from mancala.board import Board
from mancala.exceptions import InvalidInput, EmptyPit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def run():
    engine = create_engine("postgresql://postgres:65266526@localhost/mancala")
    Base.metadata.create_all(engine)
    player_1 = input("First player, enter your name: ")
    player_2 = input("Second player, enter your name: ")
    game = Game(player_1=player_1, player_2=player_2)
    game.start_game()

    Session = sessionmaker(engine, expire_on_commit=False)
    session = Session()
    session.add(game)
    session.commit()

    Board.print_board(game.board, player_1, player_2)
    print(game.turn + ", the first move is yours")

    while not Board.all_pits_empty(game.board):
        print(game.turn + ", it\'s your turn")
        while True:
            move = input("pit number to start the move from: ")
            try:
                game.make_move(move)
                Board.print_board(game.board, player_1, player_2)
                # board = game.board
                # session.add_all([game, board])
                session.commit()
                break
            except EmptyPit:
                print("Choose a non empty pit, genius")
            except InvalidInput:
                print("Choose valid pit number, 0-11")

    winner = str(game.end_game()).upper()
    print(winner + " WON")

    return


def get_started(engine, game):

    Session = sessionmaker(engine)
    session = Session()

    session.add(game)
    session.commit()

    pass


if __name__ == "__main__":
    run()
