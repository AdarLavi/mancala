from flask import Flask, request, g, abort, make_response

from mancala.exceptions import EmptyPit, InvalidInput
from mancala.game import Game
from mancala.game_manager import create_session, retrieve_game

app = Flask(__name__)


def get_session():
    if 'session' not in g:
        g.session = create_session()

    return g.session


# @app.teardown_appcontext
# def teardown_session():
#     session = g.pop('session', None)
#
#     if session is not None:
#         session.close()


@app.errorhandler(400)
def bad_request(error):
    return {"error": "Invalid input."}, 400


def jsonify_game(game):
    json_game = {'id': game.id,
                 'player_1': game.player_1,
                 'player_2': game.player_2,
                 'pits': game.board.pits,
                 'stores': game.board.stores,
                 'turn': game.turn,
                 'is_over': game.is_over}
    return json_game


@app.route('/game/new-game', methods=['POST'])
def new_game():
    data = request.get_json()
    player_1 = data.get('player_1', None)
    player_2 = data.get('player_2', None)
    if not player_1 or not player_2:
        return {"error": "Invalid input. Two players must have a name"}, 400
    new_game = Game(player_1, player_2)
    session = get_session()
    session.add(new_game)
    session.commit()

    return jsonify_game(new_game)


@app.route("/game/<string:game_id>", methods=['GET'])
def get_game(game_id):
    session = get_session()
    try:
        game = jsonify_game(retrieve_game(session, game_id))
        return game
    except Exception:
        return {"error": "game id doesn't exist"}, 404


@app.route('/game/<string:game_id>/make-move', methods=['POST'])
def make_move(game_id):
    session = get_session()
    data = request.get_json()
    game = retrieve_game(session, game_id)
    user = data.get('user', None)
    if user:
        if game.turn.lower() != user.lower():
            return {"error": "not this player turn"}, 400
    else:
        return {"error": "player was not declared"}, 400
    pit = data.get('pit', None)
    if pit is not None:
        try:
            game.make_move(pit)
        except EmptyPit:
            return {"error": "Invalid input. Empty pit was chosen."}, 400
        except InvalidInput:
            return {"error": "Invalid input. Not a number of a pit"}, 400
    else:
        return {"error": "pit was not declared"}, 400
    session.commit()

    if game.board.all_pits_empty():
        winner = game.end_game()
        win_json = dict({'winner': winner}, **jsonify_game(game))
        return win_json

    return jsonify_game(game)


if __name__ == '__main__':
    app.run()
