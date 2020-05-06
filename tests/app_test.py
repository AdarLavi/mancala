import json

import pytest

from mancala.app import app
from mancala.game import Game
from mancala.game_manager import create_session
from mancala.game_manager import retrieve_game


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
    response = client.get('/game/{}'.format('n0t3v3n1d'))
    status_code, response = get_code_and_response(response)

    assert status_code == 500
    assert response == {"error": "game id doesn't exist"}


def test_make_move(client, game):
    data = {"turn": game.turn, "pit": 6}
    response = client.post('/game/{}/make-move'.format(game.id), json=data)
    status_code, response = get_code_and_response(response)

    assert status_code == 200
    assert response['board'] == [4]*6 + [0] + [5]*4 + [4]
    assert response['pits'] == [0]*2




