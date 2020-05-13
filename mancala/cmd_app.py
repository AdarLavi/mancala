from signal import SIGINT, signal
import time
import pandas as pd
import requests


def run():
    saved_or_not = input("For saved game, insert 0, for new game, press enter ")
    if saved_or_not == "0":
        game = None
        while not game:
            saved_game_id = input("saved game id? ")
            name = input("and your name is...? ")
            response = requests.get('http://127.0.0.1:5000/game/{}'.format(saved_game_id))
            if not response.ok:
                print(response.text)
                continue
            game = response.json()
        game_id = game['id']
        player_1 = game['player_1']
        player_2 = game['player_2']
    else:
        while True:
            player_1 = input("Please enter YOUR name: ")
            player_2 = input("Please enter your OPPONENT name: ")
            response = requests.post("http://127.0.0.1:5000/game/new-game",
                                     json={'player_1': player_1, 'player_2': player_2})
            if not response.ok:
                print(response.text)
                continue

            break
        name = player_1
        game = response.json()
        game_id = game['id']
        print("your game id is: " + str(game_id))

    def exit_game(sig, frame):
        print("\nDon't forget your id! it's " + str(game['id']))
        exit(0)

    signal(SIGINT, exit_game)
    has_winner = False
    print_game(player_1, player_2, game)
    after_switch = False if game['turn'] == name else True

    while not has_winner:
        if name == game['turn']:
            if after_switch:
                print_game(player_1, player_2, game)
                after_switch = False
            print(game['turn'] + ", it\'s your turn")
            move = input("pit number to start the move from: ")
            url = "http://127.0.0.1:5000/game/{}/make-move".format(game_id)
            response = requests.post(url=url,
                                     json={'user': game['turn'], 'pit': int(move)})

            if not response.ok:
                print(response.text)
                continue
            game = response.json()
            print_game(player_1, player_2, game)
            if game['turn'] != name:
                after_switch = True
        else:
            print("waiting for other player to make a move...")
            time.sleep(3)
        game = requests.get("http://127.0.0.1:5000/game/{}".format(game_id)).json()

        if game['is_over']:
            print('The winner is: ' + game['winner'])
    return


def print_game(player_1, player_2, game):
    player_1_arr = game['pits'][:6]
    player_1_arr.append(game['stores'][0])
    player_1_arr = [' '] + player_1_arr

    player_2_arr = [game['stores'][1]]
    pits_reverse = game['pits'][6:]
    pits_reverse.reverse()
    player_2_arr += pits_reverse
    player_2_arr += [' ']

    columns_names = {x: 'pit' for x in range(1, 7)}
    df = pd.DataFrame({player_2: player_2_arr, player_1: player_1_arr})
    df = df.transpose()
    df = df.rename(columns={0: 'store', 7: 'store'})
    df = df.rename(columns=columns_names)
    print(df)


if __name__=='__main__':
    run()
