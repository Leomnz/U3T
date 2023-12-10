import random
import games
from games import Game, GameState


class U3T(Game):
    """Ultimate Tic Tac Toe Game, on a 9x9 grid."""

    def __init__(self, h=9, v=9, k=3):
        self.h = h
        self.v = v
        self.k = k
        self.overall_board = {}
        moves = [(x, y) for x in range(0, 9) for y in range(0, 9)]
        # to_move is a tuple(("X" or "Y"), (None, 0, 1, 2, 3, 4, 5, 6, 7, 8))
        # where the first element is the player, and the second is which board they play on
        self.initial = GameState(to_move=('X', None), utility=0, board={}, moves=moves)

    def grid_conversion(self, grid):
        # grid is a number 0-8

        """
        For grid 0, the moves are (0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)
        For grid 1, the moves are (0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)
        For grid 2, the moves are (0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 8), (2, 6), (2, 7), (2, 8)
        For grid 3, the moves are (3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2)
        For grid 4, the moves are (3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)
        For grid 5, the moves are (3, 6), (3, 7), (3, 8), (4, 6), (4, 7), (4, 8), (5, 6), (5, 7), (5, 8)
        For grid 6, the moves are (6, 0), (6, 1), (6, 2), (7, 0), (7, 1), (7, 2), (8, 0), (8, 1), (8, 2)
        For grid 7, the moves are (6, 3), (6, 4), (6, 5), (7, 3), (7, 4), (7, 5), (8, 3), (8, 4), (8, 5)
        For grid 8, the moves are (6, 6), (6, 7), (6, 8), (7, 6), (7, 7), (7, 8), (8, 6), (8, 7), (8, 8)
        """

        tiles = []
        for row in range(3 * (grid // 3), 3 * (grid // 3) + 3):
            for col in range(3 * (grid % 3), 3 * (grid % 3) + 3):
                tiles.append((row, col))
        return tiles

    def actions(self, state):
        """Legal moves are any square not yet taken. In your specified grid"""
        grid_index = state.to_move[1]
        if grid_index is None:
            return state.moves
        else:
            possible_moves = self.grid_conversion(grid_index)
            legal_moves = []

            for move in possible_moves:
                if move in state.moves:
                    legal_moves.append(move)

            return legal_moves

    def result(self, state, move):
        grid = state.to_move[1]
        # if move not in self.actions(state):
        #     print("Illegal move")
        #     return state  # Illegal move has no effect
        if grid is not None:
            if move not in self.grid_conversion(grid):
                print("Illegal move")
                return state

        board = state.board.copy()
        board[move] = state.to_move[0]
        moves = list(state.moves)
        moves.remove(move)

        # check if move results in a small board win
        converted_3x3_board, converted_move = self.normalize_board(board, move)
        utility = self.compute_utility_3x3(converted_3x3_board, converted_move, state.to_move[0])
        if utility != 0:
            finished_board_index = self.get_board_from_move(move)
            self.overall_board[finished_board_index] = state.to_move[0]

            final_moves = moves.copy()
            for i in moves:  # remove all moves in now finished grid
                if self.get_board_from_move(i) == finished_board_index:
                    final_moves.remove(i)
            moves = final_moves
        next_player = 'O' if state.to_move[0] == 'X' else 'X'

        next_grid = converted_move[0] * 3 + converted_move[1]
        if self.overall_board.get(next_grid) is not None:
            next_grid = None
        return GameState(to_move=(next_player, next_grid),
                         utility=self.compute_utility(board, move, state.to_move),
                         board=board, moves=moves)

    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player == 'X' else -state.utility

    def terminal_test(self, state):
        """A state is terminal if it is won or there are no empty squares."""
        if state.utility < -1 or state.utility > 1:
            return True
        return len(state.moves) == 0

    def display(self, state):
        board = state.board
        print("---------------------------")
        for x in range(0, 9):
            if x % 3 == 0:
                print()
            for y in range(0, 9):
                if y % 3 == 0:
                    print(" ", end='')
                print(board.get((x, y), '.'), end=' ')
            print()
        print("---------------------------")

    def k_in_row(self, board, move, player, delta_x_y):
        """Return true if there is a line through move on board for player."""
        (delta_x, delta_y) = delta_x_y
        x, y = move
        n = 0  # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Because we counted move itself twice
        return n >= self.k

    def compute_utility_3x3(self, board, move, player):
        """If 'X' wins with this move, return 1; if 'O' wins return -1; else return 0."""
        if (self.k_in_row(board, move, player, (0, 1)) or
                self.k_in_row(board, move, player[0], (1, 0)) or
                self.k_in_row(board, move, player[0], (1, -1)) or
                self.k_in_row(board, move, player[0], (1, 1))):
            return +1 if player[0] == 'X' else -1
        else:
            return 0

    def get_board_from_move(self, move):
        """Returns the 3x3 board index (0,1,2,3,4,5,6,7,8) from a move"""
        return (move[0] // 3) * 3 + move[1] // 3

    def normalize_board(self, board, move):  # returns a board and a move that are normalized to the 3x3 grid
        grid_index = self.get_board_from_move(move)
        grid_tiles = self.grid_conversion(grid_index)
        converted_3x3_board = {}
        for (x, y) in grid_tiles:
            converted_3x3_board[(x % 3, y % 3)] = board.get((x, y))

        converted_move = (move[0] % 3, move[1] % 3)
        return converted_3x3_board, converted_move

    def compute_utility(self, board, move, player):
        utility = 0
        converted_3x3_board, converted_move = self.normalize_board(board, move)
        if self.compute_utility_3x3(converted_3x3_board, converted_move, player) != 0:  # check if small grid won
            utility += 0.1 if player == 'X' else -0.1

            # check if the overall grid is won
            small_grid_index = self.get_board_from_move(move)
            # index to move
            overall_converted_move = (small_grid_index // 3, small_grid_index % 3)
            utility += self.compute_utility_3x3(self.overall_board, overall_converted_move, player)
        return utility

    def play_and_display_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        while True:
            for player in players:
                self.display(state)
                move = player(self, state)
                state = self.result(state, move)
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))

# U3T = U3T()
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


def alpha_beta_cutoff_player(game, state, d=4, cutoff_test=None, eval_fn=None):
    return games.alpha_beta_cutoff_search(state, game, d=d, cutoff_test=cutoff_test, eval_fn=eval_fn)


U3T = U3T()
# print(U3T.play_and_display_game(games.random_player, games.random_player))

eval = 0
while eval == 0:
    eval = U3T.play_and_display_game(games.random_player, games.random_player)
    print("Eval:", eval)
print("Game Over")

# # play the game as both sides
# while True:
#     print()
#     print()
#     print("You are playing as:", state.to_move[0])
#     print("---------------------------")
#     U3T.display(state)
#     print("---------------------------")
#     actions = U3T.actions(state)
#     print("Possible Actions:", actions)
#     print("Random Player Action:", games.random_player(U3T, state))
#     print("Alpha Beta Cutoff Player Action:", alpha_beta_cutoff_player(U3T, state))
#
#     move = int(input('Enter your move: '))
#
#     move = actions[move]
#     state = U3T.result(state, move)
#     print("State:", state)
#     if U3T.terminal_test(state):
#         print('Game over!')
#         break
