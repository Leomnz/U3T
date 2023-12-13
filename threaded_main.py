from U3T import U3T
import games
# from games import GameState
from U3T import GameState
import games4e

import multiprocessing
import tracemalloc
import time


def alpha_beta_cutoff_player(game, state, d=4, cutoff_test=None, eval_fn=None):
    return games.alpha_beta_cutoff_search(state, game, d=d, cutoff_test=cutoff_test, eval_fn=eval_fn)


def heatmap_player(game, state):
    return game.heatmap_choose_move(state)


players = [alpha_beta_cutoff_player, games.random_player, heatmap_player, games4e.mcts_player]

queue = multiprocessing.Queue()


def simulate_games(num_games, game, player1, player2, thread_num, queue):
    U3T = game
    X_wins = 0
    O_wins = 0
    Draws = 0
    memory_usage = [None] * num_games
    time_usage = [None] * num_games
    for i in range(0, num_games):
        tracemalloc.start()
        start = time.time()
        U3T.__init__()
        eval = U3T.play_game_silent(player1, player2)
        if eval >= 1:
            X_wins += 1
        elif eval <= -1:
            O_wins += 1
        else:
            Draws += 1
        memory_usage[i] = tracemalloc.get_traced_memory()[1]
        end = time.time()
        tracemalloc.stop()
        time_usage[i] = (end - start) * 10 ** 3  # conversion for ms
        if thread_num == 0:
            print(
                f"Thread [{thread_num}], Game Number: [{i}], Eval: [{eval}], Memory Usage: [{memory_usage[i]}], Time Usage: [{time_usage[i]}]")
    average_memory_usage = sum(memory_usage) / len(memory_usage)
    average_time_usage = sum(time_usage) / len(time_usage)
    # results[thread_num] = (X_wins, O_wins, Draws, average_memory_usage, average_time_usage)
    # print(f"Thread [{thread_num}], X wins: [{X_wins}], O wins: [{O_wins}], Draws: [{Draws}], Average Memory Usage: [{average_memory_usage}], Average Time Usage: [{average_time_usage}]")
    queue.put((X_wins, O_wins, Draws, average_memory_usage, average_time_usage))


if __name__ == "__main__":
    thread_count = 20
    threads = [None] * thread_count
    total_games = 500
    games_per_thread = total_games // thread_count
    print("Games per thread: ", games_per_thread)
    print("Total games: ", total_games)
    print("Threads: ", thread_count)

    for i in range(0, thread_count):
        threads[i] = multiprocessing.Process(target=simulate_games,
                                             args=(
                                                 games_per_thread, U3T(), alpha_beta_cutoff_player, games4e.mcts_player,
                                                 i, queue))
    for i in range(0, thread_count):
        threads[i].start()
        print("Thread ", i, " started")

    for i in range(0, thread_count):
        threads[i].join()

    print("All threads joined")
    Total_X_wins = 0
    Total_O_wins = 0
    Total_Draws = 0
    Total_Memory_Usage = [0] * thread_count
    Total_Time_Usage = [0] * thread_count
    Average_Memory_Usage = 0
    Average_Time_Usage = 0
    for element in range(0, queue.qsize()):
        X_wins, O_wins, Draws, average_memory_usage, average_time_usage = queue.get()
        Total_X_wins += X_wins
        Total_O_wins += O_wins
        Total_Draws += Draws
        Total_Memory_Usage[element] = average_memory_usage
        Total_Time_Usage[element] = average_time_usage

    Average_Time_Usage = sum(Total_Time_Usage) / len(Total_Time_Usage)
    Average_Memory_Usage = sum(Total_Memory_Usage) / len(Total_Memory_Usage)
    print("Total X wins: ", Total_X_wins)
    print("Total O wins: ", Total_O_wins)
    print("Total Draws: ", Total_Draws)
    print("Average Memory Usage: ", Average_Memory_Usage / 1000, "KB")
    print("Average Time Usage: ", Average_Time_Usage / 1000, "ms")