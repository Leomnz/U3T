from U3T import U3T
import games
# from games import GameState
from U3T import GameState
import games4e


#
# state = U3T.initial
# state = GameState(to_move=('O', 0), utility=0,
#                   board={(0, 0): 'X', (0, 1): 'O', (0, 3): 'X', (0, 2): 'O', (0, 6): 'X', (1, 0): 'O', (3, 0): 'X',
#                          (1, 1): 'O', (3, 3): 'X'},
#                   moves=[(0, 4), (0, 5), (0, 7), (0, 8), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (2, 0),
#                          (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (3, 1), (3, 2), (3, 4), (3, 5),
#                          (3, 6), (3, 7), (3, 8), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8),
#                          (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (6, 0), (6, 1), (6, 2),
#                          (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5),
#                          (7, 6), (7, 7), (7, 8), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7),
#                          (8, 8)])
#
#
# leo_board = U3T.normalize_board(state.board, (1, 2))
# print("Leo Normalize Board", leo_board)
# print("Henry Normalize Board", U3T.henry_normalize_board(state.board, (1, 2), state.to_move[0]))
# print("Leo Compute Utility", U3T.compute_utility_3x3(leo_board[0], leo_board[1], state.to_move))
# print("overall utility", U3T.compute_utility(state.board, (1, 2), state.to_move))

def alpha_beta_cutoff_player(game, state, d=4, cutoff_test=None, eval_fn=None):
    return games.alpha_beta_cutoff_search(state, game, d=d, cutoff_test=cutoff_test, eval_fn=eval_fn)


def heatmap_player(game, state):
    return game.heatmap_choose_move(state)


players = [alpha_beta_cutoff_player, games.random_player, heatmap_player, games4e.mcts_player]

# play the game as X
# eval = 0
U3T = U3T()
state = U3T.initial
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

# U3T.play_and_display_game(alpha_beta_cutoff_player, games.random_player)

# state = GameState(to_move='X', next_grid=None, utility=0,
#                   board={(0, 0): 'X', (2, 0): 'O', (6, 0): 'X', (0, 2): 'X', (0, 6): 'X', (2, 2): 'X', (6, 6): 'X',
#                          (0, 1): 'O', (0, 3): 'X', (1, 0): 'O', (3, 0): 'X', (1, 2): 'X', (3, 6): 'X', (3, 8): 'O',
#                          (0, 7): 'X', (0, 5): 'O', (0, 8): 'X', (5, 2): 'O', (6, 7): 'X', (1, 3): 'O', (3, 1): 'X',
#                          (0, 4): 'O', (1, 4): 'X', (4, 3): 'O', (3, 2): 'X', (6, 5): 'O'},
#                   moves=[(1, 5), (2, 3), (2, 4), (2, 5), (3, 3), (3, 4), (3, 5), (3, 7), (4, 4), (4, 5), (4, 6), (4, 7),
#                          (4, 8), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (6, 1), (6, 2), (6, 3), (6, 4), (6, 8),
#                          (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (8, 0), (8, 1), (8, 2),
#                          (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8)], overall_board={0: 'X', 2: 'X', 3: 'X'})
# U3T.display(state)
# for i in range(0, 9):
#     x, y = U3T.toLoc[i][0] * 3, U3T.toLoc[i][1] * 3
#     print("i", i, "toLoc", (x, y))
#     converted_board, converted_move = U3T.normalize_board(state.board, (x, y), "X")
#     print(converted_board, converted_move)
#     print(U3T.compute_utility_3x3(converted_board, converted_move, "X"))
# print(state)
# print(move)
# utility = U3T.compute_utility(state.board, state.overall_board, move, state.to_move)
# print(utility)

# # play the game as both sides
X = 0
O = 0
D = 0
#
# U3T = U3T()
# state = U3T.initial
# while True:
#     print()
#     print()
#     print("You are playing as:", state.to_move[0])
#     print("---------------------------")
#     U3T.display(state)
#     print("---------------------------")
#     actions = U3T.actions(state)
#     print("Possible Actions:", actions)
#
#     # print("Random Player Action:", games.random_player(U3T, state))
#     # print("Alpha Beta Cutoff Player Action:", alpha_beta_cutoff_player(U3T, state))
#
#     move = int(input('Enter your move: '))
#     move = actions[move]
#     state = U3T.result(state, move)
#     print("---------------------------")
#     U3T.display(state)
#     print("---------------------------")
#     if (U3T.gameWon(U3T.overall_board, 'X') != ''):
#         print("---------------------------")
#         U3T.display(state)
#         print("---------------------------")
#         print("You Win!")
#         break
#
#     move = U3T.heatmap_choose_move(state)
#     if (move == None):
#         D += 1
#         break
#     state = U3T.result(state, move)
#     if (U3T.gameWon(U3T.overall_board, 'O') != ''):
#         print("---------------------------")
#         U3T.display(state)
#         print("---------------------------")
#         print("You Lose!")
#         break

# U3T = U3T()
# for i in range(0, 500):
#     state = U3T.initial
#
#     while True:
#         # print("Random Player Action:", games.random_player(U3T, state))
#         # print("Alpha Beta Cutoff Player Action:", alpha_beta_cutoff_player(U3T, state))
#
#         # print("---------------------------")
#         # U3T.display(state)
#         # print("---------------------------")
#
#         move = U3T.heatmap_choose_move(state)
#         if(move == None):
#             D += 1
#             break
#         state = U3T.result(state, move)
#         if(U3T.gameWon(state.overall_board, 'X') != ''):
#             X += 1
#
#             print("---------------------------")
#             U3T.display(state)
#             print("---------------------------")
#             break
#
#         # print("---------------------------")
#         # U3T.display(state)
#         # print("---------------------------")
#
#         move = games4e.mcts_player(U3T, state)
#         if(move == None):
#             D += 1
#             break
#         state = U3T.result(state, move)
#         if(U3T.gameWon(state.overall_board, 'O') != ''):
#             O += 1
#
#             print("---------------------------")
#             U3T.display(state)
#             print("---------------------------")
#             break
#
#
# print("X Wins: " + str(X))
# print("O Wins: " + str(O))
# print("Draws: " + str(D))
