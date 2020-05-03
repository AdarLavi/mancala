from flask import Flask, request, g, abort, make_response, jsonify

from mancala.exceptions import EmptyPit, InvalidInput
from mancala.game import Game
from mancala.game_manager import create_session

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


@app.errorhandler
def bad_request(error):
    return make_response(jsonify({'error': 'Not found'}), 400)
    # return make_response({"error": "Invalid Input"}, 400)


def jsonify_game(game):
    json_game = {'id': game.id,
                 'player_1': game.player_1,
                 'player_2': game.player_2,
                 'pits': game.board.pits,
                 'stores': game.board.stores,
                 'turn': game.turn}
    return json_game


@app.route('/game/new-game', methods=['POST'])
def new_game():
    data = request.get_json()
    player_1 = data.get('player_1', None)
    player_2 = data.get('player_2', None)
    new_game = Game(player_1, player_2)
    new_game.start_game()
    session = get_session()
    session.add(new_game)
    session.commit()

    return jsonify_game(new_game)


@app.route("/game/<string:game_id>", methods=['GET'])
def get_game(game_id):
    session = get_session()
    return jsonify_game(session.query(Game).filter_by(id=game_id).first())


@app.route('/game/<string:game_id>/make-move', methods=['POST'])
def make_move(game_id):
    session = get_session()
    game = session.query(Game).filter_by(id=game_id).first()
    pit = request.get_json().get('pit', None)
    try:
        game.make_move(pit)
    except EmptyPit:
        abort(400)
    except InvalidInput:
        abort(400)
    session.commit()
    return jsonify_game(game)


if __name__ == '__main__':
    app.run()
