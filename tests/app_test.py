import json
from uuid import uuid4

import pytest

from mancala.app import app, jsonify_game
from mancala.game import Game
from mancala.game_manager import create_session, retrieve_game


def get_code_and_response(response):
    return response.status_code, json.loads(response.data)


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def session():
    return create_session()


@pytest.fixture
def game(client, session):
    game = Game(player_1="Tester", player_2="Checker")
    session.add(game)
    session.commit()
    yield game
    session.delete(game)
    session.commit()


def test_new_game(client, session):
    player_1 = "moshe"
    player_2 = "simcha_balulu"
    data = {"player_1": player_1, "player_2": player_2}
    response = client.post('/game/new-game', json=data)

    status_code, response = get_code_and_response(response)
    game_id = response['id']

    assert response['player_1'] == player_1
    assert response['player_2'] == player_2
    assert response['turn'] is not None
    assert game_id is not None
    assert status_code == 200

    game = retrieve_game(session, game_id)
    session.delete(game)
    session.commit()


def test_new_game_no_player(client):
    data = {"player_1": "Simba"}
    response = client.post('/game/new-game', json=data)
    status_code, response = get_code_and_response(response)

    assert status_code == 400
    assert response == {"error": "Invalid input. Two players must have a name"}


def test_get_game(game, client):
    response = client.get('/game/{}'.format(game.id))
    status_code, response = get_code_and_response(response)

    assert status_code == 200
    assert response['id'] == str(game.id)


def test_get_game_doesnt_exist(client):
    response = client.get('/game/{}'.format(uuid4()))
    status_code, response = get_code_and_response(response)

    assert status_code == 404
    assert response == {"error": "game id doesn't exist"}


def test_make_move(client, game):
    data = {"user": game.turn, "pit": 6}
    response = client.post('/game/{}/make-move'.format(game.id), json=data)
    status_code, response = get_code_and_response(response)

    assert status_code == 200
    assert response['pits'] == [4]*6 + [0] + [5]*4 + [4]
    assert response['stores'] == [0]*2


def test_make_move_wrong_player(client, game):
    user = game.player_2 if game.turn == game.player_1 else game.player_1
    data = {"user": user, "pit": 6}
    response = client.post('/game/{}/make-move'.format(game.id), json=data)
    status_code, response = get_code_and_response(response)

    assert status_code == 400
    assert response == {"error": "not this player turn"}


def test_make_move_no_player(client, game):
    data = {"pit": 6}
    response = client.post('/game/{}/make-move'.format(game.id), json=data)
    status_code, response = get_code_and_response(response)

    assert status_code == 400
    assert response == {"error": "player was not declared"}


def test_make_move_no_pit(client, game):
    data = {"user": game.turn}
    response = client.post('/game/{}/make-move'.format(game.id), json=data)
    status_code, response = get_code_and_response(response)

    assert status_code == 400
    assert response == {"error": "pit was not declared"}


def test_make_move_invalid_pit(client, game):
    data = {"user": game.turn, "pit": 80}
    response = client.post('/game/{}/make-move'.format(game.id), json=data)
    status_code, response = get_code_and_response(response)

    assert status_code == 400
    assert response == {"error": "Invalid input. Not a number of a pit"}


def test_jsonify_game(game):
    j_game = jsonify_game(game)

    assert j_game == {'id': game.id,
                      'player_1': game.player_1,
                      'player_2': game.player_2,
                      'pits': game.board.pits,
                      'stores': game.board.stores,
                      'turn': game.turn,
                      'is_over': game.is_over}
