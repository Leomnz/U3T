import random
import games
from games import Game, GameState

class U3T(Game):
    """Ultimate Tic Tac Toe Game, on a 9x9 grid."""

    toLoc = {
        0: (0, 0), 1: (0, 1), 2: (0, 2),
        3: (1, 0), 4: (1, 1), 5: (1, 2),
        6: (2, 0), 7: (2, 1), 8: (2, 2),
    }


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
            self.overall_board[self.toLoc[finished_board_index]] = state.to_move[0]

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
        if (self.k_in_row(board, move, player[0], (0, 1)) or
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
        if self.compute_utility_3x3(converted_3x3_board, converted_move, player) == 1:  # check if small grid won
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
                
    def heatmap_choose_move(self, state):
        player = state.to_move[0]
        # Define other player
        if(player == 'X'):
            otherPlayer = 'O'
        else:
            otherPlayer = 'X'

        hotnessDict = {}
        if(state.to_move[1] == None):
            # Use all heuristics
            for move in self.actions(state):
                playerTileHeat = self.compute_tile_wins_heat(state.board, move, player, otherPlayer, self.get_board_from_move(move))      # If player tile heat is high, playing in this tile increases tile win likelihood
                opponentTileHeat = self.compute_tile_wins_heat(state.board, move, otherPlayer, player, self.get_board_from_move(move))    # If opponent tile heat is high, playing in this tile will block the opponent in some way
                opponentHappinessHeat = self.compute_opponent_board_heat(player, otherPlayer, ((move[0] % 3) * 3) + (move[1] % 3))        # If opponent is likely to win from being sent to this board, don't send them there
                playerBoardHeat = self.compute_board_wins_heat(player, otherPlayer, self.get_board_from_move(move))                       # If player is likely to win by playing in this board, play there
                opponentBoardHeat = self.compute_board_wins_heat(otherPlayer, player, self.get_board_from_move(move))                     # If opponent is likely to win by playing in this board, playing in this will block the opponent in some way
        
                hotnessDict[move] = 4 * playerTileHeat * playerBoardHeat + 0 * opponentTileHeat * opponentBoardHeat + 0.5 * opponentHappinessHeat
                # print("Move: (" + str(move[0]) + "," + str(move[1]) + "), Player Tile Heat: " + str(playerTileHeat) + ", Opponent Tile Heat: " + str(opponentTileHeat) + ", Opponent Happiness Heat: " + str(opponentHappinessHeat) + ", Player Board Heat: " + str(playerBoardHeat) + ", Opponent Board Heat: " + str(opponentBoardHeat) + ", Total Heat: " + str(hotnessDict[move]))
        # Just use tile heat and opponent board heat
        else:
            for move in self.actions(state):
                playerTileHeat = self.compute_tile_wins_heat(state.board, move, player, otherPlayer, self.get_board_from_move(move))      # If player tile heat is high, playing in this tile increases tile win likelihood
                opponentTileHeat = self.compute_tile_wins_heat(state.board, move, otherPlayer, player, self.get_board_from_move(move))    # If opponent tile heat is high, playing in this tile will block the opponent in some way
                opponentHappinessHeat = self.compute_opponent_board_heat(player, otherPlayer, ((move[0] % 3) * 3) + (move[1] % 3))        # If opponent is likely to win from being sent to this board, don't send them there
                
                hotnessDict[move] = 4 * playerTileHeat + 0 * opponentTileHeat + 0.5 * opponentHappinessHeat
                # print("Move: (" + str(move[0]) + "," + str(move[1]) + "), Player Tile Heat: " + str(playerTileHeat) + ", Opponent Tile Heat: " + str(opponentTileHeat) + ", Opponent Happiness Heat: " + str(opponentHappinessHeat) + ", Total Heat: " + str(hotnessDict[move]))

        # If dictionary is empty, there is no available move. 
        if(not hotnessDict):
           return None
        
        return max(hotnessDict, key=hotnessDict.get)
    
    # How many board win conditions involve this tile?
    def compute_tile_wins_heat(self, board, move, player, otherPlayer, boardNum):
        # If wins a board, hotness level 100
        if(self.small_board_win(board, move, player) != 0):
            return 5
        # Else, check how many moves can result in win
        else:
            # Return number of possible ways player can win
            heat = 0
            heat += self.k_in_row_possible(board, move, player, otherPlayer, boardNum, (0, 1)) # Columns
            heat += self.k_in_row_possible(board, move, player, otherPlayer, boardNum, (1, 0)) # Rows
            heat += self.k_in_row_possible(board, move, player, otherPlayer, boardNum, (1, -1)) # First diagonal
            heat += self.k_in_row_possible(board, move, player, otherPlayer, boardNum, (1, 1)) # Second diagonal
            return heat
    
    # How many game win conditions involve this board?
    def compute_board_wins_heat(self, player, otherPlayer, boardNum):
        # Check how many possible win conditions contain this boardNum
        overall_converted_move = (boardNum // 3, boardNum % 3)
        heat = 0
        heat += self.k_in_row_possible(self.overall_board, overall_converted_move, player, otherPlayer, 0, (0, 1)) # Rows
        heat += self.k_in_row_possible(self.overall_board, overall_converted_move, player, otherPlayer, 0, (1, 0)) # Columns
        heat += self.k_in_row_possible(self.overall_board, overall_converted_move, player, otherPlayer, 0, (1, -1)) # First diagonal
        heat += self.k_in_row_possible(self.overall_board, overall_converted_move, player, otherPlayer, 0, (1, 1)) # Second diagonal
        
        return heat
    
    # How good is it for your opponent to be sent to this board?
    def compute_opponent_board_heat(self, player, otherPlayer, boardNum):
        # If board is already captured, don't want them to be able to go anywhere
        if(self.overall_board.get(boardNum) == 'O' or self.overall_board.get(boardNum) == 'X'):
            return -5
        # Otherwise, see how likely opponent is to win from capturing that board
        else:
            return -1 * self.compute_board_wins_heat(otherPlayer, player, boardNum)
        
    def henry_normalize_board(self, board, move, player):
        boardNum = self.get_board_from_move(move)

        newBoard = {}
        newBoard[(0, 0)] = board.get((0 + (boardNum // 3) * 3, 0 + (boardNum % 3) * 3))
        newBoard[(0, 1)] = board.get((0 + (boardNum // 3) * 3, 1 + (boardNum % 3) * 3))
        newBoard[(0, 2)] = board.get((0 + (boardNum // 3) * 3, 2 + (boardNum % 3) * 3))
        newBoard[(1, 0)] = board.get((1 + (boardNum // 3) * 3, 0 + (boardNum % 3) * 3))
        newBoard[(1, 1)] = board.get((1 + (boardNum // 3) * 3, 1 + (boardNum % 3) * 3))
        newBoard[(1, 2)] = board.get((1 + (boardNum // 3) * 3, 2 + (boardNum % 3) * 3))
        newBoard[(2, 0)] = board.get((2 + (boardNum // 3) * 3, 0 + (boardNum % 3) * 3))
        newBoard[(2, 1)] = board.get((2 + (boardNum // 3) * 3, 1 + (boardNum % 3) * 3))
        newBoard[(2, 2)] = board.get((2 + (boardNum // 3) * 3, 2 + (boardNum % 3) * 3))

        newMove = (move[0] % 3, move[1] % 3)
        newBoard[newMove] = player
        
        return newBoard

    # Returns 1 if playing move wins a small board
    def small_board_win(self, board, move, player):
        converted_3x3_board = self.henry_normalize_board(board, move, player)

        # If small board is won with this move, return 1
        if self.gameWon(converted_3x3_board, player) != '':
            return 1

        # Else return 0
        return 0
        
    def k_in_row_possible(self, board, move, player, otherPlayer, boardNum, delta_x_y):
        (delta_x, delta_y) = delta_x_y
        x, y = move
        n = 0  # n is number of moves in row

        # Check to the forwards (while tile is not claimed by other player and is in correct board)
        while (board.get((x, y)) != otherPlayer) and (self.get_board_from_move((x, y)) == boardNum):
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move

        # Check to the backwards (while tile is not claimed by other player and is in correct board)
        while (board.get((x, y)) != otherPlayer) and (self.get_board_from_move((x, y)) == boardNum):
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Because we counted move itself twice

        # If can win in this way, return 1
        if(n >= self.k):
            return 1
        
        # If cannot win in this way, return 0
        return 0

    def gameWon(self, board, player):
        # Check Rows
        if(board.get(0) == player and board.get(1) == player and board.get(2) == player):
            return player
        if(board.get(3) == player and board.get(4) == player and board.get(5) == player):
            return player
        if(board.get(6) == player and board.get(7) == player and board.get(8) == player):
            return player
        
        # Check Columns
        if(board.get(0) == player and board.get(3) == player and board.get(6) == player):
            return player
        if(board.get(1) == player and board.get(4) == player and board.get(7) == player):
            return player
        if(board.get(2) == player and board.get(5) == player and board.get(8) == player):
            return player
        
        # Check Diagonals
        if(board.get(0) == player and board.get(4) == player and board.get(8) == player):
            return player
        if(board.get(2) == player and board.get(4) == player and board.get(6) == player):
            return player
        
        return ''

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

# print(U3T.play_and_display_game(games.random_player, games.random_player))

# eval = 0
# while eval == 0:
#     # games.random_player
#     eval = U3T.play_game(games.query_player, alpha_beta_cutoff_player)
#     print("Eval:", eval)
# print("Game Over")


# play the game as both sides
X = 0
O = 0
D = 0

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

#     # print("Random Player Action:", games.random_player(U3T, state))
#     # print("Alpha Beta Cutoff Player Action:", alpha_beta_cutoff_player(U3T, state))

#     move = int(input('Enter your move: '))
#     move = actions[move]

#     # move = games.random_player(U3T, state)
#     state = U3T.result(state, move)
#     if U3T.terminal_test(state):
#         # print('A Wins!')
#         A += 1
#         break

#     move = U3T.heatmap_choose_move(state)
#     state = U3T.result(state, move)
#     if U3T.terminal_test(state):
#         # print('B Wins!')
#         B += 1
#         break

U3T = U3T()
for i in range(0, 1000):
    state = U3T.initial
    U3T.overall_board = {}

    while True:
        # print("Random Player Action:", games.random_player(U3T, state))
        # print("Alpha Beta Cutoff Player Action:", alpha_beta_cutoff_player(U3T, state))

        # print("---------------------------")
        # U3T.display(state)
        # print("---------------------------")

        move = U3T.heatmap_choose_move(state)
        if(move == None):
            D += 1
            break
        state = U3T.result(state, move)
        if(U3T.gameWon(U3T.overall_board, 'X') != ''):
            X += 1

            # print("---------------------------")
            # U3T.display(state)
            # print("---------------------------")
            break
        
        # print("---------------------------")
        # U3T.display(state)
        # print("---------------------------")

        move = games.random_player(U3T, state)
        if(move == None):
            D += 1
            break
        state = U3T.result(state, move)
        if(U3T.gameWon(U3T.overall_board, 'O') != ''):
            O += 1

            # print("---------------------------")
            # U3T.display(state)
            # print("---------------------------")
            break

    

print("X Wins: " + str(X))
print("O Wins: " + str(O))
print("Draws: " + str(D))
