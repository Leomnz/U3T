import threading
import time
import tracemalloc

from U3T import U3T
import games
from U3T import GameState
import games4e


def play_games(number_of_games, player1, player2):
    U3T = U3T()
    X_wins = 0
    O_wins = 0
    Draws = 0
    for i in range(0, 5):
        U3T.__init__()
        eval = U3T.play_game(heatmap_player, alpha_beta_cutoff_player)
        if eval >= 1:
            X_wins += 1
        elif eval <= -1:
            O_wins += 1
        else:
            Draws += 1
        print("Game Number:", i, "Eval: ", eval)
    print("X Wins: ", X_wins)
    print("O Wins: ", O_wins)
    print("Draws: ", Draws)


print(threading.active_count())
