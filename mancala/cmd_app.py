from signal import SIGINT, signal

import pandas as pd
import requests


def run():
    saved_or_not = input("For saved game, insert 0, for new game, press enter ")
    if saved_or_not == "0":
        game = None
        while not game:
            saved_game_id = input("saved game id? ")
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
            player_1 = input("First player, enter your name: ")
            player_2 = input("Second player, enter your name: ")
            response = requests.post("http://127.0.0.1:5000/game/new-game",
                                     json={'player_1': player_1, 'player_2': player_2})
            if not response.ok:
                print(response.text)
                continue
            break

        game = response.json()
        game_id = game['id']
        print("your game id is: " + str(game_id))
        print(game['turn'] + ", the first move is yours")

    def exit_game(sig, frame):
        print("\nDon't forget your id! it's " + str(game['id']))
        exit(0)

    signal(SIGINT, exit_game)
    print_game(player_1, player_2, game)
    has_winner = False

    while not has_winner:
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

        if 'The winner is:' in response:
            has_winner = True
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
