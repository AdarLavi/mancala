from mancala.app import app, get_session
import pytest
import uuid
from mancala.game import Game
import json

#setup, tear down, before-after?
from mancala.game_manager import create_session


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


def test_new_game(client):
    player_1 = "moshe"
    player_2 = "simcha"
    data = {"player_1": player_1, "player_2": player_2}
    response = client.post('/game/new-game', json=data)
    status_code = response.status_code
    response = json.loads(response.data)

    assert response['player_1'] == player_1
    assert response['player_2'] == player_2
    assert status_code == 200


def test_new_game_no_player(client):
    pass


def test_get_game(game, client):
    response = client.get('/game/{}'.format(game.id))
    status_code = response.status_code
    response = json.loads(response.data)
    assert status_code == 200



