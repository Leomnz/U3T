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
    memory_usage_player1 = []
    time_usage_player1 = []
    memory_usage_player2 = []
    time_usage_player2 = []
    for i in range(0, num_games):
        U3T.__init__()

        state = U3T.initial
        eval = None
        while eval is None:
            # player 1
            tracemalloc.start()
            start = time.time()
            move = player1(U3T, state)
            state = U3T.result(state, move)
            if U3T.terminal_test(state):
                eval = U3T.utility(state, U3T.to_move(U3T.initial))
            end = time.time()
            memory_usage_player1.append(tracemalloc.get_traced_memory()[1])
            time_usage_player1.append((end - start) * 10 ** 3)  # conversion for ms

            # player 1
            tracemalloc.clear_traces()
            start = time.time()
            move = player2(U3T, state)
            state = U3T.result(state, move)
            if U3T.terminal_test(state):
                eval = U3T.utility(state, U3T.to_move(U3T.initial))
            end = time.time()
            memory_usage_player2.append(tracemalloc.get_traced_memory()[1])
            tracemalloc.stop()
            # print(i, tracemalloc.get_traced_memory())
            time_usage_player2.append((end - start) * 10 ** 3)  # conversion for ms

        if eval >= 1:
            X_wins += 1
        elif eval <= -1:
            O_wins += 1
        else:
            Draws += 1
        if thread_num == 0:
            print(
                f"Thread [{thread_num}], Game Number: [{i}], Eval: [{eval}], Memory Usage Player 1: [{memory_usage_player1[i]}], Memory Usage Player 2: [{memory_usage_player2[i]}],Time Usage Player 1: [{time_usage_player1[i]}], Time Usage Player 2: [{time_usage_player2[i]}]")
    average_memory_usage_player1 = sum(memory_usage_player1) / len(memory_usage_player1)
    average_memory_usage_player2 = sum(memory_usage_player2) / len(memory_usage_player2)
    average_time_usage_player1 = sum(time_usage_player1) / len(time_usage_player1)
    average_time_usage_player2 = sum(time_usage_player2) / len(time_usage_player2)
    # results[thread_num] = (X_wins, O_wins, Draws, average_memory_usage, average_time_usage)
    # print(f"Thread [{thread_num}], X wins: [{X_wins}], O wins: [{O_wins}], Draws: [{Draws}], Average Memory Usage: [{average_memory_usage}], Average Time Usage: [{average_time_usage}]")
    queue.put((X_wins, O_wins, Draws, average_memory_usage_player1, average_memory_usage_player2,
               average_time_usage_player1, average_time_usage_player2))


if __name__ == "__main__":
    thread_count = 20
    threads = [None] * thread_count
    total_games = 100
    games_per_thread = total_games // thread_count
    print("Games per thread: ", games_per_thread)
    print("Total games: ", total_games)
    print("Threads: ", thread_count)

    for i in range(0, thread_count):
        threads[i] = multiprocessing.Process(target=simulate_games,
                                             args=(
                                                 games_per_thread, U3T(), games.random_player, games4e.mcts_player,
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
    Total_Memory_Usage_player1 = [0] * thread_count
    Total_Memory_Usage_player2 = [0] * thread_count
    Total_Time_Usage_player1 = [0] * thread_count
    Total_Time_Usage_player2 = [0] * thread_count
    for element in range(0, queue.qsize()):
        X_wins, O_wins, Draws, average_memory_usage_player1, average_memory_usage_player2, average_time_usage_player1, average_time_usage_player2 = queue.get()
        Total_X_wins += X_wins
        Total_O_wins += O_wins
        Total_Draws += Draws
        Total_Memory_Usage_player1[element] = average_memory_usage_player1
        Total_Memory_Usage_player2[element] = average_memory_usage_player2
        Total_Time_Usage_player1[element] = average_time_usage_player1
        Total_Time_Usage_player2[element] = average_time_usage_player2

    Average_Time_Usage_player1 = sum(Total_Time_Usage_player1) / len(Total_Time_Usage_player1)
    Average_Time_Usage_player2 = sum(Total_Time_Usage_player2) / len(Total_Time_Usage_player2)
    Average_Memory_Usage_player1 = sum(Total_Memory_Usage_player1) / len(Total_Memory_Usage_player1)
    Average_Memory_Usage_player2 = sum(Total_Memory_Usage_player2) / len(Total_Memory_Usage_player2)
    print("Total X wins: ", Total_X_wins)
    print("Total O wins: ", Total_O_wins)
    print("Total Draws: ", Total_Draws)
    print("Average Memory Usage Player 1: ", Average_Memory_Usage_player1 / 1000, "KB")
    print("Average Memory Usage Player 2: ", Average_Memory_Usage_player2 / 1000, "KB")
    print("Average Time Usage Player 1: ", Average_Time_Usage_player1 / 1000, "s")
    print("Average Time Usage Player 2: ", Average_Time_Usage_player2 / 1000, "s")
