from mancala.game import Game, Base
from mancala.board import Board
from mancala.game_manager import create_session
from mancala.exceptions import InvalidInput, EmptyPit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uuid


def run():
    session = create_session()

    saved_or_not = input("For saved game, insert 0, for new game, press enter ")
    if saved_or_not == "0":
        while True:
            try:
                saved_game_id = uuid.UUID(input("saved game id? "))
                break
            except ValueError:
                print("Invalid game id")
        game = session.query(Game).filter_by(id=saved_game_id).first()
        player_1 = game.player_1
        player_2 = game.player_2
    else:
        player_1 = input("First player, enter your name: ")
        player_2 = input("Second player, enter your name: ")
        game = Game(player_1=player_1, player_2=player_2)
        game.start_game()
        session.add(game)
        session.commit()
        print("your game id is: " + str(game.id))
        print(game.turn + ", the first move is yours")

    Board.print_board(game.board, player_1, player_2)

    while not Board.all_pits_empty(game.board):
        print(game.turn + ", it\'s your turn")
        while True:
            move = input("pit number to start the move from: ")
            try:
                game.make_move(move)
                Board.print_board(game.board, player_1, player_2)
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
